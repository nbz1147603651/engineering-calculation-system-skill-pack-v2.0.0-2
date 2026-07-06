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
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
RELEASE_CONFIG_PATH = REPO_ROOT / "engineering-calculation-system" / "tools" / "release_config.json"
SOURCE_SKILL_ROOT = REPO_ROOT / "engineering-calculation-system" / "core" / "engineering-calculation-system"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "engineering-calculation-system"
OVERLAY_ROOT = PLUGIN_ROOT / "overlays" / "engineering-calculation-system"
TODO_PATTERN = re.compile(r"\[TODO:")
HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
CODEX_PLUGIN_VERSION_RE = re.compile(
    r"^(?P<skill_version>\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\+codex\.(?P<date>\d{8})$"
)
FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
IGNORED_SYNC_NAMES = {"__pycache__"}
IGNORED_SYNC_SUFFIXES = {".pyc", ".pyo"}

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
    "docs/CODEX_QUICKSTART.md",
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
    "skills/01-reference-adequacy-and-gap-assessment.skill.md",
    "skills/02-reference-discovery-and-acquisition.skill.md",
    "skills/03-reference-persistence-and-local-library.skill.md",
    "skills/04-source-intake-and-authority.skill.md",
    "skills/05-engineering-logic-blueprint.skill.md",
    "skills/06-formula-lookup-branch-extraction.skill.md",
    "skills/07-implementation-handoff-contract.skill.md",
    "skills/08-calculation-book-architecture.skill.md",
    "skills/09-core-and-data-models.skill.md",
    "skills/10-reusable-calculation-modules.skill.md",
    "skills/11-book-runner-and-governing-summary.skill.md",
    "skills/12-report-review-batch-interfaces.skill.md",
    "skills/12a-report-context-and-rendering.skill.md",
    "skills/12b-frontend-and-review-interfaces.skill.md",
    "skills/12c-batch-import-export-packages.skill.md",
    "skills/13-verification-regression-traceability.skill.md",
    "skills/14-cloud-web-release-deployment.skill.md",
    "parent/engineering-calculation-reference-acquisition.skill.md",
    "parent/engineering-calculation-logic-architecture.skill.md",
    "parent/engineering-calculation-book.skill.md",
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
    "source-backed",
    "web-complete",
    "golden-case",
}

REQUIRED_CAPABILITIES = {
    "Lifecycle Routing",
    "Formula Verification",
    "Calculation Books",
    "Golden-Case Regression",
    "Web-Complete Delivery",
    "Codex Workspace Validation",
}

REQUIRED_PROMPT_PHRASES = {
    "route this project",
    "web-complete",
    "golden cases",
}

REQUIRED_MANIFEST_TEXT = (
    "CodeGraph-aware",
    "golden-case verification",
    "web-complete",
)

REQUIRED_CODEX_ADAPTER_PHRASES = {
    "resource root": [
        "directory containing the root `SKILL.md`",
        "Resolve `skills/`, `parent/`, `shared/`, `templates/`, `schemas/`",
    ],
    "workspace boundary": [
        "Do not write into the plugin package during normal user project work",
        "plugin package is read-only unless the user explicitly asks for plugin maintenance",
    ],
    "load order": [
        "read this adapter, then the router",
        "only the parent/child skills needed for the task",
    ],
    "Codex discovery": [
        "If a target repository has `.codegraph/`, use CodeGraph before text search",
        "Use `rg` or CodeGraph for code discovery",
    ],
    "tool limitations": [
        "Record unavailable tools as validation or acquisition limitations",
    ],
    "route card": [
        "task_type:",
        "material_state:",
        "required_skill_path:",
        "delivery_mode:",
        "gate_status:",
        "completion_evidence_category:",
    ],
    "web-complete default": [
        "Use `web-complete` by default",
        "Default to `web-complete` for online calculators",
    ],
    "runner boundary": [
        "run_book(BookInput) -> BookResult",
    ],
    "generated project validation": [
        "python scripts/verify_golden_cases.py --project-root <project-root>",
        "python -m pytest",
        "validate_artifacts.py --package-root <skill-root>",
    ],
    "reference acquisition": [
        "require current source verification",
        "Persist accepted and rejected candidates",
    ],
    "multi-agent boundary": [
        "Use Codex subagents only when the user explicitly asks",
        "Keep lifecycle routing, evidence gates, source authority",
    ],
    "completion summary": [
        "lifecycle route and gate status",
        "validation commands run and results",
    ],
}

