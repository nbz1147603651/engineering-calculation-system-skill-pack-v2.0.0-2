"""Deployment engine: build, copy, verify, uninstall for each agent.

Design rules (mirrors the approved plan):

* **Reuse, don't reinvent.** Release artifacts are produced by the existing
  ``tools/build_release.py``; the Qoder user-level install is delegated to the
  existing ``tools/install_qoder_user.py`` (which already builds, installs,
  verifies, audits and uninstalls). This module only orchestrates subprocess
  calls + filesystem copies.
* **No silent overwrite.** When a target path already exists it is backed up to
  ``<path>.bak.<timestamp>`` before being replaced.
* **Streaming logs.** Every deploy/verify/uninstall callable accepts a
  ``log`` callable and a ``progress`` callable (0..1) so the UI thread can show
  live output without freezing. Failures raise :class:`DeployError` carrying the
  last log lines.
* **Idempotent uninstall.** We only remove files this package owns (the known
  sentinel + overlay tree), never user content.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import detector


# --------------------------------------------------------------------------- #
# Repo-root + interpreter resolution (source mode vs frozen/exe mode)
# --------------------------------------------------------------------------- #
#
# In source mode the deployer lives at <repo>/tools/installer_gui/deployer.py,
# so the repo root is ``parents[2]`` and build_release.py is invoked with the
# current interpreter (``sys.executable``).
#
# In frozen mode (PyInstaller exe) ``__file__`` points at a temp extraction
# directory, so neither trick works. The exe is a *deployment tool*, not a
# bundle of the skill source, so it must be told where the skill-pack repo
# lives (via ``ECS_REPO_ROOT`` env var, set by app.py from a folder picker) and
# must find a system Python on PATH to run build_release.py / install_qoder_user.py
# (the exe carries no interpreter of its own).

def _default_repo_root() -> Path | None:
    """Best-effort repo root when running from source. ``None`` if unknown."""
    here = Path(__file__).resolve()
    candidate = here.parents[2]               # .../engineering-calculation-system
    if (candidate / "tools" / "build_release.py").exists():
        return candidate
    return None


REPO_ROOT: Path | None = _default_repo_root()
TOOLS_DIR: Path = (REPO_ROOT / "tools") if REPO_ROOT else Path("tools")
BUILD_SCRIPT: Path = TOOLS_DIR / "build_release.py"
QODER_INSTALL_SCRIPT: Path = TOOLS_DIR / "install_qoder_user.py"
DIST_ROOT: Path = (REPO_ROOT / "dist") if REPO_ROOT else Path("dist")
DIST_CORE: Path = DIST_ROOT / "core" / "engineering-calculation-system"
DIST_ADAPTERS_LIGHT: Path = DIST_ROOT / "adapters-light"
DIST_QODER_ADDON: Path = DIST_ROOT / "qoder-addon"


def is_frozen() -> bool:
    """True when running inside a PyInstaller bundle."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def set_repo_root(path: Path | None) -> None:
    """Override the repo root (used by app.py when the exe prompts the user).

    Re-derives every dependent path so callers keep using the module-level
    constants without needing to plumb a parameter through every function.

    Validates the new root *before* mutating any global so a rejected path
    leaves the previously-set (or source-detected) root intact.
    """
    global REPO_ROOT, TOOLS_DIR, BUILD_SCRIPT, QODER_INSTALL_SCRIPT, DIST_ROOT, DIST_CORE, DIST_ADAPTERS_LIGHT, DIST_QODER_ADDON
    candidate = Path(path).expanduser() if path else None
    if candidate is not None and not (candidate / "tools" / "build_release.py").exists():
        raise DeployError(
            f"selected folder does not look like the skill-pack repo "
            f"(tools/build_release.py missing): {candidate}"
        )
    REPO_ROOT = candidate
    TOOLS_DIR = (REPO_ROOT / "tools") if REPO_ROOT else Path("tools")
    BUILD_SCRIPT = TOOLS_DIR / "build_release.py"
    QODER_INSTALL_SCRIPT = TOOLS_DIR / "install_qoder_user.py"
    DIST_ROOT = (REPO_ROOT / "dist") if REPO_ROOT else Path("dist")
    DIST_CORE = DIST_ROOT / "core" / "engineering-calculation-system"
    DIST_ADAPTERS_LIGHT = DIST_ROOT / "adapters-light"
    DIST_QODER_ADDON = DIST_ROOT / "qoder-addon"


