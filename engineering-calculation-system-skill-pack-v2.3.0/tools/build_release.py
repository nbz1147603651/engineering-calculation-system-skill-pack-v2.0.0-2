#!/usr/bin/env python3
"""Build layered release artifacts for the engineering calculation skill pack."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SOURCE = REPO_ROOT / "core" / "engineering-calculation-system"
LIGHT_ADAPTER_SOURCE = REPO_ROOT / "adapter_sources" / "light"
QODER_ADAPTER_SOURCE = REPO_ROOT / "adapter_sources" / "qoder"
DIST_ROOT = REPO_ROOT / "dist"
VERSION = "2.3.0"
CREATED_AT = "2026-06-17"

PROFILE_CHOICES = ("core", "adapters-light", "qoder-addon", "singlefile", "source-dev")
DEFAULT_ALL_PROFILES = PROFILE_CHOICES

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

SINGLEFILE_PREFIXES = (
    "SKILL.md",
    "agents/",
    "parent/",
    "skills/",
    "shared/",
    "templates/",
    "schemas/",
    "scripts/validate_artifacts.py",
    "project_template/engineering_calc_project/README.md",
    "project_template/engineering_calc_project/pyproject.toml",
    "project_template/engineering_calc_project/implementation/02_modules/module_asset_registry.csv",
    "project_template/engineering_calc_project/webapp/",
    "project_template/engineering_calc_project/apps/",
    "project_template/engineering_calc_project/data/formula_registry/",
    "project_template/engineering_calc_project/deploy/",
    "project_template/engineering_calc_project/release/",
    "project_template/engineering_calc_project/src/",
    "project_template/engineering_calc_project/tests/",
)


def should_skip(path: Path) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True
    if path.name in EXCLUDED_FILE_NAMES:
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


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if should_skip(path.relative_to(root)):
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
    files = [
        path for path in iter_files(profile_root)
        if path.name not in {"MANIFEST.yaml", "CHECKSUMS.txt", "TREE.md"}
    ]

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
    write_indexes(profile_root, "engineering-calculation-system-core")
    return profile_root


def build_adapters_light() -> Path:
    profile_root = DIST_ROOT / "adapters-light"
    clean_dir(profile_root)
    copy_tree(LIGHT_ADAPTER_SOURCE, profile_root)
    write_indexes(profile_root, "engineering-calculation-system-adapters-light")
    return profile_root


def build_qoder_addon() -> Path:
    profile_root = DIST_ROOT / "qoder-addon"
    clean_dir(profile_root)
    copy_tree(QODER_ADAPTER_SOURCE, profile_root)
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
    for rel in ("core", "adapter_sources", "docs", "archive", "tools", ".gitignore"):
        src = REPO_ROOT / rel
        if not src.exists():
            continue
        dst = profile_root / rel
        if src.is_dir():
            copy_tree(src, dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    write_indexes(profile_root, "engineering-calculation-system-source-dev")
    return profile_root


def build_profile(profile: str) -> Path:
    builders = {
        "core": build_core,
        "adapters-light": build_adapters_light,
        "qoder-addon": build_qoder_addon,
        "singlefile": build_singlefile,
        "source-dev": build_source_dev,
    }
    return builders[profile]()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILE_CHOICES, help="Release profile to build")
    parser.add_argument("--all", action="store_true", help="Build every release profile")
    args = parser.parse_args(argv)

    if not args.profile and not args.all:
        parser.error("pass --profile <name> or --all")

    profiles = DEFAULT_ALL_PROFILES if args.all else (args.profile,)
    built: list[Path] = []
    for profile in profiles:
        assert profile is not None
        built.append(build_profile(profile))

    for path in built:
        files = iter_files(path)
        total_kb = sum(file.stat().st_size for file in files) / 1024
        print(f"built {path.relative_to(REPO_ROOT).as_posix()} ({len(files)} files, {total_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
