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


def copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


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
        "--no-validate",
        action="store_true",
        help="Skip plugin validation after syncing.",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.exists():
        raise SystemExit(f"source skill root does not exist: {source}")
    if not (source / "SKILL.md").exists():
        raise SystemExit(f"source skill root is missing SKILL.md: {source}")

    with tempfile.TemporaryDirectory(prefix="engineering-calc-codex-sync-") as tmp:
        staged = Path(tmp) / "engineering-calculation-system"
        shutil.copytree(source, staged)
        overlay_tree(OVERLAY_ROOT, staged)
        ensure_codex_block(staged / "SKILL.md")
        copy_tree(staged, DESTINATION)

    if not args.no_validate:
        validate_plugin()

    print(f"Synced bundled skill from {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

