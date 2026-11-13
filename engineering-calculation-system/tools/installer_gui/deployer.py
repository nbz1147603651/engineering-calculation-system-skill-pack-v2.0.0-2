"""Deployment engine: build, copy, verify, uninstall for each agent.

Design rules (mirrors the approved plan):

* Release artifacts are produced once by ``tools/build_release.py``. The
  standalone client verifies and installs prebuilt resources directly; source
  development can still rebuild profiles. Native host package managers retain
  responsibility for their own profile registration.
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
import hashlib
import json
import queue
import re
import signal
import shutil
import subprocess
import sys
import threading
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import detector, dsh, managed_files
from .i18n import t
from .platform_contracts import ProfileCopy, UPLOAD_KIT_SENTINELS, get_contract


# --------------------------------------------------------------------------- #
# Repo-root + interpreter resolution (source mode vs frozen/exe mode)
# --------------------------------------------------------------------------- #
#
# In source mode the deployer lives at <repo>/tools/installer_gui/deployer.py,
# so the repo root is ``parents[2]`` and build_release.py is invoked with the
# current interpreter (``sys.executable``).
#
# The standalone executable carries prebuilt platform profiles. Frozen installs
# verify/copy these resources directly, using neither a source checkout nor a
# system Python. Development builds from a checkout remain available in source mode.

def bundled_runtime_root() -> Path | None:
    """Locate the versioned, prebuilt skill payload inside a standalone client."""
    if not getattr(sys, "frozen", False) or not hasattr(sys, "_MEIPASS"):
        return None
    root = Path(sys._MEIPASS) / "nimo-runtime"
    return root if (root / "NIMO-RUNTIME.json").is_file() else None


# Public spelling retained for the application shell.
embedded_runtime_root = bundled_runtime_root


def using_bundled_runtime() -> bool:
    root = bundled_runtime_root()
    return root is not None and REPO_ROOT is not None and root.resolve() == REPO_ROOT.resolve()


def runtime_status() -> dict:
    root = bundled_runtime_root()
    if root is None:
        return {"bundled": False, "ready": False, "profiles": [], "version": ""}
    try:
        manifest = json.loads((root / "NIMO-RUNTIME.json").read_text(encoding="utf-8"))
        profiles = manifest.get("profiles", [])
        ready = manifest.get("schemaVersion") == 1 and bool(profiles) and all((root / "dist" / profile).is_dir() for profile in profiles)
        return {"bundled": True, "ready": ready, "profiles": profiles, "version": manifest.get("version", "")}
    except (OSError, ValueError, AttributeError):
        return {"bundled": True, "ready": False, "profiles": [], "version": ""}


def _verify_bundled_profiles(profiles: tuple[str, ...]) -> None:
    root = bundled_runtime_root()
    if root is None:
        raise DeployError("Standalone engineering resources are missing; reinstall the client")
    manifest = json.loads((root / "NIMO-RUNTIME.json").read_text(encoding="utf-8"))
    if set(profiles) - set(manifest.get("profiles", [])):
        raise DeployError("This resource is not included in the client; use a current standalone installer")
    for relative, expected in manifest.get("files", {}).items():
        if not any(relative.startswith(f"dist/{profile}/") for profile in profiles):
            continue
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise DeployError(f"Packaged engineering resource failed integrity verification: {relative}")

def _default_repo_root() -> Path | None:
    """Best-effort repo root when running from source. ``None`` if unknown."""
    embedded = bundled_runtime_root()
    if embedded is not None:
        return embedded
    here = Path(__file__).resolve()
    candidate = here.parents[2]               # .../engineering-calculation-system
    if (candidate / "tools" / "build_release.py").exists():
        return candidate
    return None


REPO_ROOT: Path | None = _default_repo_root()
TOOLS_DIR: Path = (REPO_ROOT / "tools") if REPO_ROOT else Path("tools")
BUILD_SCRIPT: Path = TOOLS_DIR / "build_release.py"
DIST_ROOT: Path = (REPO_ROOT / "dist") if REPO_ROOT else Path("dist")
DIST_CORE: Path = DIST_ROOT / "core" / "engineering-calculation-system"
DIST_CODEX_PLUGIN: Path = DIST_ROOT / "codex-plugin" / "engineering-calculation-system"
DIST_ADAPTERS_LIGHT: Path = DIST_ROOT / "adapters-light"
DIST_QODER_ADDON: Path = DIST_ROOT / "qoder-addon"
DIST_QODERWORKCN_PLUGIN: Path = DIST_ROOT / "qoderworkcn-plugin"
DIST_ZCODE_PLUGIN: Path = DIST_ROOT / "zcode-plugin" / "engineering-calculation-system-zcode"
DIST_DSH_PLUGIN: Path = DIST_ROOT / "dsh-plugin" / "engineering-calculation-system-dsh"


PROFILE_REQUIRED_PATHS: dict[str, tuple[str, ...]] = {
    "core": ("SKILL.md",),
    "dsh-plugin": ("package.json", "cordis.patch.yml", "lib/index.js", "skills/engineering-calculation-system/SKILL.md"),
    "codex-plugin": (
        ".codex-plugin/plugin.json",
        "skills/engineering-calculation-system/SKILL.md",
        "skills/engineering-calculation-system/shared/codex-plugin-adapter.md",
    ),
    "adapters-light": ("AGENTS.md",),
    "qoder-addon": (".qoder/skills/engineering-calc-system/SKILL.md",),
    "qoderworkcn-plugin": (".qoder-plugin/plugin.json",),
    "zcode-plugin": (".zcode-plugin/plugin.json", "marketplace.json"),
}


def is_frozen() -> bool:
    """True when running inside a PyInstaller bundle."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def set_repo_root(path: Path | None, *, validate: bool = True) -> None:
    """Override the repo root (used by app.py when the exe prompts the user).

    Re-derives every dependent path so callers keep using the module-level
    constants without needing to plumb a parameter through every function.

    When *validate* is True (default), the new root is checked for
    ``tools/build_release.py`` before any globals are mutated.  Set it to
    False when pointing at a workspace directory that may not yet contain
    the full skill-pack source (deploy / build will fail gracefully later).
    """
    global REPO_ROOT, TOOLS_DIR, BUILD_SCRIPT, DIST_ROOT, DIST_CORE, DIST_CODEX_PLUGIN, DIST_ADAPTERS_LIGHT, DIST_QODER_ADDON, DIST_QODERWORKCN_PLUGIN, DIST_ZCODE_PLUGIN, DIST_DSH_PLUGIN
    candidate = Path(path).expanduser() if path else None
    if validate and candidate is not None and not (candidate / "tools" / "build_release.py").exists():
        raise DeployError(
            t("deployer_invalid_repo", path=candidate)
        )
    REPO_ROOT = candidate
    TOOLS_DIR = (REPO_ROOT / "tools") if REPO_ROOT else Path("tools")
    BUILD_SCRIPT = TOOLS_DIR / "build_release.py"
    DIST_ROOT = (REPO_ROOT / "dist") if REPO_ROOT else Path("dist")
    DIST_CORE = DIST_ROOT / "core" / "engineering-calculation-system"
    DIST_CODEX_PLUGIN = DIST_ROOT / "codex-plugin" / "engineering-calculation-system"
    DIST_ADAPTERS_LIGHT = DIST_ROOT / "adapters-light"
    DIST_QODER_ADDON = DIST_ROOT / "qoder-addon"
    DIST_QODERWORKCN_PLUGIN = DIST_ROOT / "qoderworkcn-plugin"
    DIST_ZCODE_PLUGIN = DIST_ROOT / "zcode-plugin" / "engineering-calculation-system-zcode"
    DIST_DSH_PLUGIN = DIST_ROOT / "dsh-plugin" / "engineering-calculation-system-dsh"