def resolve_python() -> str:
    """Return the Python interpreter to use for subprocess calls.

    Source mode: the current interpreter (``sys.executable``).
    Frozen mode: a system ``python`` on PATH (the exe has no embedded one).
    Raises :class:`DeployError` if frozen and no system Python is reachable.
    """
    if not is_frozen():
        return sys.executable
    found = shutil.which("python") or shutil.which("python3") or shutil.which("py")
    if found:
        return found
    raise DeployError(
        "no system Python found on PATH. The deployment exe needs Python 3.9+ "
        "installed on the target machine to build the skill pack "
        "(it runs tools/build_release.py). Install Python or run from source."
    )


def require_repo_root() -> Path:
    """Return the resolved repo root, raising a clear error if unset."""
    if REPO_ROOT is None:
        raise DeployError(
            "skill-pack repository location is not set. "
            + ("Select the repo folder in the UI first." if is_frozen()
               else "ECS_REPO_ROOT is unset and the source layout was not detected.")
        )
    return REPO_ROOT


LogFn = Callable[[str], None]
ProgressFn = Callable[[float, str], None]


class DeployError(RuntimeError):
    """Raised when a deploy/verify/uninstall step fails."""


# --------------------------------------------------------------------------- #
# Subprocess helper with streaming output
# --------------------------------------------------------------------------- #

def _run_streaming(
    argv: list[str],
    *,
    log: LogFn,
    cwd: Path | None = None,
    timeout: float | None = None,
    env: dict[str, str] | None = None,
) -> int:
    """Run ``argv`` and stream stdout/stderr to ``log`` line by line.

    Returns the exit code. Does not raise on non-zero exit; callers decide
    whether a non-zero code is an error (so verify commands can report cleanly).
    """
    log(f"$ {' '.join(argv)}")
    proc_env = os.environ.copy()
    if env:
        proc_env.update(env)
    try:
        proc = subprocess.Popen(
            argv,
            cwd=str(cwd) if cwd else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env=proc_env,
        )
    except FileNotFoundError as exc:
        log(f"[error] failed to launch: {exc}")
        raise DeployError(str(exc)) from exc

    assert proc.stdout is not None
    for line in proc.stdout:
        log(line.rstrip("\n"))
    proc.wait(timeout=timeout)
    return proc.returncode


# --------------------------------------------------------------------------- #
# Build (reuse build_release.py)
# --------------------------------------------------------------------------- #

def build_profiles(
    profiles: tuple[str, ...],
    *,
    log: LogFn,
    progress: ProgressFn,
) -> None:
    """Ensure the given release profiles exist under ``dist/``.

    Calls ``python tools/build_release.py --profile <p>`` for each profile.
    build_release.py is idempotent (it cleans its target dir first), so this is
    safe to re-run.
    """
    if not profiles:
        return
    repo = require_repo_root()
    python = resolve_python()
    total = len(profiles)
    for index, profile in enumerate(profiles):
        progress(index / total, f"building profile: {profile}")
        rc = _run_streaming(
            [python, str(BUILD_SCRIPT), "--profile", profile],
            log=log,
            cwd=repo,
        )
        if rc != 0:
            raise DeployError(f"build_release.py failed for profile '{profile}' (exit {rc})")
    progress(1.0, "build complete")


def ensure_profiles(profiles: tuple[str, ...], *, log: LogFn, progress: ProgressFn) -> None:
    """Build only profiles whose dist output is missing.

    Keeps re-deploys fast when dist/ is already populated.
    """
    profile_to_dist = {
        "core": DIST_CORE,
        "adapters-light": DIST_ADAPTERS_LIGHT,
        "qoder-addon": DIST_QODER_ADDON,
    }
    missing = tuple(p for p in profiles if not profile_to_dist.get(p, Path("__none__")).exists())
    if not missing:
        log("[skip] all required dist profiles already present")
        progress(1.0, "dist already built")
        return
    build_profiles(missing, log=log, progress=progress)


# --------------------------------------------------------------------------- #
# Filesystem copy + backup helpers
# --------------------------------------------------------------------------- #

