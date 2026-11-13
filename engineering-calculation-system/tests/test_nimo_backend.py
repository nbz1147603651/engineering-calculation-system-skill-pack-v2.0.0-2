from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from installer_gui import deployer, dsh, managed_files, service, workflow  # noqa: E402


def test_dsh_profile_requires_native_bundle_registration(tmp_path: Path) -> None:
    root = tmp_path / "profiles/web"
    package = root / dsh.PACKAGE_PATH
    for relative in ("package.json", "cordis.patch.yml", "lib/index.js", "skills/engineering-calculation-system/SKILL.md"):
        path = package / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("bundle", encoding="utf-8")
    (root / "package.json").write_text(json.dumps({"dependencies": {dsh.PACKAGE_NAME: "file:bundle"}}), encoding="utf-8")
    assert not dsh.installed(root)[0]
    (root / "package.json").write_text(json.dumps({"dependencies": {dsh.PACKAGE_NAME: "file:bundle"}, "dsh": {"profile": {"bundles": [dsh.PACKAGE_NAME]}}}), encoding="utf-8")
    assert dsh.installed(root)[0]


def test_dsh_commands_preserve_profile_boundary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(dsh, "launcher", lambda: ["dsh"])
    root = tmp_path / "Harness home/profiles/web"
    bundle = tmp_path / "bundle with spaces"
    argv, env = dsh.command(root, "install", bundle)
    assert argv == ["dsh", "plugin", "--profile", "web", "add", "file:" + bundle.resolve().as_posix()]
    assert env["DSH_HOME"] == str(root.parent.parent.resolve())
    with pytest.raises(ValueError, match="profile directory"):
        dsh.command(tmp_path / "business-data", "uninstall")


