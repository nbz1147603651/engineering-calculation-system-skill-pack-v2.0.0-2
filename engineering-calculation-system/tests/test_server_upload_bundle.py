from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

import pytest


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = WORKSPACE_ROOT / "engineering-calculation-system"
TOOLS_ROOT = PACKAGE_ROOT / "tools"
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

import build_release  # noqa: E402


def _write_file(root: Path, relative: str, content: bytes | str = "sentinel\n") -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    return path


def test_desktop_receipt_inputs_include_runtime_assets_and_exclude_bytecode(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_release, "REPO_ROOT", tmp_path)
    for relative in ("tools/installer_gui/app.py", "tools/installer_gui/assets/nimo.png", "tools/release_config.json", "tools/build_release.py"):
        _write_file(tmp_path, relative)
    _write_file(tmp_path, "tools/installer_gui/__pycache__/app.pyc", b"cache")
    before = build_release.ui_client_source_files()
    assert len(before) == 4
    assert "tools/installer_gui/assets/nimo.png" in before
    _write_file(tmp_path, "tools/installer_gui/assets/nimo.png", b"changed mascot")
    assert before != build_release.ui_client_source_files()


def test_server_upload_validation_accepts_single_gui_copy(tmp_path: Path) -> None:
    package_root = tmp_path / build_release.upload_package_root_name()
    installer = build_release.ui_client_installer_name()
    installer_path = _write_file(package_root, f"data/{installer}", b"fake installer")
    gui_sha = build_release.sha256(installer_path)

    _write_file(package_root, "home/index.html", "<!doctype html>\n")
    _write_file(package_root, "home/version.json", json.dumps({"version": build_release.VERSION}))
    build_release.write_update_manifest(
        package_root / "dist" / "update-manifest.stable.json",
        built_at="2026-07-06T00:00:00Z",
        gui_sha=gui_sha,
        gui_size=installer_path.stat().st_size,
    )
    _write_file(package_root, "README_UPLOAD.md")
    _write_file(package_root, "VERSION", build_release.VERSION + "\n")
    _write_file(package_root, "version.json", json.dumps({"version": build_release.VERSION}))
    _write_file(package_root, "CHECKSUMS.txt")

    archive_path = tmp_path / build_release.upload_archive_name()
    build_release.write_upload_zip(package_root, archive_path, archive_root_name=package_root.name)

    build_release.validate_server_upload_bundle(package_root, archive_path)


def test_server_upload_validation_rejects_duplicate_gui_copy(tmp_path: Path) -> None:
    package_root = tmp_path / "upload-root"
    installer = build_release.ui_client_installer_name()
    payload = b"same installer bytes"
    _write_file(package_root, f"data/{installer}", payload)
    _write_file(package_root, f"dist/{installer}", payload)

    with pytest.raises(RuntimeError, match="exactly one GUI installer"):
        build_release.assert_no_duplicate_upload_payloads(package_root)


def test_server_upload_validation_rejects_nested_zip_payload(tmp_path: Path) -> None:
    package_root = tmp_path / "upload-root"
    installer = build_release.ui_client_installer_name()
    _write_file(package_root, f"data/{installer}", b"fake installer")
    nested_zip = package_root / "dist" / "ecs-homepage-linux-web.zip"
    nested_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(nested_zip, "w") as archive:
        archive.writestr(f"site/data/{installer}", b"fake installer")

    with pytest.raises(RuntimeError, match="nested zip archive"):
        build_release.assert_no_duplicate_upload_payloads(package_root)
