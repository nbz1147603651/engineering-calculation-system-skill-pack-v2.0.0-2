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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_contract(package_root: Path) -> dict:
    path = package_root / "schemas" / "artifact_contracts.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_exists(root: Path, rel_path: str, errors: list[str]) -> None:
    if not (root / rel_path).exists():
        errors.append(f"missing required path: {rel_path}")


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


def validate_project(project_root: Path, contract: dict) -> list[str]:
    errors: list[str] = []
    for rel_path in contract["project_required_paths"]:
        check_exists(project_root, rel_path, errors)
    check_csv_headers(project_root, contract["project_csv_headers"], errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", default=".", help="Skill pack root directory")
    parser.add_argument("--project", help="Generated engineering calculation project root")
    args = parser.parse_args(argv)

    package_root = Path(args.package_root).resolve()
    contract = load_contract(package_root)
    errors = validate_package(package_root, contract)

    if args.project:
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
