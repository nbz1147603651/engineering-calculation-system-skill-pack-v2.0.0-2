#!/usr/bin/env python3
"""Build layered release artifacts for the engineering calculation skill pack."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from versioning import (
    assert_skill_frontmatter_versions,
    load_release_config,
    sync_skill_frontmatter_versions,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SOURCE = REPO_ROOT / "core" / "engineering-calculation-system"
LIGHT_ADAPTER_SOURCE = REPO_ROOT / "adapter_sources" / "light"
QODER_ADAPTER_SOURCE = REPO_ROOT / "adapter_sources" / "qoder"
DIST_ROOT = REPO_ROOT / "dist"
RELEASE_ROOT = DIST_ROOT / "release"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".blocked_pytest_cache_container",
    "dist",
}

EXCLUDED_FILE_NAMES = {
    ".DS_Store",
    "MANIFEST.yaml",
    "CHECKSUMS.txt",
    "TREE.md",
}

FORBIDDEN_CACHE_SUFFIXES = {
    ".pyc",
    ".pyo",
}

@dataclass(frozen=True)
class BundleCopy:
    profile: str
    source: str
    target: str
    is_file: bool = False


@dataclass(frozen=True)
class BundleTarget:
    name: str
    path: str
    install_text: str
    include_core: bool = True
    include_adapter_docs: bool = False
    payload_at_root: bool = False
    include_install_guide: bool = True
    copies: tuple[BundleCopy, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReleaseArchive:
    target: BundleTarget
    archive_path: Path
    install_folder: str
    file_count: int


def parse_bundle_copy(data: dict) -> BundleCopy:
    return BundleCopy(
        profile=data["profile"],
        source=data["source"],
        target=data["target"],
        is_file=bool(data.get("is_file", False)),
    )


def parse_bundle_target(data: dict) -> BundleTarget:
    return BundleTarget(
        name=data["name"],
        path=data["path"],
        install_text=data["install_text"],
        include_core=bool(data.get("include_core", True)),
        include_adapter_docs=bool(data.get("include_adapter_docs", False)),
        payload_at_root=bool(data.get("payload_at_root", False)),
        include_install_guide=bool(data.get("include_install_guide", True)),
        copies=tuple(parse_bundle_copy(copy) for copy in data.get("copies", ())),
        notes=tuple(data.get("notes", ())),
    )


def validate_rel_path(value: str, field: str, *, allow_dot: bool = False) -> None:
    if not value:
        raise ValueError(f"{field} must not be empty")
    if value == "." and allow_dot:
        return
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field} must be a relative path inside the release bundle: {value}")


def validate_release_config(
    config: dict,
    targets: tuple[BundleTarget, ...],
) -> None:
    profiles = set(config["profiles"])
    for field in ("default_all_profiles", "release_required_profiles"):
        unknown = set(config.get(field, ())) - profiles
        if unknown:
            raise ValueError(f"{field} references unknown profile(s): {', '.join(sorted(unknown))}")

    seen_paths: set[str] = set()
    for target in targets:
        validate_rel_path(
            target.path,
            f"classified target {target.name} path",
            allow_dot=target.payload_at_root,
        )
        if target.path in seen_paths:
            raise ValueError(f"duplicate classified target path: {target.path}")
        seen_paths.add(target.path)
        for copy in target.copies:
            validate_bundle_copy(copy, profiles, f"classified target {target.name}")

    target_names = {target.name for target in targets}
    unknown_publish_targets = set(config.get("publish_targets", ())) - target_names
    if unknown_publish_targets:
        raise ValueError(
            "publish_targets references unknown target(s): "
            + ", ".join(sorted(unknown_publish_targets))
        )

    if not config.get("singlefile_prefixes"):
        raise ValueError("singlefile_prefixes must not be empty")
    if not config.get("source_dev_includes"):
        raise ValueError("source_dev_includes must not be empty")


def validate_bundle_copy(copy: BundleCopy, profiles: set[str], context: str) -> None:
    if copy.profile not in profiles:
        raise ValueError(f"{context} references unknown profile: {copy.profile}")
    validate_rel_path(copy.source, f"{context} source", allow_dot=True)
    validate_rel_path(copy.target, f"{context} target", allow_dot=True)


CONFIG = load_release_config()
VERSION = CONFIG["version"]
CREATED_AT = CONFIG["created_at"]
PACKAGE_PREFIX = CONFIG.get("package_prefix", "engineering-calculation-system")
PROFILE_CHOICES = tuple(CONFIG["profiles"])
DEFAULT_ALL_PROFILES = tuple(CONFIG.get("default_all_profiles", PROFILE_CHOICES))
RELEASE_REQUIRED_PROFILES = tuple(CONFIG.get("release_required_profiles", PROFILE_CHOICES))
SINGLEFILE_PREFIXES = tuple(CONFIG["singlefile_prefixes"])
SOURCE_DEV_INCLUDES = tuple(CONFIG["source_dev_includes"])
UI_CLIENT_CONFIG = CONFIG.get("ui_client", {})
CLASSIFIED_TARGETS = tuple(parse_bundle_target(target) for target in CONFIG["classified_targets"])
PUBLISH_TARGET_NAMES = tuple(CONFIG.get("publish_targets", (target.name for target in CLASSIFIED_TARGETS)))
validate_release_config(CONFIG, CLASSIFIED_TARGETS)


def should_skip(path: Path, *, include_indexes: bool = False) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True
    if not include_indexes and path.name in EXCLUDED_FILE_NAMES:
        return True
    if path.suffix in FORBIDDEN_CACHE_SUFFIXES:
        return True
    return False


def clean_dir(path: Path) -> None:
    resolved = path.resolve()
    dist_resolved = DIST_ROOT.resolve()
    if not str(resolved).startswith(str(dist_resolved)):
        raise RuntimeError(f"refusing to clean outside dist: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if should_skip(rel):
            continue
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def sync_frontmatter_versions(root: Path) -> None:
    """Synchronize SKILL.md frontmatter versions in generated artifacts."""
    sync_skill_frontmatter_versions(root, VERSION)


def assert_frontmatter_versions(root: Path) -> None:
    assert_skill_frontmatter_versions(root, VERSION)


def require_paths(root: Path, paths: list[str], *, context: str) -> None:
    missing = [path for path in paths if not (root / path).exists()]
    if missing:
        raise RuntimeError(f"{context} missing required path(s): {', '.join(missing)}")


def require_text(path: Path, phrases: list[str], *, context: str) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [phrase for phrase in phrases if phrase not in text]
    if missing:
        raise RuntimeError(f"{context} missing required phrase(s): {', '.join(missing)}")


def iter_files(root: Path, *, include_indexes: bool = False) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if should_skip(path.relative_to(root), include_indexes=include_indexes):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_lines(root: Path, files: list[Path]) -> list[str]:
    tree: dict[str, dict] = {}
    for path in files:
        node = tree
        for part in path.relative_to(root).parts:
            node = node.setdefault(part, {})

    lines = ["# Package Tree", "", "```text", f"{root.name}/"]

    def render(node: dict[str, dict], prefix: str = "") -> None:
        items = sorted(node.items(), key=lambda item: item[0])
        for index, (name, child) in enumerate(items):
            last = index == len(items) - 1
            connector = "\\-- " if last else "+-- "
            lines.append(f"{prefix}{connector}{name}")
            if child:
                render(child, prefix + ("    " if last else "|   "))

    render(tree)
    lines.extend(["```", ""])
    return lines


def write_indexes(profile_root: Path, package_name: str) -> None:
    files = iter_files(profile_root)

    manifest = [
        f"package: {package_name}",
        f"version: {VERSION}",
        f"created_at: {CREATED_AT}",
        f"file_count_excluding_manifest_and_checksums: {len(files)}",
        "files:",
    ]
    for path in files:
        rel = path.relative_to(profile_root).as_posix()
        manifest.extend(
            [
                f"  - path: {rel}",
                f"    size_bytes: {path.stat().st_size}",
                f"    sha256: {sha256(path)}",
            ]
        )
    (profile_root / "MANIFEST.yaml").write_text("\n".join(manifest) + "\n", encoding="utf-8")

    checksums = [f"{sha256(path)}  {path.relative_to(profile_root).as_posix()}" for path in files]
    (profile_root / "CHECKSUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    (profile_root / "TREE.md").write_text("\n".join(tree_lines(profile_root, files)), encoding="utf-8")


def include_singlefile(path: Path) -> bool:
    rel = path.relative_to(CORE_SOURCE).as_posix()
    return any(rel == prefix or rel.startswith(prefix) for prefix in SINGLEFILE_PREFIXES)


def build_core() -> Path:
    profile_root = DIST_ROOT / "core"
    clean_dir(profile_root)
    copy_tree(CORE_SOURCE, profile_root / "engineering-calculation-system")
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    write_indexes(profile_root, "engineering-calculation-system-core")
    return profile_root


def build_adapters_light() -> Path:
    profile_root = DIST_ROOT / "adapters-light"
    clean_dir(profile_root)
    copy_tree(LIGHT_ADAPTER_SOURCE, profile_root)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    write_indexes(profile_root, "engineering-calculation-system-adapters-light")
    return profile_root


def build_qoder_addon() -> Path:
    profile_root = DIST_ROOT / "qoder-addon"
    clean_dir(profile_root)
    copy_tree(QODER_ADAPTER_SOURCE, profile_root)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    write_indexes(profile_root, "engineering-calculation-system-qoder-addon")
    return profile_root


def build_singlefile() -> Path:
    profile_root = DIST_ROOT / "singlefile"
    clean_dir(profile_root)
    output = profile_root / "engineering-calculation-system.all-in-one.md"
    lines = [
        "# Engineering Calculation System - All-in-One Skill Pack",
        f"Version: {VERSION}",
        "",
        "This generated file is for agents that cannot load the layered skill package.",
        "Prefer dist/core/engineering-calculation-system/ when multi-file loading is available.",
        "",
    ]
    for path in iter_files(CORE_SOURCE):
        if not include_singlefile(path):
            continue
        rel = path.relative_to(CORE_SOURCE).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lines.extend(["", "---", "", f"## {rel}", "", content.rstrip(), ""])
    output.write_text("\n".join(lines), encoding="utf-8")
    write_indexes(profile_root, "engineering-calculation-system-singlefile")
    return profile_root


def build_source_dev() -> Path:
    profile_root = DIST_ROOT / "source-dev"
    clean_dir(profile_root)
    for rel in SOURCE_DEV_INCLUDES:
        src = REPO_ROOT / rel
        if not src.exists():
            continue
        dst = profile_root / rel
        if src.is_dir():
            copy_tree(src, dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    write_indexes(profile_root, "engineering-calculation-system-source-dev")
    return profile_root


def build_ui_client() -> Path:
    """Build the one-click deployment console as a Windows single-file exe.

    Driven by the ``ui_client`` block in release_config.json. Uses PyInstaller
    ``--onefile`` so the result is a self-contained exe that needs no Python on
    the target machine. If PyInstaller is not installed, this is a soft failure:
    we emit a README explaining how to install it, so the rest of the release
    build is not blocked.
    """
    profile_root = DIST_ROOT / "ui-client"
    clean_dir(profile_root)

    if not UI_CLIENT_CONFIG:
        raise RuntimeError("ui_client config missing from release_config.json")

    exe_name = UI_CLIENT_CONFIG["exe_name_template"].format(version=VERSION)
    entry_module = UI_CLIENT_CONFIG["entry_module"]            # e.g. tools.installer_gui.app
    collect_all = tuple(UI_CLIENT_CONFIG.get("collect_all", ()))
    collect_submodules = tuple(UI_CLIENT_CONFIG.get("collect_submodules", ()))
    onefile = bool(UI_CLIENT_CONFIG.get("onefile", True))
    windowed = bool(UI_CLIENT_CONFIG.get("windowed", True))

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        readme = profile_root / "README.md"
        readme.write_text(
            "# UI client not built\n\n"
            "PyInstaller is not installed in this environment, so the deployment\n"
            "console exe was skipped. Install it and re-run:\n\n"
            "```bash\npip install pyinstaller\npython tools/build_release.py --profile ui-client\n```\n",
            encoding="utf-8",
        )
        print(f"ui-client: PyInstaller not installed; wrote {readme.relative_to(REPO_ROOT)}")
        return profile_root

    # PyInstaller must import the installer_gui package, which lives under
    # tools/ (not an installed distribution). We give it an entry script that
    # puts tools/ on sys.path before importing the real entry module.
    tools_dir = REPO_ROOT / "tools"
    bootstrap = profile_root / "_entry_bootstrap.py"
    bootstrap.write_text(
        "import sys\n"
        "from pathlib import Path\n"
        f"sys.path.insert(0, r'{tools_dir}')\n"
        f"from {entry_module} import main\n"
        "main()\n",
        encoding="utf-8",
    )

    argv: list[str] = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(bootstrap),
        f"--name={exe_name}",
        f"--distpath={profile_root}",
        f"--workpath={(profile_root / '_build').as_posix()}",
        f"--specpath={(profile_root / '_spec').as_posix()}",
        "--noconfirm",
        "--clean",
    ]
    if onefile:
        argv.append("--onefile")
    if windowed:
        argv.append("--windowed")
    for pkg in collect_all:
        argv.append(f"--collect-all={pkg}")
    for mod in collect_submodules:
        argv.append(f"--collect-submodules={mod}")

    print(f"ui-client: running PyInstaller -> {exe_name}")
    result = subprocess.run(argv, cwd=str(REPO_ROOT))
    # Clean up build scratch dirs PyInstaller leaves behind.
    for scratch in ("_build", "_spec"):
        scratch_dir = profile_root / scratch
        if scratch_dir.exists():
            shutil.rmtree(scratch_dir, ignore_errors=True)
    bootstrap.unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(f"PyInstaller failed (exit {result.returncode})")

    exe_path = profile_root / (exe_name + ".exe")
    if not exe_path.exists():
        raise RuntimeError(f"PyInstaller reported success but {exe_path} was not produced")

    write_indexes(profile_root, "engineering-calculation-system-ui-client")
    return profile_root


def build_profile(profile: str) -> Path:
    builders = {
        "core": build_core,
        "adapters-light": build_adapters_light,
        "qoder-addon": build_qoder_addon,
        "singlefile": build_singlefile,
        "source-dev": build_source_dev,
        "ui-client": build_ui_client,
    }
    return builders[profile]()


def archive_name(profile: str) -> str:
    return f"engineering-calculation-system-{profile}-v{VERSION}.zip"


def target_slug(name: str) -> str:
    return "".join(char if char.isalnum() else "-" for char in name).strip("-")


def release_archive_name(target: BundleTarget) -> str:
    return f"{PACKAGE_PREFIX}-{target_slug(target.name)}-v{VERSION}.zip"


def release_package_root_name(target: BundleTarget) -> str:
    return f"{PACKAGE_PREFIX}-{target_slug(target.name)}-v{VERSION}"


def target_install_folder(target: BundleTarget) -> str:
    if target.payload_at_root:
        return "."
    return Path(target.path).name


def write_zip(source_root: Path, archive_path: Path, *, archive_root_name: str | None = None) -> None:
    files = iter_files(source_root, include_indexes=True)
    with zipfile.ZipFile(archive_path, "w") as archive:
        for file in files:
            rel = file.relative_to(source_root).as_posix()
            if archive_root_name:
                rel = f"{archive_root_name}/{rel}"
            info = zipfile.ZipInfo(rel, date_time=(2026, 6, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, file.read_bytes())


def bundle_path(root: Path, rel: str) -> Path:
    return root / Path(rel)


def profile_path(profile_roots: dict[str, Path], copy: BundleCopy) -> Path:
    base = profile_roots[copy.profile]
    if copy.source == ".":
        return base
    return base / copy.source


def apply_bundle_copy(profile_roots: dict[str, Path], copy: BundleCopy, dst_root: Path) -> None:
    src = profile_path(profile_roots, copy)
    dst = bundle_path(dst_root, copy.target)
    if copy.is_file:
        copy_file(src, dst)
    else:
        copy_tree(src, dst)


def published_targets() -> tuple[BundleTarget, ...]:
    by_name = {target.name: target for target in CLASSIFIED_TARGETS}
    return tuple(by_name[name] for name in PUBLISH_TARGET_NAMES)


def write_target_install_guide(package_root: Path, target: BundleTarget, install_folder: str) -> None:
    lines = [
        f"# Engineering Calculation System v{VERSION} - {target.name}",
        "",
        f"This package is prepared for {target.name}.",
        "",
        target.install_text,
        "",
        "```text",
        f"{install_folder}/",
        "```",
        "",
    ]
    for note in target.notes:
        lines.extend([note, ""])
    (package_root / "INSTALL.md").write_text("\n".join(lines), encoding="utf-8")


def write_minimax_readmes(payload_root: Path) -> None:
    """Write repo-root guides for MiniMax Code local and Github import flows."""
    readme = f"""# Engineering Calculation System for MiniMax Code

