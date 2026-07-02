"""PySide6 deployment console using Qt's model/view architecture."""

from __future__ import annotations

import json
import os
import queue
import sys
from dataclasses import dataclass, field
from html import escape
from pathlib import Path
from typing import Any

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    QSize,
    QSortFilterProxyModel,
    Qt,
    QTimer,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QDesktopServices,
    QFont,
    QIcon,
    QPainter,
    QPixmap,
    QTextCursor,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QStyle,
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QTableView,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from . import agents, config, deployer, detector, styles
from .agents import AgentSpec
from .detector import Detection
from .i18n import Language, set_language, t
from .workers import (
    Event,
    EventKind,
    Worker,
    make_build_all_job,
    make_deploy_job,
    make_uninstall_job,
    make_verify_job,
)


STATUS_OK_ROLE = int(Qt.ItemDataRole.UserRole) + 1
DETAIL_ROLE = int(Qt.ItemDataRole.UserRole) + 2
SORT_ROLE = int(Qt.ItemDataRole.UserRole) + 3

MAX_LOG_LINES = 1200


def _load_release_meta() -> tuple[str, tuple[str, ...]]:
    config_path = Path(__file__).resolve().parents[1] / "release_config.json"
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        version = data.get("version", "0.0.0")
        profiles = tuple(data.get("default_all_profiles") or data.get("profiles") or ())
        return version, profiles
    except (OSError, ValueError):
        from . import __version__ as pkg_version

        return pkg_version, ("core", "adapters-light", "qoder-addon", "singlefile", "source-dev", "ui-client")


def _asset_path(name: str) -> Path:
    if getattr(sys, "frozen", False):
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        return base / "installer_gui" / "assets" / name
    return Path(__file__).resolve().parent / "assets" / name


AGENT_LOGOS = {
    "codex": "codex.png",
    "minimax": "minimax-code.png",
    "zcode": "zcode.png",
    "qoder": "qoder.png",
    "qoder-project": "qoder.png",
    "qodercn": "qoder-cn.png",
    "qodercn-project": "qoder-cn.png",
    "trae": "trae.png",
    "opencode": "opencode.png",
}

_ICON_CACHE: dict[str, QIcon] = {}


def _agent_logo_path(agent_name: str) -> Path | None:
    filename = AGENT_LOGOS.get(agent_name)
    if filename is None:
        return None
    path = _asset_path(f"platform-logos/{filename}")
    return path if path.exists() else None


def _agent_icon(agent_name: str) -> QIcon | None:
    if agent_name in _ICON_CACHE:
        return _ICON_CACHE[agent_name]
    path = _agent_logo_path(agent_name)
    if path is None:
        return None
    icon = QIcon(str(path))
    if icon.isNull():
        return None
    _ICON_CACHE[agent_name] = icon
    return icon


def _font(spec: tuple[Any, ...] | None = None, *, size: int | None = None, bold: bool = False) -> QFont:
    if spec is None:
        point_size = size or 10
        weight = QFont.Weight.Bold if bold else QFont.Weight.Normal
        return QFont(styles.FONT_FAMILY, point_size, weight)

    family = str(spec[0])
    point_size = int(spec[1]) if len(spec) > 1 else (size or 10)
    is_bold = bold or (len(spec) > 2 and str(spec[2]).lower() == "bold")
    weight = QFont.Weight.Bold if is_bold else QFont.Weight.Normal
    return QFont(family, point_size, weight)


def _short_path(path: Path | None, *, limit: int = 58) -> str:
    if path is None:
        return t("root_not_set")
    text = str(path)
    if len(text) <= limit:
        return text
    return "..." + text[-(limit - 3):]


def _root_detail_text(path: Path | None) -> str:
    if path is not None:
        return str(path)
    text = t("root_not_set")
    prefix = t("root_prefix")
    if prefix and text.startswith(prefix):
        return text[len(prefix):].strip()
    return text


@dataclass
class AgentRow:
    specs: dict[str, AgentSpec]
    mode_order: tuple[str, ...]
    selected_name: str
    roots: dict[str, Path | None]
    detections: dict[str, Detection | None] = field(default_factory=dict)
    busy_names: set[str] = field(default_factory=set)

    @property
    def spec(self) -> AgentSpec:
        return self.specs[self.selected_name]

    @property
    def display_spec(self) -> AgentSpec:
        return self.specs[self.mode_order[0]]

    @property
    def root(self) -> Path | None:
        return self.roots.get(self.selected_name)

    @property
    def detection(self) -> Detection | None:
        return self.detections.get(self.selected_name)

    @property
    def busy(self) -> bool:
        return self.selected_name in self.busy_names

    @property
    def has_modes(self) -> bool:
        return len(self.mode_order) > 1

    def spec_for(self, name: str) -> AgentSpec | None:
        return self.specs.get(name)

    def root_for(self, name: str) -> Path | None:
        return self.roots.get(name)


MERGED_AGENT_ROWS = {
    "qoder": ("qoder", "qoder-project"),
    "qodercn": ("qodercn", "qodercn-project"),
}


def _build_agent_rows(specs: list[AgentSpec], roots: dict[str, Path | None]) -> list[AgentRow]:
    by_name = {spec.name: spec for spec in specs}
    grouped_names = {name for names in MERGED_AGENT_ROWS.values() for name in names}
    rows: list[AgentRow] = []
    used: set[str] = set()

    for spec in specs:
        if spec.name in used:
            continue
        mode_order = MERGED_AGENT_ROWS.get(spec.name)
        if mode_order is not None and all(name in by_name for name in mode_order):
            rows.append(
                AgentRow(
                    specs={name: by_name[name] for name in mode_order},
                    mode_order=mode_order,
                    selected_name=mode_order[0],
                    roots={name: roots.get(name) for name in mode_order},
                )
            )
            used.update(mode_order)
            continue
        if spec.name in grouped_names:
            continue
        rows.append(
            AgentRow(
                specs={spec.name: spec},
                mode_order=(spec.name,),
                selected_name=spec.name,
                roots={spec.name: roots.get(spec.name)},
            )
        )
        used.add(spec.name)
    return rows


