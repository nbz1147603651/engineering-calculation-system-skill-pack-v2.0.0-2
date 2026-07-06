from __future__ import annotations

import json
import sys
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = WORKSPACE_ROOT / "engineering-calculation-system"
TOOLS_ROOT = PACKAGE_ROOT / "tools"
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from installer_gui import agents, detector  # noqa: E402
from installer_gui.platform_contracts import CONTRACTS, CORE_FORBIDDEN_PATH_PARTS  # noqa: E402


def _touch(root: Path, relative: str) -> Path:
    path = root / Path(relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("sentinel\n", encoding="utf-8")
    return path


def test_agent_specs_reuse_platform_contracts() -> None:
    specs = agents.rebuild_specs()

    assert [spec.name for spec in specs] == [contract.name for contract in CONTRACTS]
    for spec, contract in zip(specs, CONTRACTS):
        assert spec.icon == contract.icon
        assert spec.kind == contract.kind
        assert spec.default_root_fn is contract.default_root_fn
        assert spec.needs_profiles == contract.needs_profiles


def test_codex_contract_targets_plugin_not_legacy_skill() -> None:
    codex = next(contract for contract in CONTRACTS if contract.name == "codex")

    assert codex.needs_profiles == ("codex-plugin",)
    assert codex.sentinel_mode == "all"
    assert ".codex-plugin/plugin.json" in codex.sentinel_paths
    assert "skills/engineering-calculation-system/SKILL.md" in codex.sentinel_paths
    assert "SKILL.md" not in codex.sentinel_paths


def test_detector_sentinel_modes_follow_contracts(tmp_path: Path) -> None:
    for contract in CONTRACTS:
        root = tmp_path / contract.name
        ok, _detail = detector.skill_deployed(contract.name, root)
        assert not ok

        if contract.sentinel_mode == "all":
            for relative in contract.sentinel_paths[:-1]:
                _touch(root, relative)
            ok, _detail = detector.skill_deployed(contract.name, root)
            assert not ok
            _touch(root, contract.sentinel_paths[-1])
        else:
            _touch(root, contract.sentinel_paths[0])

        ok, detail = detector.skill_deployed(contract.name, root)
        assert ok, detail


def test_contract_profiles_are_declared_in_release_config() -> None:
    config = json.loads((TOOLS_ROOT / "release_config.json").read_text(encoding="utf-8"))
    declared = set(config["profiles"])
    referenced = {profile for contract in CONTRACTS for profile in contract.needs_profiles}
    referenced.update(
        copy.profile
        for contract in CONTRACTS
        if contract.project_overlay is not None
        for copy in contract.project_overlay.copies
    )

    assert referenced <= declared


def test_project_contracts_declare_overlay_boundaries() -> None:
    for contract in CONTRACTS:
        if contract.kind != "project":
            continue
        assert contract.project_overlay is not None
        assert contract.project_overlay.copies
        assert contract.project_overlay.uninstall_paths
        copy_profiles = {copy.profile for copy in contract.project_overlay.copies}
        assert copy_profiles <= set(contract.needs_profiles)
        if contract.project_overlay.include_core:
            assert "core" in contract.needs_profiles


def test_core_source_keeps_platform_install_markers_out() -> None:
    core_root = PACKAGE_ROOT / "core" / "engineering-calculation-system"
    offenders = []
    for path in core_root.rglob("*"):
        rel = path.relative_to(core_root)
        if any(part in CORE_FORBIDDEN_PATH_PARTS for part in rel.parts):
            offenders.append(rel.as_posix())

    assert offenders == []


def test_adapter_sources_keep_platform_markers_scoped() -> None:
    rules = {
        PACKAGE_ROOT / "adapter_sources" / "light": {
            ".lingma",
            ".qoder",
            ".qodercn",
            ".qoder-plugin",
            ".zcode-plugin",
            "marketplace.json",
            "qoder.md",
        },
        PACKAGE_ROOT / "adapter_sources" / "qoder": {
            ".agents",
            ".lingma",
            ".opencode",
            ".qodercn",
            ".qoder-plugin",
            ".trae",
            ".zcode-plugin",
            "marketplace.json",
            "qoder.md",
        },
    }

    offenders = []
    for root, forbidden in rules.items():
        for path in root.rglob("*"):
            rel = path.relative_to(root)
            if any(part in forbidden for part in rel.parts):
                offenders.append(f"{root.name}/{rel.as_posix()}")

    assert offenders == []
