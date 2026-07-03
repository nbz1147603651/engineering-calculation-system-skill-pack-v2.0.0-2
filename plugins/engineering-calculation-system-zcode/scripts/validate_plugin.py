#!/usr/bin/env python3
"""Validate the ZCode plugin wrapper and bundled skill pack."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
TOOLS_ROOT = REPO_ROOT / "engineering-calculation-system" / "tools"
sys.path.insert(0, str(TOOLS_ROOT))

from versioning import release_created_at, release_version, zcode_plugin_version

MANIFEST_PATH = PLUGIN_ROOT / ".zcode-plugin" / "plugin.json"
MARKETPLACE_PATH = PLUGIN_ROOT / "marketplace.json"
RELEASE_CONFIG_PATH = REPO_ROOT / "engineering-calculation-system" / "tools" / "release_config.json"
INSTALLER_GUI_ROOT = REPO_ROOT / "engineering-calculation-system" / "tools" / "installer_gui"
SOURCE_SKILL_ROOT = REPO_ROOT / "engineering-calculation-system" / "core" / "engineering-calculation-system"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "engineering-calculation-system"
OVERLAY_ROOT = PLUGIN_ROOT / "overlays" / "engineering-calculation-system"
TODO_PATTERN = re.compile(r"\[TODO:")
HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")
EXPECTED_SKILL_VERSION = release_version()
EXPECTED_PLUGIN_VERSION = zcode_plugin_version(EXPECTED_SKILL_VERSION, release_created_at())
ZCODE_PROFILE = "zcode-plugin"
ZCODE_PLUGIN_NAME = PLUGIN_ROOT.name
ZCODE_SKILL_ROOT = "skills/engineering-calculation-system"
ZCODE_SKILL_ENTRYPOINT = f"{ZCODE_SKILL_ROOT}/SKILL.md"
ZCODE_ADAPTER_REL = "shared/zcode-plugin-adapter.md"
ZCODE_BUNDLED_ADAPTER = f"{ZCODE_SKILL_ROOT}/{ZCODE_ADAPTER_REL}"
ZCODE_LAYERED_ENTRYPOINTS = {
    "engineering-calculation-reference-acquisition": "parent/engineering-calculation-reference-acquisition.skill.md",
    "engineering-calculation-logic-architecture": "parent/engineering-calculation-logic-architecture.skill.md",
    "engineering-calculation-book-delivery": "parent/engineering-calculation-book.skill.md",
}

ZCODE_BLOCK = """## ZCode Plugin Adapter

When this package is loaded from the ZCode plugin, read
`shared/zcode-plugin-adapter.md` before the router. The adapter maps this
platform-neutral skill pack onto ZCode plugin discovery, workspace context,
file references, Goal Mode, review flow, and user-facing completion rules.

