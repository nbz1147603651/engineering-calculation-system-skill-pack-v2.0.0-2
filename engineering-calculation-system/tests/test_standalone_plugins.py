from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


PLUGIN_SOURCE = Path(__file__).resolve().parents[2] / "plugins/engineering-calculation-system-zcode"


@pytest.fixture
def standalone_zcode(tmp_path: Path) -> Path:
    destination = tmp_path / "plugins/engineering-calculation-system-zcode"
    shutil.copytree(PLUGIN_SOURCE, destination, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    assert not (tmp_path / "engineering-calculation-system/tools").exists()
    return destination


def validate(plugin: Path) -> subprocess.CompletedProcess[str]:
    # Isolated Python cannot borrow the development checkout's import paths.
    return subprocess.run(
        [sys.executable, "-I", "-B", str(plugin / "scripts/validate_plugin.py")],
        cwd=plugin, capture_output=True, text=True, encoding="utf-8",
    )


def test_zcode_doctor_runs_without_source_checkout(standalone_zcode: Path) -> None:
    result = validate(standalone_zcode)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ZCode plugin validation passed." in result.stdout


def test_standalone_zcode_doctor_rejects_versions_that_disagree_with_bundled_contract(
    standalone_zcode: Path,
) -> None:
    # Even mutually consistent host metadata must match the shipped core contract.
    version = "99.0.0+zcode.19990101"
    for relative in ("package.json", ".zcode-plugin/plugin.json", "marketplace.json"):
        path = standalone_zcode / relative
        metadata = json.loads(path.read_text(encoding="utf-8"))
        if relative == "marketplace.json":
            metadata["plugins"][0]["version"] = version
        else:
            metadata["version"] = version
        path.write_text(json.dumps(metadata), encoding="utf-8")
    result = validate(standalone_zcode)
    assert result.returncode == 1
    assert "bundled artifact contract" in result.stderr
