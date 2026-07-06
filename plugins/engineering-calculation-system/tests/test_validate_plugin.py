#!/usr/bin/env python3
"""Unit checks for the Codex plugin validator."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path
from types import ModuleType


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_plugin.py"


def load_validator_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_plugin", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load validate_plugin.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_codex_plugin_version() -> None:
    validator = load_validator_module()
    assert validator.parse_codex_plugin_version("2.6.0+codex.20260701") == (
        "2.6.0",
        "2026-07-01",
    )


def test_installed_cache_path_accepts_parent_plugin_name() -> None:
    validator = load_validator_module()
    original_plugin_root = validator.PLUGIN_ROOT
    try:
        validator.PLUGIN_ROOT = Path(
            "/cache/engineering-calculation-system-local/"
            "engineering-calculation-system/2.6.0+codex.20260701"
        )
        assert "engineering-calculation-system" in validator.valid_manifest_path_names()
        assert "2.6.0+codex.20260701" in validator.valid_manifest_path_names()
    finally:
        validator.PLUGIN_ROOT = original_plugin_root


def test_sync_file_map_ignores_python_caches() -> None:
    validator = load_validator_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "scripts" / "__pycache__").mkdir(parents=True)
        (root / "scripts" / "__pycache__" / "ecs_execution.cpython-313.pyc").write_bytes(b"cache")
        (root / "scripts" / "ecs_execution.py").write_text("print('ok')\n", encoding="utf-8")

        files = validator.sync_file_map(root)

    assert "scripts/ecs_execution.py" in files
    assert "scripts/__pycache__/ecs_execution.cpython-313.pyc" not in files


def test_codex_adapter_capability_markers_are_checked() -> None:
    validator = load_validator_module()
    original_skill_root = validator.SKILL_ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            adapter = root / "shared" / "codex-plugin-adapter.md"
            adapter.parent.mkdir(parents=True)
            adapter.write_text("# Codex Plugin Adapter\n", encoding="utf-8")
            validator.SKILL_ROOT = root

            errors: list[str] = []
            validator.check_codex_adapter_content(errors)

        assert any("route card" in error for error in errors)
        assert any("web-complete default" in error for error in errors)
    finally:
        validator.SKILL_ROOT = original_skill_root


def test_codex_quickstart_markers_are_checked() -> None:
    validator = load_validator_module()
    original_plugin_root = validator.PLUGIN_ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            quickstart = root / "docs" / "CODEX_QUICKSTART.md"
            quickstart.parent.mkdir(parents=True)
            quickstart.write_text("# Codex Quickstart\n", encoding="utf-8")
            validator.PLUGIN_ROOT = root

            errors: list[str] = []
            validator.check_quickstart_content(errors)

        assert any("python scripts/validate_plugin.py" in error for error in errors)
        assert any("python scripts/verify_golden_cases.py" in error for error in errors)
    finally:
        validator.PLUGIN_ROOT = original_plugin_root


def main() -> int:
    tests = [
        test_parse_codex_plugin_version,
        test_installed_cache_path_accepts_parent_plugin_name,
        test_sync_file_map_ignores_python_caches,
        test_codex_adapter_capability_markers_are_checked,
        test_codex_quickstart_markers_are_checked,
    ]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} validate_plugin tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