REQUIRED_CODEX_QUICKSTART_PHRASES = [
    "skills/engineering-calculation-system/shared/codex-plugin-adapter.md",
    "skills/engineering-calculation-system/skills/00-engineering-calculation-router.skill.md",
    "rather than jumping directly into code",
    "If the target repository has `.codegraph/`, use CodeGraph",
    "python scripts/validate_plugin.py",
    "python scripts/verify_golden_cases.py --project-root .",
    "python -m pytest",
    "scripts/validate_artifacts.py --package-root . --profile core",
    "python scripts/sync_from_core.py --dry-run",
    "python scripts/sync_from_core.py --force",
]


def rel(path: Path) -> str:
    return path.relative_to(PLUGIN_ROOT).as_posix()


def has_phrase(text: str, phrase: str) -> bool:
    return " ".join(phrase.split()) in " ".join(text.split())


def in_source_checkout() -> bool:
    return (REPO_ROOT / ".git").exists() or SOURCE_SKILL_ROOT.exists() or MARKETPLACE_PATH.exists()


def read_json_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def manifest_version() -> str:
    value = read_json_object(MANIFEST_PATH).get("version")
    return value if isinstance(value, str) else ""


def release_config_value(key: str) -> str:
    value = read_json_object(RELEASE_CONFIG_PATH).get(key)
    return value if isinstance(value, str) else ""


def skill_frontmatter_version(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return ""
    version_match = re.search(r"^version:\s*(.+)$", match.group("body"), re.MULTILINE)
    return version_match.group(1).strip().strip('"').strip("'") if version_match else ""


def parse_codex_plugin_version(version: str) -> tuple[str, str]:
    match = CODEX_PLUGIN_VERSION_RE.match(version)
    if not match:
        return "", ""
    raw_date = match.group("date")
    return match.group("skill_version"), f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"


def expected_skill_version() -> str:
    config_version = release_config_value("version")
    if config_version and SEMVER_RE.match(config_version):
        return config_version
    skill_version = skill_frontmatter_version(SKILL_ROOT / "SKILL.md")
    if skill_version and SEMVER_RE.match(skill_version):
        return skill_version
    parsed_version, _created_at = parse_codex_plugin_version(manifest_version())
    return parsed_version


def expected_release_created_at() -> str:
    created_at = release_config_value("created_at")
    if created_at:
        return created_at
    _skill_version, parsed_created_at = parse_codex_plugin_version(manifest_version())
    return parsed_created_at


def expected_codex_plugin_version() -> str:
    skill_version = expected_skill_version()
    created_at = expected_release_created_at()
    if not skill_version or not created_at:
        return ""
    return f"{skill_version}+codex.{created_at.replace('-', '')}"


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


def valid_manifest_path_names() -> set[str]:
    return {PLUGIN_ROOT.name, PLUGIN_ROOT.parent.name}


def check_manifest(manifest: dict[str, Any], errors: list[str]) -> None:
    raw = json.dumps(manifest, sort_keys=True)
    if TODO_PATTERN.search(raw):
        errors.append("manifest still contains [TODO:] placeholders")

    for key in ("name", "version", "description", "license", "skills", "interface"):
        if key not in manifest:
            errors.append(f"manifest is missing required key: {key}")

    valid_path_names = valid_manifest_path_names()
    if manifest.get("name") not in valid_path_names:
        errors.append(
            "manifest name must match the plugin folder name "
            f"(accepted: {', '.join(sorted(valid_path_names))})"
        )

    version = str(manifest.get("version", ""))
    expected_version = expected_codex_plugin_version()
    if expected_version:
        if version != expected_version:
            errors.append(f"manifest version must be {expected_version}")
    elif not CODEX_PLUGIN_VERSION_RE.match(version):
        errors.append("manifest version must use <skill-version>+codex.<YYYYMMDD>")

    if manifest.get("skills") != "./skills/":
        errors.append("manifest skills path must be ./skills/")
    elif not (PLUGIN_ROOT / "skills" / "engineering-calculation-system" / "SKILL.md").exists():
        errors.append("manifest skills path does not expose engineering-calculation-system/SKILL.md")

    description = manifest.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("manifest description must be a non-empty string")
    elif "source-backed" not in description or "web-complete" not in description:
        errors.append("manifest description should advertise source-backed and web-complete delivery")

    long_description = str((manifest.get("interface") or {}).get("longDescription", ""))
    for phrase in REQUIRED_MANIFEST_TEXT:
        if phrase not in long_description:
            errors.append(f"interface.longDescription missing Codex capability phrase: {phrase!r}")

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
    else:
        missing = REQUIRED_CAPABILITIES - set(capabilities)
        if missing:
            errors.append(f"interface.capabilities missing: {', '.join(sorted(missing))}")

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
        prompt_text = "\n".join(str(prompt).lower() for prompt in prompts)
        for phrase in REQUIRED_PROMPT_PHRASES:
            if phrase not in prompt_text:
                errors.append(f"interface.defaultPrompt missing phrase: {phrase!r}")

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
    if not MARKETPLACE_PATH.exists():
        if in_source_checkout():
            errors.append(f"missing local plugin marketplace: {MARKETPLACE_PATH.relative_to(REPO_ROOT).as_posix()}")
        return
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


def check_codex_adapter_content(errors: list[str]) -> None:
    adapter_path = SKILL_ROOT / "shared" / "codex-plugin-adapter.md"
    if not adapter_path.exists():
        return
    text = adapter_path.read_text(encoding="utf-8")
    for capability, phrases in REQUIRED_CODEX_ADAPTER_PHRASES.items():
        missing = [phrase for phrase in phrases if not has_phrase(text, phrase)]
        if missing:
            errors.append(
                f"Codex adapter missing {capability} marker(s): "
                + ", ".join(repr(phrase) for phrase in missing)
            )


def check_quickstart_content(errors: list[str]) -> None:
    quickstart_path = PLUGIN_ROOT / "docs" / "CODEX_QUICKSTART.md"
    if not quickstart_path.exists():
        return
    text = quickstart_path.read_text(encoding="utf-8")
    for phrase in REQUIRED_CODEX_QUICKSTART_PHRASES:
        if not has_phrase(text, phrase):
            errors.append(f"Codex quickstart missing marker: {phrase!r}")


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


def is_ignored_sync_file(path: Path) -> bool:
    return (
        any(part in IGNORED_SYNC_NAMES for part in path.parts)
        or path.suffix in IGNORED_SYNC_SUFFIXES
    )


def sync_file_map(root: Path) -> dict[str, Path]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file() and not is_ignored_sync_file(path)
    }


