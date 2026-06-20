#!/usr/bin/env python3
"""Shared release-version helpers for the Engineering Calculation System."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
RELEASE_CONFIG_PATH = REPO_ROOT / "tools" / "release_config.json"
FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json_lf(path: Path, data: dict[str, Any]) -> None:
    path.write_text(f"{json.dumps(data, indent=2, ensure_ascii=False)}\n", encoding="utf-8")


def write_text_lf(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def load_release_config() -> dict[str, Any]:
    return read_json(RELEASE_CONFIG_PATH)


def release_version(config: dict[str, Any] | None = None) -> str:
    value = (config or load_release_config()).get("version")
    if not isinstance(value, str) or not SEMVER_RE.match(value):
        raise ValueError(f"release_config.json version is not valid semver: {value!r}")
    return value


def release_created_at(config: dict[str, Any] | None = None) -> str:
    value = (config or load_release_config()).get("created_at")
    if not isinstance(value, str) or not value:
        raise ValueError(f"release_config.json created_at is invalid: {value!r}")
    return value


def set_release_config_version(version: str, *, created_at: str | None = None) -> dict[str, Any]:
    if not SEMVER_RE.match(version):
        raise ValueError(f"version is not valid semver: {version!r}")
    config = load_release_config()
    config["version"] = version
    if created_at:
        config["created_at"] = created_at
    write_json_lf(RELEASE_CONFIG_PATH, config)
    return config


def sync_json_version(path: Path, version: str) -> None:
    data = read_json(path)
    data["version"] = version
    write_json_lf(path, data)


def sync_skill_frontmatter_versions(root: Path, version: str) -> None:
    """Ensure every SKILL.md under root has the current release version."""
    for path in root.rglob("SKILL.md"):
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        match = FRONTMATTER_RE.match(text)
        if not match:
            continue
        body = match.group("body")
        if re.search(r"^version:\s*.+$", body, re.MULTILINE):
            body = re.sub(r"^version:\s*.+$", f"version: {version}", body, flags=re.MULTILINE)
        else:
            lines = body.splitlines()
            insert_at = len(lines)
            for index, line in enumerate(lines):
                if line.startswith("description:"):
                    insert_at = index + 1
                    break
            lines.insert(insert_at, f"version: {version}")
            body = "\n".join(lines)
        write_text_lf(path, f"---\n{body}\n---\n{text[match.end():]}")


def assert_skill_frontmatter_versions(root: Path, version: str) -> None:
    for path in root.rglob("SKILL.md"):
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            continue
        version_match = re.search(r"^version:\s*(.+)$", match.group("body"), re.MULTILINE)
        if not version_match:
            continue
        actual = version_match.group(1).strip().strip('"').strip("'")
        if actual != version:
            rel = path.relative_to(root).as_posix()
            raise RuntimeError(f"frontmatter version mismatch in {rel}: expected {version}, got {actual}")


def codex_plugin_version(version: str, created_at: str) -> str:
    return f"{version}+codex.{created_at.replace('-', '')}"
