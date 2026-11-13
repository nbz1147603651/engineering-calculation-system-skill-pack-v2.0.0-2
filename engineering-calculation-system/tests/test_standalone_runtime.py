from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from installer_gui import deployer, service  # noqa: E402


@pytest.fixture
def standalone(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    extraction = tmp_path / "_MEIPASS"
    runtime = extraction / "nimo-runtime"
    payloads = {
        "dist/core/engineering-calculation-system/SKILL.md": "canonical core",
        "dist/adapters-light/AGENTS.md": "project routing",
        "dist/adapters-light/.agents/skills/engineering-calc-system/SKILL.md": "generic adapter",
        "dist/qoder-addon/.qoder/agents/engineering-calc-system.md": "qoder agent",
        "dist/qoder-addon/.qoder/skills/engineering-calc-system/SKILL.md": "qoder skill",
        "dist/dsh-plugin/engineering-calculation-system-dsh/package.json": '{"name":"@engineering-calculation-system/dsh-plugin"}',
        "dist/dsh-plugin/engineering-calculation-system-dsh/cordis.patch.yml": "- id: engineering-calculation-system",
        "dist/dsh-plugin/engineering-calculation-system-dsh/lib/index.js": "export const name = 'engineering-calculation-system'",
        "dist/dsh-plugin/engineering-calculation-system-dsh/skills/engineering-calculation-system/SKILL.md": "harness skill",
    }
    for relative, content in payloads.items():
        path = runtime / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    manifest = {"schemaVersion": 1, "version": "2.6.0", "profiles": ["core", "adapters-light", "qoder-addon", "dsh-plugin"],
                "payloadId": "a" * 64,
                "files": {relative: hashlib.sha256((runtime / relative).read_bytes()).hexdigest() for relative in payloads}}
    (runtime / "NIMO-RUNTIME.json").write_text(json.dumps(manifest), encoding="utf-8")
    previous = deployer.REPO_ROOT
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(extraction), raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "user-data"))
    deployer.set_repo_root(runtime, validate=False)
    monkeypatch.setattr(deployer, "resolve_python", lambda: pytest.fail("Standalone install attempted to find external Python"))
    try:
        yield runtime
    finally:
        deployer.set_repo_root(previous, validate=False)


def test_standalone_core_install_verify_uninstall_needs_no_checkout(standalone: Path, tmp_path: Path) -> None:
    assert not (standalone / "tools/build_release.py").exists()
    assert deployer.using_bundled_runtime()
    result = service.runtime_self_test(tmp_path / "sandbox")
    assert result["ok"] and len(result["operations"]) == 3
    assert not (tmp_path / "sandbox/project/SKILL.md").exists()
    assert (tmp_path / "sandbox/NIMO-SELF-TEST.json").is_file()


def test_standalone_qoder_user_install_needs_no_python(standalone: Path, tmp_path: Path) -> None:
    target = tmp_path / "qoder-home"
    context = deployer.DeployContext(target, lambda _: None, lambda *_: None)
    deployer.deploy_qoder_user(context)
    assert deployer.verify_qoder_user(context)
    deployer.uninstall_qoder_user(context)
    assert not (target / "agents/engineering-calc-system.md").exists()


def test_standalone_resource_hash_failure_stops_install(standalone: Path, tmp_path: Path) -> None:
    (standalone / "dist/core/engineering-calculation-system/SKILL.md").write_text("corrupted", encoding="utf-8")
    with pytest.raises(deployer.DeployError, match="integrity verification"):
        deployer.ensure_profiles(("core",), log=lambda _: None, progress=lambda *_: None)
    assert not (tmp_path / "target").exists()


def test_harness_file_dependency_uses_durable_cache(standalone: Path, tmp_path: Path) -> None:
    context = deployer.DeployContext(tmp_path / "profile", lambda _: None, lambda *_: None)
    cached = deployer._dsh_install_source(context)
    assert not cached.is_relative_to(standalone.parent)
    assert cached.is_relative_to(tmp_path / "user-data")
    assert (cached / "skills/engineering-calculation-system/SKILL.md").is_file()
    assert deployer._dsh_install_source(context) == cached