def resolve_python() -> str:
    """Return the Python interpreter to use for subprocess calls.

    This is only for developer builds from source. A frozen deployment never
    treats its executable as an interpreter and never needs a system Python.
    """
    if is_frozen():
        raise DeployError("Developer builds require source mode; the standalone client uses prebuilt engineering resources")
    return sys.executable


def require_repo_root() -> Path:
    """Return the resolved repo root, raising a clear error if unset."""
    if REPO_ROOT is None:
        raise DeployError(
            t("deployer_no_repo_root")
        )
    return REPO_ROOT


def require_build_script() -> Path:
    repo = require_repo_root()
    if not BUILD_SCRIPT.exists():
        raise DeployError(t("deployer_invalid_repo", path=repo))
    return repo


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
    cancelled: Callable[[], bool] = lambda: False,
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
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            start_new_session=os.name != "nt",
        )
    except FileNotFoundError as exc:
        log(f"[error] failed to launch: {exc}")
        raise DeployError(str(exc)) from exc

    assert proc.stdout is not None
    lines: queue.Queue[str | None] = queue.Queue()

    def read_output() -> None:
        try:
            for line in proc.stdout:
                lines.put(line.rstrip("\n"))
        finally:
            lines.put(None)

    reader = threading.Thread(target=read_output, daemon=True, name="nimo-process-output")
    reader.start()
    deadline = time.monotonic() + timeout if timeout is not None else None
    try:
        while True:
            if cancelled():
                raise DeployError("Operation cancelled")
            if deadline is not None and time.monotonic() >= deadline:
                raise DeployError(f"Command timed out after {timeout:g} seconds")
            try:
                line = lines.get(timeout=0.1)
            except queue.Empty:
                continue
            if line is None:
                break
            log(line)
        remaining = max(0.01, deadline - time.monotonic()) if deadline is not None else None
        return proc.wait(timeout=remaining)
    except (DeployError, subprocess.TimeoutExpired):
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           capture_output=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if proc.poll() is None:
            proc.kill()
        proc.wait(timeout=5)
        raise DeployError("Operation cancelled" if cancelled() else f"Command timed out after {timeout:g} seconds")
    finally:
        reader.join(timeout=1)
        proc.stdout.close()


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
    if using_bundled_runtime():
        _verify_bundled_profiles(profiles)
        log("[verify] prebuilt engineering resources are ready; no developer checkout or Python build is required")
        progress(1.0, "Engineering skills are ready")
        return
    repo = require_build_script()
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
    """Build only profiles whose dist output is missing or incomplete.

    Keeps re-deploys fast when dist/ is already populated.
    """
    if using_bundled_runtime():
        build_profiles(profiles, log=log, progress=progress)
        return
    profile_to_dist = {
        "core": DIST_CORE,
        "codex-plugin": DIST_CODEX_PLUGIN,
        "adapters-light": DIST_ADAPTERS_LIGHT,
        "qoder-addon": DIST_QODER_ADDON,
        "qoderworkcn-plugin": DIST_QODERWORKCN_PLUGIN,
        "zcode-plugin": DIST_ZCODE_PLUGIN,
        "dsh-plugin": DIST_DSH_PLUGIN,
    }
    def profile_ready(profile: str) -> bool:
        root = profile_to_dist.get(profile)
        if root is None or not root.exists():
            return False
        required = PROFILE_REQUIRED_PATHS.get(profile, ())
        return all((root / Path(relative)).exists() for relative in required)

    missing = tuple(p for p in profiles if not profile_ready(p))
    if not missing:
        log("[skip] all required dist profiles already present")
        progress(1.0, "dist already built")
        return
    build_profiles(missing, log=log, progress=progress)
    incomplete = tuple(profile for profile in profiles if not profile_ready(profile))
    if incomplete:
        raise DeployError(f"dist profile incomplete after build: {', '.join(incomplete)}")