def _timestamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def _backup(path: Path, *, log: LogFn) -> None:
    """Rename an existing path to ``<path>.bak.<ts>`` so it can be restored."""
    if not path.exists():
        return
    backup = path.with_name(f"{path.name}.bak.{_timestamp()}")
    log(f"[backup] {path} -> {backup}")
    shutil.move(str(path), str(backup))


def _files_equal(a: Path, b: Path) -> bool:
    """True if two files have identical bytes (cheap size check first)."""
    try:
        if a.stat().st_size != b.stat().st_size:
            return False
    except OSError:
        return False
    import filecmp
    return filecmp.cmp(a, b, shallow=False)


def _copy_tree(src: Path, dst: Path, *, log: LogFn, merge: bool = False) -> None:
    """Copy ``src`` tree onto ``dst``.

    * ``merge=False`` (default, user-level installs): the destination is owned
      by this skill, so if it exists we back it up wholesale and replace it.
    * ``merge=True`` (project overlays): the destination is a project root that
      may contain unrelated user files, so we merge with ``dirs_exist_ok=True``
      and back up only the *individual files* whose content actually differs -
      never the whole root, and never identical files (so a no-op re-deploy
      produces zero backups).
    """
    if not src.exists():
        raise DeployError(f"source missing: {src} (run build first)")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if merge:
        backed = 0
        for s in src.rglob("*"):
            if not s.is_file():
                continue
            d = dst / s.relative_to(src)
            if d.exists() and not _files_equal(s, d):
                _backup(d, log=log)
                backed += 1
        if backed:
            log(f"[backup] {backed} changed file(s) backed up before merge")
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        if dst.exists():
            _backup(dst, log=log)
        shutil.copytree(src, dst, dirs_exist_ok=True)
    log(f"[copy] {src} -> {dst}")


def _copy_file(src: Path, dst: Path, *, log: LogFn) -> None:
    if not src.exists():
        raise DeployError(f"source file missing: {src}")
    if dst.exists():
        if _files_equal(src, dst):
            log(f"[skip] {dst} unchanged")
            return
        _backup(dst, log=log)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    log(f"[copy] {src} -> {dst}")


def _remove_managed(path: Path, *, log: LogFn) -> None:
    """Remove a path this package owns, tolerating absence."""
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
        log(f"[remove] {path}/")
    else:
        path.unlink()
        log(f"[remove] {path}")


def _remove_managed_and_backups(name: str, parent: Path, *, log: LogFn) -> None:
    """Remove a managed entry plus any ``<name>.bak.<ts>`` siblings we created.

    Used by project-overlay uninstalls so re-deploy/uninstall cycles do not
    leave stray backup files lying around in the user's project root.
    """
    _remove_managed(parent / name, log=log)
    for sibling in parent.glob(f"{name}.bak.*"):
        _remove_managed(sibling, log=log)


# --------------------------------------------------------------------------- #
# Common deploy skeleton
# --------------------------------------------------------------------------- #

@dataclass
class DeployContext:
    """Inputs handed to every per-agent deploy/verify/uninstall callable."""

    install_root: Path | None
    log: LogFn
    progress: ProgressFn


def _resolve_root(ctx: DeployContext) -> Path:
    if ctx.install_root is None:
        raise DeployError("no install root selected (pick a directory first)")
    return Path(ctx.install_root).expanduser()


# --------------------------------------------------------------------------- #
# Codex
# --------------------------------------------------------------------------- #

