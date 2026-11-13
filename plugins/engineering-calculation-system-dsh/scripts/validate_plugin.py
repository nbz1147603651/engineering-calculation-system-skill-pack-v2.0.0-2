#!/usr/bin/env python3
"""Validate the DeepSeek Harness plugin wrapper and its bundled skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PLUGIN_NAME = "@engineering-calculation-system/dsh-plugin"
BUNDLE_RELATIVE = Path("skills") / "engineering-calculation-system"
INSTRUCTIONS_RELATIVE = BUNDLE_RELATIVE / "SKILL.md"
ADAPTER_RELATIVE = Path("shared") / "dsh-plugin-adapter.md"
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROW_ID_RE = re.compile(r"export const name = '([^']+)'")
PATCH_NAME_RE = re.compile(r"name: '([^']+)'")
BUNDLE_REFERENCE_RE = re.compile(
    r"(?<![\w/.-])((?:skills|shared|parent|templates|schemas|scripts|project_template|agents)"
    r"/[A-Za-z0-9_./-]+\.(?:md|py|yaml|yml|json|csv|j2|tex|toml|txt|sh))"
)
# A source-checkout distribution tree the installed bundle does not carry. The
# sync step rewrites the core paragraph that names it, so a match here means
# that rewrite regressed.
FOREIGN_TREE_REFERENCE_RE = re.compile(r"(?<![\w/.-])(dist/[A-Za-z0-9_./-]+)")
FORBIDDEN_DIR_NAMES = {"__pycache__", ".pytest_cache"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


def parse_frontmatter(text: str, label: str) -> tuple[dict[str, str], str]:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{label}: frontmatter must start on the first line")
    try:
        closing = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{label}: frontmatter is not closed") from error
    fields: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, "\n".join(lines[closing + 1 :])


def check_wrapper(plugin_root: Path, errors: list[str]) -> None:
    manifest_path = plugin_root / "package.json"
    if not manifest_path.is_file():
        errors.append(f"missing package.json at {manifest_path}")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        errors.append(f"package.json is not valid JSON: {error}")
        return
    if manifest.get("name") != PLUGIN_NAME:
        errors.append(f"package.json name must be {PLUGIN_NAME}, found {manifest.get('name')!r}")
    patch_relative = manifest.get("dsh", {}).get("bundle", {}).get("patch")
    if not patch_relative:
        errors.append("package.json must declare dsh.bundle.patch")
    patch_path = plugin_root / str(patch_relative)
    if patch_relative and not patch_path.is_file():
        errors.append(f"dsh.bundle.patch points at a missing file: {patch_path}")
    entry_relative = manifest.get("main")
    if not entry_relative or not (plugin_root / str(entry_relative)).is_file():
        errors.append(f"package.json main must point at an existing module, found {entry_relative!r}")
    for shipped in ("lib", "skills", "cordis.patch.yml"):
        if shipped not in manifest.get("files", []):
            errors.append(f"package.json files must ship {shipped!r} so pnpm installs it")
    if not patch_path.is_file():
        return
    patch_text = patch_path.read_text(encoding="utf-8")
    names = PATCH_NAME_RE.findall(patch_text)
    if PLUGIN_NAME not in names:
        errors.append(f"{patch_path.name} must insert a row named {PLUGIN_NAME}")
    entry_path = plugin_root / str(entry_relative)
    if not entry_path.is_file():
        return
    row_ids = ROW_ID_RE.findall(entry_path.read_text(encoding="utf-8"))
    if not row_ids:
        errors.append(f"{entry_path.name} must export a Cordis plugin name")
        return
    if f"id: {row_ids[0]}" not in patch_text:
        errors.append(f"{patch_path.name} row id must match the plugin name {row_ids[0]!r}")


def check_skill(plugin_root: Path, errors: list[str]) -> None:
    instructions_path = plugin_root / INSTRUCTIONS_RELATIVE
    if not instructions_path.is_file():
        errors.append(f"missing bundled instructions: {instructions_path}")
        return
    text = instructions_path.read_text(encoding="utf-8")
    try:
        fields, body = parse_frontmatter(text, INSTRUCTIONS_RELATIVE.as_posix())
    except ValueError as error:
        errors.append(str(error))
        return
    skill_name = fields.get("name", "")
    if not SKILL_NAME_RE.match(skill_name):
        errors.append(f"{INSTRUCTIONS_RELATIVE.as_posix()}: frontmatter name {skill_name!r} is not kebab-case")
    description = fields.get("description", "")
    if len(description) <= 40:
        errors.append(f"{INSTRUCTIONS_RELATIVE.as_posix()}: frontmatter description is missing or too short")
    if "## DSH Plugin Adapter" not in body:
        errors.append(f"{INSTRUCTIONS_RELATIVE.as_posix()}: the DSH adapter section is missing")
    bundle_root = plugin_root / BUNDLE_RELATIVE
    if not (bundle_root / ADAPTER_RELATIVE).is_file():
        errors.append(f"missing overlay file: {(BUNDLE_RELATIVE / ADAPTER_RELATIVE).as_posix()}")
    for reference in sorted(set(BUNDLE_REFERENCE_RE.findall(text))):
        if not (bundle_root / reference).exists():
            errors.append(f"referenced path does not exist in the bundle: {reference}")
    for reference in sorted(set(FOREIGN_TREE_REFERENCE_RE.findall(text))):
        errors.append(
            f"{INSTRUCTIONS_RELATIVE.as_posix()}: references a tree the bundle does not carry: {reference}"
        )


def check_residue(plugin_root: Path, errors: list[str]) -> None:
    for path in plugin_root.rglob("*"):
        if path.is_dir() and path.name in FORBIDDEN_DIR_NAMES:
            errors.append(f"build residue must not be shipped: {path.relative_to(plugin_root).as_posix()}")
        elif path.is_file() and path.suffix in FORBIDDEN_SUFFIXES:
            errors.append(f"build residue must not be shipped: {path.relative_to(plugin_root).as_posix()}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Plugin root. Defaults to the directory containing this script's parent.",
    )
    args = parser.parse_args()
    plugin_root = args.plugin_root.resolve()
    if not plugin_root.is_dir():
        print(f"plugin root does not exist: {plugin_root}", file=sys.stderr)
        return 1

    errors: list[str] = []
    check_wrapper(plugin_root, errors)
    check_skill(plugin_root, errors)
    check_residue(plugin_root, errors)
    if errors:
        print(f"plugin validation failed for {plugin_root}:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"plugin validation passed for {plugin_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