def check_bundled_source_sync(errors: list[str]) -> None:
    if not SOURCE_SKILL_ROOT.exists():
        if in_source_checkout():
            errors.append(f"source skill root is missing: {SOURCE_SKILL_ROOT}")
        return
    overlay_rels = {
        path.relative_to(OVERLAY_ROOT).as_posix()
        for path in OVERLAY_ROOT.rglob("*")
        if path.is_file() and not is_ignored_sync_file(path)
    } if OVERLAY_ROOT.exists() else set()
    source_files = sync_file_map(SOURCE_SKILL_ROOT)
    bundled_files = sync_file_map(SKILL_ROOT)

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


def run_project_template_validation(errors: list[str]) -> None:
    validator = SKILL_ROOT / "scripts" / "validate_artifacts.py"
    project_root = SKILL_ROOT / "project_template" / "engineering_calc_project"
    if not validator.exists() or not project_root.exists():
        errors.append("cannot run project-template validation because validator or template is missing")
        return

    command = [
        sys.executable,
        str(validator),
        "--package-root",
        str(SKILL_ROOT),
        "--profile",
        "core",
        "--project",
        str(project_root),
        "--delivery",
        "web-complete",
    ]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    completed = subprocess.run(command, text=True, capture_output=True, env=env)
    if completed.returncode != 0:
        errors.append(
            "bundled web-complete project-template validation failed:\n"
            + completed.stdout.strip()
            + ("\n" + completed.stderr.strip() if completed.stderr.strip() else "")
        )


def run_golden_case_validation(errors: list[str]) -> None:
    project_root = SKILL_ROOT / "project_template" / "engineering_calc_project"
    runner = project_root / "scripts" / "verify_golden_cases.py"
    if not runner.exists():
        errors.append("bundled project template is missing scripts/verify_golden_cases.py")
        return
    command = [
        sys.executable,
        str(runner),
        "--project-root",
        str(project_root),
    ]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    completed = subprocess.run(command, text=True, capture_output=True, cwd=project_root, env=env)
    if completed.returncode != 0:
        errors.append(
            "bundled golden-case validation failed:\n"
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
    check_codex_adapter_content(errors)
    check_quickstart_content(errors)
    check_overlay_sync(errors)
    check_sync_script_capabilities(errors)
    check_bundled_source_sync(errors)

    if not args.skip_skill_validation:
        run_skill_validation(errors)
        run_project_template_validation(errors)
        run_golden_case_validation(errors)

    if errors:
        print("Codex plugin validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Codex plugin validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