# --------------------------------------------------------------------------- #
# Filesystem copy + backup helpers
# --------------------------------------------------------------------------- #

def _timestamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def _backup(path: Path, *, log: LogFn) -> None:
    """Rename an existing path to ``<path>.bak.<ts>`` so it can be restored."""
    if not path.exists():
        return
    backup = path.with_name(f"{path.name}.bak.{_timestamp()}.{time.time_ns()}")
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
        raise DeployError(t("deployer_source_missing", src=src))
    if src.resolve() == dst.resolve() or dst.resolve().is_relative_to(src.resolve()):
        raise DeployError(f"Deployment target overlaps its source: {dst}")
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
        raise DeployError(t("deployer_source_file_missing", src=src))
    if dst.exists():
        if _files_equal(src, dst):
            log(f"[skip] {dst} unchanged")
            return
        _backup(dst, log=log)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    log(f"[copy] {src} -> {dst}")


def _remove_managed(path: Path, *, log: LogFn) -> None:
    """Detach a managed path and keep a recoverable copy, tolerating absence."""
    if not path.exists():
        return
    # A separate container prevents a skill scanner from discovering the backup
    # as another direct <skills>/<name>/SKILL.md entry after uninstall.
    recovery = path.parent / ".engineering-calc-recovery"
    if not recovery.resolve().is_relative_to(path.parent.resolve()):
        raise DeployError(f"Recovery directory leaves the selected install parent: {recovery}")
    recovery.mkdir(exist_ok=True)
    archive = recovery / f"{path.name}.uninstalled.{time.time_ns()}"
    path.rename(archive)
    log(f"[uninstall] {path} -> {archive} (retained for recovery)")