This package is prepared as a MiniMax Code skills repository.

## Local Install

For a local MiniMax Code / Mavis install on Windows:

1. Unzip this archive.
2. Copy `skills/engineering-calculation-system/` to:

```text
%USERPROFILE%\\.mavis\\skills\\engineering-calculation-system\\
```

3. Restart MiniMax Code, or verify from PowerShell:

```powershell
& "$env:USERPROFILE\\.mavis\\bin\\mavis.cmd" skill list
& "$env:USERPROFILE\\.mavis\\bin\\mavis.cmd" skill show engineering-calculation-system
```

If your MiniMax Code / Mavis build reports a different user skill root, use the reported root.

## Delivery Contract

For implementation or release work, the skill must use:

```text
shared/lifecycle.md
```

`web-complete` means dual closure: a readable A4/LaTeX calculation book with
real input and non-empty `BookResult.checks`, plus a complete web system with
API/UI, import/export, batch, deployment artifacts, and smoke tests. The
MiniMaxCode entrypoint must use the full core package, project template, and
validator before making a production completion claim.

## Import from Github

1. Unzip this archive.
2. Publish the unzipped contents as a Github repository root.
3. In MiniMax Code, open Skills, choose Create, then Import from Github.
4. Paste the repository URL.

The skill entry is:

