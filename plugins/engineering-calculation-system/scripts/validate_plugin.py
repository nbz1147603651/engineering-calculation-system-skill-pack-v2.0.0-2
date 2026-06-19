#!/usr/bin/env python3
"""Validate the Codex plugin wrapper and bundled skill pack."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "engineering-calculation-system"
TODO_PATTERN = re.compile(r"\[TODO:")
HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")

REQUIRED_PLUGIN_PATHS = [
    ".codex-plugin/plugin.json",
    "README.md",
    "skills/engineering-calculation-system/SKILL.md",
    "skills/engineering-calculation-system/shared/codex-plugin-adapter.md",
    "skills/engineering-calculation-system/scripts/validate_artifacts.py",
    "overlays/engineering-calculation-system/shared/codex-plugin-adapter.md",
    "scripts/sync_from_core.py",
    "scripts/validate_plugin.py",
]

REQUIRED_SKILL_PATHS = [
    "SKILL.md",
    "skills/00-engineering-calculation-router.skill.md",
    "shared/codex-plugin-adapter.md",
    "shared/quality-gates.md",
    "shared/multi-agent-orchestration.md",
    "templates/orchestration/parallel_work_plan.yaml",
    "templates/orchestration/agent_result_packet.yaml",
    "templates/orchestration/merge_review.md",
    "schemas/artifact_contracts.json",
    "scripts/validate_artifacts.py",
]


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


def require_path(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required path: {rel(path)}")


def check_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    raw = json.dumps(manifest, sort_keys=True)
    if TODO_PATTERN.search(raw):
        errors.append("manifest still contains [TODO:] placeholders")

    expected_name = PLUGIN_ROOT.name
    if manifest.get("name") != expected_name:
        errors.append(f"manifest name must match folder name {expected_name!r}")

    if manifest.get("version") != "2.4.0":
        errors.append("manifest version must match bundled skill schema 2.4.0")

    if manifest.get("skills") != "./skills/":
        errors.append("manifest skills path must be ./skills/")

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
    completed = subprocess.run(command, text=True, capture_output=True)
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
    check_skill_frontmatter(errors)

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

