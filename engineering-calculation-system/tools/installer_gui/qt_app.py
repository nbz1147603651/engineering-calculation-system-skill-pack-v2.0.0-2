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
    QPalette,
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
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStyle,
    QStackedWidget,
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
    bundled = deployer.bundled_runtime_root()
    config_path = (bundled / "tools" / "release_config.json") if bundled else Path(__file__).resolve().parents[1] / "release_config.json"
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        version = data.get("version", "0.0.0")
        profiles = tuple(data.get("default_all_profiles") or data.get("profiles") or ())
        return version, profiles
    except (OSError, ValueError):
        from . import __version__ as pkg_version

        return pkg_version, (
            "core",
            "codex-plugin",
            "adapters-light",
            "qoder-addon",
            "qoder-plugin",
            "qoderworkcn-plugin",
            "singlefile",
            "source-dev",
            "zcode-plugin",
            "ui-client",
        )


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
    "qoderworkcn": "qoderwork-cn.png",
    "workbuddy": "workbuddy.png",
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


def _soft_wrap(text: str) -> str:
    """Allow long native paths to wrap while tooltips retain their exact value."""
    for separator in ("\\", "/", "_"):
        text = text.replace(separator, separator + "\u200b")
    return text


def _dialog_start_dir(path: Path | None) -> str:
    if path is None:
        return ""
    expanded = path.expanduser()
    if expanded.is_dir():
        return str(expanded)
    parent = expanded.parent
    return str(parent) if parent.is_dir() else ""


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
                return t("program_available") if det.program else t("program_unavailable")
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
            return None  # The native palette owns normal and selected text.

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

        dark = option.palette.color(QPalette.ColorRole.Base).lightness() < 128
        if ok is True:
            bg = QColor("#214438" if dark else "#E7F4EB")
            fg = QColor("#9FE0BB" if dark else "#246C41")
        elif ok is False:
            bg = QColor("#35414B" if dark else "#EDF0F3")
            fg = QColor("#CBD4DC" if dark else styles.TEXT_SECONDARY)
        else:
            bg = QColor("#F3F5F7")
            fg = QColor(styles.TEXT_TERTIARY)

        rect = option.rect.adjusted(9, 7, -9, -7)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(rect, 5, 5)
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
        roots = {spec.name: self._configured_root_for(spec) for spec in specs}
        self._model = AgentTableModel(specs, roots)
        self._proxy = AgentFilterProxyModel()
        self._proxy.setSourceModel(self._model)

        self._build_ui()
        self._set_window_icon()
        self._apply_theme(self._app_config.theme)
        self._refresh_static_texts()
        self._select_first_row()
        codex_row = self._model.row_for_name("codex")
        if codex_row is not None:
            self._table.setCurrentIndex(self._proxy.mapFromSource(self._model.index(codex_row, 0)))

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._drain_events)
        self._timer.start(80)
        QTimer.singleShot(0, self._refresh_all_detection)

    def _set_window_icon(self) -> None:
        ico_path = _asset_path("nimo-mascot.ico")
        png_path = _asset_path("nimo-mascot.png")
        path = ico_path if sys.platform.startswith("win") and ico_path.exists() else png_path
        if path.exists():
            icon = QIcon(str(path))
            self.setWindowIcon(icon)
            app = QApplication.instance()
            if app is not None:
                app.setWindowIcon(icon)

    def _configured_root_for(self, spec: AgentSpec) -> Path | None:
        configured = self._app_config.agent_roots.get(spec.name, "").strip()
        if configured:
            return Path(configured).expanduser()
        return spec.default_root_fn()

    def _save_agent_root(self, name: str, root: Path | None) -> None:
        if root is None:
            self._app_config.agent_roots.pop(name, None)
        else:
            self._app_config.agent_roots[name] = str(root)
        self._app_config.save()

    def _init_repo_root(self) -> None:
        if deployer.using_bundled_runtime():
            return
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
        self.resize(1536, 1024)
        central = QWidget(self)
        shell = QHBoxLayout(central)
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)
        self.setCentralWidget(central)
        shell.addWidget(self._build_sidebar(central))

        workspace = QWidget(central)
        workspace.setObjectName("workspace")
        root = QVBoxLayout(workspace)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        shell.addWidget(workspace, 1)
        self._build_topbar(root)

        self._main_splitter = QSplitter(Qt.Orientation.Vertical, workspace)
        self._main_splitter.setChildrenCollapsible(False)
        root.addWidget(self._main_splitter, 1)
        self._pages = QStackedWidget(self._main_splitter)
        self._main_splitter.addWidget(self._pages)
        deployment_page = QWidget(self._pages)
        page_layout = QVBoxLayout(deployment_page)
        page_layout.setContentsMargins(24, 12, 24, 12)
        page_layout.setSpacing(14)
        content_splitter = QSplitter(Qt.Orientation.Horizontal, deployment_page)
        content_splitter.setChildrenCollapsible(False)
        content_splitter.setHandleWidth(14)
        content_splitter.addWidget(self._build_table_panel(content_splitter))
        content_splitter.addWidget(self._build_detail_panel(content_splitter))
        content_splitter.setSizes([740, 370])
        page_layout.addWidget(content_splitter, 1)
        page_layout.addWidget(self._build_action_strip(deployment_page))
        self._pages.addWidget(deployment_page)
        self._workflow_page = None
        self._log_panel = self._build_log_panel(self._main_splitter)
        self._main_splitter.addWidget(self._log_panel)
        self._main_splitter.setSizes([720, 190])

    def _build_sidebar(self, parent: QWidget) -> QFrame:
        sidebar = QFrame(parent)
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(254)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 26, 18, 20)
        layout.setSpacing(8)
        brand_row = QHBoxLayout()
        mascot = QLabel(sidebar)
        mascot.setPixmap(QPixmap(str(_asset_path("nimo-mascot.png"))).scaled(
            56, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
        brand_row.addWidget(mascot)
        brand = QLabel("NIMO\nEngineering", sidebar)
        brand.setObjectName("sidebarBrand")
        brand_row.addWidget(brand, 1)
        layout.addLayout(brand_row)
        layout.addSpacing(22)
        self._nav_buttons = {}
        for name, key in (("platforms", "nav_platforms"), ("workflow", "nav_workflow"), ("activity", "nav_activity")):
            button = QPushButton(t(key), sidebar)
            button.setIcon(QIcon(str(_asset_path(f"nav-{name}.svg"))))
            button.setIconSize(QSize(19, 19))
            button.setCheckable(True)
            button.setMinimumHeight(46)
            button.clicked.connect(lambda _checked=False, page=name: self._navigate(page))
            self._nav_buttons[name] = button
            layout.addWidget(button)
        self._nav_buttons["platforms"].setChecked(True)
        layout.addStretch(1)
        self._sidebar_tools = QVBoxLayout()
        self._sidebar_tools.setSpacing(8)
        layout.addLayout(self._sidebar_tools)
        self._sidebar_version = QLabel(sidebar)
        self._sidebar_version.setObjectName("sidebarProduct")
        layout.addSpacing(18)
        layout.addWidget(self._sidebar_version)
        self._sidebar_local = QLabel(sidebar)
        self._sidebar_local.setObjectName("sidebarProduct")
        layout.addWidget(self._sidebar_local)
        return sidebar

    def _build_topbar(self, root: QVBoxLayout) -> None:
        topbar = QFrame(self)
        topbar.setObjectName("topbar")
        topbar.setMinimumHeight(108)
        layout = QHBoxLayout(topbar)
        layout.setContentsMargins(26, 16, 24, 14)
        layout.setSpacing(12)
        heading = QVBoxLayout()
        heading.setSpacing(4)
        self._title_label = QLabel(topbar)
        self._title_label.setObjectName("topbarTitle")
        self._subtitle_label = QLabel(topbar)
        self._subtitle_label.setObjectName("topbarSubtitle")
        self._subtitle_label.setWordWrap(True)
        heading.addWidget(self._title_label)
        heading.addWidget(self._subtitle_label)
        layout.addLayout(heading, 1)
        self._topbar_actions = QHBoxLayout()
        self._topbar_actions.setSpacing(8)
        layout.addLayout(self._topbar_actions)
        self._version_label = QLabel(topbar)
        self._version_label.setObjectName("versionTag")
        self._version_label.hide()
        self._language_combo = QComboBox(topbar)
        self._language_combo.setObjectName("topbarCombo")
        self._language_combo.currentIndexChanged.connect(self._on_language_changed)
        self._topbar_actions.addWidget(self._language_combo)
        self._theme_combo = QComboBox(topbar)
        self._theme_combo.setObjectName("topbarCombo")
        self._theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        self._topbar_actions.addWidget(self._theme_combo)
        root.addWidget(topbar)

    def _build_action_strip(self, parent: QWidget) -> QFrame:
        strip = QFrame(parent)
        strip.setObjectName("actionStrip")
        layout = QHBoxLayout(strip)
        layout.setContentsMargins(18, 8, 18, 8)
        layout.setSpacing(14)
        mascot = QLabel(strip)
        mascot.setPixmap(QPixmap(str(_asset_path("nimo-mascot.png"))).scaled(
            44, 62, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
        layout.addWidget(mascot)
        self._helper_label = QLabel(strip)
        self._helper_label.setObjectName("actionHelper")
        self._helper_label.setWordWrap(True)
        layout.addWidget(self._helper_label, 1)
        self._verify_btn.setMinimumSize(94, 42)
        self._deploy_btn.setMinimumSize(120, 42)
        layout.addWidget(self._verify_btn)
        layout.addWidget(self._deploy_btn)
        return strip

    def _navigate(self, name: str) -> None:
        self._current_page = name
        for key, button in self._nav_buttons.items():
            button.setChecked(key == name)
        self._pages.setVisible(name != "activity")
        if name == "workflow":
            if self._workflow_page is None:
                self._workflow_page = self._build_workflow_panel(self._pages)
                self._pages.addWidget(self._workflow_page)
            self._pages.setCurrentWidget(self._workflow_page)
        elif name == "platforms":
            self._pages.setCurrentIndex(0)
        else:
            self._log_text.setFocus()
        self._title_label.setText(t("nav_" + name) if name != "platforms" else t("title"))
        self._subtitle_label.setText(t(name + "_subtitle") if name != "platforms" else t("subtitle"))
        self._rescan_btn.setVisible(name == "platforms")
        self._scope_combo.setVisible(name == "platforms")

    def _build_workflow_panel(self, parent: QWidget) -> QWidget:
        from .workflow import overview

        scroll = QScrollArea(parent)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        page = QWidget(scroll)
        page.setObjectName("workspace")
        scroll.setWidget(page)
        outer = QVBoxLayout(page)
        outer.setContentsMargins(24, 12, 24, 16)
        panel = QFrame(page)
        panel.setObjectName("workflowPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(18)
        for index, group in enumerate(overview(), 1):
            row = QHBoxLayout()
            number = QLabel(f"{index:02d}", panel)
            number.setObjectName("workflowNumber")
            number.setFixedWidth(48)
            row.addWidget(number, 0, Qt.AlignmentFlag.AlignTop)
            text = QVBoxLayout()
            heading = QLabel(t("workflow_" + group["id"] + "_title"), panel)
            heading.setObjectName("workflowHeading")
            text.addWidget(heading)
            description = QLabel(t("workflow_" + group["id"] + "_description"), panel)
            description.setObjectName("workflowDescription")
            description.setWordWrap(True)
            text.addWidget(description)
            stages = QLabel(t("workflow_stages") + " " + " / ".join(group["stages"]), panel)
            stages.setObjectName("muted")
            stages.setWordWrap(True)
            text.addWidget(stages)
            gate = QLabel(t("workflow_gate_" + group["gate"]), panel)
            gate.setObjectName("muted")
            gate.setWordWrap(True)
            text.addWidget(gate)
            row.addLayout(text, 1)
            layout.addLayout(row)
        layout.addStretch(1)
        outer.addWidget(panel)
        return scroll

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
        self._filter_edit.textChanged.connect(self._select_first_row)
        toolbar.addWidget(self._filter_edit)

        self._scope_combo = QComboBox(panel)
        self._scope_combo.currentIndexChanged.connect(self._on_scope_changed)
        self._scope_combo.setMinimumWidth(110)
        self._topbar_actions.insertWidget(0, self._scope_combo)

        self._rescan_btn = self._tool_button(
            t("btn_rescan"),
            self._refresh_all_detection,
            panel,
        )
        self._topbar_actions.insertWidget(0, self._rescan_btn)

        self._build_all_btn = self._tool_button(
            t("btn_build_all"),
            self._on_build_all,
            panel,
            variant="secondary",
        )
        self._sidebar_tools.addWidget(self._build_all_btn)
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
        self._table.verticalHeader().setDefaultSectionSize(40)
        self._table.horizontalHeader().setHighlightSections(False)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_AGENT, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_PROGRAM, QHeaderView.ResizeMode.Fixed)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_DEPLOYMENT, QHeaderView.ResizeMode.Fixed)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_ROOT, QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_PROFILES, QHeaderView.ResizeMode.ResizeToContents)
        self._table.setColumnHidden(AgentTableModel.COL_ROOT, True)
        self._table.setColumnHidden(AgentTableModel.COL_PROFILES, True)
        self._table.horizontalHeader().setSectionResizeMode(AgentTableModel.COL_AGENT, QHeaderView.ResizeMode.Stretch)
        self._table.setColumnWidth(AgentTableModel.COL_PROGRAM, 148)
        self._table.setColumnWidth(AgentTableModel.COL_DEPLOYMENT, 122)
        self._table.selectionModel().currentChanged.connect(self._on_current_changed)
        self._table.doubleClicked.connect(lambda _index: self._on_verify_selected())
        layout.addWidget(self._table, 1)

        self._empty_label = QLabel(t("empty_results"), panel)
        self._empty_label.setObjectName("muted")
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.hide()
        layout.addWidget(self._empty_label)

        return panel

    def _build_detail_panel(self, parent: QWidget) -> QWidget:
        scroll = QScrollArea(parent)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setMinimumWidth(350)
        panel = QFrame(scroll)
        panel.setObjectName("panel")
        scroll.setWidget(panel)
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
            caption.setFixedWidth(78)
            value.setObjectName("fieldValue")
            value.setMinimumWidth(0)
            policy = value.sizePolicy()
            policy.setHorizontalPolicy(QSizePolicy.Policy.Ignored)
            policy.setHeightForWidth(True)
            value.setSizePolicy(policy)
            details.addWidget(caption, row_index, 0)
            details.addWidget(value, row_index, 1)
        details.setColumnMinimumWidth(0, 78)
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
        button_grid.addWidget(self._folder_btn, 0, 0)
        button_grid.addWidget(self._open_root_btn, 0, 1)
        button_grid.addWidget(self._remove_btn, 1, 0, 1, 2)
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

        return scroll

    def _build_log_panel(self, parent: QWidget) -> QWidget:
        panel = QFrame(parent)
        panel.setObjectName("panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, styles.PAD_SM, 24, 16)
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
            self._clear_log,
            panel,
        )
        header.addWidget(self._clear_log_btn)
        self._stop_btn = self._tool_button(
            t("btn_stop"),
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
        self._log_text.setMinimumHeight(80)
        self._log_text.setPlaceholderText(t("log_placeholder"))
        layout.addWidget(self._log_text, 1)

        return panel

    def _tool_button(
        self,
        text: str,
        slot: Any,
        parent: QWidget,
        *,
        variant: str = "secondary",
    ) -> QToolButton:
        button = QToolButton(parent)
        button.setText(text)
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
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
        self._subtitle_label.setText(t("subtitle"))
        self._helper_label.setText(t("nimo_helper"))
        self._sidebar_version.setText(f"v{self.version}")
        self._sidebar_local.setText(t("local_client"))
        self._log_text.setPlaceholderText(t("log_placeholder"))
        self._empty_label.setText(t("empty_results"))
        for name, button in self._nav_buttons.items():
            button.setText(t("nav_" + name))
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
        if self._workflow_page is not None:
            self._pages.removeWidget(self._workflow_page)
            self._workflow_page.deleteLater()
            self._workflow_page = None
        self._navigate(getattr(self, "_current_page", "platforms"))

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
        dark = mode.lower() == "dark" or (
            mode.lower() == "system"
            and QApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark
        )
        self.setStyleSheet(styles.stylesheet(dark))
        self._dark_theme = dark
        self._table.viewport().update()
        self._rebuild_log()

    @staticmethod
    def _theme_colors(dark: bool) -> dict[str, str]:
        return styles.theme_colors(dark)

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
        bundled = deployer.using_bundled_runtime()
        self._repo_btn.setVisible(not bundled)
        self._build_all_btn.setVisible(not bundled)
        if bundled:
            status = deployer.runtime_status()
            self._repo_label.setText(t("runtime_ready") if status["ready"] else t("runtime_unavailable"))
            self._repo_label.setToolTip(f"NIMO Engineering {status['version']}")
            return
        if deployer.REPO_ROOT is None:
            self._repo_label.setText(t("repo_not_set"))
        else:
            value = f"{t('repo_prefix')}{deployer.REPO_ROOT}"
            self._repo_label.setToolTip(value)
            self._repo_label.setText(_soft_wrap(value))

    def _select_first_row(self) -> None:
        self._empty_label.setVisible(self._proxy.rowCount() <= 0)
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
            for label in (self._root_value, self._program_value, self._deploy_value):
                label.setToolTip("")
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
        root_text = _root_detail_text(row.root)
        self._root_value.setText(_soft_wrap(root_text))
        self._root_value.setToolTip(root_text)
        self._profiles_value.setText(", ".join(spec.needs_profiles) if spec.needs_profiles else "-")
        if det is None:
            self._program_value.setText(t("checking"))
            self._deploy_value.setText(t("checking"))
            self._program_value.setToolTip("")
            self._deploy_value.setToolTip("")
        else:
            program_text = f"{t('program_installed') if det.program else t('program_not_found')}\n{det.program_detail}"
            deployment_text = f"{t('deployed') if det.deployed else t('not_deployed')}\n{det.deployed_detail}"
            self._program_value.setText(_soft_wrap(program_text))
            self._program_value.setToolTip(program_text)
            self._deploy_value.setText(t("deployed") if det.deployed else t("not_deployed"))
            self._deploy_value.setToolTip(deployment_text)

        can_act = not busy
        self._deploy_btn.setEnabled(can_act)
        self._verify_btn.setEnabled(can_act)
        self._folder_btn.setText(t("btn_project_root") if spec.kind == "project" else t("btn_folder"))
        self._folder_btn.setEnabled(can_act)
        self._open_root_btn.setEnabled(row.root is not None and Path(row.root).exists())
        self._remove_btn.setEnabled(
            can_act
            and spec.supports_uninstall
            and row.root is not None
            and det is not None
            and det.deployed
        )

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
        chosen = QFileDialog.getExistingDirectory(
            self,
            t(title_key, name=spec.display_name),
            _dialog_start_dir(self._model.root_for(spec.name)),
        )
        if not chosen:
            return False
        root = Path(chosen).expanduser()
        self._model.set_root(spec.name, root)
        self._save_agent_root(spec.name, root)
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
        html = "".join(f'<span style="color:{self._log_color(line)}">{escape(line)}</span><br>' for line, _color in self._log_lines)
        self._log_text.setHtml(html)
        self._log_text.verticalScrollBar().setValue(self._log_text.verticalScrollBar().maximum())

    def _clear_log(self) -> None:
        self._log_lines.clear()
        self._log_text.clear()

    def _log_color(self, line: str) -> str:
        lower = line.lower()
        dark = getattr(self, "_dark_theme", False)
        if line.startswith("$ "):
            return "#AFBBC5" if dark else styles.TEXT_SECONDARY
        if "[error]" in lower or "traceback" in lower or "failed" in lower or "[错误]" in line:
            return "#FFA099" if dark else styles.DANGER
        if "[verify]" in lower or "[done]" in lower or "complete" in lower or "[完成]" in line:
            return "#9FE0BB" if dark else styles.SUCCESS
        if "[backup]" in lower or "[skip]" in lower or "warning" in lower or "[警告]" in line:
            return "#F0AE60" if dark else "#9C5F09"
        return "#F0F3F6" if dark else styles.TEXT_PRIMARY


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    app = QApplication.instance() or QApplication(args)
    window = AppWindow()
    if "--smoke" in args:
        window.show()
        app.processEvents()
        smoke_language = os.environ.get("NIMO_SMOKE_LANGUAGE")
        if smoke_language in ("en", "zh"):
            window._language_combo.setCurrentIndex(window._language_combo.findData(smoke_language))
            app.processEvents()
        if deployer.using_bundled_runtime():
            assert window._repo_btn.isHidden() and window._build_all_btn.isHidden()
            assert window._repo_label.text() == t("runtime_ready")
            assert all("_MEI" not in label.text() for label in window.findChildren(QLabel))
        screenshot = os.environ.get("NIMO_SMOKE_SCREENSHOT")
        if screenshot:
            assert window.grab().save(screenshot), "Unable to save runtime smoke screenshot"
        window.close()
        return 0
    window.show()
    return int(app.exec())
