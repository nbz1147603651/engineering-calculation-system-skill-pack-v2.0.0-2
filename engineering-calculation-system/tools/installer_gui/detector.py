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

def detect_codex_program() -> tuple[bool, str]:
    """Codex CLI: ``codex`` on PATH, or a ``~/.codex`` home directory."""
    exe = _exe_on_path("codex")
    if exe:
        return True, f"CLI found: {exe}"
    home = _home() / ".codex"
    if _dir_exists(home):
        return True, f"home dir found: {home}"
    return False, t("detector_codex_not_found")


def detect_mavis_program() -> tuple[bool, str]:
    """MiniMax Code / Mavis: ``mavis``/``mavis.cmd`` on PATH or under ~/.mavis."""
    for name in ("mavis", "mavis.cmd"):
        exe = _exe_on_path(name)
        if exe:
            return True, f"CLI found: {exe}"
    bin_dir = _home() / ".mavis" / "bin"
    if _dir_exists(bin_dir):
        return True, f"bin dir found: {bin_dir}"
    if _dir_exists(_home() / ".mavis"):
        return True, f"home dir found: {_home() / '.mavis'}"
    return False, t("detector_mavis_not_found")


def detect_qoder_program() -> tuple[bool, str]:
    """Qoder: ``qoder`` on PATH, or QODER_HOME / ~/.qoder present."""
    exe = _exe_on_path("qoder")
    if exe:
        return True, f"CLI found: {exe}"
    home = Path(os.environ.get("QODER_HOME", "")).expanduser() if os.environ.get("QODER_HOME") else _home() / ".qoder"
    if _dir_exists(home):
        return True, f"home dir found: {home}"
    return False, t("detector_qoder_not_found")


def detect_qodercn_program() -> tuple[bool, str]:
    """Qoder CN: QoderCN/Lingma executable or known user state directories."""
    for name in ("qodercn", "QoderCN", "QoderCN.exe", "Lingma.exe"):
        exe = _exe_on_path(name)
        if exe:
            return True, f"CLI found: {exe}"
    for env_name in ("QODER_CN_HOME", "QODERCN_HOME", "LINGMA_HOME"):
        configured = os.environ.get(env_name)
        if configured:
            home = Path(configured).expanduser()
            if _dir_exists(home):
                return True, f"home dir found: {home}"
    for home in (_home() / ".qodercn", _home() / ".lingma", _home() / ".qoder-cn"):
        if _dir_exists(home):
            return True, f"home dir found: {home}"
    return False, t("detector_qodercn_not_found")


def detect_zcode_program() -> tuple[bool, str]:
    """ZCode desktop app: ``zcode`` on PATH, or a ``~/.zcode`` home directory."""
    exe = _exe_on_path("zcode")
    if exe:
        return True, f"CLI found: {exe}"
    home = _home() / ".zcode"
    if _dir_exists(home):
        return True, f"home dir found: {home}"
    return False, t("detector_zcode_not_found")


def detect_trae_program() -> tuple[bool, str]:
    """Trae: ``trae`` on PATH (best-effort; Trae is mostly an IDE)."""
    exe = _exe_on_path("trae")
    if exe:
        return True, f"CLI found: {exe}"
    return False, t("detector_trae_not_found")


def detect_opencode_program() -> tuple[bool, str]:
    """OpenCode: ``opencode`` on PATH."""
    exe = _exe_on_path("opencode")
    if exe:
        return True, f"CLI found: {exe}"
    return False, t("detector_opencode_not_found")


def detect_agents_generic_program() -> tuple[bool, str]:
    """AGENTS.md is a convention, not a program; always treated as available."""
    return True, "AGENTS.md convention - always available"


# Map agent name -> detector for the program itself.
PROGRAM_DETECTORS = {
    "codex": detect_codex_program,
    "minimax": detect_mavis_program,
    "zcode": detect_zcode_program,
    "qoder": detect_qoder_program,
    "qoder-project": detect_qoder_program,
    "qodercn": detect_qodercn_program,
    "qodercn-project": detect_qodercn_program,
    "trae": detect_trae_program,
    "opencode": detect_opencode_program,
    "agents-generic": detect_agents_generic_program,
}


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

    # Each agent has a different sentinel file that proves the skill landed.
    sentinels = {
        "codex": [root / "SKILL.md"],
        "minimax": [root / "engineering-calculation-system" / "SKILL.md"],
        "zcode": [root / "SKILL.md"],
        "qoder": [
            root / "agents" / "engineering-calc-system.md",
            root / "skills" / "engineering-calc-system" / "SKILL.md",
        ],
        "qoder-project": [
            root / ".qoder" / "agents" / "engineering-calc-system.md",
        ],
        "qodercn": [
            root / "agents" / "engineering-calc-system.md",
            root / "skills" / "engineering-calc-system" / "SKILL.md",
        ],
        "qodercn-project": [
            root / ".lingma" / "agents" / "engineering-calc-system.md",
            root / ".qodercn" / "agents" / "engineering-calc-system.md",
        ],
        "trae": [
            root / ".trae" / "project_rules.md",
            root / ".trae" / "rules" / "engineering-calc-system.md",
        ],
        "opencode": [
            root / ".opencode" / "skills" / "engineering-calc-system" / "SKILL.md",
        ],
        "agents-generic": [
            root / "AGENTS.md",
            root / ".agents" / "skills" / "engineering-calc-system" / "SKILL.md",
        ],
    }
    candidates = sentinels.get(agent_name, [])
    if not candidates:
        return False, f"{t('detector_no_sentinel')}: {agent_name}"

    present = [p for p in candidates if _file_exists(p)]
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