```text
skills/engineering-calculation-system/SKILL.md
```

## Smoke Prompt

After import, start a task with:

```text
Use engineering-calculation-system to create a web-complete engineering calculation scaffold with capability detection, Marimo optional review, and HTML/LaTeX report export.
```

## Validation

When the package is available on disk, validate it with:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core
```
"""
    readme_zh = f"""# MiniMax Code Engineering Calculation System

This ASCII guide replaces the previous encoded Chinese fallback to avoid mojibake in strict package validation.

Use `skills/engineering-calculation-system/SKILL.md` as the skill entrypoint. For implementation or release work, load `shared/lifecycle.md`.

`web-complete` means dual closure: a readable A4/LaTeX calculation book with real input and non-empty `BookResult.checks`, plus a complete web system with API/UI, import/export, batch, deployment artifacts, and smoke tests.

Validate before completion:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core
```
"""
    (payload_root / "README.md").write_text(readme, encoding="utf-8")
    (payload_root / "README_zh.md").write_text(readme_zh, encoding="utf-8")


def merge_core_into(dst: Path, profile_roots: dict[str, Path]) -> None:
    copy_tree(profile_roots["core"] / "engineering-calculation-system", dst)


def merge_adapter_docs_into(dst: Path, profile_roots: dict[str, Path]) -> None:
    copy_tree(profile_roots["adapters-light"] / "adapters", dst / "adapters")


def stage_target_payload(profile_roots: dict[str, Path], target: BundleTarget, payload_root: Path) -> None:
    if target.include_core:
        merge_core_into(payload_root, profile_roots)
    if target.include_adapter_docs:
        merge_adapter_docs_into(payload_root, profile_roots)
    for copy in target.copies:
        apply_bundle_copy(profile_roots, copy, payload_root)
    if target.name == "MiniMaxCode":
        write_minimax_readmes(payload_root)


def validate_target_payload(target: BundleTarget, payload_root: Path) -> None:
    context = f"{target.name} payload"
    if target.name == "QODER":
        require_paths(
            payload_root,
            [
                "SKILL.md",
                "reference.md",
                "qoder_quickstart.md",
                "assets/lifecycle-console.html",
            ],
            context=context,
        )
        require_text(
            payload_root / "SKILL.md",
            [
                "QODER-Project",
                "web-complete",
                "Stable ASCII Contract",
                "shared/lifecycle.md",
                "dual closure",
                "qoder_quickstart.md",
            ],
            context=context,
        )
        require_text(
            payload_root / "qoder_quickstart.md",
            [
                "Qoder Package Self-Check",
                "Direct QODER Skill",
                "QODER Project overlay",
                "Complete core project",
            ],
            context=context,
        )
        require_text(
                payload_root / "assets" / "lifecycle-console.html",
                [
                f"v{VERSION}",
                "12a",
                "12b",
                "12c",
                "14",
            ],
            context=context,
        )
        return

    if target.name == "MiniMaxCode":
        require_paths(
            payload_root,
            [
                "README.md",
                "README_zh.md",
                "skills/engineering-calculation-system/SKILL.md",
                "skills/engineering-calculation-system/shared/lifecycle.md",
                "skills/engineering-calculation-system/scripts/validate_artifacts.py",
                "skills/engineering-calculation-system/project_template/engineering_calc_project/src/pkg/core/capabilities.py",
            ],
            context=context,
        )
        require_text(
            payload_root / "skills/engineering-calculation-system/SKILL.md",
            [
                "name: engineering-calculation-system",
                "shared/lifecycle.md",
                "dual closure",
                "run_book(BookInput) -> BookResult",
            ],
            context=context,
        )
        require_text(
            payload_root / "README.md",
            [
                "Local Install",
                "Import from Github",
                "%USERPROFILE%\\.mavis\\skills\\engineering-calculation-system\\",
                "skills/engineering-calculation-system/SKILL.md",
                "shared/lifecycle.md",
                "dual closure",
                "BookResult.checks",
            ],
            context=context,
        )
        return

    if target.include_core:
        require_paths(
            payload_root,
            [
                "SKILL.md",
                "skills/00-engineering-calculation-router.skill.md",
                "shared/lifecycle.md",
                "templates/implementation/ui_layout_spec.md",
                "schemas/artifact_contracts.json",
                "scripts/validate_artifacts.py",
                "project_template/engineering_calc_project/webapp/routes.py",
                "project_template/engineering_calc_project/webapp/i18n.py",
                "project_template/engineering_calc_project/webapp/templates/base.html",
                "project_template/engineering_calc_project/webapp/templates/partials/_topbar.html",
                "project_template/engineering_calc_project/webapp/static/js/i18n.js",
                "project_template/engineering_calc_project/deploy/Dockerfile",
                "project_template/engineering_calc_project/tests/smoke/test_web_routes.py",
            ],
            context=context,
        )
        require_text(
            payload_root / "SKILL.md",
            [
                "shared/lifecycle.md",
                "dual closure",
            ],
            context=context,
        )
        require_text(
            payload_root / "shared/lifecycle.md",
            [
                "Engineering Calculation Lifecycle",
                "Web-Complete Exit Gate",
                "BookResult.checks",
            ],
            context=context,
        )
        require_text(
            payload_root / "project_template/engineering_calc_project/webapp/templates/partials/_topbar.html",
            [
                "id=\"langToggle\"",
                "data-lang=\"en\"",
                "data-lang=\"zh\"",
            ],
            context=context,
        )
        require_text(
            payload_root / "project_template/engineering_calc_project/webapp/static/js/i18n.js",
            [
                "localStorage",
                "document.documentElement.lang",
                "setLanguage",
            ],
            context=context,
        )

    platform_required = {
        "QODER Project": [
            ".qoder/skills/engineering-calc-system/SKILL.md",
            ".qoder/skills/engineering-calc-system/reference.md",
            ".qoder/skills/engineering-calc-system/qoder_quickstart.md",
            ".qoder/skills/engineering-calc-system/assets/lifecycle-console.html",
            ".qoder/agents/engineering-calc-system.md",
            ".qoder/agents/engineering-calc-reference-acquirer.md",
            ".qoder/agents/engineering-calc-source-intake.md",
            ".qoder/agents/engineering-calc-logic-extractor.md",
            ".qoder/agents/engineering-calc-module-worker.md",
            ".qoder/agents/engineering-calc-interface-worker.md",
            ".qoder/agents/engineering-calc-verification-worker.md",
            ".qoder/agents/engineering-calc-release-worker.md",
            ".qoder/references/engineering-calc-system.md",
        ],
        "TRAE": [
            ".trae/project_rules.md",
            ".trae/rules/engineering-calc-system.md",
        ],
        "OpenCode": [
            ".opencode/skills/engineering-calc-system/SKILL.md",
        ],
        "AGENTS Generic": [
            "AGENTS.md",
            ".agents/skills/engineering-calc-system/SKILL.md",
        ],
    }
    if target.name in platform_required:
        require_paths(payload_root, platform_required[target.name], context=context)
        if target.name == "QODER Project":
            require_text(
                payload_root / ".qoder" / "skills" / "engineering-calc-system" / "assets" / "lifecycle-console.html",
                [f"v{VERSION}", "12a", "12b", "12c", "14"],
                context=context,
            )

    if target.include_adapter_docs:
        require_paths(
            payload_root,
            [
                "adapters/agent-entrypoints.md",
                "adapters/mcp-recommendations.md",
            ],
            context=context,
        )


def build_platform_package(profile_roots: dict[str, Path], target: BundleTarget, package_root: Path) -> Path:
    missing = [profile for profile in RELEASE_REQUIRED_PROFILES if profile not in profile_roots]
    if missing:
        raise RuntimeError(f"release package requires profiles: {', '.join(missing)}")

    if package_root.exists():
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True, exist_ok=True)

    install_folder = target_install_folder(target)
    payload_root = package_root if target.payload_at_root else package_root / install_folder
    stage_target_payload(profile_roots, target, payload_root)
    sync_frontmatter_versions(package_root)
    assert_frontmatter_versions(package_root)
    validate_target_payload(target, payload_root)
    if target.include_install_guide:
        write_target_install_guide(package_root, target, install_folder)
    return package_root


def write_release_index(archives: list[ReleaseArchive]) -> None:
    lines = [
        "# Engineering Calculation System Release Bundles",
        "",
        f"Version: {VERSION}",
        f"Created at: {CREATED_AT}",
        "",
        "## Publish Files",
        "",
        "| Target | Archive | Install Folder | Files | Size KB | SHA256 |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for item in archives:
        lines.append(
            f"| {item.target.name} | `{item.archive_path.name}` | "
            f"`{item.install_folder}/` | {item.file_count} | "
            f"{item.archive_path.stat().st_size / 1024:.1f} | `{sha256(item.archive_path)}` |"
        )
    lines.extend(
        [
            "",
            "## Install",
            "",
        ]
    )
    for item in archives:
        lines.extend(
            [
                f"### {item.target.name}",
                "",
                item.target.install_text,
                "",
                "```text",
                f"{item.install_folder}/",
                "```",
                "",
            ]
        )
        for note in item.target.notes:
            lines.extend([note, ""])
    lines.extend(
        [
            "## Non-Published Build Outputs",
            "",
            "`dist/singlefile/` and `dist/source-dev/` are still generated for fallback and development use, but they are not part of the default platform publish packages.",
            "",
        ]
    )
    (RELEASE_ROOT / "RELEASE_INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def build_split_archives(built_profiles: dict[str, Path]) -> list[Path]:
    split_root = RELEASE_ROOT / "split-archives"
    split_root.mkdir(parents=True, exist_ok=True)
    archives: list[Path] = []
    for profile, profile_root in built_profiles.items():
        archive_path = split_root / archive_name(profile)
        write_zip(profile_root, archive_path)
        archives.append(archive_path)
    return archives


def build_release_packages(
    built_profiles: dict[str, Path],
    *,
    split_archives: bool = False,
) -> list[ReleaseArchive]:
    clean_dir(RELEASE_ROOT)
    archives: list[ReleaseArchive] = []
    with tempfile.TemporaryDirectory(prefix="ecs-release-") as temp_dir:
        temp_root = Path(temp_dir)
        for target in published_targets():
            package_name = release_package_root_name(target)
            package_root = build_platform_package(built_profiles, target, temp_root / package_name)
            archive_path = RELEASE_ROOT / release_archive_name(target)
            archive_root_name = None if target.payload_at_root else package_root.name
            write_zip(package_root, archive_path, archive_root_name=archive_root_name)
            archives.append(
                ReleaseArchive(
                    target=target,
                    archive_path=archive_path,
                    install_folder=target_install_folder(target),
                    file_count=len(iter_files(package_root, include_indexes=True)),
                )
            )

    checksum_lines = [f"{sha256(item.archive_path)}  {item.archive_path.name}" for item in archives]
    if split_archives:
        for archive in build_split_archives(built_profiles):
            checksum_lines.append(f"{sha256(archive)}  split-archives/{archive.name}")
    (RELEASE_ROOT / "CHECKSUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    write_release_index(archives)
    return archives


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        choices=PROFILE_CHOICES,
        action="append",
        help="Release profile to build. May be passed more than once.",
    )
    parser.add_argument("--all", action="store_true", help="Build every release profile")
    parser.add_argument(
        "--archives",
        action="store_true",
        help="Also create platform release zip packages under dist/release",
    )
    parser.add_argument(
        "--no-archives",
        action="store_true",
        help="Do not create platform release zip packages when building every profile",
    )
    parser.add_argument(
        "--split-archives",
        action="store_true",
        help="Also create legacy per-profile zip archives under dist/release/split-archives",
    )
    parser.add_argument(
        "--no-ui-client",
        action="store_true",
        help="Skip the ui-client profile (the PyInstaller exe build) when building all profiles. "
        "Has no effect when --profile ui-client is passed explicitly.",
    )
    args = parser.parse_args(argv)

    if args.profile and args.all:
        parser.error("use either --profile or --all, not both")
    if args.archives and args.no_archives:
        parser.error("use either --archives or --no-archives, not both")

    default_publish = not args.profile and not args.all
    profiles = DEFAULT_ALL_PROFILES if args.all or default_publish else tuple(args.profile or ())
    # --no-ui-client drops the (slow, PyInstaller-dependent) exe build from the
    # default all-profiles set, but never blocks an explicit --profile ui-client.
    if args.no_ui_client and not args.profile:
        profiles = tuple(p for p in profiles if p != "ui-client")
    create_archives = args.archives or ((args.all or default_publish) and not args.no_archives)

    if default_publish:
        print("no profile specified; building all profiles and platform release packages")

    built: dict[str, Path] = {}
    for profile in profiles:
        built[profile] = build_profile(profile)

    for path in built.values():
        files = iter_files(path)
        total_kb = sum(file.stat().st_size for file in files) / 1024
        print(f"built {path.relative_to(REPO_ROOT).as_posix()} ({len(files)} files, {total_kb:.1f} KB)")

    if create_archives:
        if set(RELEASE_REQUIRED_PROFILES) - set(built):
            missing = ", ".join(sorted(set(RELEASE_REQUIRED_PROFILES) - set(built)))
            raise RuntimeError(f"platform release packages require all profiles; missing: {missing}")
        archives = build_release_packages(built, split_archives=args.split_archives)
        print(f"built {RELEASE_ROOT.relative_to(REPO_ROOT).as_posix()} ({len(archives)} platform archives)")
        for archive in archives:
            print(
                f"  {archive.archive_path.name} "
                f"({archive.file_count} files, {archive.archive_path.stat().st_size / 1024:.1f} KB)"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
