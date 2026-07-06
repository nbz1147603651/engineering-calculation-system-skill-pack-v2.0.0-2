"""Platform contracts shared by the installer UI, detector, and tests.

This module is intentionally declarative. Platform-specific differences live
here as data: roots, profiles, program probes, and deployment sentinels. The
deployment engine can then grow strategy-based behavior without copying platform
branches across the UI and detector.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal


SentinelMode = Literal["any", "all"]
DefaultRootFn = Callable[[], Path | None]


@dataclass(frozen=True)
class HomeProbe:
    """A user-home-relative directory that indicates a platform is installed."""

    path: str
    detail_prefix: str = "home dir found"


@dataclass(frozen=True)
class ProgramProbe:
    """Signals used to detect whether an agent program exists locally."""

    executable_names: tuple[str, ...] = field(default_factory=tuple)
    executable_detail_prefix: str = "CLI found"
    env_home_names: tuple[str, ...] = field(default_factory=tuple)
    env_home_detail_prefix: str = "home dir found"
    home_dirs: tuple[HomeProbe, ...] = field(default_factory=tuple)
    not_found_key: str | None = None
    always_available_detail: str | None = None


@dataclass(frozen=True)
class ProfileCopy:
    """Copy one path from a release profile into the selected install root."""

    profile: str
    source: str
    target: str


@dataclass(frozen=True)
class ProjectOverlay:
    """Declarative project-root overlay install/uninstall behavior."""

    agent_label: str
    copies: tuple[ProfileCopy, ...]
    uninstall_paths: tuple[str, ...]
    include_core: bool = True


@dataclass(frozen=True)
class AgentContract:
    """Single source of truth for one install target's platform shape."""

    name: str
    icon: str
    kind: Literal["user", "project"]
    summary_key: str
    default_root_fn: DefaultRootFn
    needs_profiles: tuple[str, ...]
    program_probe: ProgramProbe
    sentinel_paths: tuple[str, ...]
    sentinel_mode: SentinelMode = "any"
    display_name: str | None = None
    display_name_key: str | None = None
    project_overlay: ProjectOverlay | None = None


def _env_or_default(env_names: tuple[str, ...], fallback: Path) -> Path:
    for env_name in env_names:
        configured = os.environ.get(env_name)
        if configured:
            return Path(configured).expanduser()
    return fallback


CODEX_PLUGIN_NAME = "engineering-calculation-system"
CODEX_LOCAL_MARKETPLACE_NAME = "engineering-calculation-system-local"


def _existing_codex_plugin_cache_root() -> Path | None:
    cache_parent = (
        Path.home()
        / ".codex"
        / "plugins"
        / "cache"
        / CODEX_LOCAL_MARKETPLACE_NAME
        / CODEX_PLUGIN_NAME
    )
    if not cache_parent.exists():
        return None
    try:
        candidates = [
            path
            for path in cache_parent.iterdir()
            if path.is_dir() and (path / ".codex-plugin" / "plugin.json").is_file()
        ]
    except OSError:
        return None
    if not candidates:
        return None

    def mtime(path: Path) -> float:
        try:
            return path.stat().st_mtime
        except OSError:
            return 0.0

    return sorted(candidates, key=mtime, reverse=True)[0]


def codex_root() -> Path:
    configured = os.environ.get("ENGINEERING_CALC_CODEX_PLUGIN_ROOT") or os.environ.get("CODEX_PLUGIN_ROOT")
    if configured:
        return Path(configured).expanduser()
    cached = _existing_codex_plugin_cache_root()
    if cached is not None:
        return cached
    return Path.home() / ".codex" / "plugins" / CODEX_PLUGIN_NAME


def mavis_root() -> Path:
    return Path.home() / ".mavis" / "skills" / "engineering-calculation-system"


def zcode_root() -> Path:
    return Path.home() / ".zcode" / "plugins" / "engineering-calculation-system-zcode"


def qoder_root() -> Path:
    return _env_or_default(("QODER_HOME",), Path.home() / ".qoder")


def qodercn_root() -> Path:
    return _env_or_default(("QODER_CN_HOME", "QODERCN_HOME", "LINGMA_HOME"), Path.home() / ".lingma")


def qoderworkcn_root() -> Path:
    return _env_or_default(
        ("QODERWORK_CN_KIT_HOME", "QODERWORK_KIT_HOME"),
        Path.home() / "QoderWorkCN-Expert-Kits" / "engineering-calculation-system-qoderworkcn",
    )


def workbuddy_root() -> Path:
    return _env_or_default(
        ("WORKBUDDY_KIT_HOME", "WORKBUDDY_HOME", "TENCENT_WORKBUDDY_HOME"),
        Path.home() / "WorkBuddy-Expert-Kits" / "engineering-calculation-system-workbuddy",
    )


def no_default_root() -> Path | None:
    return None


UPLOAD_KIT_SENTINELS = (
    ".qoder-plugin/plugin.json",
    "qoder.md",
    "skills/engineering-calculation-system/SKILL.md",
    "skills/engineering-calc-system/SKILL.md",
    "agents/engineering-calc-system.md",
)

