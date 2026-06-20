#!/usr/bin/env python3
"""Synchronize release-version fields from tools/release_config.json."""

from __future__ import annotations

import argparse
from datetime import date
import json
import re
from pathlib import Path

from versioning import (
    REPO_ROOT,
    WORKSPACE_ROOT,
    codex_plugin_version,
    load_release_config,
    release_created_at,
    release_version,
    set_release_config_version,
    sync_json_version,
    sync_skill_frontmatter_versions,
    write_json_lf,
)


CORE_SKILL_ROOT = REPO_ROOT / "core" / "engineering-calculation-system"
LIGHT_ADAPTER_ROOT = REPO_ROOT / "adapter_sources" / "light"
QODER_ADAPTER_ROOT = REPO_ROOT / "adapter_sources" / "qoder"
PLUGIN_ROOT = WORKSPACE_ROOT / "plugins" / "engineering-calculation-system"
OPENCODE_ROOT = WORKSPACE_ROOT / "opencodeplugin"


VERSIONED_DOC_PATTERNS = [
    (REPO_ROOT / "docs" / "README.md", re.compile(r"(# Engineering Calculation System Skill Pack )v\d+\.\d+\.\d+"), r"\1v{version}"),
    (REPO_ROOT / "docs" / "README.md", re.compile(r"engineering-calculation-system-([A-Za-z-]+)-v\d+\.\d+\.\d+\.zip"), r"engineering-calculation-system-\1-v{version}.zip"),
    (REPO_ROOT / "docs" / "README.zh-CN.md", re.compile(r"(# 工程计算系统技能包 )v\d+\.\d+\.\d+"), r"\1v{version}"),
    (REPO_ROOT / "docs" / "README.zh-CN.md", re.compile(r"engineering-calculation-system-([A-Za-z-]+)-v\d+\.\d+\.\d+\.zip"), r"engineering-calculation-system-\1-v{version}.zip"),
    (REPO_ROOT / "docs" / "README.zh-CN.md", re.compile(r"version: \d+\.\d+\.\d+"), "version: {version}"),
    (REPO_ROOT / "docs" / "README.zh-CN.md", re.compile(r"created_at: \d{4}-\d{2}-\d{2}"), "created_at: {created_at}"),
    (REPO_ROOT / "docs" / "INSTALL.md", re.compile(r"engineering-calculation-system-([A-Za-z-]+)-v\d+\.\d+\.\d+\.zip"), r"engineering-calculation-system-\1-v{version}.zip"),
    (REPO_ROOT / "docs" / "SKILL_PACKAGE_SUMMARY.md", re.compile(r"engineering-calculation-system-([A-Za-z-]+)-v\d+\.\d+\.\d+\.zip"), r"engineering-calculation-system-\1-v{version}.zip"),
    (REPO_ROOT / "adapter_sources" / "light" / "adapters" / "agent-entrypoints.md", re.compile(r"engineering-calculation-system-([A-Za-z-]+)-v\d+\.\d+\.\d+\.zip"), r"engineering-calculation-system-\1-v{version}.zip"),
    (OPENCODE_ROOT / "README.md", re.compile(r"Target skill pack schema: `[^`]+`"), "Target skill pack schema: `{version}`"),
    (OPENCODE_ROOT / "docs" / "installation.md", re.compile(r"schema version `[^`]+`"), "schema version `{version}`"),
]


def sync_opencode_package(version: str) -> None:
    package_path = OPENCODE_ROOT / "package.json"
    package = json.loads(package_path.read_text(encoding="utf-8"))
    package.setdefault("skillPack", {})["schemaVersion"] = version
    write_json_lf(package_path, package)


def sync_codex_manifest(version: str, created_at: str) -> None:
    manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["version"] = codex_plugin_version(version, created_at)
    write_json_lf(manifest_path, manifest)


def sync_current_docs(version: str) -> None:
    created_at = load_release_config()["created_at"]
    for path, pattern, replacement in VERSIONED_DOC_PATTERNS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        updated = pattern.sub(replacement.format(version=version, created_at=created_at), text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def sync_versions(version: str, created_at: str) -> None:
    sync_json_version(CORE_SKILL_ROOT / "schemas" / "artifact_contracts.json", version)
    sync_skill_frontmatter_versions(CORE_SKILL_ROOT, version)
    sync_skill_frontmatter_versions(LIGHT_ADAPTER_ROOT, version)
    sync_skill_frontmatter_versions(QODER_ADAPTER_ROOT, version)
    sync_opencode_package(version)
    sync_codex_manifest(version, created_at)
    sync_current_docs(version)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="New release version. Omit to re-sync the configured version.")
    parser.add_argument(
        "--created-at",
        default=None,
        help="Release date written to release_config.json when --version is used. Defaults to today.",
    )
    args = parser.parse_args(argv)

    if args.version:
        config = set_release_config_version(args.version, created_at=args.created_at or date.today().isoformat())
    else:
        config = load_release_config()

    version = release_version(config)
    created_at = release_created_at(config)
    sync_versions(version, created_at)
    print(f"Synchronized release version {version} ({created_at})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
