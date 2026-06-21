"""Agent metadata: the single source of truth for the 8 deployment targets.

Each :class:`AgentSpec` knows how to:

* locate its default install root (and let the user override it),
* build the required release profile(s) if missing,
* copy the right overlay into place (with backup),
* verify the deployment landed,
* uninstall itself.

The deploy/verify/uninstall *callables* live in :mod:`deployer`; this module
only wires names to those callables plus display metadata, so the UI can render
cards generically from a list.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from . import detector
from .i18n import t


# --------------------------------------------------------------------------- #
# Default install-root resolution (user-level agents)
# --------------------------------------------------------------------------- #

def _codex_root() -> Path:
    return Path.home() / ".codex" / "skills" / "engineering-calculation-system"


def _mavis_root() -> Path:
    return Path.home() / ".mavis" / "skills" / "engineering-calculation-system"


def _zcode_root() -> Path:
    return Path.home() / ".zcode" / "skills" / "engineering-calculation-system"


def _qoder_root() -> Path:
    configured = os.environ.get("QODER_HOME")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".qoder"


# Project-overlay agents have no default root; the user picks one.
def _no_default() -> Path | None:
    return None


# --------------------------------------------------------------------------- #
# Spec
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class AgentSpec:
    """Everything the UI needs to render and operate one target agent."""

    name: str                          # stable key, used by detector / deployer
    display_name: str                  # card title
    icon: str                          # short glyph shown next to the title
    kind: str                          # "user" or "project"
    summary: str                       # one-line description under the title
    default_root_fn: Callable[[], Path | None]
    # Callable signatures are defined in deployer.py; we keep them as opaque
    # Callables here so this module stays free of heavy imports.
    deploy_fn: Callable[..., object]
    verify_fn: Callable[..., object]
    uninstall_fn: Callable[..., object]
    needs_profiles: tuple[str, ...] = field(default_factory=tuple)
    supports_uninstall: bool = True
    # Optional CLI verify command builder; returns argv list or None.
    cli_verify_fn: Callable[[Path | None], list[str] | None] | None = None


# Forward declarations: deployer.py provides these. We import lazily inside a
# builder to avoid a circular import at module load (agents -> deployer ->
# agents). The builder runs once at first access.
def _build_specs() -> list[AgentSpec]:
    from . import deployer

    def mavis_cli_verify(root: Path | None) -> list[str] | None:
        mavis_cmd = detector._exe_on_path("mavis") or str(Path.home() / ".mavis" / "bin" / "mavis.cmd")
        return [mavis_cmd, "skill", "show", "engineering-calculation-system"]

    return [
        AgentSpec(
            name="codex",
            display_name="Codex",
            icon="C",
            kind="user",
            summary=t("summary_codex"),
            default_root_fn=_codex_root,
            deploy_fn=deployer.deploy_codex,
            verify_fn=deployer.verify_codex,
            uninstall_fn=deployer.uninstall_codex,
            needs_profiles=("core",),
        ),
        AgentSpec(
            name="minimax",
            display_name="MiniMax Code",
            icon="M",
            kind="user",
            summary=t("summary_minimax"),
            default_root_fn=_mavis_root,
            deploy_fn=deployer.deploy_minimax,
            verify_fn=deployer.verify_minimax,
            uninstall_fn=deployer.uninstall_minimax,
            needs_profiles=("core",),
            cli_verify_fn=mavis_cli_verify,
        ),
        AgentSpec(
            name="zcode",
            display_name="ZCode",
            icon="Z",
            kind="user",
            summary=t("summary_zcode"),
            default_root_fn=_zcode_root,
            deploy_fn=deployer.deploy_zcode,
            verify_fn=deployer.verify_zcode,
            uninstall_fn=deployer.uninstall_zcode,
            needs_profiles=("core",),
        ),
        AgentSpec(
            name="qoder",
            display_name=t("name_qoder_user"),
            icon="Q",
            kind="user",
            summary=t("summary_qoder"),
            default_root_fn=_qoder_root,
            deploy_fn=deployer.deploy_qoder_user,
            verify_fn=deployer.verify_qoder_user,
            uninstall_fn=deployer.uninstall_qoder_user,
            needs_profiles=("qoder-addon",),
        ),
        AgentSpec(
            name="qoder-project",
            display_name=t("name_qoder_project"),
            icon="Q+",
            kind="project",
            summary=t("summary_qoder_project"),
            default_root_fn=_no_default,
            deploy_fn=deployer.deploy_qoder_project,
            verify_fn=deployer.verify_qoder_project,
            uninstall_fn=deployer.uninstall_qoder_project,
            needs_profiles=("core", "qoder-addon"),
        ),
        AgentSpec(
            name="trae",
            display_name="Trae",
            icon="T",
            kind="project",
            summary=t("summary_trae"),
            default_root_fn=_no_default,
            deploy_fn=deployer.deploy_trae,
            verify_fn=deployer.verify_trae,
            uninstall_fn=deployer.uninstall_trae,
            needs_profiles=("core", "adapters-light"),
        ),
        AgentSpec(
            name="opencode",
            display_name="OpenCode",
            icon="O",
            kind="project",
            summary=t("summary_opencode"),
            default_root_fn=_no_default,
            deploy_fn=deployer.deploy_opencode,
            verify_fn=deployer.verify_opencode,
            uninstall_fn=deployer.uninstall_opencode,
            needs_profiles=("core", "adapters-light"),
        ),
        AgentSpec(
            name="agents-generic",
            display_name=t("name_agents_generic"),
            icon="A",
            kind="project",
            summary=t("summary_agents_generic"),
            default_root_fn=_no_default,
            deploy_fn=deployer.deploy_agents_generic,
            verify_fn=deployer.verify_agents_generic,
            uninstall_fn=deployer.uninstall_agents_generic,
            needs_profiles=("core", "adapters-light"),
        ),
    ]


_SPECS: list[AgentSpec] | None = None


def all_agents() -> list[AgentSpec]:
    """Return all agent specs (built once, cached)."""
    global _SPECS
    if _SPECS is None:
        _SPECS = _build_specs()
    return _SPECS


def get(name: str) -> AgentSpec | None:
    for spec in all_agents():
        if spec.name == name:
            return spec
    return None


def rebuild_specs() -> list[AgentSpec]:
    """Rebuild specs with current language (call after language switch)."""
    global _SPECS
    _SPECS = None
    return all_agents()
