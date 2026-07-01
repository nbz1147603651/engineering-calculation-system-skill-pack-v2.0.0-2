#!/usr/bin/env python3
"""Refresh the bundled skill from the source core package and reapply overlays."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
DEFAULT_SOURCE = REPO_ROOT / "engineering-calculation-system" / "core" / "engineering-calculation-system"
DESTINATION = PLUGIN_ROOT / "skills" / "engineering-calculation-system"
OVERLAY_ROOT = PLUGIN_ROOT / "overlays" / "engineering-calculation-system"

CODEX_BLOCK = """## Codex Plugin Adapter

When this package is loaded from the Codex plugin, read
`shared/codex-plugin-adapter.md` before the router. The adapter maps this
platform-neutral skill pack onto Codex tool use, workspace edits, validation,
multi-agent boundaries, and user-facing completion rules.

"""

IGNORED_COPY_NAMES = {"__pycache__"}
IGNORED_COPY_SUFFIXES = {".pyc", ".pyo"}


def rel_to_repo(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def assert_plugin_child(path: Path) -> None:
    resolved = path.resolve()
    plugin_root = PLUGIN_ROOT.resolve()
    if not resolved.is_relative_to(plugin_root):
        raise RuntimeError(f"refusing to write outside plugin root: {path}")


def copy_tree(source: Path, destination: Path) -> None:
    assert_plugin_child(destination)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, ignore=copy_ignore)


def copy_ignore(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name in IGNORED_COPY_NAMES or Path(name).suffix in IGNORED_COPY_SUFFIXES
    }


def overlay_tree(source: Path, destination: Path) -> None:
    if not source.exists():
        return
    for path in source.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(source)
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def ensure_codex_block(skill_path: Path) -> None:
    text = skill_path.read_text(encoding="utf-8")
    if "## Codex Plugin Adapter" in text:
        return
    marker = "# Engineering Calculation System\n\n"
    if marker not in text:
        raise RuntimeError("cannot locate root heading in bundled SKILL.md")
    skill_path.write_text(text.replace(marker, marker + CODEX_BLOCK, 1), encoding="utf-8")


def staged_skill(source: Path, stage_parent: Path) -> Path:
    staged = stage_parent / "engineering-calculation-system"
    shutil.copytree(source, staged, ignore=copy_ignore)
    overlay_tree(OVERLAY_ROOT, staged)
    ensure_codex_block(staged / "SKILL.md")
    return staged


def file_map(root: Path) -> dict[str, Path]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }


def compare_trees(current: Path, desired: Path) -> list[tuple[str, str]]:
    current_files = file_map(current)
    desired_files = file_map(desired)
    changes: list[tuple[str, str]] = []
    for rel in sorted(set(desired_files) - set(current_files)):
        changes.append(("ADD", rel))
    for rel in sorted(set(current_files) - set(desired_files)):
        changes.append(("DELETE", rel))
    for rel in sorted(set(current_files) & set(desired_files)):
        if current_files[rel].read_bytes() != desired_files[rel].read_bytes():
            changes.append(("MODIFY", rel))
    return changes


def print_preview(changes: list[tuple[str, str]]) -> None:
    if not changes:
        print("Dry run: bundled skill already matches staged core + overlay.")
        return
    print("Dry run: planned bundled skill changes:")
    for action, rel in changes:
        print(f"{action:6} {rel}")


def check_dirty_destination(force: bool) -> None:
    if force:
        return
    if not (REPO_ROOT / ".git").exists():
        return
    rel_dest = rel_to_repo(DESTINATION)
    completed = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain", "--", rel_dest],
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git status failed")
    if completed.stdout.strip():
        raise RuntimeError(
            "bundled skill has uncommitted changes; rerun with --force after confirming overwrite is intended:\n"
            + completed.stdout.strip()
        )


def validate_plugin() -> None:
    command = [sys.executable, str(PLUGIN_ROOT / "scripts" / "validate_plugin.py")]
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Source core skill root. Defaults to the repository core package.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview added, modified, and deleted bundled-skill paths without writing.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow overwriting a bundled skill with uncommitted local changes.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip plugin validation after syncing.",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    if source == DESTINATION.resolve():
        raise SystemExit("source and bundled destination must be different paths")
    if not source.exists():
        raise SystemExit(f"source skill root does not exist: {source}")
    if not (source / "SKILL.md").exists():
        raise SystemExit(f"source skill root is missing SKILL.md: {source}")

    with tempfile.TemporaryDirectory(prefix="engineering-calc-codex-sync-") as tmp:
        staged = staged_skill(source, Path(tmp))
        changes = compare_trees(DESTINATION, staged)
        if args.dry_run:
            print_preview(changes)
            return 0

        if not changes:
            if not args.no_validate:
                validate_plugin()
            print("Bundled skill already matches staged core + overlay.")
            return 0

        check_dirty_destination(args.force)
        copy_tree(staged, DESTINATION)

    if not args.no_validate:
        validate_plugin()

    print(f"Synced bundled skill from {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
