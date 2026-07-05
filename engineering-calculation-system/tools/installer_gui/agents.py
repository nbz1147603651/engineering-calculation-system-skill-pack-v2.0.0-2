"""Agent metadata rendered by the deployment UI.

Each :class:`AgentSpec` knows how to:

* locate its default install root (and let the user override it),
* build the required release profile(s) if missing,
* copy the right overlay into place (with backup),
* verify the deployment landed,
* uninstall itself.

Platform contracts live in :mod:`platform_contracts`. The deploy/verify/
uninstall *callables* live in :mod:`deployer`; this module only binds those
callables to the declarative platform contracts so the UI can render cards
generically from a list.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .i18n import t
from .platform_contracts import AgentContract, CONTRACTS


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
        mavis_cmd = shutil.which("mavis") or str(Path.home() / ".mavis" / "bin" / "mavis.cmd")
        return [mavis_cmd, "skill", "show", "engineering-calculation-system"]

    callables = {
        "codex": (deployer.deploy_codex, deployer.verify_codex, deployer.uninstall_codex),
        "minimax": (deployer.deploy_minimax, deployer.verify_minimax, deployer.uninstall_minimax),
        "zcode": (deployer.deploy_zcode, deployer.verify_zcode, deployer.uninstall_zcode),
        "qoder": (deployer.deploy_qoder_user, deployer.verify_qoder_user, deployer.uninstall_qoder_user),
        "qoder-project": (
            deployer.deploy_qoder_project,
            deployer.verify_qoder_project,
            deployer.uninstall_qoder_project,
        ),
        "qodercn": (
            deployer.deploy_qodercn_user,
            deployer.verify_qodercn_user,
            deployer.uninstall_qodercn_user,
        ),
        "qodercn-project": (
            deployer.deploy_qodercn_project,
            deployer.verify_qodercn_project,
            deployer.uninstall_qodercn_project,
        ),
        "qoderworkcn": (
            deployer.deploy_qoderworkcn_plugin,
            deployer.verify_qoderworkcn_plugin,
            deployer.uninstall_qoderworkcn_plugin,
        ),
        "workbuddy": (
            deployer.deploy_workbuddy_plugin,
            deployer.verify_workbuddy_plugin,
            deployer.uninstall_workbuddy_plugin,
        ),
        "trae": (deployer.deploy_trae, deployer.verify_trae, deployer.uninstall_trae),
        "opencode": (deployer.deploy_opencode, deployer.verify_opencode, deployer.uninstall_opencode),
        "agents-generic": (
            deployer.deploy_agents_generic,
            deployer.verify_agents_generic,
            deployer.uninstall_agents_generic,
        ),
    }

    def display_name(contract: AgentContract) -> str:
        if contract.display_name is not None:
            return contract.display_name
        if contract.display_name_key is not None:
            return t(contract.display_name_key)
        return contract.name

    specs: list[AgentSpec] = []
    for contract in CONTRACTS:
        deploy_fn, verify_fn, uninstall_fn = callables[contract.name]
        specs.append(
            AgentSpec(
                name=contract.name,
                display_name=display_name(contract),
                icon=contract.icon,
                kind=contract.kind,
                summary=t(contract.summary_key),
                default_root_fn=contract.default_root_fn,
                deploy_fn=deploy_fn,
                verify_fn=verify_fn,
                uninstall_fn=uninstall_fn,
                needs_profiles=contract.needs_profiles,
                cli_verify_fn=mavis_cli_verify if contract.name == "minimax" else None,
            )
        )
    return specs


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