def deploy_codex(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    ensure_profiles(("core",), log=ctx.log, progress=ctx.progress)
    ctx.progress(0.7, "copying core skill")
    _copy_tree(DIST_CORE, root, log=ctx.log)
    ctx.progress(1.0, "Codex deploy complete")


def verify_codex(ctx: DeployContext) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed("codex", root)
    ctx.log(f"[verify] {detail}")
    return ok


def uninstall_codex(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    _remove_managed(root, log=ctx.log)
    ctx.log("[done] Codex skill removed")


# --------------------------------------------------------------------------- #
# MiniMax Code (Mavis) - repository layout skills/<name>/
# --------------------------------------------------------------------------- #

def _mavis_target(parent: Path) -> Path:
    return parent / "engineering-calculation-system"


def deploy_minimax(ctx: DeployContext) -> None:
    # Mavis expects skills/engineering-calculation-system/ under the skills root.
    root = _resolve_root(ctx)
    skills_root = root.parent if root.name == "engineering-calculation-system" else root
    target = _mavis_target(skills_root)
    ensure_profiles(("core",), log=ctx.log, progress=ctx.progress)
    ctx.progress(0.7, "copying skill into skills/engineering-calculation-system/")
    _copy_tree(DIST_CORE, target, log=ctx.log)
    ctx.progress(1.0, "MiniMax deploy complete")


def verify_minimax(ctx: DeployContext) -> bool:
    root = _resolve_root(ctx)
    skills_root = root.parent if root.name == "engineering-calculation-system" else root
    target = _mavis_target(skills_root)
    ok, detail = detector.skill_deployed("minimax", skills_root)
    ctx.log(f"[verify] {detail}")
    if not ok:
        return False
    # If the mavis CLI is reachable, ask it to confirm the skill is discoverable.
    mavis_cmd = detector._exe_on_path("mavis") or (
        str(Path.home() / ".mavis" / "bin" / "mavis.cmd")
        if (Path.home() / ".mavis" / "bin" / "mavis.cmd").exists()
        else None
    )
    if mavis_cmd is None:
        return ok  # CLI not installed; trust the filesystem sentinel.
    rc = _run_streaming([mavis_cmd, "skill", "show", "engineering-calculation-system"], log=ctx.log)
    return rc == 0


def uninstall_minimax(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    skills_root = root.parent if root.name == "engineering-calculation-system" else root
    _remove_managed(_mavis_target(skills_root), log=ctx.log)
    ctx.log("[done] MiniMax skill removed")


# --------------------------------------------------------------------------- #
# Qoder (user-level) - delegate to install_qoder_user.py
# --------------------------------------------------------------------------- #

def _qoder_home(ctx: DeployContext) -> Path:
    root = _resolve_root(ctx)
    return root


def deploy_qoder_user(ctx: DeployContext) -> None:
    home = _qoder_home(ctx)
    repo = require_repo_root()
    python = resolve_python()
    ctx.progress(0.2, "building qoder-addon + installing overlay")
    rc = _run_streaming(
        [python, str(QODER_INSTALL_SCRIPT), "--build", "--qoder-home", str(home)],
        log=ctx.log,
        cwd=repo,
    )
    if rc != 0:
        raise DeployError(f"install_qoder_user.py failed (exit {rc})")
    ctx.progress(1.0, "Qoder user overlay installed")


def verify_qoder_user(ctx: DeployContext) -> bool:
    home = _qoder_home(ctx)
    ok, detail = detector.skill_deployed("qoder", home)
    ctx.log(f"[verify] {detail}")
    if ok:
        # Run the script's own audit for a thorough check.
        repo = require_repo_root()
        python = resolve_python()
        rc = _run_streaming(
            [python, str(QODER_INSTALL_SCRIPT), "--audit", "--qoder-home", str(home)],
            log=ctx.log,
            cwd=repo,
        )
        return rc == 0
    return False


def uninstall_qoder_user(ctx: DeployContext) -> None:
    home = _qoder_home(ctx)
    repo = require_repo_root()
    python = resolve_python()
    rc = _run_streaming(
        [python, str(QODER_INSTALL_SCRIPT), "--uninstall", "--qoder-home", str(home)],
        log=ctx.log,
        cwd=repo,
    )
    if rc != 0:
        raise DeployError(f"install_qoder_user.py --uninstall failed (exit {rc})")
    ctx.log("[done] Qoder user overlay removed")


# --------------------------------------------------------------------------- #
# Project-overlay agents (Qoder Project / Trae / OpenCode / AGENTS Generic)
# --------------------------------------------------------------------------- #

def _deploy_project_overlay(
    ctx: DeployContext,
    *,
    agent_name: str,
    overlay_copies: list[tuple[Path, Path]],
    include_core: bool,
) -> None:
    """Common path for project-root overlays.

    ``overlay_copies`` is a list of (src_under_dist, rel_target) pairs.
    ``include_core`` also drops the full core skill at the project root.
    """
    project_root = _resolve_root(ctx)
    profiles: list[str] = ["core"]
    # add the adapter profile any copy needs
    for src, _ in overlay_copies:
        if "adapters-light" in src.parts:
            if "adapters-light" not in profiles:
                profiles.append("adapters-light")
        if "qoder-addon" in src.parts:
            if "qoder-addon" not in profiles:
                profiles.append("qoder-addon")
    ensure_profiles(tuple(profiles), log=ctx.log, progress=ctx.progress)

    ctx.progress(0.6, f"copying overlay into {project_root}")
    if include_core:
        # Merge core skill into the project root - never replace the root itself,
        # only back up individual files we are about to overwrite.
        _copy_tree(DIST_CORE, project_root, log=ctx.log, merge=True)
    steps = len(overlay_copies) or 1
    for index, (src, rel) in enumerate(overlay_copies):
        dst = project_root / rel
        if src.is_dir():
            _copy_tree(src, dst, log=ctx.log, merge=True)
        else:
            _copy_file(src, dst, log=ctx.log)
        ctx.progress(0.6 + 0.35 * (index + 1) / steps, f"copied {rel}")
    ctx.progress(1.0, f"{agent_name} project overlay deployed")


# ---- Qoder Project ---- #

def deploy_qoder_project(ctx: DeployContext) -> None:
    _deploy_project_overlay(
        ctx,
        agent_name="Qoder Project",
        overlay_copies=[(DIST_QODER_ADDON / ".qoder", Path(".qoder"))],
        include_core=True,
    )


def verify_qoder_project(ctx: DeployContext) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed("qoder-project", root)
    ctx.log(f"[verify] {detail}")
    return ok


def uninstall_qoder_project(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    _remove_managed_and_backups(".qoder", root, log=ctx.log)
    ctx.log("[done] .qoder overlay removed (core skill left intact)")


# ---- Trae ---- #

def deploy_trae(ctx: DeployContext) -> None:
    _deploy_project_overlay(
        ctx,
        agent_name="Trae",
        overlay_copies=[
            (DIST_ADAPTERS_LIGHT / ".trae", Path(".trae")),
            (DIST_ADAPTERS_LIGHT / "AGENTS.md", Path("AGENTS.md")),
        ],
        include_core=True,
    )


def verify_trae(ctx: DeployContext) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed("trae", root)
    ctx.log(f"[verify] {detail}")
    return ok


def uninstall_trae(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    _remove_managed_and_backups(".trae", root, log=ctx.log)
    _remove_managed_and_backups("AGENTS.md", root, log=ctx.log)
    ctx.log("[done] .trae overlay removed")


# ---- OpenCode ---- #

def deploy_opencode(ctx: DeployContext) -> None:
    _deploy_project_overlay(
        ctx,
        agent_name="OpenCode",
        overlay_copies=[
            (DIST_ADAPTERS_LIGHT / ".opencode", Path(".opencode")),
            (DIST_ADAPTERS_LIGHT / "AGENTS.md", Path("AGENTS.md")),
        ],
        include_core=True,
    )


def verify_opencode(ctx: DeployContext) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed("opencode", root)
    ctx.log(f"[verify] {detail}")
    return ok


def uninstall_opencode(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    _remove_managed_and_backups(".opencode", root, log=ctx.log)
    _remove_managed_and_backups("AGENTS.md", root, log=ctx.log)
    ctx.log("[done] .opencode overlay removed")


# ---- AGENTS Generic ---- #

def deploy_agents_generic(ctx: DeployContext) -> None:
    _deploy_project_overlay(
        ctx,
        agent_name="AGENTS Generic",
        overlay_copies=[
            (DIST_ADAPTERS_LIGHT / "AGENTS.md", Path("AGENTS.md")),
            (DIST_ADAPTERS_LIGHT / ".agents", Path(".agents")),
        ],
        include_core=True,
    )


def verify_agents_generic(ctx: DeployContext) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed("agents-generic", root)
    ctx.log(f"[verify] {detail}")
    return ok


def uninstall_agents_generic(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    _remove_managed_and_backups(".agents", root, log=ctx.log)
    _remove_managed_and_backups("AGENTS.md", root, log=ctx.log)
    ctx.log("[done] AGENTS.md + .agents overlay removed")
