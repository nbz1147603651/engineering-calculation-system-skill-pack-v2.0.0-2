"""Detect whether each target agent program is installed on this machine.

Two independent checks are exposed per agent:

* :func:`program_installed` - is the agent's CLI executable on PATH or its
  well-known home directory present? This drives the colored status dot on each
  card ("agent program installed" vs "not installed").
* :func:`skill_deployed` - is the skill/plugin already present at the agent's
  install root? This drives the "deployed / not deployed" badge.

The detection is deliberately conservative: we only report ``True`` when we have
a concrete positive signal (an executable we can resolve, or a directory/file we
can stat). Absence is reported as ``False``, never as an error.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


from .i18n import t
from .platform_contracts import CONTRACTS, ProgramProbe, get_contract


@dataclass(frozen=True)
class Detection:
    """Result of probing one agent."""

    program: bool            # the agent program itself appears installed
    program_detail: str      # human-readable reason (path / version / clue)
    deployed: bool           # the skill is already present at the install root
    deployed_detail: str


def _home() -> Path:
    """Cross-platform user home (respects USERPROFILE on Windows)."""
    return Path.home()


def _exe_on_path(name: str) -> str | None:
    """Return the path to ``name`` on PATH, else ``None``.

    On Windows ``shutil.which`` already searches PATHEXT, so ``codex`` matches
    ``codex.cmd`` / ``codex.exe`` automatically.
    """
    found = shutil.which(name)
    return found


def _dir_exists(path: Path) -> bool:
    try:
        return path.is_dir()
    except OSError:
        return False


def _file_exists(path: Path) -> bool:
    try:
        return path.is_file()
    except OSError:
        return False


# --------------------------------------------------------------------------- #
# Per-agent program detection
# --------------------------------------------------------------------------- #

def _detect_with_probe(agent_name: str, probe: ProgramProbe) -> tuple[bool, str]:
    if probe.always_available_detail:
        return True, probe.always_available_detail

    for name in probe.executable_names:
        exe = _exe_on_path(name)
        if exe:
            return True, f"{probe.executable_detail_prefix}: {exe}"

    for env_name in probe.env_home_names:
        configured = os.environ.get(env_name)
        if not configured:
            continue
        home = Path(configured).expanduser()
        if _dir_exists(home):
            return True, f"{probe.env_home_detail_prefix}: {home}"

    for home_probe in probe.home_dirs:
        home = _home() / Path(home_probe.path)
        if _dir_exists(home):
            return True, f"{home_probe.detail_prefix}: {home}"

    if probe.not_found_key is not None:
        return False, t(probe.not_found_key)
    return False, f"{t('detector_unknown_agent')}: {agent_name}"


def _detect_program(agent_name: str) -> tuple[bool, str]:
    if agent_name == "deepseek-harness":
        from .dsh import launcher
        try:
            return True, f"Harness launcher: {launcher()[0]}"
        except ValueError:
            return False, t("detector_dsh_not_found")
    contract = get_contract(agent_name)
    if contract is None:
        return False, f"{t('detector_unknown_agent')}: {agent_name}"
    return _detect_with_probe(agent_name, contract.program_probe)


def detect_codex_program() -> tuple[bool, str]:
    return _detect_program("codex")


def detect_mavis_program() -> tuple[bool, str]:
    return _detect_program("minimax")


def detect_qoder_program() -> tuple[bool, str]:
    return _detect_program("qoder")


def detect_qodercn_program() -> tuple[bool, str]:
    return _detect_program("qodercn")


def detect_qoderworkcn_program() -> tuple[bool, str]:
    return _detect_program("qoderworkcn")


def detect_workbuddy_program() -> tuple[bool, str]:
    return _detect_program("workbuddy")


def detect_zcode_program() -> tuple[bool, str]:
    return _detect_program("zcode")


def detect_trae_program() -> tuple[bool, str]:
    return _detect_program("trae")


def detect_opencode_program() -> tuple[bool, str]:
    return _detect_program("opencode")


def detect_agents_generic_program() -> tuple[bool, str]:
    return _detect_program("agents-generic")


PROGRAM_DETECTORS = {
    contract.name: (lambda name=contract.name: _detect_program(name))
    for contract in CONTRACTS
}
STRICT_SENTINEL_AGENTS = {contract.name for contract in CONTRACTS if contract.sentinel_mode == "all"}


def program_installed(agent_name: str) -> tuple[bool, str]:
    detector = PROGRAM_DETECTORS.get(agent_name)
    if detector is None:
        return False, f"{t('detector_unknown_agent')}: {agent_name}"
    return detector()


# --------------------------------------------------------------------------- #
# Skill deployment detection
# --------------------------------------------------------------------------- #

def skill_deployed(agent_name: str, install_root: Path | None) -> tuple[bool, str]:
    """Return (deployed, detail) for the skill at this agent's install root.

    ``install_root`` for project-overlay agents is the chosen project root; for
    user-level agents it is the computed home path. ``None`` means "no root
    chosen yet", which we report as not deployed.
    """
    if install_root is None:
        return False, t("detector_no_root_selected")

    root = Path(install_root).expanduser()

    if agent_name == "deepseek-harness":
        from .dsh import installed
        return installed(root)

    contract = get_contract(agent_name)
    if contract is None or not contract.sentinel_paths:
        return False, f"{t('detector_no_sentinel')}: {agent_name}"
    candidates = [root / Path(path) for path in contract.sentinel_paths]

    present: list[Path] = []
    missing: list[Path] = []
    for candidate in candidates:
        (present if _file_exists(candidate) else missing).append(candidate)

    if contract.sentinel_mode == "all":
        if missing:
            return False, f"{t('detector_sentinel_missing')} {missing[0]}"
        return True, f"sentinels found: {', '.join(str(p) for p in present)}"
    if present:
        return True, f"sentinel found: {present[0]}"
    return False, f"{t('detector_sentinel_missing')} {root}"


def detect(agent_name: str, install_root: Path | None) -> Detection:
    """Combined program + deployment detection for one agent."""
    prog_ok, prog_detail = program_installed(agent_name)
    dep_ok, dep_detail = skill_deployed(agent_name, install_root)
    return Detection(
        program=prog_ok,
        program_detail=prog_detail,
        deployed=dep_ok,
        deployed_detail=dep_detail,
    )


# --------------------------------------------------------------------------- #
# Optional CLI verification (e.g. ``mavis skill show ...``)
# --------------------------------------------------------------------------- #

def run_cli_verify(command: list[str], *, timeout: float = 15.0) -> tuple[bool, str]:
    """Run a verification CLI and return (ok, combined_output).

    Used only for agents that expose a real ``skill show`` / ``skill list``
    command. Failures to launch (e.g. not installed) are reported as ``False``
    with the error text rather than raised.
    """
    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except (FileNotFoundError, subprocess.SubprocessError) as exc:
        return False, f"verify command failed to run: {exc}"
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, output.strip()