CORE_FORBIDDEN_PATH_PARTS = (
    ".agents",
    ".lingma",
    ".opencode",
    ".qoder",
    ".qodercn",
    ".qoder-plugin",
    ".trae",
    ".zcode-plugin",
    "marketplace.json",
    "qoder.md",
)


CONTRACTS = (
    AgentContract(
        name="codex",
        display_name="Codex",
        icon="C",
        kind="user",
        summary_key="summary_codex",
        default_root_fn=codex_root,
        needs_profiles=("codex-plugin",),
        program_probe=ProgramProbe(
            executable_names=("codex",),
            home_dirs=(HomeProbe(".codex"),),
            not_found_key="detector_codex_not_found",
        ),
        sentinel_paths=(
            ".codex-plugin/plugin.json",
            "skills/engineering-calculation-system/SKILL.md",
            "skills/engineering-calculation-system/shared/codex-plugin-adapter.md",
        ),
        sentinel_mode="all",
    ),
    AgentContract(
        name="minimax",
        display_name="MiniMax Code",
        icon="M",
        kind="user",
        summary_key="summary_minimax",
        default_root_fn=mavis_root,
        needs_profiles=("core",),
        program_probe=ProgramProbe(
            executable_names=("mavis", "mavis.cmd"),
            home_dirs=(HomeProbe(".mavis/bin", "bin dir found"), HomeProbe(".mavis")),
            not_found_key="detector_mavis_not_found",
        ),
        sentinel_paths=("engineering-calculation-system/SKILL.md",),
    ),
    AgentContract(
        name="zcode",
        display_name="ZCode",
        icon="Z",
        kind="user",
        summary_key="summary_zcode",
        default_root_fn=zcode_root,
        needs_profiles=("zcode-plugin",),
        program_probe=ProgramProbe(
            executable_names=("zcode",),
            home_dirs=(HomeProbe(".zcode"),),
            not_found_key="detector_zcode_not_found",
        ),
        sentinel_paths=(
            "marketplace.json",
            ".zcode-plugin/plugin.json",
            "skills/engineering-calculation-book-delivery/SKILL.md",
            "skills/engineering-calculation-logic-architecture/SKILL.md",
            "skills/engineering-calculation-reference-acquisition/SKILL.md",
            "skills/engineering-calculation-system/SKILL.md",
        ),
        sentinel_mode="all",
    ),
    AgentContract(
        name="qoder",
        display_name_key="name_qoder_user",
        icon="Q",
        kind="user",
        summary_key="summary_qoder",
        default_root_fn=qoder_root,
        needs_profiles=("qoder-addon",),
        program_probe=ProgramProbe(
            executable_names=("qoder",),
            env_home_names=("QODER_HOME",),
            home_dirs=(HomeProbe(".qoder"),),
            not_found_key="detector_qoder_not_found",
        ),
        sentinel_paths=(
            "agents/engineering-calc-system.md",
            "skills/engineering-calc-system/SKILL.md",
        ),
    ),
    AgentContract(
        name="qoder-project",
        display_name_key="name_qoder_project",
        icon="Q+",
        kind="project",
        summary_key="summary_qoder_project",
        default_root_fn=no_default_root,
        needs_profiles=("core", "qoder-addon"),
        program_probe=ProgramProbe(
            executable_names=("qoder",),
            env_home_names=("QODER_HOME",),
            home_dirs=(HomeProbe(".qoder"),),
            not_found_key="detector_qoder_not_found",
        ),
        sentinel_paths=(".qoder/agents/engineering-calc-system.md",),
        project_overlay=ProjectOverlay(
            agent_label="Qoder Project",
            copies=(ProfileCopy("qoder-addon", ".qoder", ".qoder"),),
            uninstall_paths=(".qoder",),
        ),
    ),
    AgentContract(
        name="qodercn",
        display_name_key="name_qodercn_user",
        icon="CN",
        kind="user",
        summary_key="summary_qodercn",
        default_root_fn=qodercn_root,
        needs_profiles=("qoder-addon",),
        program_probe=ProgramProbe(
            executable_names=("qodercn", "QoderCN", "QoderCN.exe", "Lingma.exe"),
            env_home_names=("QODER_CN_HOME", "QODERCN_HOME", "LINGMA_HOME"),
            home_dirs=(HomeProbe(".qodercn"), HomeProbe(".lingma"), HomeProbe(".qoder-cn")),
            not_found_key="detector_qodercn_not_found",
        ),
        sentinel_paths=(
            "agents/engineering-calc-system.md",
            "skills/engineering-calc-system/SKILL.md",
        ),
    ),
    AgentContract(
        name="qodercn-project",
        display_name_key="name_qodercn_project",
        icon="CN+",
        kind="project",
        summary_key="summary_qodercn_project",
        default_root_fn=no_default_root,
        needs_profiles=("core", "qoder-addon"),
        program_probe=ProgramProbe(
            executable_names=("qodercn", "QoderCN", "QoderCN.exe", "Lingma.exe"),
            env_home_names=("QODER_CN_HOME", "QODERCN_HOME", "LINGMA_HOME"),
            home_dirs=(HomeProbe(".qodercn"), HomeProbe(".lingma"), HomeProbe(".qoder-cn")),
            not_found_key="detector_qodercn_not_found",
        ),
        sentinel_paths=(
            ".lingma/agents/engineering-calc-system.md",
            ".qodercn/agents/engineering-calc-system.md",
        ),
        project_overlay=ProjectOverlay(
            agent_label="Qoder CN Project",
            copies=(ProfileCopy("qoder-addon", ".qoder", ".lingma"),),
            uninstall_paths=(".lingma",),
        ),
    ),
    AgentContract(
        name="qoderworkcn",
        display_name_key="name_qoderworkcn",
        icon="QW",
        kind="user",
        summary_key="summary_qoderworkcn",
        default_root_fn=qoderworkcn_root,
        needs_profiles=("qoderworkcn-plugin",),
        program_probe=ProgramProbe(
            executable_names=(
                "qoderwork",
                "qoderworkcn",
                "QoderWork",
                "QoderWorkCN",
                "QoderWork.exe",
                "QoderWorkCN.exe",
                "qodercli",
            ),
            executable_detail_prefix="CLI/app found",
            env_home_names=("QODERWORK_CN_HOME", "QODERWORK_HOME"),
            home_dirs=(HomeProbe(".qoderwork"), HomeProbe(".qoderwork-cn"), HomeProbe(".qoderworkcn")),
            not_found_key="detector_qoderworkcn_not_found",
        ),
        sentinel_paths=UPLOAD_KIT_SENTINELS,
        sentinel_mode="all",
    ),
    AgentContract(
        name="workbuddy",
        display_name_key="name_workbuddy",
        icon="WB",
        kind="user",
        summary_key="summary_workbuddy",
        default_root_fn=workbuddy_root,
        needs_profiles=("qoderworkcn-plugin",),
        program_probe=ProgramProbe(
            executable_names=(
                "workbuddy",
                "WorkBuddy",
                "WorkBuddy.exe",
                "codebuddy",
                "CodeBuddy",
                "CodeBuddy.exe",
            ),
            executable_detail_prefix="CLI/app found",
            env_home_names=("WORKBUDDY_HOME", "TENCENT_WORKBUDDY_HOME", "WORKBUDDY_KIT_HOME"),
            home_dirs=(HomeProbe(".workbuddy"), HomeProbe(".workbuddy-cn"), HomeProbe("WorkBuddy")),
            not_found_key="detector_workbuddy_not_found",
        ),
        sentinel_paths=UPLOAD_KIT_SENTINELS,
        sentinel_mode="all",
    ),
    AgentContract(
        name="trae",
        display_name="Trae",
        icon="T",
        kind="project",
        summary_key="summary_trae",
        default_root_fn=no_default_root,
        needs_profiles=("core", "adapters-light"),
        program_probe=ProgramProbe(
            executable_names=("trae",),
            not_found_key="detector_trae_not_found",
        ),
        sentinel_paths=(
            ".trae/project_rules.md",
            ".trae/rules/engineering-calc-system.md",
        ),
        project_overlay=ProjectOverlay(
            agent_label="Trae",
            copies=(
                ProfileCopy("adapters-light", ".trae", ".trae"),
                ProfileCopy("adapters-light", "AGENTS.md", "AGENTS.md"),
            ),
            uninstall_paths=(".trae", "AGENTS.md"),
        ),
    ),
    AgentContract(
        name="opencode",
        display_name="OpenCode",
        icon="O",
        kind="project",
        summary_key="summary_opencode",
        default_root_fn=no_default_root,
        needs_profiles=("core", "adapters-light"),
        program_probe=ProgramProbe(
            executable_names=("opencode",),
            not_found_key="detector_opencode_not_found",
        ),
        sentinel_paths=(".opencode/skills/engineering-calc-system/SKILL.md",),
        project_overlay=ProjectOverlay(
            agent_label="OpenCode",
            copies=(
                ProfileCopy("adapters-light", ".opencode", ".opencode"),
                ProfileCopy("adapters-light", "AGENTS.md", "AGENTS.md"),
            ),
            uninstall_paths=(".opencode", "AGENTS.md"),
        ),
    ),
    AgentContract(
        name="agents-generic",
        display_name_key="name_agents_generic",
        icon="A",
        kind="project",
        summary_key="summary_agents_generic",
        default_root_fn=no_default_root,
        needs_profiles=("core", "adapters-light"),
        program_probe=ProgramProbe(always_available_detail="AGENTS.md convention - always available"),
        sentinel_paths=(
            "AGENTS.md",
            ".agents/skills/engineering-calc-system/SKILL.md",
        ),
        project_overlay=ProjectOverlay(
            agent_label="AGENTS Generic",
            copies=(
                ProfileCopy("adapters-light", "AGENTS.md", "AGENTS.md"),
                ProfileCopy("adapters-light", ".agents", ".agents"),
            ),
            uninstall_paths=(".agents", "AGENTS.md"),
        ),
    ),
)

CONTRACTS_BY_NAME = {contract.name: contract for contract in CONTRACTS}


def get_contract(name: str) -> AgentContract | None:
    return CONTRACTS_BY_NAME.get(name)
