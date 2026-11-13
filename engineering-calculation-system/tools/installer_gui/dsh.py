"""Native DeepSeek Harness profile integration, with no profile-file rewrites."""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path

PACKAGE_NAME = "@engineering-calculation-system/dsh-plugin"
PROFILE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
PACKAGE_PATH = Path("node_modules/@engineering-calculation-system/dsh-plugin")


def default_profile_root() -> Path:
    configured = os.environ.get("DSH_HOME")
    custom = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "DSH Custom Client/data"
    home = Path(configured).expanduser() if configured else custom if custom.is_dir() else Path.home() / ".dsh"
    return home / "profiles" / "web"


def profile_location(root: Path) -> tuple[Path, str]:
    root = root.expanduser().resolve()
    if root.parent.name != "profiles" or not PROFILE_NAME.fullmatch(root.name):
        raise ValueError("Choose a Harness profile directory: <DSH_HOME>/profiles/<profile>, for example ~/.dsh/profiles/web")
    return root.parent.parent, root.name


def launcher() -> list[str]:
    configured = os.environ.get("DSH_EXECUTABLE")
    if configured:
        executable = Path(configured).expanduser()
        if not executable.is_file():
            raise ValueError(f"DSH_EXECUTABLE does not exist: {executable}")
        return [str(executable)]
    command = shutil.which("dsh")
    if command:
        return [command]
    client = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "DSH Custom Client/app"
    executable = client / "bin/dsh.exe"
    entry = client / "runtime/node_modules/@deepseek-ai/dsh/lib/bin.js"
    if executable.is_file() and entry.is_file():
        return [str(executable), str(entry)]
    raise ValueError("DeepSeek Harness launcher not found. Install dsh or set DSH_EXECUTABLE to its launcher.")


def installed(root: Path) -> tuple[bool, str]:
    """A copied skill is insufficient: require a dependency and active bundle layer."""
    try:
        profile_location(root)
        manifest = json.loads((root / "package.json").read_text(encoding="utf-8"))
        dependency = manifest.get("dependencies", {}).get(PACKAGE_NAME)
        bundles = manifest.get("dsh", {}).get("profile", {}).get("bundles", [])
        if not isinstance(dependency, str) or not dependency or not isinstance(bundles, list) or PACKAGE_NAME not in bundles:
            return False, "Harness dependency or dsh.profile.bundles registration missing"
        package = root / PACKAGE_PATH
        required = ("package.json", "cordis.patch.yml", "lib/index.js", "skills/engineering-calculation-system/SKILL.md")
        missing = next((relative for relative in required if not (package / relative).is_file()), None)
        if missing:
            return False, f"Harness bundle incomplete: {missing}"
        return True, f"Harness profile bundle registered: {root}"
    except (OSError, ValueError, TypeError, AttributeError) as error:
        return False, f"Harness profile unavailable: {error}"


def command(root: Path, action: str, package: Path | None = None) -> tuple[list[str], dict[str, str]]:
    home, profile = profile_location(root)
    prefix = launcher()
    if action == "verify":
        arguments = ["--profile", profile, "--dump-config"]
    elif action == "install" and package is not None:
        arguments = ["plugin", "--profile", profile, "add", "file:" + package.resolve().as_posix()]
    elif action == "uninstall":
        arguments = ["plugin", "--profile", profile, "remove", PACKAGE_NAME]
    else:
        raise ValueError(f"Unsupported Harness action: {action}")
    return prefix + arguments, {"DSH_HOME": str(home)}
