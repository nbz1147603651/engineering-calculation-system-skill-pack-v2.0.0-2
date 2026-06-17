#!/usr/bin/env python3
"""Rebuild package tree, manifest, checksums, and all-in-one skill file."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.2.0"
CREATED_AT = "2026-06-16"

EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
}

EXCLUDED_FILES = {
    ".DS_Store",
    "MANIFEST.yaml",
    "CHECKSUMS.txt",
    "TREE.md",
    "engineering-calculation-system.all-in-one.md",
}

ALL_IN_ONE_PREFIXES = (
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "adapters/",
    "parent/",
    "skills/",
    "shared/",
    "templates/",
    "schemas/",
    "scripts/validate_artifacts.py",
    "workflow_diagrams/",
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


def include_path(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts
    if any(part in EXCLUDED_DIRS for part in rel_parts):
        return False
    if path.name in EXCLUDED_FILES:
        return False
    return path.is_file()


def all_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if include_path(path))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rebuild_checksums(files: list[Path]) -> None:
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in files]
    (ROOT / "CHECKSUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rebuild_manifest(files: list[Path]) -> None:
    lines = [
        "package: engineering-calculation-system-skill-pack",
        f"version: {VERSION}",
        f"created_at: {CREATED_AT}",
        f"file_count_excluding_manifest_and_checksums: {len(files)}",
        "lifecycle:",
        "  - reference_acquisition_and_persistence",
        "  - reference_analysis_and_logic_blueprint",
        "  - implementation_and_verification",
        "  - release_and_linux_cloud_deployment",
        "files:",
    ]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        lines.extend(
            [
                f"  - path: {rel}",
                f"    size_bytes: {path.stat().st_size}",
                f"    sha256: {sha256(path)}",
            ]
        )
    (ROOT / "MANIFEST.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def tree_lines(paths: list[Path]) -> list[str]:
    tree: dict[str, dict] = {}
    for path in paths:
        node = tree
        for part in path.relative_to(ROOT).parts:
            node = node.setdefault(part, {})

    lines = ["# Package Tree", "", "```text", f"{ROOT.name}/"]

    def render(node: dict[str, dict], prefix: str = "") -> None:
        items = sorted(node.items(), key=lambda item: item[0])
        for index, (name, child) in enumerate(items):
            last = index == len(items) - 1
            connector = "└── " if last else "├── "
            lines.append(f"{prefix}{connector}{name}")
            if child:
                render(child, prefix + ("    " if last else "│   "))

    render(tree)
    lines.extend(["```", ""])
    return lines


def rebuild_tree(files: list[Path]) -> None:
    (ROOT / "TREE.md").write_text("\n".join(tree_lines(files)), encoding="utf-8")


def include_all_in_one(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(rel == prefix or rel.startswith(prefix) for prefix in ALL_IN_ONE_PREFIXES)


def rebuild_all_in_one(files: list[Path]) -> None:
    lines = [
        "# Engineering Calculation System - All-in-One Skill Pack",
        f"Version: {VERSION}",
        "",
        "This merged file combines the root entrypoint, parent skills, child skills, shared contracts, key templates, validation schema, and scaffold files.",
        "",
    ]
    for path in files:
        if not include_all_in_one(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lines.extend(["", "---", "", f"## {rel}", "", content.rstrip(), ""])
    (ROOT / "engineering-calculation-system.all-in-one.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    files = all_files()
    rebuild_tree(files)
    rebuild_all_in_one(files)
    files = all_files()
    rebuild_manifest(files)
    files = all_files()
    rebuild_checksums(files)
    print(f"Rebuilt package indexes for {len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