class AgentTableModel(QAbstractTableModel):
    COL_AGENT = 0
    COL_PROGRAM = 1
    COL_DEPLOYMENT = 2
    COL_ROOT = 3
    COL_PROFILES = 4

    HEADERS = (
        "col_agent",
        "col_program",
        "col_deployment",
        "col_root",
        "col_profiles",
    )

    def __init__(self, specs: list[AgentSpec], roots: dict[str, Path | None]) -> None:
        super().__init__()
        self._rows = _build_agent_rows(specs, roots)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self.HEADERS)

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = int(Qt.ItemDataRole.DisplayRole),
    ) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == int(Qt.ItemDataRole.DisplayRole):
            return t(self.HEADERS[section])
        return None

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:  # noqa: N802
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = int(Qt.ItemDataRole.DisplayRole)) -> Any:
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        spec = row.spec
        det = row.detection
        col = index.column()

        if role == int(Qt.ItemDataRole.DisplayRole):
            if col == self.COL_AGENT:
                return row.display_spec.display_name
            if col == self.COL_PROGRAM:
                if det is None:
                    return t("checking")
                return t("program_installed") if det.program else t("program_not_found")
            if col == self.COL_DEPLOYMENT:
                if det is None:
                    return t("checking")
                return t("deployed") if det.deployed else t("not_deployed")
            if col == self.COL_ROOT:
                return _short_path(row.root)
            if col == self.COL_PROFILES:
                return ", ".join(spec.needs_profiles) if spec.needs_profiles else "-"

        if role == int(Qt.ItemDataRole.DecorationRole) and col == self.COL_AGENT:
            return _agent_icon(row.display_spec.name)

        if role == int(Qt.ItemDataRole.ToolTipRole):
            return self._tooltip(row)

        if role == int(Qt.ItemDataRole.FontRole):
            if col == self.COL_AGENT:
                return _font(styles.FONT_BODY, bold=True)
            return _font(styles.FONT_SMALL)

        if role == int(Qt.ItemDataRole.ForegroundRole):
            if col == self.COL_ROOT and row.root is None:
                return QBrush(QColor(styles.TEXT_TERTIARY))
            return QBrush(QColor(styles.TEXT_PRIMARY))

        if role == int(Qt.ItemDataRole.TextAlignmentRole):
            if col in (self.COL_PROGRAM, self.COL_DEPLOYMENT):
                return Qt.AlignmentFlag.AlignCenter
            return Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft

        if role == STATUS_OK_ROLE:
            if col == self.COL_PROGRAM:
                return None if det is None else det.program
            if col == self.COL_DEPLOYMENT:
                return None if det is None else det.deployed

        if role == DETAIL_ROLE:
            return row

        if role == SORT_ROLE:
            if col == self.COL_PROGRAM:
                return -1 if det is None else int(det.program)
            if col == self.COL_DEPLOYMENT:
                return -1 if det is None else int(det.deployed)
            return self.data(index, int(Qt.ItemDataRole.DisplayRole))

        return None

    def _tooltip(self, row: AgentRow) -> str:
        parts = [row.spec.summary, f"{t('root_prefix')}{row.root or t('root_not_set')}"]
        if row.detection is not None:
            parts.extend([row.detection.program_detail, row.detection.deployed_detail])
        return "\n".join(parts)

    def row_at(self, row: int) -> AgentRow:
        return self._rows[row]

    def row_for_name(self, name: str) -> int | None:
        for index, row in enumerate(self._rows):
            if name in row.specs:
                return index
        return None

    def root_for(self, name: str) -> Path | None:
        row_index = self.row_for_name(name)
        if row_index is None:
            return None
        return self._rows[row_index].root_for(name)

    def set_root(self, name: str, root: Path | None) -> None:
        row_index = self.row_for_name(name)
        if row_index is None:
            return
        self._rows[row_index].roots[name] = root
        left = self.index(row_index, 0)
        right = self.index(row_index, self.columnCount() - 1)
        self.dataChanged.emit(left, right, [])

    def set_detection(self, name: str, detection: Detection | None) -> None:
        row_index = self.row_for_name(name)
        if row_index is None:
            return
        self._rows[row_index].detections[name] = detection
        left = self.index(row_index, 0)
        right = self.index(row_index, self.columnCount() - 1)
        self.dataChanged.emit(left, right, [])

    def set_busy(self, name: str | None, busy: bool) -> None:
        if name is None:
            return
        row_index = self.row_for_name(name)
        if row_index is None:
            return
        if busy:
            self._rows[row_index].busy_names.add(name)
        else:
            self._rows[row_index].busy_names.discard(name)
        left = self.index(row_index, 0)
        right = self.index(row_index, self.columnCount() - 1)
        self.dataChanged.emit(left, right, [])

    def update_specs(self, specs: list[AgentSpec]) -> None:
        by_name = {spec.name: spec for spec in specs}
        for row in self._rows:
            for name in tuple(row.specs):
                if name in by_name:
                    row.specs[name] = by_name[name]
        if self._rows:
            self.headerDataChanged.emit(Qt.Orientation.Horizontal, 0, self.columnCount() - 1)
            self.dataChanged.emit(self.index(0, 0), self.index(len(self._rows) - 1, self.columnCount() - 1), [])

    def set_selected_spec(self, row_index: int, name: str) -> None:
        if row_index < 0 or row_index >= len(self._rows):
            return
        row = self._rows[row_index]
        if name not in row.specs or row.selected_name == name:
            return
        row.selected_name = name
        left = self.index(row_index, 0)
        right = self.index(row_index, self.columnCount() - 1)
        self.dataChanged.emit(left, right, [])

    def metrics(self) -> tuple[int, int, int, int]:
        total = len(self._rows)
        deployed = sum(1 for row in self._rows if row.detection and row.detection.deployed)
        programs = sum(1 for row in self._rows if row.detection and row.detection.program)
        missing_roots = sum(1 for row in self._rows if row.root is None)
        return total, deployed, programs, missing_roots


class AgentFilterProxyModel(QSortFilterProxyModel):
    def __init__(self) -> None:
        super().__init__()
        self._text = ""
        self._scope = "all"
        self.setSortRole(SORT_ROLE)

    def set_filter_text(self, text: str) -> None:
        self._text = text.strip().lower()
        self.invalidateFilter()

    def set_scope(self, scope: str) -> None:
        self._scope = scope
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:  # noqa: N802
        model = self.sourceModel()
        if not isinstance(model, AgentTableModel):
            return True
        row = model.row_at(source_row)

        if self._scope == "attention" and not self._needs_attention(row):
            return False

        if not self._text:
            return True

        haystack = " ".join(
            [
                " ".join(spec.name for spec in row.specs.values()),
                " ".join(spec.display_name for spec in row.specs.values()),
                " ".join(spec.summary for spec in row.specs.values()),
                " ".join(str(root or "") for root in row.roots.values()),
                " ".join(" ".join(spec.needs_profiles) for spec in row.specs.values()),
            ]
        ).lower()
        return self._text in haystack

    @staticmethod
    def _needs_attention(row: AgentRow) -> bool:
        if row.root is None:
            return True
        if row.detection is None:
            return True
        return not row.detection.deployed


class StatusPillDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        ok = index.data(STATUS_OK_ROLE)
        text = str(index.data(Qt.ItemDataRole.DisplayRole) or "")

        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.text = ""
        if option.widget is not None:
            option.widget.style().drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, option.widget)

        if ok is True:
            bg = QColor(styles.SUCCESS if index.column() == AgentTableModel.COL_PROGRAM else styles.PRIMARY)
            fg = QColor("#FFFFFF")
        elif ok is False:
            bg = QColor("#E8EDF2")
            fg = QColor(styles.TEXT_SECONDARY)
        else:
            bg = QColor("#F3F5F7")
            fg = QColor(styles.TEXT_TERTIARY)

        rect = option.rect.adjusted(9, 7, -9, -7)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 12, 12)
        painter.setPen(fg)
        painter.setFont(_font(styles.FONT_TAG))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
        painter.restore()


class AppWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.version, self.profiles = _load_release_meta()
        self._app_config = config.AppConfig.load()
        set_language(self._app_config.language)

        self._worker = Worker()
        self._busy_agent: str | None = None
        self._log_lines: list[tuple[str, str]] = []

        self._init_repo_root()

        specs = agents.all_agents()
        roots = {spec.name: spec.default_root_fn() for spec in specs}
        self._model = AgentTableModel(specs, roots)
        self._proxy = AgentFilterProxyModel()
        self._proxy.setSourceModel(self._model)

        self._build_ui()
        self._set_window_icon()
        self._apply_theme(self._app_config.theme)
        self._refresh_static_texts()
        self._select_first_row()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._drain_events)
        self._timer.start(80)
        QTimer.singleShot(0, self._refresh_all_detection)

    def _set_window_icon(self) -> None:
        ico_path = _asset_path("brand-logo.ico")
        png_path = _asset_path("brand-logo.png")
        path = ico_path if sys.platform.startswith("win") and ico_path.exists() else png_path
        if path.exists():
            icon = QIcon(str(path))
            self.setWindowIcon(icon)
            app = QApplication.instance()
            if app is not None:
                app.setWindowIcon(icon)

    def _init_repo_root(self) -> None:
        if not deployer.is_frozen():
            return

        env_root = os.environ.get("ECS_REPO_ROOT")
        if env_root:
            try:
                deployer.set_repo_root(Path(env_root))
                return
            except deployer.DeployError:
                pass

        exe_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else None
        if exe_dir:
            candidate = exe_dir
            for _ in range(5):
                try:
                    deployer.set_repo_root(candidate)
                    self._app_config.repo_root = str(candidate)
                    self._app_config.save()
                    return
                except deployer.DeployError:
                    parent = candidate.parent
                    if parent == candidate:
                        break
                    candidate = parent

        if self._app_config.repo_root:
            try:
                deployer.set_repo_root(Path(self._app_config.repo_root))
                return
            except deployer.DeployError:
                pass

        workspace = (exe_dir or Path.cwd()) / "workspace"
        workspace.mkdir(parents=True, exist_ok=True)
        deployer.set_repo_root(workspace, validate=False)
        self._app_config.repo_root = str(workspace)
        self._app_config.save()

    def _build_ui(self) -> None:
        self.setMinimumSize(styles.WINDOW_MIN_W, styles.WINDOW_MIN_H)

        central = QWidget(self)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.setCentralWidget(central)

        self._build_topbar(root)

        main_splitter = QSplitter(Qt.Orientation.Vertical, central)
        main_splitter.setChildrenCollapsible(False)
        root.addWidget(main_splitter, 1)

        body = QWidget(main_splitter)
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(styles.PAD, styles.PAD, styles.PAD, styles.PAD_SM)
        body_layout.setSpacing(styles.PAD)
        main_splitter.addWidget(body)

        content_splitter = QSplitter(Qt.Orientation.Horizontal, body)
        content_splitter.setChildrenCollapsible(False)
        body_layout.addWidget(content_splitter, 1)

        content_splitter.addWidget(self._build_table_panel(content_splitter))
        content_splitter.addWidget(self._build_detail_panel(content_splitter))
        content_splitter.setSizes([790, 370])

        main_splitter.addWidget(self._build_log_panel(main_splitter))
        main_splitter.setSizes([600, 210])

    def _build_topbar(self, root: QVBoxLayout) -> None:
        topbar = QFrame(self)
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(styles.TOPBAR_HEIGHT)
        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(styles.PAD, 0, styles.PAD, 0)
        layout.setSpacing(styles.PAD_SM)

        self._title_label = QLabel(topbar)
        self._title_label.setFont(_font(styles.FONT_TITLE))
        self._title_label.setObjectName("topbarTitle")
        self._title_label.setMinimumWidth(420)
        self._title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(self._title_label, 1)

        self._version_label = QLabel(topbar)
        self._version_label.setObjectName("versionTag")
        self._version_label.setFont(_font(styles.FONT_TAG))
        layout.addWidget(self._version_label, 0)
        layout.addStretch(0)

        self._language_combo = QComboBox(topbar)
        self._language_combo.setObjectName("topbarCombo")
        self._language_combo.currentIndexChanged.connect(self._on_language_changed)
        layout.addWidget(self._language_combo, 0)

        self._theme_combo = QComboBox(topbar)
        self._theme_combo.setObjectName("topbarCombo")
        self._theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        layout.addWidget(self._theme_combo, 0)

        root.addWidget(topbar)

    def _build_table_panel(self, parent: QWidget) -> QWidget:
        panel = QFrame(parent)
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(styles.PAD, styles.PAD, styles.PAD, styles.PAD)
        layout.setSpacing(styles.PAD_SM)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(styles.PAD_SM)

        self._target_label = QLabel(panel)
        self._target_label.setObjectName("sectionTitle")
        self._target_label.setFont(_font(styles.FONT_HEADING))
        toolbar.addWidget(self._target_label)
        toolbar.addStretch(1)

        self._filter_edit = QLineEdit(panel)
        self._filter_edit.setClearButtonEnabled(True)
        self._filter_edit.setMinimumWidth(220)
        self._filter_edit.textChanged.connect(self._proxy.set_filter_text)
        toolbar.addWidget(self._filter_edit)

        self._scope_combo = QComboBox(panel)
        self._scope_combo.currentIndexChanged.connect(self._on_scope_changed)
        self._scope_combo.setMinimumWidth(110)
        toolbar.addWidget(self._scope_combo)

        self._rescan_btn = self._tool_button(
            t("btn_rescan"),
            QStyle.StandardPixmap.SP_BrowserReload,
            self._refresh_all_detection,
            panel,
        )
        toolbar.addWidget(self._rescan_btn)

        self._build_all_btn = self._tool_button(
            t("btn_build_all"),
            QStyle.StandardPixmap.SP_DialogApplyButton,
            self._on_build_all,
            panel,
            variant="primary",
        )
        toolbar.addWidget(self._build_all_btn)
        layout.addLayout(toolbar)

        metric_row = QHBoxLayout()
        metric_row.setSpacing(styles.PAD_SM)
        self._metric_targets = self._metric_label(panel)
        self._metric_deployed = self._metric_label(panel)
        self._metric_programs = self._metric_label(panel)
        self._metric_missing_roots = self._metric_label(panel)
        for label in (
            self._metric_targets,
            self._metric_deployed,
            self._metric_programs,
            self._metric_missing_roots,
        ):
            metric_row.addWidget(label)
        metric_row.addStretch(1)
        layout.addLayout(metric_row)

        self._table = QTableView(panel)
        self._table.setModel(self._proxy)
        self._table.setIconSize(QSize(24, 24))
        self._table.setItemDelegateForColumn(AgentTableModel.COL_PROGRAM, StatusPillDelegate(self._table))
        self._table.setItemDelegateForColumn(AgentTableModel.COL_DEPLOYMENT, StatusPillDelegate(self._table))
        self._table.setAlternatingRowColors(True)
        self._table.setSortingEnabled(True)
        self._table.sortByColumn(AgentTableModel.COL_AGENT, Qt.SortOrder.AscendingOrder)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self._table.setShowGrid(False)
        self._table.verticalHeader().setVisible(False)
        self._table.verticalHeader().setDefaultSectionSize(46)
        self._table.horizontalHeader().setHighlightSections(False)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_AGENT, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_PROGRAM, QHeaderView.ResizeMode.Fixed)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_DEPLOYMENT, QHeaderView.ResizeMode.Fixed)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_ROOT, QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_PROFILES, QHeaderView.ResizeMode.ResizeToContents)
        self._table.setColumnWidth(AgentTableModel.COL_PROGRAM, 104)
        self._table.setColumnWidth(AgentTableModel.COL_DEPLOYMENT, 88)
        self._table.selectionModel().currentChanged.connect(self._on_current_changed)
        self._table.doubleClicked.connect(lambda _index: self._on_verify_selected())
        layout.addWidget(self._table, 1)

        return panel

    def _build_detail_panel(self, parent: QWidget) -> QWidget:
        panel = QFrame(parent)
        panel.setObjectName("panel")
        panel.setMinimumWidth(350)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(styles.PAD, styles.PAD, styles.PAD, styles.PAD)
        layout.setSpacing(styles.PAD_SM)

        header = QHBoxLayout()
        header.setSpacing(styles.PAD_SM)
        self._detail_icon = QLabel(panel)
        self._detail_icon.setObjectName("agentIcon")
        self._detail_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._detail_icon.setFixedSize(38, 38)
        self._detail_icon.setFont(_font(styles.FONT_SUBTITLE, bold=True))
        header.addWidget(self._detail_icon)

        title_stack = QVBoxLayout()
        title_stack.setSpacing(2)
        self._detail_name = QLabel(panel)
        self._detail_name.setObjectName("detailTitle")
        self._detail_name.setFont(_font(styles.FONT_HEADING))
        title_stack.addWidget(self._detail_name)
        self._detail_summary = QLabel(panel)
        self._detail_summary.setObjectName("muted")
        self._detail_summary.setWordWrap(True)
        title_stack.addWidget(self._detail_summary)
        header.addLayout(title_stack, 1)
        layout.addLayout(header)

        self._root_hint = QLabel(panel)
        self._root_hint.setObjectName("rootHint")
        self._root_hint.setWordWrap(True)
        layout.addWidget(self._root_hint)

        mode_row = QHBoxLayout()
        mode_row.setSpacing(styles.PAD_SM)
        self._mode_caption = QLabel(panel)
        self._mode_caption.setObjectName("fieldCaption")
        self._mode_caption.setFixedWidth(78)
        self._mode_caption.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        mode_row.addWidget(self._mode_caption, 0)
        self._mode_combo = QComboBox(panel)
        self._mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        mode_row.addWidget(self._mode_combo, 1)
        layout.addLayout(mode_row)

        details = QGridLayout()
        details.setContentsMargins(0, styles.PAD_SM, 0, styles.PAD_SM)
        details.setHorizontalSpacing(styles.PAD_SM)
        details.setVerticalSpacing(12)

        self._root_caption = QLabel(panel)
        self._root_value = QLabel(panel)
        self._root_value.setWordWrap(True)
        self._program_caption = QLabel(panel)
        self._program_value = QLabel(panel)
        self._program_value.setWordWrap(True)
        self._program_value.setMinimumHeight(44)
        self._deploy_caption = QLabel(panel)
        self._deploy_value = QLabel(panel)
        self._deploy_value.setWordWrap(True)
        self._deploy_value.setMinimumHeight(44)
        self._profiles_caption = QLabel(panel)
        self._profiles_value = QLabel(panel)
        self._profiles_value.setWordWrap(True)

        rows = [
            (self._root_caption, self._root_value),
            (self._program_caption, self._program_value),
            (self._deploy_caption, self._deploy_value),
            (self._profiles_caption, self._profiles_value),
        ]
        for row_index, (caption, value) in enumerate(rows):
            caption.setObjectName("fieldCaption")
            caption.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
            caption.setFixedWidth(50)
            value.setObjectName("fieldValue")
            details.addWidget(caption, row_index, 0)
            details.addWidget(value, row_index, 1)
        details.setColumnMinimumWidth(0, 50)
        details.setColumnStretch(1, 1)
        layout.addLayout(details)

        action_title = QLabel(panel)
        action_title.setObjectName("sectionTitle")
        action_title.setFont(_font(styles.FONT_SUBTITLE))
        self._actions_title = action_title
        layout.addWidget(action_title)

        button_grid = QGridLayout()
        button_grid.setSpacing(styles.PAD_SM)
        self._deploy_btn = self._push_button(t("btn_deploy"), self._on_deploy_selected, panel, "primary")
        self._verify_btn = self._push_button(t("btn_verify"), self._on_verify_selected, panel)
        self._folder_btn = self._push_button(t("btn_folder"), self._on_pick_root_selected, panel)
        self._open_root_btn = self._push_button(t("btn_open_root"), self._on_open_root, panel)
        self._remove_btn = self._push_button(t("btn_remove"), self._on_uninstall_selected, panel, "danger")
        button_grid.addWidget(self._deploy_btn, 0, 0)
        button_grid.addWidget(self._verify_btn, 0, 1)
        button_grid.addWidget(self._folder_btn, 1, 0)
        button_grid.addWidget(self._open_root_btn, 1, 1)
        button_grid.addWidget(self._remove_btn, 2, 0, 1, 2)
        layout.addLayout(button_grid)

        layout.addStretch(1)

        repo_row = QHBoxLayout()
        repo_row.setSpacing(styles.PAD_SM)
        self._repo_label = QLabel(panel)
        self._repo_label.setObjectName("muted")
        self._repo_label.setWordWrap(True)
        repo_row.addWidget(self._repo_label, 1)
        self._repo_btn = self._push_button(t("btn_repo"), self._change_repo_root, panel)
        repo_row.addWidget(self._repo_btn, 0)
        layout.addLayout(repo_row)

        return panel

    def _build_log_panel(self, parent: QWidget) -> QWidget:
        panel = QFrame(parent)
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(styles.PAD, styles.PAD_SM, styles.PAD, styles.PAD)
        layout.setSpacing(styles.PAD_SM)

        progress_row = QHBoxLayout()
        progress_row.setSpacing(styles.PAD_SM)
        self._progress = QProgressBar(panel)
        self._progress.setRange(0, 1000)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(8)
        progress_row.addWidget(self._progress, 1)
        self._status_label = QLabel(panel)
        self._status_label.setObjectName("muted")
        self._status_label.setMinimumWidth(260)
        progress_row.addWidget(self._status_label)
        layout.addLayout(progress_row)

        header = QHBoxLayout()
        self._log_title = QLabel(panel)
        self._log_title.setObjectName("sectionTitle")
        self._log_title.setFont(_font(styles.FONT_SUBTITLE))
        header.addWidget(self._log_title)
        header.addStretch(1)
        self._clear_log_btn = self._tool_button(
            t("btn_clear_log"),
            QStyle.StandardPixmap.SP_DialogResetButton,
            self._clear_log,
            panel,
        )
        header.addWidget(self._clear_log_btn)
        self._stop_btn = self._tool_button(
            t("btn_stop"),
            QStyle.StandardPixmap.SP_MediaStop,
            self._on_stop,
            panel,
            variant="danger",
        )
        self._stop_btn.setEnabled(False)
        header.addWidget(self._stop_btn)
        layout.addLayout(header)

        self._log_text = QTextEdit(panel)
        self._log_text.setReadOnly(True)
        self._log_text.setFont(_font(("Consolas", 10)))
        self._log_text.setMinimumHeight(130)
        layout.addWidget(self._log_text, 1)

        return panel

    def _tool_button(
        self,
        text: str,
        icon: QStyle.StandardPixmap,
        slot: Any,
        parent: QWidget,
        *,
        variant: str = "secondary",
    ) -> QToolButton:
        button = QToolButton(parent)
        button.setText(text)
        button.setIcon(self.style().standardIcon(icon))
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        button.setProperty("variant", variant)
        button.clicked.connect(slot)
        return button

    def _push_button(self, text: str, slot: Any, parent: QWidget, variant: str = "secondary") -> QPushButton:
        button = QPushButton(text, parent)
        button.setProperty("variant", variant)
        button.clicked.connect(slot)
        button.setMinimumHeight(34)
        return button

    def _metric_label(self, parent: QWidget) -> QLabel:
        label = QLabel(parent)
        label.setObjectName("metric")
        label.setFont(_font(styles.FONT_TAG))
        return label

    def _refresh_static_texts(self) -> None:
        self.setWindowTitle(f"{t('window_title')}  v{self.version}")
        self._title_label.setText(t("title"))
        self._version_label.setText(f"v{self.version}")
        self._target_label.setText(t("target_agents"))
        self._filter_edit.setPlaceholderText(t("filter_placeholder"))
        self._rescan_btn.setText(t("btn_rescan"))
        self._build_all_btn.setText(t("btn_build_all"))
        self._actions_title.setText(t("actions_title"))
        self._mode_caption.setText(t("detail_mode"))
        self._root_caption.setText(t("detail_root"))
        self._program_caption.setText(t("detail_program"))
        self._deploy_caption.setText(t("detail_deployment"))
        self._profiles_caption.setText(t("detail_profiles"))
        self._deploy_btn.setText(t("btn_deploy"))
        self._verify_btn.setText(t("btn_verify"))
        self._folder_btn.setText(t("btn_folder"))
        self._open_root_btn.setText(t("btn_open_root"))
        self._remove_btn.setText(t("btn_remove"))
        self._repo_btn.setText(t("btn_repo"))
        self._log_title.setText(t("log_title"))
        self._clear_log_btn.setText(t("btn_clear_log"))
        self._stop_btn.setText(t("btn_stop"))
        self._status_label.setText(t("status_ready"))
        self._refresh_repo_label()
        self._refresh_combo_texts()
        self._refresh_metrics()
        self._refresh_detail()

    def _refresh_combo_texts(self) -> None:
        current_lang = self._app_config.language
        self._language_combo.blockSignals(True)
        self._language_combo.clear()
        self._language_combo.addItem(t("lang_en"), "en")
        self._language_combo.addItem(t("lang_zh"), "zh")
        self._language_combo.setCurrentIndex(1 if current_lang == "zh" else 0)
        self._language_combo.blockSignals(False)

        current_theme = self._app_config.theme
        self._theme_combo.blockSignals(True)
        self._theme_combo.clear()
        for mode, key in (("Light", "theme_light"), ("Dark", "theme_dark"), ("System", "theme_system")):
            self._theme_combo.addItem(t(key), mode)
        theme_index = max(0, self._theme_combo.findData(current_theme))
        self._theme_combo.setCurrentIndex(theme_index)
        self._theme_combo.blockSignals(False)

        current_scope = self._scope_combo.currentData() or "all"
        self._scope_combo.blockSignals(True)
        self._scope_combo.clear()
        for scope, key in (
            ("all", "scope_all"),
            ("attention", "scope_attention"),
        ):
            self._scope_combo.addItem(t(key), scope)
        scope_index = max(0, self._scope_combo.findData(current_scope))
        self._scope_combo.setCurrentIndex(scope_index)
        self._scope_combo.blockSignals(False)

    def _apply_theme(self, mode: str) -> None:
        dark = mode.lower() == "dark"
        colors = self._theme_colors(dark)
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {colors['windowGradient']};
            }}
            QWidget {{
                color: {colors['text']};
                font-family: "{styles.FONT_FAMILY}";
            }}
            QFrame#topbar {{
                background: {colors['topbarGradient']};
            }}
            QFrame#topbar QLabel {{
                background: transparent;
            }}
            QLabel#topbarTitle {{
                color: white;
            }}
            QLabel#versionTag {{
                color: {styles.ACCENT_PALE};
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.20);
                border-radius: 10px;
                padding: 3px 9px;
            }}
            QComboBox#topbarCombo {{
                background: rgba(255, 255, 255, 0.18);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.30);
                border-radius: 9px;
                padding: 5px 9px;
            }}
            QFrame#panel {{
                background: {colors['panelGlass']};
                border: 1px solid {colors['panelBorder']};
                border-radius: 14px;
            }}
            QLabel#sectionTitle, QLabel#detailTitle {{
                color: {colors['text']};
            }}
            QLabel#muted, QLabel#fieldCaption {{
                color: {colors['muted']};
            }}
            QLabel#rootHint {{
                background: {colors['hintGlass']};
                color: {colors['muted']};
                border: 1px solid {colors['panelBorder']};
                border-radius: 9px;
                padding: 8px 10px;
            }}
            QLabel#fieldValue {{
                color: {colors['text']};
            }}
            QLabel#agentIcon {{
                background: {colors['chipGlass']};
                color: {colors['text']};
                border: 1px solid {colors['panelBorder']};
                border-radius: 11px;
            }}
            QLabel#metric {{
                background: {colors['chipGlass']};
                color: {colors['text']};
                border: 1px solid {colors['panelBorder']};
                border-radius: 12px;
                padding: 4px 10px;
            }}
            QLineEdit, QComboBox {{
                background: {colors['inputGlass']};
                color: {colors['text']};
                border: 1px solid {colors['panelBorder']};
                border-radius: 9px;
                padding: 6px 9px;
                selection-background-color: {colors['selection']};
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 1px solid {styles.PRIMARY_LIGHT};
            }}
            QTableView {{
                background: {colors['tableGlass']};
                alternate-background-color: {colors['alt']};
                color: {colors['text']};
                border: 1px solid {colors['panelBorder']};
                border-radius: 11px;
                selection-background-color: {colors['selection']};
                selection-color: {colors['selectionText']};
            }}
            QHeaderView::section {{
                background: {colors['headerGlass']};
                color: {colors['muted']};
                border: none;
                border-bottom: 1px solid {colors['panelBorder']};
                padding: 8px 8px;
                font-weight: 700;
            }}
            QTextEdit {{
                background: {colors['inputGlass']};
                color: {colors['text']};
                border: 1px solid {colors['panelBorder']};
                border-radius: 11px;
                padding: 8px;
            }}
            QProgressBar {{
                background: {colors['chipGlass']};
                border: none;
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background: {colors['progressGradient']};
                border-radius: 5px;
            }}
            QPushButton, QToolButton {{
                background: {colors['buttonGlass']};
                color: {colors['text']};
                border: 1px solid {colors['panelBorder']};
                border-radius: 9px;
                padding: 8px 12px;
            }}
            QPushButton:hover, QToolButton:hover {{
                background: {colors['buttonHover']};
            }}
            QPushButton[variant="primary"], QToolButton[variant="primary"] {{
                background: {colors['primaryButton']};
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.18);
            }}
            QPushButton[variant="primary"]:hover, QToolButton[variant="primary"]:hover {{
                background: {colors['primaryButtonHover']};
            }}
            QPushButton[variant="danger"], QToolButton[variant="danger"] {{
                background: {colors['dangerButton']};
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.14);
            }}
            QPushButton[variant="danger"]:hover, QToolButton[variant="danger"]:hover {{
                background: {styles.DANGER_HOVER};
            }}
            QPushButton:disabled, QToolButton:disabled {{
                color: {colors['disabledText']};
                background: {colors['disabled']};
                border-color: {colors['border']};
            }}
            """
        )

    @staticmethod
    def _theme_colors(dark: bool) -> dict[str, str]:
        if dark:
            return {
                "windowGradient": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0E1724, stop:1 #172338)",
                "topbarGradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #005EB8, stop:0.55 #0B73CE, stop:1 #003C7A)",
                "panelGlass": "rgba(22, 36, 54, 218)",
                "panelBorder": "rgba(148, 176, 205, 0.22)",
                "inputGlass": "rgba(13, 20, 28, 185)",
                "buttonGlass": "rgba(28, 48, 71, 195)",
                "buttonHover": "rgba(38, 62, 89, 230)",
                "chipGlass": "rgba(28, 48, 71, 185)",
                "hintGlass": "rgba(19, 32, 51, 185)",
                "tableGlass": "rgba(22, 36, 54, 200)",
                "headerGlass": "rgba(16, 24, 32, 210)",
                "primaryButton": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0B73CE, stop:1 #005EB8)",
                "primaryButtonHover": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1383E4, stop:1 #0068C9)",
                "dangerButton": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E34034, stop:1 #C52418)",
                "progressGradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4EA3F1, stop:1 #005EB8)",
                "alt": "#132033",
                "border": "#2C4158",
                "text": "#E8EDF2",
                "muted": "#9AA8B7",
                "selection": "#204F7F",
                "selectionText": "#FFFFFF",
                "disabled": "#172535",
                "disabledText": "#66788A",
            }
        return {
            "windowGradient": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E8F1F8, stop:0.48 #F6F8FB, stop:1 #EAF0F5)",
            "topbarGradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #005EB8, stop:0.55 #0878D8, stop:1 #003087)",
            "panelGlass": "rgba(255, 255, 255, 218)",
            "panelBorder": "rgba(124, 145, 164, 0.32)",
            "inputGlass": "rgba(255, 255, 255, 224)",
            "buttonGlass": "rgba(255, 255, 255, 212)",
            "buttonHover": "rgba(232, 241, 248, 238)",
            "chipGlass": "rgba(255, 255, 255, 180)",
            "hintGlass": "rgba(247, 249, 250, 214)",
            "tableGlass": "rgba(255, 255, 255, 205)",
            "headerGlass": "rgba(240, 244, 245, 225)",
            "primaryButton": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0878D8, stop:1 #005EB8)",
            "primaryButtonHover": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0B86EA, stop:1 #0068C9)",
            "dangerButton": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #E34034, stop:1 #C52418)",
            "progressGradient": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #51A7F5, stop:1 #005EB8)",
            "alt": "rgba(247, 249, 250, 210)",
            "border": styles.BORDER,
            "text": styles.TEXT_PRIMARY,
            "muted": styles.TEXT_SECONDARY,
            "selection": "#D7E8F6",
            "selectionText": styles.TEXT_PRIMARY,
            "disabled": "#F3F5F7",
            "disabledText": "#9AA5B1",
        }

    def _on_language_changed(self) -> None:
        lang = self._language_combo.currentData()
        if lang not in ("en", "zh") or lang == self._app_config.language:
            return
        set_language(lang)
        self._app_config.language = lang
        self._app_config.save()
        self._model.update_specs(agents.rebuild_specs())
        self._refresh_static_texts()
        self._refresh_all_detection()

    def _on_theme_changed(self) -> None:
        mode = self._theme_combo.currentData()
        if not mode:
            return
        self._app_config.theme = str(mode)
        self._app_config.save()
        self._apply_theme(str(mode))

    def _on_scope_changed(self) -> None:
        self._proxy.set_scope(str(self._scope_combo.currentData() or "all"))
        self._select_first_row()

    def _refresh_repo_label(self) -> None:
        if deployer.REPO_ROOT is None:
            self._repo_label.setText(t("repo_not_set"))
        else:
            self._repo_label.setText(f"{t('repo_prefix')}{deployer.REPO_ROOT}")

    def _select_first_row(self) -> None:
        if self._proxy.rowCount() <= 0:
            self._refresh_detail()
            return
        index = self._proxy.index(0, 0)
        self._table.setCurrentIndex(index)
        self._table.selectRow(0)
        self._refresh_detail()

    def _selected_source_row(self) -> AgentRow | None:
        source_index = self._selected_source_index()
        if source_index is None:
            return None
        return self._model.row_at(source_index.row())

    def _selected_source_index(self) -> QModelIndex | None:
        proxy_index = self._table.currentIndex()
        if not proxy_index.isValid():
            return None
        source_index = self._proxy.mapToSource(proxy_index)
        if not source_index.isValid():
            return None
        return source_index

    def _on_current_changed(self, _current: QModelIndex, _previous: QModelIndex) -> None:
        self._refresh_detail()

    @staticmethod
    def _mode_label(spec: AgentSpec) -> str:
        return t("deploy_mode_project") if spec.kind == "project" else t("deploy_mode_user")

    def _refresh_detail(self) -> None:
        row = self._selected_source_row()
        busy = self._worker.is_busy()
        if row is None:
            self._detail_icon.setPixmap(QPixmap())
            self._detail_icon.setText("")
            self._detail_name.setText(t("panel_no_selection"))
            self._detail_summary.setText("")
            self._root_hint.setText("")
            self._root_hint.setVisible(False)
            self._root_value.setText("")
            self._program_value.setText("")
            self._deploy_value.setText("")
            self._profiles_value.setText("")
            self._set_action_buttons_enabled(False)
            self._folder_btn.setText(t("btn_folder"))
            self._mode_caption.setVisible(False)
            self._mode_combo.setVisible(False)
            self._mode_combo.clear()
            return

        spec = row.spec
        det = row.detection
        logo_path = _agent_logo_path(row.display_spec.name)
        if logo_path is not None:
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                self._detail_icon.setPixmap(
                    pixmap.scaled(QSize(28, 28), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                )
                self._detail_icon.setText("")
            else:
                self._detail_icon.setPixmap(QPixmap())
                self._detail_icon.setText(row.display_spec.icon)
        else:
            self._detail_icon.setPixmap(QPixmap())
            self._detail_icon.setText(row.display_spec.icon)
        self._detail_name.setText(row.display_spec.display_name)
        self._detail_summary.setText(spec.summary)
        self._mode_caption.setVisible(row.has_modes)
        self._mode_combo.setVisible(row.has_modes)
        self._mode_combo.blockSignals(True)
        self._mode_combo.clear()
        for name in row.mode_order:
            mode_spec = row.specs[name]
            self._mode_combo.addItem(self._mode_label(mode_spec), name)
        mode_index = max(0, self._mode_combo.findData(row.selected_name))
        self._mode_combo.setCurrentIndex(mode_index)
        self._mode_combo.blockSignals(False)
        self._root_hint.setVisible(row.root is None)
        if row.root is None:
            hint_key = "project_root_required_hint" if spec.kind == "project" else "install_root_required_hint"
            self._root_hint.setText(t(hint_key))
        else:
            self._root_hint.setText("")
        self._root_value.setText(_root_detail_text(row.root))
        self._profiles_value.setText(", ".join(spec.needs_profiles) if spec.needs_profiles else "-")
        if det is None:
            self._program_value.setText(t("checking"))
            self._deploy_value.setText(t("checking"))
        else:
            self._program_value.setText(
                f"{t('program_installed') if det.program else t('program_not_found')}\n{det.program_detail}"
            )
            self._deploy_value.setText(
                f"{t('deployed') if det.deployed else t('not_deployed')}\n{det.deployed_detail}"
            )

        can_act = not busy
        self._deploy_btn.setEnabled(can_act)
        self._verify_btn.setEnabled(can_act)
        self._folder_btn.setText(t("btn_project_root") if spec.kind == "project" else t("btn_folder"))
        self._folder_btn.setEnabled(can_act)
        self._open_root_btn.setEnabled(row.root is not None and Path(row.root).exists())
        self._remove_btn.setEnabled(can_act and spec.supports_uninstall and row.root is not None)

    def _on_mode_changed(self, _index: int = -1) -> None:
        source_index = self._selected_source_index()
        if source_index is None:
            return
        row = self._model.row_at(source_index.row())
        name = self._mode_combo.currentData()
        if not isinstance(name, str) or name == row.selected_name:
            return
        self._model.set_selected_spec(source_index.row(), name)
        spec = row.spec_for(name)
        if spec is not None and row.detections.get(name) is None:
            self._refresh_one(spec)
        self._refresh_metrics()
        self._refresh_detail()

    def _set_action_buttons_enabled(self, enabled: bool) -> None:
        for button in (
            self._deploy_btn,
            self._verify_btn,
            self._folder_btn,
            self._open_root_btn,
            self._remove_btn,
        ):
            button.setEnabled(enabled)

    def _refresh_metrics(self) -> None:
        total, deployed, programs, missing_roots = self._model.metrics()
        self._metric_targets.setText(f"{total} {t('metric_targets')}")
        self._metric_deployed.setText(f"{deployed} {t('metric_deployed')}")
        self._metric_programs.setText(f"{programs} {t('metric_programs')}")
        self._metric_missing_roots.setText(f"{missing_roots} {t('metric_missing_roots')}")

    def _refresh_all_detection(self) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            for row_index in range(self._model.rowCount()):
                row = self._model.row_at(row_index)
                for spec in row.specs.values():
                    self._model.set_detection(spec.name, detector.detect(spec.name, self._model.root_for(spec.name)))
        finally:
            QApplication.restoreOverrideCursor()
        self._refresh_metrics()
        self._refresh_detail()

    def _refresh_one(self, spec: AgentSpec) -> None:
        self._model.set_detection(spec.name, detector.detect(spec.name, self._model.root_for(spec.name)))
        self._refresh_metrics()
        self._refresh_detail()

    def _change_repo_root(self) -> None:
        self._prompt_for_repo_root()

    def _prompt_for_repo_root(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, t("dlg_select_repo_title"))
        if not chosen:
            self._append_log(t("dlg_no_repo_warn"))
            return
        try:
            deployer.set_repo_root(Path(chosen))
        except deployer.DeployError as exc:
            QMessageBox.critical(self, t("dlg_invalid_repo"), str(exc))
            QTimer.singleShot(50, self._prompt_for_repo_root)
            return
        self._app_config.repo_root = chosen
        self._app_config.save()
        self._refresh_repo_label()
        self._append_log(t("log_repo_set", path=chosen))

    def _on_pick_root_selected(self) -> None:
        row = self._selected_source_row()
        if row is None:
            return
        self._on_pick_root(row.spec)

    def _on_pick_root(self, spec: AgentSpec) -> bool:
        title_key = "dlg_select_project_root" if spec.kind == "project" else "dlg_select_install_root"
        chosen = QFileDialog.getExistingDirectory(self, t(title_key, name=spec.display_name))
        if not chosen:
            return False
        self._model.set_root(spec.name, Path(chosen))
        self._refresh_one(spec)
        return True

    def _on_open_root(self) -> None:
        row = self._selected_source_row()
        if row is None or row.root is None:
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(row.root)))

    def _root_provider(self, spec: AgentSpec):
        return lambda: self._model.root_for(spec.name)

    def _submit(self, job: Any, *, busy_agent: str | None = None) -> bool:
        if self._worker.is_busy():
            self._append_log(t("log_job_busy"))
            return False
        self._busy_agent = busy_agent
        self._stop_btn.setEnabled(True)
        self._progress.setValue(0)
        self._status_label.setText(t("progress_starting"))
        self._model.set_busy(busy_agent, True)
        self._refresh_detail()
        ok = self._worker.submit(job)
        if not ok:
            self._append_log(t("log_job_rejected"))
            self._model.set_busy(busy_agent, False)
            self._stop_btn.setEnabled(False)
            self._busy_agent = None
            self._refresh_detail()
        return ok

    def _selected_spec(self) -> AgentSpec | None:
        row = self._selected_source_row()
        return None if row is None else row.spec

    def _on_deploy_selected(self) -> None:
        spec = self._selected_spec()
        if spec is not None:
            self._on_deploy(spec)

    def _on_verify_selected(self) -> None:
        spec = self._selected_spec()
        if spec is not None:
            self._on_verify(spec)

    def _on_uninstall_selected(self) -> None:
        spec = self._selected_spec()
        if spec is not None:
            self._on_uninstall(spec)

    def _on_deploy(self, spec: AgentSpec) -> None:
        if self._model.root_for(spec.name) is None and not self._on_pick_root(spec):
            self._append_log(t("dlg_no_root_warn", name=spec.display_name))
            return
        self._append_log(t("log_deploy", name=spec.display_name))
        self._submit(make_deploy_job(spec, self._root_provider(spec)), busy_agent=spec.name)

    def _on_verify(self, spec: AgentSpec) -> None:
        self._append_log(t("log_verify", name=spec.display_name))
        self._submit(make_verify_job(spec, self._root_provider(spec)), busy_agent=spec.name)

    def _on_uninstall(self, spec: AgentSpec) -> None:
        if self._model.root_for(spec.name) is None:
            QMessageBox.information(
                self,
                t("dlg_select_root_title"),
                t("dlg_select_root_msg", name=spec.display_name),
            )
            return
        reply = QMessageBox.question(
            self,
            t("dlg_confirm_uninstall"),
            t("dlg_confirm_uninstall_msg", name=spec.display_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        self._append_log(t("log_uninstall", name=spec.display_name))
        self._submit(make_uninstall_job(spec, self._root_provider(spec)), busy_agent=spec.name)

    def _on_build_all(self) -> None:
        self._append_log(t("log_build_all"))
        self._submit(make_build_all_job(self.profiles), busy_agent=None)

    def _on_stop(self) -> None:
        self._worker.request_cancel()
        self._append_log(t("log_cancel"))

    def _drain_events(self) -> None:
        try:
            while True:
                event: Event = self._worker.events.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass

    def _handle_event(self, event: Event) -> None:
        if event.kind is EventKind.LOG:
            self._append_log(str(event.payload))
            return
        if event.kind is EventKind.PROGRESS:
            fraction, label = event.payload
            self._progress.setValue(int(max(0.0, min(1.0, fraction)) * 1000))
            self._status_label.setText(str(label))
            return
        if event.kind is EventKind.STARTED:
            self._status_label.setText(str(event.payload))
            self._progress.setValue(0)
            return
        if event.kind is EventKind.DONE:
            ok, message = event.payload
            self._stop_btn.setEnabled(False)
            finished_agent = self._busy_agent
            self._model.set_busy(finished_agent, False)
            self._busy_agent = None

            if finished_agent:
                spec = agents.get(finished_agent)
                if spec is not None:
                    self._refresh_one(spec)
            else:
                self._refresh_all_detection()

            if ok:
                text = f"{t('progress_done')} - {message}"
                self._progress.setValue(1000)
                self._status_label.setText(text)
                self._append_log(t("log_done", msg=message))
            else:
                text = f"{t('progress_failed')} - {message}"
                self._status_label.setText(text)
                self._append_log(t("log_error", msg=message))
            self._refresh_detail()

    def _append_log(self, line: str) -> None:
        color = self._log_color(line)
        self._log_lines.append((line, color))
        if len(self._log_lines) > MAX_LOG_LINES:
            self._log_lines = self._log_lines[-MAX_LOG_LINES:]
            self._rebuild_log()
            return

        self._log_text.moveCursor(QTextCursor.MoveOperation.End)
        self._log_text.insertHtml(f'<span style="color:{color}">{escape(line)}</span><br>')
        self._log_text.verticalScrollBar().setValue(self._log_text.verticalScrollBar().maximum())

    def _rebuild_log(self) -> None:
        html = "".join(f'<span style="color:{color}">{escape(line)}</span><br>' for line, color in self._log_lines)
        self._log_text.setHtml(html)
        self._log_text.verticalScrollBar().setValue(self._log_text.verticalScrollBar().maximum())

    def _clear_log(self) -> None:
        self._log_lines.clear()
        self._log_text.clear()

    @staticmethod
    def _log_color(line: str) -> str:
        lower = line.lower()
        if line.startswith("$ "):
            return styles.TEXT_SECONDARY
        if "[error]" in lower or "traceback" in lower or "failed" in lower or "[错误]" in line:
            return styles.DANGER
        if "[verify]" in lower or "[done]" in lower or "complete" in lower or "[完成]" in line:
            return styles.SUCCESS
        if "[backup]" in lower or "[skip]" in lower or "warning" in lower or "[警告]" in line:
            return "#B36B00"
        return styles.TEXT_PRIMARY


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    app = QApplication.instance() or QApplication(args)
    window = AppWindow()
    if "--smoke" in args:
        window.show()
        app.processEvents()
        window.close()
        return 0
    window.show()
    return int(app.exec())