"""

REQUIRED_PLUGIN_PATHS = [
    ".zcode-plugin/plugin.json",
    "marketplace.json",
    "README.md",
    "docs/ADAPTATION.md",
    ZCODE_SKILL_ENTRYPOINT,
    ZCODE_BUNDLED_ADAPTER,
    "skills/engineering-calculation-reference-acquisition/SKILL.md",
    "skills/engineering-calculation-logic-architecture/SKILL.md",
    "skills/engineering-calculation-book-delivery/SKILL.md",
    f"{ZCODE_SKILL_ROOT}/shared/execution-discipline.md",
    f"{ZCODE_SKILL_ROOT}/shared/planning-discipline.md",
    f"{ZCODE_SKILL_ROOT}/shared/review-feedback-discipline.md",
    f"{ZCODE_SKILL_ROOT}/shared/version-control-discipline.md",
    f"{ZCODE_SKILL_ROOT}/shared/completion-evidence.md",
    f"{ZCODE_SKILL_ROOT}/shared/systematic-debugging.md",
    f"{ZCODE_SKILL_ROOT}/scripts/validate_artifacts.py",
    f"{ZCODE_SKILL_ROOT}/scripts/ecs_execution.py",
    "overlays/engineering-calculation-system/shared/zcode-plugin-adapter.md",
    "scripts/sync_from_core.py",
    "scripts/validate_plugin.py",
]

REQUIRED_SKILL_PATHS = [
    "SKILL.md",
    "skills/00-engineering-calculation-router.skill.md",
    ZCODE_ADAPTER_REL,
    "shared/lifecycle.md",
    "shared/execution-discipline.md",
    "shared/planning-discipline.md",
    "shared/review-feedback-discipline.md",
    "shared/version-control-discipline.md",
    "shared/completion-evidence.md",
    "shared/systematic-debugging.md",
    "shared/quality-gates.md",
    "shared/delivery-contract.md",
    "shared/lifecycle-matrix.md",
    "shared/multi-agent-orchestration.md",
    "templates/orchestration/parallel_work_plan.yaml",
    "templates/orchestration/agent_result_packet.yaml",
    "templates/orchestration/merge_review.md",
    "templates/orchestration/task_brief.md",
    "templates/orchestration/task_review.md",
    "templates/orchestration/progress_ledger.md",
    "templates/verification/root_cause_trace.md",
    "schemas/artifact_contracts.json",
    "scripts/validate_artifacts.py",
    "scripts/ecs_execution.py",
]

REQUIRED_INTERFACE_STRINGS = [
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
]

REQUIRED_KEYWORDS = {
    "zcode",
    "zcode-plugin",
    "engineering-calculation",
}


def rel(path: Path) -> str:
    return path.relative_to(PLUGIN_ROOT).as_posix()


def display_path(path: Path) -> str:
    try:
        return path.relative_to(PLUGIN_ROOT).as_posix()
    except ValueError:
        try:
            return path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return str(path)


def load_json(path: Path, errors: list[str], context: str) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"missing {context}: {display_path(path)}")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid {context} JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{context} must be a JSON object")
        return {}
    return data


def require_path(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required path: {rel(path)}")


def require_phrases(text: str, phrases: Sequence[str], errors: list[str], context: str) -> None:
    for phrase in phrases:
        if phrase not in text:
            errors.append(f"{context} missing marker: {phrase}")


def require_file_phrases(path: Path, phrases: Sequence[str], errors: list[str], context: str) -> None:
    if not path.exists():
        errors.append(f"missing {context}: {display_path(path)}")
        return
    require_phrases(path.read_text(encoding="utf-8"), phrases, errors, context)


def check_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    raw = json.dumps(manifest, sort_keys=True)
    if TODO_PATTERN.search(raw):
        errors.append("manifest still contains [TODO:] placeholders")

    for key in ("name", "version", "description", "license", "skills", "interface"):
        if key not in manifest:
            errors.append(f"manifest is missing required key: {key}")

    if manifest.get("name") != ZCODE_PLUGIN_NAME:
        errors.append(f"manifest name must match folder name {ZCODE_PLUGIN_NAME!r}")

    version = str(manifest.get("version", ""))
    if version != EXPECTED_PLUGIN_VERSION:
        errors.append(f"manifest version must be {EXPECTED_PLUGIN_VERSION}")

    if manifest.get("skills") != "skills":
        errors.append('manifest skills component must be "skills" for ZCode plugin discovery')
    elif not (PLUGIN_ROOT / Path(ZCODE_SKILL_ENTRYPOINT)).exists():
        errors.append("manifest skills component does not expose engineering-calculation-system/SKILL.md")

    description = manifest.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("manifest description must be a non-empty string")

    keywords = manifest.get("keywords")
    if not isinstance(keywords, list) or not all(isinstance(item, str) and item for item in keywords):
        errors.append("manifest keywords must be a non-empty string list")
    elif missing := REQUIRED_KEYWORDS - set(keywords):
        errors.append(f"manifest keywords must include: {', '.join(sorted(missing))}")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("manifest interface must be an object")
        return

    for key in REQUIRED_INTERFACE_STRINGS:
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"interface.{key} must be a non-empty string")

    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append("interface.capabilities must be a non-empty string list")
    elif not all(isinstance(item, str) and item.strip() for item in capabilities):
        errors.append("interface.capabilities must contain only non-empty strings")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not prompts:
        errors.append("interface.defaultPrompt must contain 1-3 prompts")
    elif len(prompts) > 3:
        errors.append("interface.defaultPrompt must contain at most 3 prompts")
    else:
        for index, prompt in enumerate(prompts, start=1):
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"defaultPrompt[{index}] must be a non-empty string")
            elif len(prompt) > 128:
                errors.append(f"defaultPrompt[{index}] exceeds 128 characters")

    brand_color = interface.get("brandColor")
    if not isinstance(brand_color, str) or not HEX_COLOR_PATTERN.match(brand_color):
        errors.append("interface.brandColor must be a #RRGGBB color")

    screenshots = interface.get("screenshots")
    if screenshots is None:
        errors.append("interface.screenshots must be present; use [] when no screenshots ship")
    elif not isinstance(screenshots, list):
        errors.append("interface.screenshots must be a list")

    zcode = manifest.get("zcode")
    if not isinstance(zcode, dict):
        errors.append("manifest zcode extension must be an object")
        return
    if zcode.get("entrypoint") != ZCODE_SKILL_ENTRYPOINT:
        errors.append("manifest zcode.entrypoint must point to the bundled skill entrypoint")
    if zcode.get("skillName") != "engineering-calculation-system":
        errors.append("manifest zcode.skillName must be engineering-calculation-system")


def check_marketplace(errors: list[str]) -> None:
    marketplace = load_json(MARKETPLACE_PATH, errors, "ZCode marketplace")
    if not marketplace:
        return
    if marketplace.get("name") != f"{ZCODE_PLUGIN_NAME}-marketplace":
        errors.append(f"ZCode marketplace name must be {ZCODE_PLUGIN_NAME}-marketplace")
    if marketplace.get("version") != 1:
        errors.append("ZCode marketplace version must be 1")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        errors.append("ZCode marketplace must contain a plugins list")
        return
    matches = [entry for entry in plugins if isinstance(entry, dict) and entry.get("name") == ZCODE_PLUGIN_NAME]
    if len(matches) != 1:
        errors.append(f"ZCode marketplace must contain exactly one {ZCODE_PLUGIN_NAME!r} entry")
        return
    entry = matches[0]
    if entry.get("source") != ".":
        errors.append("ZCode marketplace entry source must be .")
    if entry.get("category") != "development":
        errors.append("ZCode marketplace entry category must be development")
    if entry.get("version") != EXPECTED_PLUGIN_VERSION:
        errors.append(f"ZCode marketplace plugin version must be {EXPECTED_PLUGIN_VERSION}")


def check_skill_frontmatter(errors: list[str]) -> None:
    skill_path = SKILL_ROOT / "SKILL.md"
    if not skill_path.exists():
        return
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append("bundled SKILL.md is missing YAML frontmatter")
    if "name: engineering-calculation-system" not in text:
        errors.append("bundled SKILL.md frontmatter name is missing or changed")
    if ZCODE_ADAPTER_REL not in text:
        errors.append(f"bundled SKILL.md must load {ZCODE_ADAPTER_REL}")
    adapter_index = text.find("## ZCode Plugin Adapter")
    router_index = text.find("skills/00-engineering-calculation-router.skill.md")
    if adapter_index < 0:
        errors.append("bundled SKILL.md is missing the ZCode Plugin Adapter section")
    elif router_index >= 0 and adapter_index > router_index:
        errors.append("bundled SKILL.md must load the ZCode adapter before the router")

    for name, canonical_parent in ZCODE_LAYERED_ENTRYPOINTS.items():
        wrapper_path = PLUGIN_ROOT / "skills" / name / "SKILL.md"
        if not wrapper_path.exists():
            errors.append(f"missing layered ZCode skill entrypoint: skills/{name}/SKILL.md")
            continue
        wrapper_text = wrapper_path.read_text(encoding="utf-8")
        if not wrapper_text.startswith("---"):
            errors.append(f"layered ZCode skill {name} is missing YAML frontmatter")
        if f"name: {name}" not in wrapper_text:
            errors.append(f"layered ZCode skill {name} frontmatter name is missing or changed")
        require_phrases(
            wrapper_text,
            [
                "../engineering-calculation-system/SKILL.md",
                f"../engineering-calculation-system/{canonical_parent}",
            ],
            errors,
            f"layered ZCode skill {name}",
        )


def check_overlay_sync(errors: list[str]) -> None:
    if not OVERLAY_ROOT.exists():
        errors.append(f"missing overlay root: {rel(OVERLAY_ROOT)}")
        return
    for overlay_path in sorted(path for path in OVERLAY_ROOT.rglob("*") if path.is_file()):
        overlay_rel = overlay_path.relative_to(OVERLAY_ROOT)
        bundled_path = SKILL_ROOT / overlay_rel
        if not bundled_path.exists():
            errors.append(f"overlay file is not present in bundled skill: {overlay_rel.as_posix()}")
            continue
        if overlay_path.read_bytes() != bundled_path.read_bytes():
            errors.append(f"overlay file is out of sync in bundled skill: {overlay_rel.as_posix()}")


def check_sync_script_capabilities(errors: list[str]) -> None:
    script_path = PLUGIN_ROOT / "scripts" / "sync_from_core.py"
    if not script_path.exists():
        return
    require_file_phrases(
        script_path,
        ("--dry-run", "--force", "compare_trees", "check_dirty_destination"),
        errors,
        "sync_from_core.py",
    )


def check_gui_deployment_support(errors: list[str]) -> None:
    release_config = load_json(RELEASE_CONFIG_PATH, errors, "release config")
    if release_config:
        profiles = release_config.get("profiles")
        if not isinstance(profiles, list) or ZCODE_PROFILE not in profiles:
            errors.append(f"release_config.json must include the {ZCODE_PROFILE} profile")

        targets = release_config.get("classified_targets")
        if not isinstance(targets, list):
            errors.append("release_config.json must contain classified_targets")
        else:
            matches = [target for target in targets if isinstance(target, dict) and target.get("name") == "ZCode"]
            if len(matches) != 1:
                errors.append("release_config.json must contain exactly one ZCode target")
            else:
                target = matches[0]
                if target.get("path") != "ZCode/engineering-calculation-system-zcode":
                    errors.append("ZCode release target path must install the plugin folder")
                if target.get("include_core") is not False:
                    errors.append("ZCode release target must not stage the bare core skill as include_core")
                copies = target.get("copies")
                if not isinstance(copies, list) or not any(
                    isinstance(copy, dict)
                    and copy.get("profile") == ZCODE_PROFILE
                    and copy.get("source") == ZCODE_PLUGIN_NAME
                    for copy in copies
                ):
                    errors.append(f"ZCode release target must copy from the {ZCODE_PROFILE} profile")

    installer_checks = {
        "deployer.py": [
            "DIST_ZCODE_PLUGIN",
            f"ensure_profiles((\"{ZCODE_PROFILE}\",)",
            "_copy_tree(DIST_ZCODE_PLUGIN",
        ],
        "agents.py": [
            ".zcode",
            "plugins",
            ZCODE_PLUGIN_NAME,
            f"needs_profiles=(\"{ZCODE_PROFILE}\",)",
        ],
        "detector.py": [
            "marketplace.json",
            ".zcode-plugin",
            "skills",
            "engineering-calculation-system",
            "sentinels found:",
        ],
    }
    for filename, phrases in installer_checks.items():
        path = INSTALLER_GUI_ROOT / filename
        if not path.exists():
            errors.append(f"installer GUI file missing: {path.relative_to(REPO_ROOT).as_posix()}")
            continue
        require_file_phrases(path, phrases, errors, f"installer GUI {filename}")


def check_bundled_source_sync(errors: list[str]) -> None:
    if not SOURCE_SKILL_ROOT.exists():
        errors.append(f"source skill root is missing: {SOURCE_SKILL_ROOT}")
        return
    overlay_rels = {
        path.relative_to(OVERLAY_ROOT).as_posix()
        for path in OVERLAY_ROOT.rglob("*")
        if path.is_file()
    } if OVERLAY_ROOT.exists() else set()
    source_files = {
        path.relative_to(SOURCE_SKILL_ROOT).as_posix(): path
        for path in SOURCE_SKILL_ROOT.rglob("*")
        if path.is_file()
    }
    bundled_files = {
        path.relative_to(SKILL_ROOT).as_posix(): path
        for path in SKILL_ROOT.rglob("*")
        if path.is_file()
    } if SKILL_ROOT.exists() else {}

    for rel_path, source_path in sorted(source_files.items()):
        if rel_path in overlay_rels:
            continue
        bundled_path = SKILL_ROOT / rel_path
        if not bundled_path.exists():
            errors.append(f"bundled skill is missing source file: {rel_path}")
            continue
        if rel_path == "SKILL.md":
            bundled_text = bundled_path.read_text(encoding="utf-8").replace(ZCODE_BLOCK, "")
            source_text = source_path.read_text(encoding="utf-8")
            if bundled_text != source_text:
                errors.append("bundled SKILL.md is not synchronized with source SKILL.md plus ZCode block")
        elif bundled_path.read_bytes() != source_path.read_bytes():
            errors.append(f"bundled skill file is not synchronized with source: {rel_path}")

    for rel_path in sorted(set(bundled_files) - set(source_files) - overlay_rels):
        errors.append(f"bundled skill contains non-overlay extra file: {rel_path}")


def run_skill_validation(errors: list[str]) -> None:
    validator = SKILL_ROOT / "scripts" / "validate_artifacts.py"
    if not validator.exists():
        errors.append("cannot run skill validation because validate_artifacts.py is missing")
        return

    command = [
        sys.executable,
        str(validator),
        "--package-root",
        str(SKILL_ROOT),
        "--profile",
        "core",
    ]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    completed = subprocess.run(command, text=True, capture_output=True, env=env)
    if completed.returncode != 0:
        errors.append(
            "bundled skill validation failed:\n"
            + completed.stdout.strip()
            + ("\n" + completed.stderr.strip() if completed.stderr.strip() else "")
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-skill-validation",
        action="store_true",
        help="Only validate plugin structure and manifest.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    for required in REQUIRED_PLUGIN_PATHS:
        require_path(PLUGIN_ROOT / required, errors)
    for required in REQUIRED_SKILL_PATHS:
        require_path(SKILL_ROOT / required, errors)

    manifest = load_json(MANIFEST_PATH, errors, "ZCode plugin manifest")
    if manifest:
        check_manifest(manifest, errors)
    check_marketplace(errors)
    check_skill_frontmatter(errors)
    check_overlay_sync(errors)
    check_sync_script_capabilities(errors)
    check_gui_deployment_support(errors)
    check_bundled_source_sync(errors)

    if not args.skip_skill_validation:
        run_skill_validation(errors)

    if errors:
        print("ZCode plugin validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("ZCode plugin validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