# --------------------------------------------------------------------------- #
# Common deploy skeleton
# --------------------------------------------------------------------------- #

@dataclass
class DeployContext:
    """Inputs handed to every per-agent deploy/verify/uninstall callable."""

    install_root: Path | None
    log: LogFn
    progress: ProgressFn
    cancelled: Callable[[], bool] = lambda: False


def _resolve_root(ctx: DeployContext) -> Path:
    if ctx.install_root is None:
        raise DeployError(t("deployer_no_install_root"))
    return Path(ctx.install_root).expanduser()


# --------------------------------------------------------------------------- #
# Codex
# --------------------------------------------------------------------------- #

def deploy_codex(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    ensure_profiles(("codex-plugin",), log=ctx.log, progress=ctx.progress)
    ctx.progress(0.7, "copying Codex plugin")
    _copy_tree(DIST_CODEX_PLUGIN, root, log=ctx.log)
    ctx.progress(1.0, t("deploy_codex_done"))


def verify_codex(ctx: DeployContext) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed("codex", root)
    ctx.log(f"[verify] {detail}")
    return ok


def uninstall_codex(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    if not (root / ".codex-plugin" / "plugin.json").is_file():
        raise DeployError(t("deployer_codex_plugin_sentinel_missing", path=root))
    _remove_managed(root, log=ctx.log)
    ctx.log(t("uninstall_codex_done"))


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
    ctx.progress(1.0, t("deploy_minimax_done"))


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
    ctx.log(t("uninstall_minimax_done"))


# --------------------------------------------------------------------------- #
# ZCode - local marketplace folder under ~/.zcode/plugins/<plugin-name>/
# --------------------------------------------------------------------------- #

def deploy_zcode(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    ensure_profiles(("zcode-plugin",), log=ctx.log, progress=ctx.progress)
    ctx.progress(0.7, "copying ZCode plugin")
    _copy_tree(DIST_ZCODE_PLUGIN, root, log=ctx.log)
    ctx.log(t("deploy_zcode_notice", path=root))
    ctx.progress(1.0, t("deploy_zcode_done"))


def verify_zcode(ctx: DeployContext) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed("zcode", root)
    ctx.log(f"[verify] {detail}")
    return ok


def uninstall_zcode(ctx: DeployContext) -> None:
    root = _resolve_root(ctx)
    _remove_managed(root, log=ctx.log)
    ctx.log(t("uninstall_zcode_done"))


# --------------------------------------------------------------------------- #
# Qoder / Qoder CN (user-level) - shared prebuilt file installation
# --------------------------------------------------------------------------- #

def _deploy_qoder_user_overlay(ctx: DeployContext, agent_name: str) -> None:
    ensure_profiles(("qoder-addon",), log=ctx.log, progress=ctx.progress)
    root = _resolve_root(ctx)
    try:
        managed_files.install(root, agent_name, [(DIST_QODER_ADDON / ".qoder", Path("."))], ctx.log)
    except (OSError, ValueError) as error:
        raise DeployError(str(error)) from error
    ctx.progress(1.0, f"{agent_name} engineering skills installed")


def _verify_qoder_user_overlay(ctx: DeployContext, agent_name: str) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed(agent_name, root)
    ctx.log(f"[verify] {detail}")
    if not ok:
        return False
    try:
        files = managed_files.read_manifest(root.resolve(), agent_name)["files"]
        return bool(files) and all(managed_files.child(root, relative).is_file() and
                                   managed_files.digest(managed_files.child(root, relative)) == entry["sha256"]
                                   for relative, entry in files.items())
    except (OSError, ValueError) as error:
        ctx.log(f"[verify] {error}")
        return False


def _uninstall_qoder_user_overlay(ctx: DeployContext, agent_name: str) -> None:
    try:
        managed_files.uninstall(_resolve_root(ctx), agent_name, ctx.log)
    except (OSError, ValueError) as error:
        raise DeployError(str(error)) from error
    ctx.progress(1.0, f"{agent_name} managed engineering skills removed")


def deploy_qoder_user(ctx: DeployContext) -> None:
    _deploy_qoder_user_overlay(ctx, "qoder")


def verify_qoder_user(ctx: DeployContext) -> bool:
    return _verify_qoder_user_overlay(ctx, "qoder")


def uninstall_qoder_user(ctx: DeployContext) -> None:
    _uninstall_qoder_user_overlay(ctx, "qoder")


def deploy_qodercn_user(ctx: DeployContext) -> None:
    _deploy_qoder_user_overlay(ctx, "qodercn")


def verify_qodercn_user(ctx: DeployContext) -> bool:
    return _verify_qoder_user_overlay(ctx, "qodercn")


def uninstall_qodercn_user(ctx: DeployContext) -> None:
    _uninstall_qoder_user_overlay(ctx, "qodercn")


# --------------------------------------------------------------------------- #
# QoderWork CN Expert Kit - official .qoder-plugin upload package
# --------------------------------------------------------------------------- #

def _write_upload_zip(source_root: Path, zip_path: Path, *, log: LogFn) -> None:
    if not source_root.exists():
        raise DeployError(t("deployer_source_missing", src=source_root))
    if zip_path.exists():
        _backup(zip_path, log=log)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(source_root).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(2026, 6, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    log(f"[zip] {source_root} -> {zip_path}")


def _deploy_upload_kit(
    ctx: DeployContext,
    *,
    copy_message: str,
    zip_message: str,
    notice_key: str,
    done_key: str,
) -> None:
    root = _resolve_root(ctx)
    build_profiles(("qoderworkcn-plugin",), log=ctx.log, progress=ctx.progress)
    ctx.progress(0.65, copy_message)
    _copy_tree(DIST_QODERWORKCN_PLUGIN, root, log=ctx.log)
    zip_path = root.with_suffix(".zip")
    ctx.progress(0.9, zip_message)
    _write_upload_zip(root, zip_path, log=ctx.log)
    ctx.log(t(notice_key, path=root, zip=zip_path))
    ctx.progress(1.0, t(done_key))


def _verify_upload_kit(ctx: DeployContext, *, agent_name: str) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed(agent_name, root)
    ctx.log(f"[verify] {detail}")
    zip_path = root.with_suffix(".zip")
    if not ok:
        return False
    if not zip_path.exists():
        ctx.log(f"[verify] upload zip missing: {zip_path}")
        return False
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    required = set(UPLOAD_KIT_SENTINELS)
    missing = sorted(required - names)
    if missing:
        ctx.log(f"[verify] upload zip missing: {', '.join(missing)}")
        return False
    ctx.log(f"[verify] upload zip ready: {zip_path}")
    return True


def _uninstall_upload_kit(ctx: DeployContext, *, done_key: str) -> None:
    root = _resolve_root(ctx)
    _remove_managed(root, log=ctx.log)
    _remove_managed(root.with_suffix(".zip"), log=ctx.log)
    ctx.log(t(done_key))


def deploy_qoderworkcn_plugin(ctx: DeployContext) -> None:
    _deploy_upload_kit(
        ctx,
        copy_message="copying QoderWork CN expert kit",
        zip_message="creating QoderWork CN upload zip",
        notice_key="deploy_qoderworkcn_notice",
        done_key="deploy_qoderworkcn_done",
    )


def verify_qoderworkcn_plugin(ctx: DeployContext) -> bool:
    return _verify_upload_kit(ctx, agent_name="qoderworkcn")


def uninstall_qoderworkcn_plugin(ctx: DeployContext) -> None:
    _uninstall_upload_kit(ctx, done_key="uninstall_qoderworkcn_done")


def deploy_workbuddy_plugin(ctx: DeployContext) -> None:
    _deploy_upload_kit(
        ctx,
        copy_message="copying WorkBuddy expert kit",
        zip_message="creating WorkBuddy upload zip",
        notice_key="deploy_workbuddy_notice",
        done_key="deploy_workbuddy_done",
    )


def verify_workbuddy_plugin(ctx: DeployContext) -> bool:
    return _verify_upload_kit(ctx, agent_name="workbuddy")


def uninstall_workbuddy_plugin(ctx: DeployContext) -> None:
    _uninstall_upload_kit(ctx, done_key="uninstall_workbuddy_done")


# --------------------------------------------------------------------------- #
# Project-overlay agents (Qoder / Qoder CN / Trae / OpenCode / AGENTS Generic)
# --------------------------------------------------------------------------- #

def _profile_root(profile: str) -> Path:
    roots = {
        "core": DIST_CORE,
        "adapters-light": DIST_ADAPTERS_LIGHT,
        "qoder-addon": DIST_QODER_ADDON,
        "qoderworkcn-plugin": DIST_QODERWORKCN_PLUGIN,
        "zcode-plugin": DIST_ZCODE_PLUGIN,
        "dsh-plugin": DIST_DSH_PLUGIN,
    }
    try:
        return roots[profile]
    except KeyError as exc:
        raise DeployError(f"unknown release profile for project overlay: {profile}") from exc


def _resolve_profile_copy(copy: ProfileCopy) -> tuple[Path, Path]:
    source_root = _profile_root(copy.profile)
    source = source_root if copy.source == "." else source_root / Path(copy.source)
    return source, Path(copy.target)


def _project_overlay_for(agent_name: str):
    contract = get_contract(agent_name)
    if contract is None or contract.project_overlay is None:
        raise DeployError(f"agent has no project overlay contract: {agent_name}")
    return contract.project_overlay


def _deploy_contract_project_overlay(ctx: DeployContext, *, agent_name: str) -> None:
    contract = get_contract(agent_name)
    overlay = _project_overlay_for(agent_name)
    assert contract is not None
    ensure_profiles(contract.needs_profiles, log=ctx.log, progress=ctx.progress)
    copies = [_resolve_profile_copy(copy) for copy in overlay.copies]
    if overlay.include_core:
        copies.insert(0, (DIST_CORE, Path(".")))
    try:
        managed_files.install(_resolve_root(ctx), agent_name, copies, ctx.log)
    except (OSError, ValueError) as error:
        raise DeployError(str(error)) from error
    ctx.progress(1.0, t("deploy_project_done", agent=overlay.agent_label))


def _verify_contract_agent(ctx: DeployContext, *, agent_name: str) -> bool:
    root = _resolve_root(ctx)
    ok, detail = detector.skill_deployed(agent_name, root)
    ctx.log(f"[verify] {detail}")
    return ok


def _uninstall_contract_project_overlay(ctx: DeployContext, *, agent_name: str, done_key: str) -> None:
    try:
        managed_files.uninstall(_resolve_root(ctx), agent_name, ctx.log)
    except (OSError, ValueError) as error:
        raise DeployError(str(error)) from error
    ctx.log(t(done_key))


# ---- Qoder Project ---- #

def deploy_qoder_project(ctx: DeployContext) -> None:
    _deploy_contract_project_overlay(ctx, agent_name="qoder-project")


def verify_qoder_project(ctx: DeployContext) -> bool:
    return _verify_contract_agent(ctx, agent_name="qoder-project")


def uninstall_qoder_project(ctx: DeployContext) -> None:
    _uninstall_contract_project_overlay(
        ctx,
        agent_name="qoder-project",
        done_key="uninstall_qoder_project_done",
    )


# ---- Qoder CN Project ---- #

def deploy_qodercn_project(ctx: DeployContext) -> None:
    _deploy_contract_project_overlay(ctx, agent_name="qodercn-project")


def verify_qodercn_project(ctx: DeployContext) -> bool:
    return _verify_contract_agent(ctx, agent_name="qodercn-project")


def uninstall_qodercn_project(ctx: DeployContext) -> None:
    _uninstall_contract_project_overlay(
        ctx,
        agent_name="qodercn-project",
        done_key="uninstall_qodercn_project_done",
    )


# ---- Trae ---- #

def deploy_trae(ctx: DeployContext) -> None:
    _deploy_contract_project_overlay(ctx, agent_name="trae")


def verify_trae(ctx: DeployContext) -> bool:
    return _verify_contract_agent(ctx, agent_name="trae")


def uninstall_trae(ctx: DeployContext) -> None:
    _uninstall_contract_project_overlay(ctx, agent_name="trae", done_key="uninstall_trae_done")


# ---- OpenCode ---- #

def deploy_opencode(ctx: DeployContext) -> None:
    _deploy_contract_project_overlay(ctx, agent_name="opencode")


def verify_opencode(ctx: DeployContext) -> bool:
    return _verify_contract_agent(ctx, agent_name="opencode")


def uninstall_opencode(ctx: DeployContext) -> None:
    _uninstall_contract_project_overlay(ctx, agent_name="opencode", done_key="uninstall_opencode_done")


# ---- AGENTS Generic ---- #

def deploy_agents_generic(ctx: DeployContext) -> None:
    _deploy_contract_project_overlay(ctx, agent_name="agents-generic")


def verify_agents_generic(ctx: DeployContext) -> bool:
    return _verify_contract_agent(ctx, agent_name="agents-generic")


def uninstall_agents_generic(ctx: DeployContext) -> None:
    _uninstall_contract_project_overlay(
        ctx,
        agent_name="agents-generic",
        done_key="uninstall_agents_generic_done",
    )


# Native Harness profile operations. The host owns profile reconciliation.
def _dsh_install_source(ctx: DeployContext) -> Path:
    if not using_bundled_runtime():
        return DIST_DSH_PLUGIN
    root = bundled_runtime_root()
    assert root is not None
    manifest = json.loads((root / "NIMO-RUNTIME.json").read_text(encoding="utf-8"))
    package_id = manifest["payloadId"]
    if not re.fullmatch(r"[a-f0-9]{64}", package_id):
        raise DeployError("Invalid bundled engineering payload identifier")
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local/share")) / "NIMO Engineering/runtime" / package_id
    destination = base / "dsh-plugin"
    source_files = {path.relative_to(DIST_DSH_PLUGIN).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in DIST_DSH_PLUGIN.rglob("*") if path.is_file()}

    def matches(candidate: Path) -> bool:
        if not candidate.is_dir():
            return False
        actual = {path.relative_to(candidate).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                  for path in candidate.rglob("*") if path.is_file()}
        return actual == source_files

    if matches(destination):
        return destination
    if destination.exists():
        # Preserve a modified cache rather than overwrite user material.
        destination = base / f"dsh-plugin-{time.time_ns()}"
    if not destination.resolve().is_relative_to(base.resolve()):
        raise DeployError("Harness runtime cache leaves its managed directory")
    base.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DIST_DSH_PLUGIN, destination)
    if not matches(destination):
        raise DeployError("Persistent Harness bundle failed integrity verification")
    ctx.log("[ready] Harness bundle retained in the application runtime cache for future repair")
    return destination


def _dsh_action(ctx: DeployContext, action: str, output: list[str] | None = None) -> int:
    root = _resolve_root(ctx)
    try:
        argv, environment = dsh.command(root, action, _dsh_install_source(ctx) if action == "install" else None)
    except ValueError as error:
        raise DeployError(str(error)) from error
    def log(line: str) -> None:
        # A composed profile may contain credentials/settings. Inspect its row
        # identifiers in memory, never dump the full configuration into UI logs.
        if action != "verify":
            ctx.log(line)
        if output is not None:
            output.append(line)
    return _run_streaming(argv, log=log, env=environment, timeout=300, cancelled=ctx.cancelled)


def deploy_dsh(ctx: DeployContext) -> None:
    # Validate the launcher/profile before doing build work.
    try:
        dsh.command(_resolve_root(ctx), "install", DIST_DSH_PLUGIN)
    except ValueError as error:
        raise DeployError(str(error)) from error
    build_profiles(("dsh-plugin",), log=ctx.log, progress=ctx.progress)
    ctx.progress(0.7, "Installing native Harness profile bundle")
    if _dsh_action(ctx, "install") != 0:
        raise DeployError("Harness plugin installation failed")
    if not verify_dsh(ctx):
        raise DeployError("Harness bundle installation did not pass profile verification")
    ctx.progress(1.0, "Harness bundle installed; restart the client to reload skills")


def verify_dsh(ctx: DeployContext) -> bool:
    ok, detail = dsh.installed(_resolve_root(ctx))
    ctx.log(f"[verify] {detail}")
    if not ok:
        return False
    output: list[str] = []
    if _dsh_action(ctx, "verify", output) != 0:
        return False
    mounted = any(re.match(r"^\s*-\s+id:\s*['\"]?engineering-calculation-system['\"]?\s*$", line) for line in output)
    if not mounted:
        ctx.log("[verify] Harness composition did not include the skill provider row")
    return mounted


def uninstall_dsh(ctx: DeployContext) -> None:
    if _dsh_action(ctx, "uninstall") != 0:
        raise DeployError("Harness plugin removal failed")
    ctx.progress(1.0, "Harness bundle removed; profile data and unrelated plugins retained")
