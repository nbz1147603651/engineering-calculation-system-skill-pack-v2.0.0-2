#!/usr/bin/env python3
"""Unit checks for the Codex bundled-skill sync helper."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_from_core.py"


def load_sync_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("sync_from_core", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load sync_from_core.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_help_exposes_dry_run_and_force() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--help"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "--dry-run" in completed.stdout
    assert "--force" in completed.stdout


def test_compare_trees_reports_add_modify_delete() -> None:
    sync = load_sync_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        current = root / "current"
        desired = root / "desired"
        current.mkdir()
        desired.mkdir()

        (current / "deleted.txt").write_text("old", encoding="utf-8")
        (current / "modified.txt").write_text("old", encoding="utf-8")
        (desired / "modified.txt").write_text("new", encoding="utf-8")
        (desired / "added.txt").write_text("new", encoding="utf-8")

        changes = set(sync.compare_trees(current, desired))

    assert ("ADD", "added.txt") in changes
    assert ("MODIFY", "modified.txt") in changes
    assert ("DELETE", "deleted.txt") in changes


def test_dirty_protection_marker_exists() -> None:
    sync = load_sync_module()
    assert callable(sync.check_dirty_destination)


def main() -> int:
    tests = [
        test_help_exposes_dry_run_and_force,
        test_compare_trees_reports_add_modify_delete,
        test_dirty_protection_marker_exists,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} sync_from_core tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