def test_project_uninstall_preserves_unrelated_modified_and_original_files(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    for name in ("owned.md", "edited.md", "original.md", "borrowed.md"):
        (source / name).write_text("skill", encoding="utf-8")
    root = tmp_path / "project"
    overlay = root / ".opencode"
    overlay.mkdir(parents=True)
    (overlay / "unrelated.md").write_text("business", encoding="utf-8")
    (overlay / "original.md").write_text("original", encoding="utf-8")
    (overlay / "borrowed.md").write_text("skill", encoding="utf-8")
    managed_files.install(root, "opencode", [(source, Path(".opencode"))], lambda _: None)
    (overlay / "edited.md").write_text("user change", encoding="utf-8")
    managed_files.uninstall(root, "opencode", lambda _: None)
    assert not (overlay / "owned.md").exists()
    assert (overlay / "unrelated.md").read_text() == "business"
    assert (overlay / "edited.md").read_text() == "user change"
    assert (overlay / "original.md").read_text() == "original"
    assert (overlay / "borrowed.md").read_text() == "skill"
    assert list(overlay.glob("original.md.bak.nimo-*"))


def test_redeploy_keeps_original_baseline_for_uninstall(tmp_path: Path) -> None:
    root, source = tmp_path / "project", tmp_path / "source.md"
    root.mkdir()
    (root / "AGENTS.md").write_text("original", encoding="utf-8")
    source.write_text("version one", encoding="utf-8")
    managed_files.install(root, "generic", [(source, Path("AGENTS.md"))], lambda _: None)
    source.write_text("version two", encoding="utf-8")
    managed_files.install(root, "generic", [(source, Path("AGENTS.md"))], lambda _: None)
    managed_files.uninstall(root, "generic", lambda _: None)
    assert (root / "AGENTS.md").read_text() == "original"
    assert len(list(root.glob("AGENTS.md.bak.nimo-*"))) == 2


def test_multiple_hosts_share_core_until_the_last_uninstall(tmp_path: Path) -> None:
    root, source = tmp_path / "project", tmp_path / "source.md"
    root.mkdir()
    (root / "shared.md").write_text("original", encoding="utf-8")
    source.write_text("shared core", encoding="utf-8")
    managed_files.install(root, "opencode", [(source, Path("shared.md"))], lambda _: None)
    managed_files.install(root, "trae", [(source, Path("shared.md"))], lambda _: None)
    managed_files.uninstall(root, "opencode", lambda _: None)
    assert (root / "shared.md").read_text() == "shared core"
    managed_files.uninstall(root, "trae", lambda _: None)
    assert (root / "shared.md").read_text() == "original"


@pytest.mark.parametrize("upgraded", ["opencode", "trae"])
@pytest.mark.parametrize("remove_upgraded_first", [True, False])
def test_shared_upgrade_keeps_remaining_host_and_restores_original_last(
    tmp_path: Path, upgraded: str, remove_upgraded_first: bool,
) -> None:
    root, source = tmp_path / "project", tmp_path / "source.md"
    root.mkdir()
    destination = root / "shared.md"
    destination.write_text("original", encoding="utf-8")
    source.write_text("version one", encoding="utf-8")
    for host in ("opencode", "trae"):
        managed_files.install(root, host, [(source, Path("shared.md"))], lambda _: None)
    source.write_text("version two", encoding="utf-8")
    managed_files.install(root, upgraded, [(source, Path("shared.md"))], lambda _: None)
    other = "trae" if upgraded == "opencode" else "opencode"
    first, last = (upgraded, other) if remove_upgraded_first else (other, upgraded)

    managed_files.uninstall(root, first, lambda _: None)

    assert destination.read_text() == "version two"
    remaining = managed_files.read_manifest(root, last)["files"]["shared.md"]
    assert managed_files.digest(destination) == remaining["sha256"]
    assert not managed_files.manifest_path(root, first).exists()
    managed_files.uninstall(root, last, lambda _: None)
    assert destination.read_text() == "original"


def test_shared_upgrade_uninstall_preserves_later_user_edits(tmp_path: Path) -> None:
    root, source = tmp_path / "project", tmp_path / "source.md"
    root.mkdir()
    destination = root / "shared.md"
    destination.write_text("original", encoding="utf-8")
    source.write_text("version one", encoding="utf-8")
    for host in ("opencode", "trae"):
        managed_files.install(root, host, [(source, Path("shared.md"))], lambda _: None)
    source.write_text("version two", encoding="utf-8")
    managed_files.install(root, "trae", [(source, Path("shared.md"))], lambda _: None)
    destination.write_text("user change", encoding="utf-8")

    for host in ("opencode", "trae"):
        managed_files.uninstall(root, host, lambda _: None)

    assert destination.read_text() == "user change"
    assert any(path.read_text() == "original" for path in root.glob("shared.md.bak.nimo-*"))


def test_legacy_uninstall_and_path_traversal_do_not_delete_files(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    (root / "AGENTS.md").write_text("business", encoding="utf-8")
    with pytest.raises(ValueError, match="ownership manifest"):
        managed_files.uninstall(root, "generic", lambda _: None)
    source = tmp_path / "source.md"
    source.write_text("skill", encoding="utf-8")
    with pytest.raises(ValueError, match="leaves the project"):
        managed_files.install(root, "generic", [(source, Path("../outside.md"))], lambda _: None)
    assert not (tmp_path / "outside.md").exists()
    assert (root / "AGENTS.md").read_text() == "business"


def test_workflow_resumes_only_verified_changed_layers() -> None:
    route = workflow.route("change", "web-complete", "analysis_allowed", "production_allowed", ("ui",), True)
    assert route["stages"] == ["12b", "13"]
    assert route["incremental"] and not route["completion_verified"]
    full = workflow.route("change", "web-complete", "analysis_allowed", "production_allowed", ("ui",), False)
    assert full["stages"] == list(workflow.ORDER)


def test_workflow_does_not_promote_missing_evidence_to_production() -> None:
    route = workflow.route("change", "web-complete", "search_required", "production_allowed", ("formula",), True)
    assert route["status"] == "evidence_required"
    assert route["stages"][:3] == ["01", "02", "03"]
    route = workflow.route(evidence_gate="analysis_allowed", coding_gate="prototype_allowed")
    assert route["status"] == "handoff_required"
    with pytest.raises(ValueError):
        workflow.route(changed_layers=("unrecognized",))
    route = workflow.route("change", "web-complete", "analysis_allowed", "no_go", ("ui",), True)
    assert route["status"] == "handoff_required"


def test_dsh_configuration_is_checked_without_logging_secrets(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(dsh, "installed", lambda root: (True, "registered"))
    monkeypatch.setattr(dsh, "command", lambda *_: (["dsh"], {}))

    def fake_run(argv, *, log, **kwargs):
        log("- id: engineering-calculation-system")
        log("apiKey: secret-must-not-appear-in-logs")
        return 0

    monkeypatch.setattr(deployer, "_run_streaming", fake_run)
    messages: list[str] = []
    assert deployer.verify_dsh(deployer.DeployContext(tmp_path, messages.append, lambda *_: None))
    assert "secret-must-not-appear-in-logs" not in "\n".join(messages)


def test_headless_catalog_and_cancel_require_no_gui_imports() -> None:
    assert "deepseek-harness" in {row["id"] for row in service.catalog()}
    # Pytest's installed Qt plugin may import Qt before collection; use a clean process.
    result = subprocess.run([sys.executable, "-c", "import sys; from installer_gui.service import catalog; catalog(); assert 'PySide6' not in sys.modules; assert 'tkinter' not in sys.modules"],
                            env={**os.environ, "PYTHONPATH": str(TOOLS)}, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    with pytest.raises(deployer.DeployError, match="cancelled"):
        service.execute("deepseek-harness", "install", None, lambda _: None, lambda *_: None, lambda: True)


def test_silent_subprocess_timeout_is_enforced() -> None:
    started = time.monotonic()
    with pytest.raises(deployer.DeployError, match="timed out"):
        deployer._run_streaming([sys.executable, "-c", "import time; time.sleep(20)"], log=lambda _: None, timeout=0.2)
    assert time.monotonic() - started < 5
