#!/usr/bin/env python3
"""Validate the engineering calculation skill pack and generated project artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
YAML_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):")

PROFILE_CHOICES = {"core", "adapters-light", "qoder-addon", "singlefile"}
CORE_FORBIDDEN_ROOT_PATHS = {
    "AGENTS.md",
    "README.md",
    "README.zh-CN.md",
    "INSTALL.md",
    "CHANGELOG.md",
    "MIGRATION_NOTES.md",
    "SKILL_PACKAGE_SUMMARY.md",
    "MANIFEST.yaml",
    "CHECKSUMS.txt",
    "TREE.md",
    "engineering-calculation-system.all-in-one.md",
    ".agents",
    ".opencode",
    ".qoder",
    ".trae",
    "adapters",
    "examples",
    "workflow_diagrams",
    "original_sources",
}
FORBIDDEN_CACHE_NAMES = {".pytest_cache", "__pycache__"}
FORBIDDEN_CACHE_SUFFIXES = {".pyc", ".pyo"}
SINGLEFILE_ALLOWED_FILES = {
    "engineering-calculation-system.all-in-one.md",
    "MANIFEST.yaml",
    "CHECKSUMS.txt",
    "TREE.md",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_contract(package_root: Path) -> dict:
    path = package_root / "schemas" / "artifact_contracts.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_exists(root: Path, rel_path: str, errors: list[str]) -> None:
    if not (root / rel_path).exists():
        errors.append(f"missing required path: {rel_path}")


def check_absent(root: Path, rel_path: str, errors: list[str]) -> None:
    if (root / rel_path).exists():
        errors.append(f"forbidden path present: {rel_path}")


def check_no_cache_artifacts(root: Path, errors: list[str]) -> None:
    try:
        paths = list(root.rglob("*"))
    except OSError as exc:
        errors.append(f"could not scan package for forbidden cache artifacts: {exc}")
        return

    for path in paths:
        rel = path.relative_to(root).as_posix()
        if path.name in FORBIDDEN_CACHE_NAMES or path.suffix in FORBIDDEN_CACHE_SUFFIXES:
            errors.append(f"forbidden cache artifact present: {rel}")


def first_csv_line(path: Path) -> str:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        row = next(reader, [])
    return ",".join(row)


def check_csv_headers(root: Path, headers: dict[str, str], errors: list[str]) -> None:
    for rel_path, expected in headers.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing CSV template: {rel_path}")
            continue
        actual = first_csv_line(path)
        if actual != expected:
            errors.append(f"CSV header mismatch in {rel_path}: expected {expected!r}, got {actual!r}")


def simple_yaml_top_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for line in text.splitlines():
        match = YAML_KEY_RE.match(line)
        if match:
            keys.add(match.group(1))
    return keys


def check_yaml_required_keys(root: Path, required: dict[str, list[str]], errors: list[str]) -> None:
    for rel_path, keys in required.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing YAML template: {rel_path}")
            continue
        present = simple_yaml_top_keys(read_text(path))
        for key in keys:
            if key not in present:
                errors.append(f"missing top-level key {key!r} in {rel_path}")


def check_text_required_phrases(root: Path, required: dict[str, list[str]], errors: list[str]) -> None:
    for rel_path, phrases in required.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing text artifact: {rel_path}")
            continue
        text = read_text(path)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"missing required phrase {phrase!r} in {rel_path}")


def check_static_html_delivery_guard(project_root: Path, errors: list[str]) -> None:
    """Catch static HTML/report-only projects before they are called web apps."""
    html_files = [
        path for path in project_root.rglob("*.html")
        if ".pytest_cache" not in path.parts and "__pycache__" not in path.parts
    ]
    if not html_files:
        return

    runtime_paths = [
        "webapp/app.py",
        "webapp/routes.py",
        "webapp/form_utils.py",
        "src/pkg/books/book_name/book_runner.py",
        "tests/smoke/test_web_routes.py",
    ]
    missing = [rel_path for rel_path in runtime_paths if not (project_root / rel_path).exists()]
    if missing:
        errors.append(
            "static HTML/report HTML alone is not a production-ready web calculation "
            f"system; missing runtime artifacts: {', '.join(missing)}"
        )


def check_skill_frontmatter(root: Path, rel_path: str, errors: list[str]) -> None:
    path = root / rel_path
    if not path.exists():
        errors.append(f"missing skill file: {rel_path}")
        return
    text = read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"missing YAML frontmatter in {rel_path}")
        return
    body = match.group("body")
    if not re.search(r"^name:\s*\S+", body, re.MULTILINE):
        errors.append(f"missing frontmatter name in {rel_path}")
    if not re.search(r"^description:\s*.+", body, re.MULTILINE):
        errors.append(f"missing frontmatter description in {rel_path}")


def validate_package(package_root: Path, contract: dict) -> list[str]:
    errors: list[str] = []
    for rel_path in contract["package_required_paths"]:
        check_exists(package_root, rel_path, errors)
    for rel_path in contract["skill_files"]:
        check_skill_frontmatter(package_root, rel_path, errors)
    check_csv_headers(package_root, contract["csv_headers"], errors)
    check_yaml_required_keys(package_root, contract["yaml_required_keys"], errors)
    check_text_required_phrases(package_root, contract.get("text_required_phrases", {}), errors)
    return errors


def validate_core_profile(package_root: Path, contract: dict) -> list[str]:
    errors = validate_package(package_root, contract)
    for rel_path in sorted(CORE_FORBIDDEN_ROOT_PATHS):
        check_absent(package_root, rel_path, errors)
    check_no_cache_artifacts(package_root, errors)
    return errors


def validate_adapters_light_profile(package_root: Path) -> list[str]:
    errors: list[str] = []
    required = [
        "AGENTS.md",
        "adapters/agent-entrypoints.md",
        "adapters/mcp-recommendations.md",
        ".agents/skills/engineering-calc-system/SKILL.md",
        ".opencode/skills/engineering-calc-system/SKILL.md",
        ".trae/project_rules.md",
        ".trae/rules/engineering-calc-system.md",
    ]
    for rel_path in required:
        check_exists(package_root, rel_path, errors)
    check_absent(package_root, ".qoder", errors)
    check_no_cache_artifacts(package_root, errors)
    return errors


def validate_qoder_addon_profile(package_root: Path) -> list[str]:
    errors: list[str] = []
    required = [
        ".qoder/skills/engineering-calc-system/SKILL.md",
        ".qoder/skills/engineering-calc-system/reference.md",
        ".qoder/skills/engineering-calc-system/assets/lifecycle-console.html",
        ".qoder/agents/engineering-calc-system.md",
        ".qoder/agents/reference.md",
    ]
    for rel_path in required:
        check_exists(package_root, rel_path, errors)
    check_absent(package_root, "SKILL.md", errors)
    check_absent(package_root, "core", errors)
    check_no_cache_artifacts(package_root, errors)
    return errors


def validate_singlefile_profile(package_root: Path) -> list[str]:
    errors: list[str] = []
    check_exists(package_root, "engineering-calculation-system.all-in-one.md", errors)
    for path in package_root.iterdir():
        if path.name not in SINGLEFILE_ALLOWED_FILES:
            errors.append(f"unexpected singlefile profile path: {path.name}")
    text_path = package_root / "engineering-calculation-system.all-in-one.md"
    if text_path.exists():
        text = read_text(text_path)
        for phrase in [
            "Engineering Calculation System - All-in-One Skill Pack",
            "## SKILL.md",
            "## skills/00-engineering-calculation-router.skill.md",
        ]:
            if phrase not in text:
                errors.append(f"singlefile output missing phrase: {phrase!r}")
    check_no_cache_artifacts(package_root, errors)
    return errors


def validate_profile(package_root: Path, profile: str, contract: dict | None) -> list[str]:
    if profile == "core":
        if contract is None:
            return ["core profile requires schemas/artifact_contracts.json"]
        return validate_core_profile(package_root, contract)
    if profile == "adapters-light":
        return validate_adapters_light_profile(package_root)
    if profile == "qoder-addon":
        return validate_qoder_addon_profile(package_root)
    if profile == "singlefile":
        return validate_singlefile_profile(package_root)
    return [f"unknown profile: {profile}"]


def validate_project(project_root: Path, contract: dict) -> list[str]:
    errors: list[str] = []
    for rel_path in contract["project_required_paths"]:
        check_exists(project_root, rel_path, errors)
    check_csv_headers(project_root, contract["project_csv_headers"], errors)
    check_yaml_required_keys(project_root, contract.get("project_yaml_required_keys", {}), errors)
    check_text_required_phrases(project_root, contract.get("project_text_required_phrases", {}), errors)
    check_static_html_delivery_guard(project_root, errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", default=".", help="Skill pack root directory")
    parser.add_argument("--profile", default="core", choices=sorted(PROFILE_CHOICES), help="Release profile to validate")
    parser.add_argument("--project", help="Generated engineering calculation project root")
    args = parser.parse_args(argv)

    package_root = Path(args.package_root).resolve()
    contract = load_contract(package_root) if (package_root / "schemas" / "artifact_contracts.json").exists() else None
    errors = validate_profile(package_root, args.profile, contract)

    if args.project:
        if contract is None:
            errors.append("--project validation requires schemas/artifact_contracts.json under --package-root")
        else:
            errors.extend(validate_project(Path(args.project).resolve(), contract))

    if errors:
        print("Artifact validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Artifact validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
