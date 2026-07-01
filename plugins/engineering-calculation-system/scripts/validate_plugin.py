#!/usr/bin/env python3
"""Validate the Codex plugin wrapper and bundled skill pack."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parents[1]
TOOLS_ROOT = REPO_ROOT / "engineering-calculation-system" / "tools"
sys.path.insert(0, str(TOOLS_ROOT))

from versioning import codex_plugin_version, release_created_at, release_version

MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
SOURCE_SKILL_ROOT = REPO_ROOT / "engineering-calculation-system" / "core" / "engineering-calculation-system"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "engineering-calculation-system"
OVERLAY_ROOT = PLUGIN_ROOT / "overlays" / "engineering-calculation-system"
TODO_PATTERN = re.compile(r"\[TODO:")
HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")
EXPECTED_SKILL_VERSION = release_version()
EXPECTED_PLUGIN_VERSION = codex_plugin_version(EXPECTED_SKILL_VERSION, release_created_at())

CODEX_BLOCK = """## Codex Plugin Adapter

When this package is loaded from the Codex plugin, read
`shared/codex-plugin-adapter.md` before the router. The adapter maps this
platform-neutral skill pack onto Codex tool use, workspace edits, validation,
multi-agent boundaries, and user-facing completion rules.

"""

REQUIRED_PLUGIN_PATHS = [
    ".codex-plugin/plugin.json",
    "README.md",
    "skills/engineering-calculation-system/SKILL.md",
    "skills/engineering-calculation-system/shared/codex-plugin-adapter.md",
    "skills/engineering-calculation-system/shared/execution-discipline.md",
    "skills/engineering-calculation-system/shared/planning-discipline.md",
    "skills/engineering-calculation-system/shared/review-feedback-discipline.md",
    "skills/engineering-calculation-system/shared/version-control-discipline.md",
    "skills/engineering-calculation-system/shared/completion-evidence.md",
    "skills/engineering-calculation-system/shared/systematic-debugging.md",
    "skills/engineering-calculation-system/scripts/validate_artifacts.py",
    "skills/engineering-calculation-system/scripts/ecs_execution.py",
    "overlays/engineering-calculation-system/shared/codex-plugin-adapter.md",
    "scripts/sync_from_core.py",
    "scripts/validate_plugin.py",
]

REQUIRED_SKILL_PATHS = [
    "SKILL.md",
    "skills/00-engineering-calculation-router.skill.md",
    "shared/codex-plugin-adapter.md",
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
    "codex",
    "codex-plugin",
    "engineering-calculation",
}


def rel(path: Path) -> str:
    return path.relative_to(PLUGIN_ROOT).as_posix()


def load_manifest(errors: list[str]) -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        errors.append(f"missing manifest: {rel(MANIFEST_PATH)}")
        return {}
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid manifest JSON: {exc}")
        return {}


def load_json(path: Path, errors: list[str], context: str) -> dict[str, Any]:
    if not path.exists():
        errors.append(f"missing {context}: {path.relative_to(REPO_ROOT).as_posix()}")
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


def check_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    raw = json.dumps(manifest, sort_keys=True)
    if TODO_PATTERN.search(raw):
        errors.append("manifest still contains [TODO:] placeholders")

    for key in ("name", "version", "description", "license", "skills", "interface"):
        if key not in manifest:
            errors.append(f"manifest is missing required key: {key}")

    expected_name = PLUGIN_ROOT.name
    if manifest.get("name") != expected_name:
        errors.append(f"manifest name must match folder name {expected_name!r}")

    version = str(manifest.get("version", ""))
    if version != EXPECTED_PLUGIN_VERSION:
        errors.append(f"manifest version must be {EXPECTED_PLUGIN_VERSION}")

    if manifest.get("skills") != "./skills/":
        errors.append("manifest skills path must be ./skills/")
    elif not (PLUGIN_ROOT / "skills" / "engineering-calculation-system" / "SKILL.md").exists():
        errors.append("manifest skills path does not expose engineering-calculation-system/SKILL.md")

    description = manifest.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("manifest description must be a non-empty string")

    keywords = manifest.get("keywords")
    if not isinstance(keywords, list) or not all(isinstance(item, str) and item for item in keywords):
        errors.append("manifest keywords must be a non-empty string list")
    elif missing := REQUIRED_KEYWORDS - set(keywords):
        errors.append(f"manifest keywords must include: {', '.join(sorted(missing))}")

    for optional_key in ("hooks", "mcpServers", "apps"):
        value = manifest.get(optional_key)
        if isinstance(value, str):
            candidate = PLUGIN_ROOT / value.removeprefix("./")
            if not candidate.exists():
                errors.append(f"manifest {optional_key} points to missing path {value!r}")

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
    else:
        for screenshot in screenshots:
            if not isinstance(screenshot, str) or not screenshot.strip():
                errors.append("interface.screenshots entries must be non-empty strings")
                continue
            if re.match(r"^https?://", screenshot):
                continue
            candidate = PLUGIN_ROOT / screenshot.removeprefix("./")
            if not candidate.exists():
                errors.append(f"interface.screenshots points to missing path {screenshot!r}")


def check_marketplace(errors: list[str]) -> None:
    marketplace = load_json(MARKETPLACE_PATH, errors, "local plugin marketplace")
    if not marketplace:
        return
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        errors.append("local plugin marketplace must contain a plugins list")
        return
    matches = [entry for entry in plugins if isinstance(entry, dict) and entry.get("name") == PLUGIN_ROOT.name]
    if len(matches) != 1:
        errors.append(f"local plugin marketplace must contain exactly one {PLUGIN_ROOT.name!r} entry")
        return

    entry = matches[0]
    source = entry.get("source")
    if not isinstance(source, dict):
        errors.append("marketplace entry source must be an object")
        return
    if source.get("source") != "local":
        errors.append("marketplace entry must use local source")
    source_path = source.get("path")
    if not isinstance(source_path, str) or not source_path.strip():
        errors.append("marketplace entry source.path must be a non-empty string")
    else:
        resolved = (REPO_ROOT / source_path).resolve()
        if resolved != PLUGIN_ROOT.resolve():
            errors.append(f"marketplace entry source.path must resolve to {PLUGIN_ROOT}")

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append("marketplace entry policy must be an object")
    else:
        if policy.get("installation") != "AVAILABLE":
            errors.append("marketplace policy.installation must be AVAILABLE")
        if policy.get("authentication") != "ON_INSTALL":
            errors.append("marketplace policy.authentication must be ON_INSTALL")

    category = entry.get("category")
    if category != "Developer Tools":
        errors.append("marketplace entry category must be Developer Tools")


def check_skill_frontmatter(errors: list[str]) -> None:
    skill_path = SKILL_ROOT / "SKILL.md"
    if not skill_path.exists():
        return
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append("bundled SKILL.md is missing YAML frontmatter")
    if "name: engineering-calculation-system" not in text:
        errors.append("bundled SKILL.md frontmatter name is missing or changed")
    if "shared/codex-plugin-adapter.md" not in text:
        errors.append("bundled SKILL.md must load shared/codex-plugin-adapter.md")
    adapter_index = text.find("## Codex Plugin Adapter")
    router_index = text.find("skills/00-engineering-calculation-router.skill.md")
    if adapter_index < 0:
        errors.append("bundled SKILL.md is missing the Codex Plugin Adapter section")
    elif router_index >= 0 and adapter_index > router_index:
        errors.append("bundled SKILL.md must load the Codex adapter before the router")


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
    text = script_path.read_text(encoding="utf-8")
    for phrase in ("--dry-run", "--force", "compare_trees", "check_dirty_destination"):
        if phrase not in text:
            errors.append(f"sync_from_core.py missing capability marker: {phrase}")


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
            bundled_text = bundled_path.read_text(encoding="utf-8").replace(CODEX_BLOCK, "")
            source_text = source_path.read_text(encoding="utf-8")
            if bundled_text != source_text:
                errors.append("bundled SKILL.md is not synchronized with source SKILL.md plus Codex block")
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

    manifest = load_manifest(errors)
    if manifest:
        check_manifest(manifest, errors)
    check_marketplace(errors)
    check_skill_frontmatter(errors)
    check_overlay_sync(errors)
    check_sync_script_capabilities(errors)
    check_bundled_source_sync(errors)

    if not args.skip_skill_validation:
        run_skill_validation(errors)

    if errors:
        print("Codex plugin validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Codex plugin validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
