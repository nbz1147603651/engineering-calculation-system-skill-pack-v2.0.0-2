#!/usr/bin/env python3
"""Build layered release artifacts for the engineering calculation skill pack."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from versioning import (
    assert_skill_frontmatter_versions,
    load_release_config,
    sync_skill_frontmatter_versions,
    write_json_lf,
    zcode_plugin_version,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
CORE_SOURCE = REPO_ROOT / "core" / "engineering-calculation-system"
LIGHT_ADAPTER_SOURCE = REPO_ROOT / "adapter_sources" / "light"
QODER_ADAPTER_SOURCE = REPO_ROOT / "adapter_sources" / "qoder"
ZCODE_PLUGIN_SOURCE = WORKSPACE_ROOT / "plugins" / "engineering-calculation-system-zcode"
DIST_ROOT = REPO_ROOT / "dist"
RELEASE_ROOT = DIST_ROOT / "release"
QODERWORKCN_PLUGIN_NAME = "engineering-calculation-system"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".blocked_pytest_cache_container",
    "dist",
}

EXCLUDED_FILE_NAMES = {
    ".DS_Store",
    "MANIFEST.yaml",
    "CHECKSUMS.txt",
    "TREE.md",
}

FORBIDDEN_CACHE_SUFFIXES = {
    ".pyc",
    ".pyo",
}

@dataclass(frozen=True)
class BundleCopy:
    profile: str
    source: str
    target: str
    is_file: bool = False


@dataclass(frozen=True)
class BundleTarget:
    name: str
    path: str
    install_text: str
    include_core: bool = True
    include_adapter_docs: bool = False
    payload_at_root: bool = False
    include_install_guide: bool = True
    copies: tuple[BundleCopy, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReleaseArchive:
    target: BundleTarget
    archive_path: Path
    install_folder: str
    file_count: int


def parse_bundle_copy(data: dict) -> BundleCopy:
    return BundleCopy(
        profile=data["profile"],
        source=data["source"],
        target=data["target"],
        is_file=bool(data.get("is_file", False)),
    )


def parse_bundle_target(data: dict) -> BundleTarget:
    return BundleTarget(
        name=data["name"],
        path=data["path"],
        install_text=data["install_text"],
        include_core=bool(data.get("include_core", True)),
        include_adapter_docs=bool(data.get("include_adapter_docs", False)),
        payload_at_root=bool(data.get("payload_at_root", False)),
        include_install_guide=bool(data.get("include_install_guide", True)),
        copies=tuple(parse_bundle_copy(copy) for copy in data.get("copies", ())),
        notes=tuple(data.get("notes", ())),
    )


def validate_rel_path(value: str, field: str, *, allow_dot: bool = False) -> None:
    if not value:
        raise ValueError(f"{field} must not be empty")
    if value == "." and allow_dot:
        return
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field} must be a relative path inside the release bundle: {value}")


def validate_release_config(
    config: dict,
    targets: tuple[BundleTarget, ...],
) -> None:
    profiles = set(config["profiles"])
    for field in ("default_all_profiles", "release_required_profiles"):
        unknown = set(config.get(field, ())) - profiles
        if unknown:
            raise ValueError(f"{field} references unknown profile(s): {', '.join(sorted(unknown))}")

    seen_paths: set[str] = set()
    for target in targets:
        validate_rel_path(
            target.path,
            f"classified target {target.name} path",
            allow_dot=target.payload_at_root,
        )
        if target.path in seen_paths:
            raise ValueError(f"duplicate classified target path: {target.path}")
        seen_paths.add(target.path)
        for copy in target.copies:
            validate_bundle_copy(copy, profiles, f"classified target {target.name}")

    target_names = {target.name for target in targets}
    unknown_publish_targets = set(config.get("publish_targets", ())) - target_names
    if unknown_publish_targets:
        raise ValueError(
            "publish_targets references unknown target(s): "
            + ", ".join(sorted(unknown_publish_targets))
        )

    if not config.get("singlefile_prefixes"):
        raise ValueError("singlefile_prefixes must not be empty")
    if not config.get("source_dev_includes"):
        raise ValueError("source_dev_includes must not be empty")


def validate_bundle_copy(copy: BundleCopy, profiles: set[str], context: str) -> None:
    if copy.profile not in profiles:
        raise ValueError(f"{context} references unknown profile: {copy.profile}")
    validate_rel_path(copy.source, f"{context} source", allow_dot=True)
    validate_rel_path(copy.target, f"{context} target", allow_dot=True)


CONFIG = load_release_config()
VERSION = CONFIG["version"]
CREATED_AT = CONFIG["created_at"]
PACKAGE_PREFIX = CONFIG.get("package_prefix", "engineering-calculation-system")
PROFILE_CHOICES = tuple(CONFIG["profiles"])
DEFAULT_ALL_PROFILES = tuple(CONFIG.get("default_all_profiles", PROFILE_CHOICES))
RELEASE_REQUIRED_PROFILES = tuple(CONFIG.get("release_required_profiles", PROFILE_CHOICES))
SINGLEFILE_PREFIXES = tuple(CONFIG["singlefile_prefixes"])
SOURCE_DEV_INCLUDES = tuple(CONFIG["source_dev_includes"])
UI_CLIENT_CONFIG = CONFIG.get("ui_client", {})
CLASSIFIED_TARGETS = tuple(parse_bundle_target(target) for target in CONFIG["classified_targets"])
PUBLISH_TARGET_NAMES = tuple(CONFIG.get("publish_targets", (target.name for target in CLASSIFIED_TARGETS)))
validate_release_config(CONFIG, CLASSIFIED_TARGETS)

CANONICAL_BEHAVIOR_DOCS = (
    "shared/lifecycle.md",
    "shared/execution-discipline.md",
    "shared/planning-discipline.md",
    "shared/review-feedback-discipline.md",
    "shared/version-control-discipline.md",
    "shared/completion-evidence.md",
    "shared/systematic-debugging.md",
    "shared/multi-agent-orchestration.md",
)

PLATFORM_ENTRYPOINTS = {
    "CODEX": "SKILL.md",
    "MiniMaxCode": "skills/engineering-calculation-system/SKILL.md",
    "ZCode": "skills/engineering-calculation-system/SKILL.md",
    "QODER": "SKILL.md",
    "QODER Project": ".qoder/agents/engineering-calc-system.md",
    "Qoder CLI Plugin": ".qoder-plugin/plugin.json",
    "QoderCN": "agents/engineering-calc-system.md",
    "QoderCN Project": ".lingma/agents/engineering-calc-system.md",
    "QoderCN CLI": ".qodercn/agents/engineering-calc-system.md",
    "QoderCN CLI Project": ".qodercn/agents/engineering-calc-system.md",
    "QoderCN Cloud Agents": "SKILL.md",
    "QoderWorkCN": ".qoder-plugin/plugin.json",
    "WorkBuddy": ".qoder-plugin/plugin.json",
    "TRAE": ".trae/project_rules.md",
    "OpenCode": ".opencode/skills/engineering-calc-system/SKILL.md",
    "AGENTS Generic": "AGENTS.md",
}

PLATFORM_FALLBACKS = {
    "QODER": "Direct skill is lightweight; use QODER Project plus complete core package before web-complete claims.",
    "Qoder CLI Plugin": "Install with Qoder CLI plugin management; if plugin install is unavailable, use QODER Project or the direct QODER Skill zip.",
    "QoderCN": "User-level resources are lightweight; use QoderCN Project plus complete core package for web-complete claims.",
    "QoderCN CLI": "Copy both .qoder-cn and .qodercn folders to the user home; use QoderCN CLI Project plus complete core package for web-complete claims.",
    "QoderCN CLI Project": "Project package is complete; keep .qoder/skills and .qodercn/agents together so QoderCN CLI can discover both Skills and Subagents.",
    "QoderCN Cloud Agents": "Upload the root SKILL.md zip to QoderCN Cloud Agents Skills; bind it to an Agent only after preserving that Agent's existing skills list.",
    "QoderWorkCN": "Upload the generated expert-kit zip through QoderWork CN Expert Kits; if plugin import cannot traverse files, use the bundled full core skill or singlefile fallback.",
    "WorkBuddy": "Upload the generated expert-kit zip through WorkBuddy Skills Marketplace / Expert Center import; if import cannot traverse files, use the bundled full core skill or singlefile fallback.",
    "MiniMaxCode": "If repository import cannot traverse files, use the same skills/engineering-calculation-system root or singlefile fallback.",
    "ZCode": "If plugin import is unavailable, use the legacy skills/engineering-calculation-system folder or singlefile fallback.",
    "TRAE": "If rules cannot traverse the package, paste the singlefile fallback.",
    "OpenCode": "If project skills cannot traverse the package, use .agents wrapper or singlefile fallback.",
    "AGENTS Generic": "If repository rules are the only available entrypoint, use AGENTS.md plus SKILL.md or singlefile fallback.",
}

ZCODE_PLUGIN_NAME = "engineering-calculation-system-zcode"
ZCODE_SKILL_ROOT = "skills/engineering-calculation-system"
ZCODE_SKILL_ENTRYPOINT = f"{ZCODE_SKILL_ROOT}/SKILL.md"
ZCODE_ENTRYPOINT_SKILLS = [
    "skills/engineering-calculation-reference-acquisition/SKILL.md",
    "skills/engineering-calculation-logic-architecture/SKILL.md",
    "skills/engineering-calculation-book-delivery/SKILL.md",
    "skills/engineering-calculation-router/SKILL.md",
    "skills/engineering-calculation-reference-adequacy/SKILL.md",
    "skills/engineering-calculation-reference-discovery/SKILL.md",
    "skills/engineering-calculation-reference-library/SKILL.md",
    "skills/engineering-calculation-source-intake/SKILL.md",
    "skills/engineering-calculation-logic-blueprint/SKILL.md",
    "skills/engineering-calculation-formula-extraction/SKILL.md",
    "skills/engineering-calculation-implementation-handoff/SKILL.md",
    "skills/engineering-calculation-book-architecture/SKILL.md",
    "skills/engineering-calculation-core-data-models/SKILL.md",
    "skills/engineering-calculation-reusable-modules/SKILL.md",
    "skills/engineering-calculation-book-runner/SKILL.md",
    "skills/engineering-calculation-report-review-batch/SKILL.md",
    "skills/engineering-calculation-report-rendering/SKILL.md",
    "skills/engineering-calculation-review-interfaces/SKILL.md",
    "skills/engineering-calculation-batch-packages/SKILL.md",
    "skills/engineering-calculation-verification/SKILL.md",
    "skills/engineering-calculation-cloud-deployment/SKILL.md",
]
ZCODE_PLUGIN_REQUIRED_PATHS = [
    ".zcode-plugin/plugin.json",
    "marketplace.json",
    "package.json",
    "README.md",
    "docs/ADAPTATION.md",
    "scripts/sync_from_core.py",
    "scripts/validate_plugin.py",
    ZCODE_SKILL_ENTRYPOINT,
    *ZCODE_ENTRYPOINT_SKILLS,
    f"{ZCODE_SKILL_ROOT}/shared/zcode-plugin-adapter.md",
    f"{ZCODE_SKILL_ROOT}/shared/lifecycle.md",
    f"{ZCODE_SKILL_ROOT}/shared/execution-discipline.md",
    f"{ZCODE_SKILL_ROOT}/shared/planning-discipline.md",
    f"{ZCODE_SKILL_ROOT}/shared/review-feedback-discipline.md",
    f"{ZCODE_SKILL_ROOT}/shared/version-control-discipline.md",
    f"{ZCODE_SKILL_ROOT}/shared/completion-evidence.md",
    f"{ZCODE_SKILL_ROOT}/scripts/validate_artifacts.py",
    f"{ZCODE_SKILL_ROOT}/project_template/engineering_calc_project/src/pkg/core/capabilities.py",
]
ZCODE_SKILL_REQUIRED_PHRASES = [
    "name: engineering-calculation-system",
    "shared/zcode-plugin-adapter.md",
    "shared/lifecycle.md",
    "shared/execution-discipline.md",
    "shared/planning-discipline.md",
    "shared/review-feedback-discipline.md",
    "shared/version-control-discipline.md",
    "shared/completion-evidence.md",
    "dual closure",
    "run_book(BookInput) -> BookResult",
]
ZCODE_ADAPTER_REQUIRED_PHRASES = [
    "ZCode Plugin Adapter",
    ".zcode-plugin/plugin.json",
    "marketplace.json",
    "Goal Mode",
    "AGENTS.md",
    "shared/completion-evidence.md",
]

QODERWORKCN_AGENT_FILES = [
    "engineering-calc-system.md",
    "engineering-calc-reference-acquirer.md",
    "engineering-calc-source-intake.md",
    "engineering-calc-logic-extractor.md",
    "engineering-calc-module-worker.md",
    "engineering-calc-interface-worker.md",
    "engineering-calc-verification-worker.md",
    "engineering-calc-release-worker.md",
]
QODERWORKCN_REQUIRED_PATHS = [
    ".qoder-plugin/plugin.json",
    "qoder.md",
    "README.md",
    "CONNECTORS.md",
    "skills/engineering-calculation-system/SKILL.md",
    "skills/engineering-calculation-system/shared/lifecycle.md",
    "skills/engineering-calculation-system/shared/execution-discipline.md",
    "skills/engineering-calculation-system/shared/planning-discipline.md",
    "skills/engineering-calculation-system/shared/version-control-discipline.md",
    "skills/engineering-calculation-system/shared/completion-evidence.md",
    "skills/engineering-calculation-system/scripts/validate_artifacts.py",
    "skills/engineering-calculation-system/project_template/engineering_calc_project/webapp/routes.py",
    "skills/engineering-calc-system/SKILL.md",
    "skills/engineering-calc-system/reference.md",
    "skills/engineering-calc-system/qoder_quickstart.md",
    "skills/engineering-calc-system/assets/lifecycle-console.html",
    "references/engineering-calc-system.md",
    "adapters/agent-entrypoints.md",
    "adapters/mcp-recommendations.md",
    *[f"agents/{name}" for name in QODERWORKCN_AGENT_FILES],
]

QODER_PLUGIN_NAME = "engineering-calculation-system-qoder"
QODER_PLUGIN_REQUIRED_PATHS = QODERWORKCN_REQUIRED_PATHS


def should_skip(path: Path, *, include_indexes: bool = False) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True
    if not include_indexes and path.name in EXCLUDED_FILE_NAMES:
        return True
    if path.suffix in FORBIDDEN_CACHE_SUFFIXES:
        return True
    return False


def clean_dir(path: Path) -> None:
    resolved = path.resolve()
    dist_resolved = DIST_ROOT.resolve()
    if not str(resolved).startswith(str(dist_resolved)):
        raise RuntimeError(f"refusing to clean outside dist: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if should_skip(rel):
            continue
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def sync_frontmatter_versions(root: Path) -> None:
    """Synchronize SKILL.md frontmatter versions in generated artifacts."""
    sync_skill_frontmatter_versions(root, VERSION)


def assert_frontmatter_versions(root: Path) -> None:
    assert_skill_frontmatter_versions(root, VERSION)


def require_paths(root: Path, paths: list[str], *, context: str) -> None:
    missing = [path for path in paths if not (root / path).exists()]
    if missing:
        raise RuntimeError(f"{context} missing required path(s): {', '.join(missing)}")


def require_text(path: Path, phrases: list[str], *, context: str) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [phrase for phrase in phrases if phrase not in text]
    if missing:
        raise RuntimeError(f"{context} missing required phrase(s): {', '.join(missing)}")


def require_text_absent(path: Path, phrases: list[str], *, context: str) -> None:
    text = path.read_text(encoding="utf-8")
    present = [phrase for phrase in phrases if phrase in text]
    if present:
        raise RuntimeError(f"{context} contains forbidden phrase(s): {', '.join(present)}")


def validate_windows_icon(icon_path: Path) -> None:
    """Require Windows-friendly small icon layers for Explorer list/detail views."""
    data = icon_path.read_bytes()
    if len(data) < 6:
        raise RuntimeError(f"ui-client icon is not a valid .ico file: {icon_path}")
    reserved, icon_type, count = struct.unpack_from("<HHH", data, 0)
    if reserved != 0 or icon_type != 1 or count <= 0:
        raise RuntimeError(f"ui-client icon is not a valid Windows icon: {icon_path}")

    entries: dict[int, tuple[int, int]] = {}
    for index in range(count):
        offset = 6 + index * 16
        if offset + 16 > len(data):
            raise RuntimeError(f"ui-client icon directory is truncated: {icon_path}")
        width_byte, height_byte, _colors, _reserved, _planes, bit_count, size, image_offset = struct.unpack_from(
            "<BBBBHHII",
            data,
            offset,
        )
        width = 256 if width_byte == 0 else width_byte
        height = 256 if height_byte == 0 else height_byte
        if width != height:
            continue
        if image_offset + size > len(data):
            raise RuntimeError(f"ui-client icon image data is truncated: {icon_path}")
        entries[width] = (bit_count, image_offset)

    required_sizes = {16, 32, 48, 256}
    missing = sorted(required_sizes - set(entries))
    if missing:
        raise RuntimeError(
            f"ui-client icon must include Explorer-friendly sizes: {', '.join(map(str, missing))}"
        )

    for size in (16, 32, 48):
        bit_count, image_offset = entries[size]
        if bit_count != 32:
            raise RuntimeError(f"ui-client icon size {size} must be 32-bit RGBA")
        if data[image_offset : image_offset + 8] == b"\x89PNG\r\n\x1a\n":
            raise RuntimeError(
                f"ui-client icon size {size} is PNG-compressed; use DIB/BGRA for Explorer list views"
            )


def iter_files(root: Path, *, include_indexes: bool = False) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if should_skip(path.relative_to(root), include_indexes=include_indexes):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_lines(root: Path, files: list[Path]) -> list[str]:
    tree: dict[str, dict] = {}
    for path in files:
        node = tree
        for part in path.relative_to(root).parts:
            node = node.setdefault(part, {})

    lines = ["# Package Tree", "", "```text", f"{root.name}/"]

    def render(node: dict[str, dict], prefix: str = "") -> None:
        items = sorted(node.items(), key=lambda item: item[0])
        for index, (name, child) in enumerate(items):
            last = index == len(items) - 1
            connector = "\\-- " if last else "+-- "
            lines.append(f"{prefix}{connector}{name}")
            if child:
                render(child, prefix + ("    " if last else "|   "))

    render(tree)
    lines.extend(["```", ""])
    return lines


def write_indexes(profile_root: Path, package_name: str) -> None:
    files = iter_files(profile_root)

    manifest = [
        f"package: {package_name}",
        f"version: {VERSION}",
        f"created_at: {CREATED_AT}",
        f"file_count_excluding_manifest_and_checksums: {len(files)}",
        "files:",
    ]
    for path in files:
        rel = path.relative_to(profile_root).as_posix()
        manifest.extend(
            [
                f"  - path: {rel}",
                f"    size_bytes: {path.stat().st_size}",
                f"    sha256: {sha256(path)}",
            ]
        )
    (profile_root / "MANIFEST.yaml").write_text("\n".join(manifest) + "\n", encoding="utf-8")

    checksums = [f"{sha256(path)}  {path.relative_to(profile_root).as_posix()}" for path in files]
    (profile_root / "CHECKSUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    (profile_root / "TREE.md").write_text("\n".join(tree_lines(profile_root, files)), encoding="utf-8")


def include_singlefile(path: Path) -> bool:
    rel = path.relative_to(CORE_SOURCE).as_posix()
    return any(rel == prefix or rel.startswith(prefix) for prefix in SINGLEFILE_PREFIXES)


def build_core() -> Path:
    profile_root = DIST_ROOT / "core"
    clean_dir(profile_root)
    copy_tree(CORE_SOURCE, profile_root / "engineering-calculation-system")
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    write_indexes(profile_root, "engineering-calculation-system-core")
    return profile_root


def build_adapters_light() -> Path:
    profile_root = DIST_ROOT / "adapters-light"
    clean_dir(profile_root)
    copy_tree(LIGHT_ADAPTER_SOURCE, profile_root)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    write_indexes(profile_root, "engineering-calculation-system-adapters-light")
    return profile_root


def build_qoder_addon() -> Path:
    profile_root = DIST_ROOT / "qoder-addon"
    clean_dir(profile_root)
    copy_tree(QODER_ADAPTER_SOURCE, profile_root)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    write_indexes(profile_root, "engineering-calculation-system-qoder-addon")
    return profile_root


def write_qoderworkcn_manifest(profile_root: Path) -> None:
    (profile_root / ".qoder-plugin").mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": QODERWORKCN_PLUGIN_NAME,
        "version": VERSION,
        "description": (
            "Expert kit for source-backed engineering calculation software: "
            "reference acquisition, logic extraction, implementation handoff, "
            "auditable calculation-book apps, reports, batch flows, verification, "
            "and deployment."
        ),
        "author": "Engineering Calculation System",
        "homepage": "https://help.aliyun.com/zh/lingma/qoderwork-cn/user-guide/expert-kit",
        "keywords": [
            "qoderwork-cn",
            "expert-kit",
            "engineering-calculation",
            "calculation-book",
            "verification",
        ],
    }
    write_json_lf(profile_root / ".qoder-plugin" / "plugin.json", manifest)


def write_qoderworkcn_guides(profile_root: Path) -> None:
    qoder_md = f"""# Engineering Calculation Expert Kit for QoderWork CN

This directory is a QoderWork CN Plugin / Expert Kit. It follows the official
expert-kit style layout: `.qoder-plugin/plugin.json`, `skills/`, `agents/`,
optional connector metadata, and kit documentation.

Use this kit when the user asks for engineering calculation references,
formula/lookup/branch extraction, calculation logic blueprints, implementation
handoff, auditable calculation-book software, reports, batch flows,
verification, or deployment.

## Official Root Layout

This expert kit is self-contained at the zip root:

```text
.qoder-plugin/plugin.json              official plugin manifest
qoder.md                               kit operating contract
README.md                              install and first-use notes
CONNECTORS.md                          connector dependency policy
agents/                                supervisor and worker role instructions
skills/engineering-calc-system/        QoderWork CN quick entry skill
skills/engineering-calculation-system/ complete core skill package
references/                            long platform-specific reference notes
adapters/                              platform entrypoint and connector notes
```

## Operating Contract

Use `agents/engineering-calc-system.md` as the QoderWork CN supervisor when role
agents are exposed from the kit. Use `skills/engineering-calc-system/SKILL.md`
as the short quick-entry skill and
`skills/engineering-calculation-system/SKILL.md` as the complete lifecycle
authority.

The quick-entry skill does not replace the full core package. The full core skill
carries the complete templates, schemas, project scaffold, scripts, and shared
contracts required for production work.

Before implementation, release, or completion claims, read these canonical
contracts from `skills/engineering-calculation-system/shared/`:

```text
lifecycle.md
execution-discipline.md
planning-discipline.md
review-feedback-discipline.md
version-control-discipline.md
completion-evidence.md
systematic-debugging.md
multi-agent-orchestration.md
```

For production calculation software, formulas and lookup logic must live only in
reusable modules and the official `run_book(BookInput) -> BookResult` runner.
UI, report templates, batch scripts, CSV/Excel files, and presentation code must
consume computed results rather than calculate.

For `web-complete`, use the full core skill, project template, validator, and
deployment artifacts bundled in this kit. A static HTML report, notebook, UI
mockup, or direct lightweight skill alone is not enough.

Validate generated projects with:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core --project <project-root> --delivery web-complete
```

Kit version: {VERSION}
"""
    readme = f"""# Engineering Calculation System - QoderWork CN Expert Kit

Version: {VERSION}

This package is an upload-ready QoderWork CN Expert Kit. It contains:

- `.qoder-plugin/plugin.json` metadata at the kit root.
- `skills/engineering-calculation-system/`: the complete core skill package with
  lifecycle contracts, templates, schemas, validators, and project scaffold.
- `skills/engineering-calc-system/`: the QoderWork CN quick-entry skill and
  lifecycle console asset.
- `agents/`: supervisor and worker role instructions for the engineering
  calculation lifecycle.
- `references/`: long reference guidance kept outside agent files.
- `adapters/`: cross-agent entrypoint and MCP recommendation notes.

## Install In QoderWork CN

1. Zip this directory so `.qoder-plugin/plugin.json` is at the zip root.
2. Open QoderWork CN -> Extensions -> Expert Kits.
3. Click `+ Add` -> Upload Kit.
4. Select the generated zip and install it.

The one-click deployment GUI creates both the staged directory and an upload zip
with the required root structure.

## First Use

Start a new task and select this expert kit. Ask for an engineering calculation
workflow, for example:

```text
Use the Engineering Calculation System expert kit to create a source-backed,
web-complete calculation-book scaffold. Start by classifying material state and
gate status.
```

The supervisor should classify install shape, material state, delivery mode,
lifecycle path, and gate status before implementation work.
"""
    connectors = """# Connector Dependencies

This expert kit has no required external Connector or MCP dependency.

When a specific project needs source search, browser access, document parsing,
code search, or GUI testing, use the tools/connectors already available in the
current QoderWork CN task with explicit user authorization. Do not declare a
required external Connector unless the workflow truly depends on a published
marketplace connector.
"""
    (profile_root / "qoder.md").write_text(qoder_md, encoding="utf-8")
    (profile_root / "README.md").write_text(readme, encoding="utf-8")
    (profile_root / "CONNECTORS.md").write_text(connectors, encoding="utf-8")


def write_qoderworkcn_native_layers(profile_root: Path) -> None:
    skill_dir = profile_root / "skills" / "engineering-calc-system"
    agents_dir = profile_root / "agents"
    references_dir = profile_root / "references"
    adapters_dir = profile_root / "adapters"

    skill = f"""---
name: engineering-calc-system
description: QoderWork CN quick entry for the Engineering Calculation System expert kit. Use when a task involves engineering calculation references, formula or lookup extraction, calculation logic blueprints, implementation handoff, auditable calculation-book software, reports, batch flows, verification, or deployment.
version: {VERSION}
---

# Engineering Calculation System - QoderWork CN Quick Entry

This skill is the short QoderWork CN Expert Kit entrypoint. It is bundled with
the complete core package in `skills/engineering-calculation-system/`; do not
treat this quick entry as a replacement for the core lifecycle authority.

## QoderWork CN Expert Kit Contract

Use this expert kit for source-backed engineering calculation workflows:
reference acquisition, source intake, logic blueprinting, formula/lookup/branch
extraction, implementation handoff, calculation modules, `run_book(BookInput) ->
BookResult`, reports, review UI, batch flows, verification, and deployment.

Start each non-trivial task by reading:

```text
qoder.md
qoder_quickstart.md
agents/engineering-calc-system.md
skills/engineering-calculation-system/SKILL.md
skills/engineering-calculation-system/skills/00-engineering-calculation-router.skill.md
```

For implementation, release, validation, or completion claims, use the canonical
contracts under `skills/engineering-calculation-system/shared/`:

```text
lifecycle.md
execution-discipline.md
planning-discipline.md
review-feedback-discipline.md
version-control-discipline.md
completion-evidence.md
systematic-debugging.md
multi-agent-orchestration.md
```

## Behavior Engineering Layer

Before implementation action, produce a route card, gate card, artifact
contract, and validation evidence frame. Use `web-complete` by default unless
the user explicitly narrows scope.

For production calculation software, formulas, lookup rules, branch decisions,
and load-combination logic must live only in reusable calculation modules and
the official `run_book(BookInput) -> BookResult` runner. UI, reports, batch
scripts, spreadsheets, and presentation code consume computed results.

For `web-complete`, the project must include API/UI, reports, import/export,
batch, deployment artifacts, smoke tests, and Marimo review/admin closure. A
static report, notebook, UI mockup, or single HTML export is not enough.

## First Step

Ask QoderWork CN to use the expert kit supervisor:

```text
Use the Engineering Calculation System expert kit supervisor. Classify material
state, delivery mode, lifecycle route, evidence gate, coding gate, and immediate
next artifacts before editing code.
```

Then validate generated projects with:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core --project <project-root> --delivery web-complete
```
"""

    quickstart = f"""# QoderWork CN Expert Kit Quickstart

Version: {VERSION}

This package is a QoderWork CN Expert Kit, not a project overlay. Install it by
uploading the generated zip through QoderWork CN -> Extensions -> Expert Kits ->
+ Add -> Upload Kit. The zip root must contain `.qoder-plugin/plugin.json`.

## Expert Kit Self-Check

Before implementation or release work, confirm the installed kit exposes:

```text
.qoder-plugin/plugin.json
qoder.md
agents/engineering-calc-system.md
skills/engineering-calc-system/SKILL.md
skills/engineering-calculation-system/SKILL.md
skills/engineering-calculation-system/shared/lifecycle.md
skills/engineering-calculation-system/scripts/validate_artifacts.py
skills/engineering-calculation-system/project_template/
```

If the complete core package is unavailable, use the task only for routing,
audit, or missing-artifact diagnosis. Do not claim `web-complete`,
production-ready, or deployable output until the core validator can run.

## Start Prompt

```text
Use the Engineering Calculation System expert kit. Start with qoder.md and the
supervisor agent. Classify material state, delivery mode, required lifecycle
path, evidence gate, coding gate, and next artifacts before implementation.
```

## Operating Flow

1. Read `skills/engineering-calculation-system/SKILL.md`.
2. Read the router at
   `skills/engineering-calculation-system/skills/00-engineering-calculation-router.skill.md`.
3. For non-trivial work, read `shared/execution-discipline.md` and prepare the
   route card, gate card, artifact contract, and validation evidence frame.
4. Load only the parent or child lifecycle skill required by the router.
5. For implementation, release, or completion claims, read `shared/lifecycle.md`,
   `shared/version-control-discipline.md`, and `shared/completion-evidence.md`.
6. Use worker agents only for bounded delegated work. The supervisor keeps
   lifecycle routing, source authority, evidence gates, ID namespaces, handoff
   freeze, `run_book(BookInput) -> BookResult`, and final acceptance serial.

## Validation Commands

From the expert kit root:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core --project <project-root> --delivery web-complete
```

From the source checkout:

```bash
python tools/build_release.py --profile qoderworkcn-plugin
python tools/build_release.py --all --no-ui-client
```

## Completion Bar

Do not claim complete, production-ready, deployable, or `web-complete` unless
fresh validation evidence supports the exact claim. Static HTML, visible UI, old
command output, or a worker summary is not enough.
"""

    reference = """# QoderWork CN Expert Kit Reference

This reference is intentionally platform-specific. It explains how QoderWork CN
should use the Engineering Calculation System expert kit after upload.

## Capability Shape

The kit packages a complete workflow, not just one atomic skill:

- `agents/engineering-calc-system.md`: supervisor role for routing, gates,
  delegation, and final acceptance.
- `agents/engineering-calc-*.md`: bounded worker roles for acquisition,
  source intake, logic extraction, modules, interfaces, verification, and
  release support.
- `skills/engineering-calc-system/`: short QoderWork CN quick-entry skill,
  quickstart, reference, and lifecycle console asset.
- `skills/engineering-calculation-system/`: complete lifecycle skill pack with
  shared contracts, templates, schemas, validator, and project scaffold.
- `CONNECTORS.md`: connector dependency policy. The kit has no required
  external connector by default.

## Routing Defaults

Use `web-complete` by default for online calculators, calculation-book software,
deployable web apps, reusable packages, batch workflows, and requests that do
not explicitly narrow scope.

Classify material state before coding:

```text
no_materials
insufficient_materials
materials_available_untrusted
local_evidence_library_available
analysis_handoff_available
static_report_or_cli_only
codebase_available
```

For bug fixes, identify the lowest correct repair layer:

```text
source/evidence -> formula_inventory/lookup_inventory/branch_inventory ->
module -> run_book() -> API/batch -> report/UI
```

## Connector Policy

MCP servers and external connectors are accelerators, not correctness
dependencies. Use search, browser, document parsing, code search, and GUI
testing tools only when available in the current QoderWork CN task and
authorized by the user.
"""

    supervisor = """---
name: engineering-calc-system
description: QoderWork CN supervisor for the Engineering Calculation System expert kit. Use for source-backed engineering calculation workflows, lifecycle routing, gate decisions, worker delegation, validation evidence, and final acceptance.
tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch
---

# Engineering Calculation System Supervisor for QoderWork CN

You are the supervisor for a QoderWork CN Expert Kit. Keep this platform shape
clean: this kit is rooted at `.qoder-plugin/plugin.json`, with `agents/`,
`skills/`, `references/`, `adapters/`, `qoder.md`, `README.md`, and
`CONNECTORS.md` at the upload zip root.

## QoderWork CN Expert Kit Architecture

- Start from `qoder.md` for the kit-level operating contract.
- Use `skills/engineering-calc-system/SKILL.md` as the quick-entry skill.
- Use `skills/engineering-calculation-system/SKILL.md` as the complete lifecycle
  authority.
- Use `skills/engineering-calculation-system/shared/` as the canonical behavior
  source.
- Use `agents/engineering-calc-*.md` only for bounded delegated work.
- Keep final lifecycle routing, source authority, evidence gates, ID allocation,
  handoff freeze, `run_book(BookInput) -> BookResult`, production labels, and
  release acceptance with this supervisor.

## Behavior Engineering Layer

For every non-trivial task, read the router and then
`skills/engineering-calculation-system/shared/execution-discipline.md`. Produce:

```text
route card
gate card
artifact contract
validation evidence
completion evidence category
```

For multi-step plans, read
`skills/engineering-calculation-system/shared/planning-discipline.md`.
For user, reviewer, or worker feedback, read
`skills/engineering-calculation-system/shared/review-feedback-discipline.md`.
For release, package, sync, or platform work, read
`skills/engineering-calculation-system/shared/version-control-discipline.md`.
Before completion claims, read
`skills/engineering-calculation-system/shared/completion-evidence.md`.

## Lifecycle Defaults

Default delivery mode is `web-complete` unless the user explicitly asks for a
narrower `core-only`, `report-only`, or `prototype-web` output.

Do not start production implementation unless `handoff/implementation_handoff.yaml`
and `handoff/coding_go_no_go.md` allow it. Do not invent formulas, coefficients,
units, lookup rules, branch logic, or source authority.

If the target project contains only scripts, notebook output, or `reports/*.html`
without `webapp/`, `apps/review/`, `src/pkg/report/`, `tests/smoke/`, `deploy/`,
and `handoff/`, classify it as `static_report_or_cli_only`. Treat static reports
as evidence or visual references, not as deployable runtime.

## Formula Boundary

Engineering formulas, lookup rules, branches, and load combinations live only in
reusable modules and the official `run_book(BookInput) -> BookResult` runner.
API, UI, reports, review notebooks, batch scripts, spreadsheets, and templates
consume computed results and do not calculate.

## Worker Agents

Delegate only bounded tasks with owned paths and expected result packets:

```text
agents/engineering-calc-reference-acquirer.md     phases 01-03
agents/engineering-calc-source-intake.md          phase 04
agents/engineering-calc-logic-extractor.md        phases 05-07
agents/engineering-calc-module-worker.md          phases 08-11
agents/engineering-calc-interface-worker.md       phases 12/12a/12b/12c
agents/engineering-calc-verification-worker.md    phase 13
agents/engineering-calc-release-worker.md         phase 14
```

Workers may propose changes to shared files, but the supervisor accepts,
rejects, or routes them upstream.

## Validation

For generated projects, run:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core --project <project-root> --delivery web-complete
```

For package maintenance, run the release builder and inspect the QoderWork CN
archive before claiming the expert kit is ready.
"""

    entrypoints = """# QoderWork CN Expert Kit Entrypoints

This package is uploaded through QoderWork CN Expert Kits. It is not a project
overlay.

Primary entrypoints:

- `.qoder-plugin/plugin.json`: official plugin manifest.
- `qoder.md`: kit operating contract.
- `agents/engineering-calc-system.md`: supervisor role.
- `skills/engineering-calc-system/SKILL.md`: quick-entry skill.
- `skills/engineering-calculation-system/SKILL.md`: complete core lifecycle
  skill.

Use the supervisor for lifecycle routing and final acceptance. Use worker agents
only after the supervisor creates a bounded task brief with owned paths and
validation expectations.
"""

    mcp = """# QoderWork CN Connector And MCP Recommendations

The Engineering Calculation System expert kit has no required external
Connector or MCP dependency by default.

Recommended optional accelerators, when available and authorized in the current
QoderWork CN task:

- web search and fetch for current standards, product data, laws, prices, or
  unstable references
- document parsing for user-provided PDFs, spreadsheets, and reports
- code search and diagnostics for existing project audits
- browser or GUI testing for web-complete smoke checks

Do not add a required external connector unless the workflow truly depends on a
published QoderWork CN connector and the user authorizes it.
"""

    (skill_dir / "SKILL.md").write_text(skill, encoding="utf-8")
    (skill_dir / "qoder_quickstart.md").write_text(quickstart, encoding="utf-8")
    (skill_dir / "reference.md").write_text(reference, encoding="utf-8")
    (references_dir / "engineering-calc-system.md").write_text(reference, encoding="utf-8")
    (agents_dir / "engineering-calc-system.md").write_text(supervisor, encoding="utf-8")
    (adapters_dir / "agent-entrypoints.md").write_text(entrypoints, encoding="utf-8")
    (adapters_dir / "mcp-recommendations.md").write_text(mcp, encoding="utf-8")

    for path in sorted(agents_dir.glob("engineering-calc-*.md")):
        if path.name == "engineering-calc-system.md":
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("## Qoder Worker Contract", "## QoderWork CN Expert Kit Worker Contract")
        text = text.replace("Qoder Worker Contract", "QoderWork CN Expert Kit Worker Contract")
        path.write_text(text, encoding="utf-8")


def validate_qoderworkcn_plugin(profile_root: Path, *, context: str) -> None:
    require_paths(profile_root, QODERWORKCN_REQUIRED_PATHS, context=context)
    require_text(
        profile_root / ".qoder-plugin" / "plugin.json",
        [
            f"\"name\": \"{QODERWORKCN_PLUGIN_NAME}\"",
            f"\"version\": \"{VERSION}\"",
            "\"qoderwork-cn\"",
            "\"expert-kit\"",
        ],
        context=context,
    )
    require_text(
        profile_root / "qoder.md",
        [
            "QoderWork CN Plugin / Expert Kit",
            "Official Root Layout",
            "skills/engineering-calculation-system/SKILL.md",
            "agents/engineering-calc-system.md",
            "run_book(BookInput) -> BookResult",
            "validate_artifacts.py",
        ],
        context=context,
    )
    require_text(
        profile_root / "skills" / "engineering-calculation-system" / "SKILL.md",
        [
            "name: engineering-calculation-system",
            "shared/lifecycle.md",
            "shared/execution-discipline.md",
            "shared/planning-discipline.md",
            "shared/version-control-discipline.md",
            "shared/completion-evidence.md",
            "run_book()",
        ],
        context=context,
    )
    require_text(
        profile_root / "skills" / "engineering-calc-system" / "SKILL.md",
        [
            "QoderWork CN Expert Kit Contract",
            "Behavior Engineering Layer",
            "qoder_quickstart.md",
            "skills/engineering-calculation-system/SKILL.md",
            "web-complete",
        ],
        context=context,
    )
    require_text(
        profile_root / "agents" / "engineering-calc-system.md",
        [
            "QoderWork CN Expert Kit Architecture",
            "Behavior Engineering Layer",
            "skills/engineering-calculation-system/shared/execution-discipline.md",
            "static_report_or_cli_only",
            "reports/*.html",
        ],
        context=context,
    )
    require_text(
        profile_root / "skills" / "engineering-calc-system" / "qoder_quickstart.md",
        [
            "QoderWork CN Expert Kit Quickstart",
            "Expert Kit Self-Check",
            ".qoder-plugin/plugin.json",
            "skills/engineering-calculation-system/scripts/validate_artifacts.py",
        ],
        context=context,
    )
    require_text(
        profile_root / "adapters" / "agent-entrypoints.md",
        [
            "QoderWork CN Expert Kit Entrypoints",
            ".qoder-plugin/plugin.json",
            "agents/engineering-calc-system.md",
        ],
        context=context,
    )
    forbidden_native_phrases = [
        "QODER Project",
        "Direct QODER",
        "Qoder Package Self-Check",
        "Qoder Architecture",
        ".qoder/",
        "v2.4.1",
        "2.4.1",
        "Qoder-compatible",
        "older Qoder",
        "WorkBuddy",
        "workbuddy",
        "Tencent",
        "tencent",
    ]
    for rel_path in [
        "qoder.md",
        "README.md",
        "skills/engineering-calc-system/SKILL.md",
        "skills/engineering-calc-system/qoder_quickstart.md",
        "skills/engineering-calc-system/reference.md",
        "agents/engineering-calc-system.md",
        "references/engineering-calc-system.md",
        "adapters/agent-entrypoints.md",
        "adapters/mcp-recommendations.md",
    ]:
        require_text_absent(profile_root / rel_path, forbidden_native_phrases, context=context)


def write_qoder_plugin_manifest(profile_root: Path) -> None:
    (profile_root / ".qoder-plugin").mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": QODER_PLUGIN_NAME,
        "version": VERSION,
        "description": (
            "Qoder CLI plugin for source-backed engineering calculation software: "
            "reference acquisition, logic extraction, implementation handoff, "
            "auditable calculation-book apps, reports, batch flows, verification, "
            "and deployment."
        ),
        "author": "Engineering Calculation System",
        "homepage": "https://docs.qoder.com/en/cli/plugins",
        "keywords": [
            "qoder-cli",
            "plugin",
            "engineering-calculation",
            "calculation-book",
            "verification",
        ],
    }
    write_json_lf(profile_root / ".qoder-plugin" / "plugin.json", manifest)


def write_qoder_plugin_guides(profile_root: Path) -> None:
    qoder_md = f"""# Engineering Calculation Plugin for Qoder CLI

This directory is a Qoder CLI plugin. It follows the official plugin layout:
`.qoder-plugin/plugin.json`, `skills/`, optional `agents/`, optional connector
metadata, and plugin documentation.

Use this plugin when the user asks for engineering calculation references,
formula/lookup/branch extraction, calculation logic blueprints, implementation
handoff, auditable calculation-book software, reports, batch flows,
verification, or deployment.

## Layout Map

```text
agents/                                -> Qoder custom agents
skills/engineering-calc-system/        -> lightweight Qoder quickstart skill
skills/engineering-calculation-system/ -> complete core skill package
references/                            -> long non-agent reference material
adapters/                              -> platform entrypoint and MCP guidance
```

## Operating Contract

Start with `agents/engineering-calc-system.md` as the supervisor when custom
agents are available. Use `skills/engineering-calculation-system/SKILL.md` for
the complete lifecycle rules, templates, schemas, validators, project scaffold,
and shared contracts required for production work.

Before implementation, release, or completion claims, read these canonical
contracts from `skills/engineering-calculation-system/shared/`:

```text
lifecycle.md
execution-discipline.md
planning-discipline.md
review-feedback-discipline.md
version-control-discipline.md
completion-evidence.md
systematic-debugging.md
multi-agent-orchestration.md
```

For production calculation software, formulas and lookup logic must live only in
reusable modules and the official `run_book(BookInput) -> BookResult` runner.
UI, report templates, batch scripts, CSV/Excel files, and presentation code must
consume computed results rather than calculate.

For `web-complete`, use the full core skill, project template, validator, and
deployment artifacts bundled in this plugin. A static HTML report, notebook, UI
mockup, or direct lightweight skill alone is not enough.

Validate generated projects with:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core --project <project-root> --delivery web-complete
```

Plugin version: {VERSION}
"""
    readme = f"""# Engineering Calculation System - Qoder CLI Plugin

Version: {VERSION}

This package is an install-ready Qoder CLI plugin. It contains:

- `.qoder-plugin/plugin.json` metadata at the plugin root.
- `skills/engineering-calculation-system/`: the complete core skill package.
- `skills/engineering-calc-system/`: the Qoder-compatible quickstart skill.
- `agents/`: supervisor and worker role instructions.
- `references/`: long reference guidance kept outside agent files.
- `adapters/`: cross-agent entrypoint and MCP recommendation notes.

## Install

Install this directory or zip through Qoder CLI plugin management, then start
from the `engineering-calc-system` supervisor agent or the bundled skill.

## First Use

```text
Use the Engineering Calculation System Qoder plugin to create a source-backed,
web-complete calculation-book scaffold. Start by classifying material state and
gate status.
```
"""
    connectors = """# Connector Dependencies

This plugin has no required external Connector or MCP dependency.

When a specific project needs source search, browser access, document parsing,
code search, or GUI testing, use the tools/connectors already available in the
current Qoder task with explicit user authorization. Do not declare a required
external Connector unless the workflow truly depends on a published marketplace
connector.
"""
    (profile_root / "qoder.md").write_text(qoder_md, encoding="utf-8")
    (profile_root / "README.md").write_text(readme, encoding="utf-8")
    (profile_root / "CONNECTORS.md").write_text(connectors, encoding="utf-8")


def validate_qoder_plugin(profile_root: Path, *, context: str) -> None:
    require_paths(profile_root, QODER_PLUGIN_REQUIRED_PATHS, context=context)
    require_text(
        profile_root / ".qoder-plugin" / "plugin.json",
        [
            f"\"name\": \"{QODER_PLUGIN_NAME}\"",
            f"\"version\": \"{VERSION}\"",
            "\"qoder-cli\"",
            "\"plugin\"",
        ],
        context=context,
    )
    require_text(
        profile_root / "qoder.md",
        [
            "Qoder CLI plugin",
            "Layout Map",
            "skills/engineering-calculation-system/SKILL.md",
            "agents/engineering-calc-system.md",
            "run_book(BookInput) -> BookResult",
            "validate_artifacts.py",
        ],
        context=context,
    )
    require_text(
        profile_root / "skills" / "engineering-calculation-system" / "SKILL.md",
        [
            "name: engineering-calculation-system",
            "shared/lifecycle.md",
            "shared/execution-discipline.md",
            "shared/planning-discipline.md",
            "shared/version-control-discipline.md",
            "shared/completion-evidence.md",
            "run_book()",
        ],
        context=context,
    )
    require_text(
        profile_root / "skills" / "engineering-calc-system" / "SKILL.md",
        [
            "Qoder Architecture",
            "Behavior Engineering Layer",
            "qoder_quickstart.md",
            "web-complete",
        ],
        context=context,
    )
    require_text(
        profile_root / "agents" / "engineering-calc-system.md",
        [
            "Qoder Architecture",
            "Behavior Engineering Layer",
            "shared/execution-discipline.md",
            "static_report_or_cli_only",
            "reports/*.html",
        ],
        context=context,
    )


def build_qoder_plugin() -> Path:
    profile_root = DIST_ROOT / "qoder-plugin"
    clean_dir(profile_root)
    copy_tree(CORE_SOURCE, profile_root / "skills" / "engineering-calculation-system")
    copy_tree(
        QODER_ADAPTER_SOURCE / ".qoder" / "skills" / "engineering-calc-system",
        profile_root / "skills" / "engineering-calc-system",
    )
    copy_tree(QODER_ADAPTER_SOURCE / ".qoder" / "agents", profile_root / "agents")
    copy_tree(QODER_ADAPTER_SOURCE / ".qoder" / "references", profile_root / "references")
    copy_tree(LIGHT_ADAPTER_SOURCE / "adapters", profile_root / "adapters")
    write_qoder_plugin_manifest(profile_root)
    write_qoder_plugin_guides(profile_root)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    validate_qoder_plugin(profile_root, context="Qoder CLI plugin profile")
    write_indexes(profile_root, "engineering-calculation-system-qoder-plugin")
    return profile_root


def build_qoderworkcn_plugin() -> Path:
    profile_root = DIST_ROOT / "qoderworkcn-plugin"
    clean_dir(profile_root)
    copy_tree(CORE_SOURCE, profile_root / "skills" / "engineering-calculation-system")
    copy_tree(
        QODER_ADAPTER_SOURCE / ".qoder" / "skills" / "engineering-calc-system",
        profile_root / "skills" / "engineering-calc-system",
    )
    copy_tree(QODER_ADAPTER_SOURCE / ".qoder" / "agents", profile_root / "agents")
    copy_tree(QODER_ADAPTER_SOURCE / ".qoder" / "references", profile_root / "references")
    copy_tree(LIGHT_ADAPTER_SOURCE / "adapters", profile_root / "adapters")
    write_qoderworkcn_manifest(profile_root)
    write_qoderworkcn_guides(profile_root)
    write_qoderworkcn_native_layers(profile_root)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    validate_qoderworkcn_plugin(profile_root, context="QoderWorkCN profile")
    write_indexes(profile_root, "engineering-calculation-system-qoderworkcn-plugin")
    return profile_root


def build_singlefile() -> Path:
    profile_root = DIST_ROOT / "singlefile"
    clean_dir(profile_root)
    output = profile_root / "engineering-calculation-system.all-in-one.md"
    lines = [
        "# Engineering Calculation System - All-in-One Skill Pack",
        f"Version: {VERSION}",
        "",
        "This generated file is for agents that cannot load the layered skill package.",
        "Prefer dist/core/engineering-calculation-system/ when multi-file loading is available.",
        "",
    ]
    for path in iter_files(CORE_SOURCE):
        if not include_singlefile(path):
            continue
        rel = path.relative_to(CORE_SOURCE).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lines.extend(["", "---", "", f"## {rel}", "", content.rstrip(), ""])
    output.write_text("\n".join(lines), encoding="utf-8")
    write_indexes(profile_root, "engineering-calculation-system-singlefile")
    return profile_root


def build_source_dev() -> Path:
    profile_root = DIST_ROOT / "source-dev"
    clean_dir(profile_root)
    for rel in SOURCE_DEV_INCLUDES:
        src = REPO_ROOT / rel
        if not src.exists():
            continue
        dst = profile_root / rel
        if src.is_dir():
            copy_tree(src, dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    write_indexes(profile_root, "engineering-calculation-system-source-dev")
    return profile_root


def sync_zcode_plugin_metadata(plugin_root: Path) -> None:
    plugin_version = zcode_plugin_version(VERSION, CREATED_AT)
    manifest_path = plugin_root / ".zcode-plugin" / "plugin.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = plugin_version
        write_json_lf(manifest_path, manifest)

    marketplace_path = plugin_root / "marketplace.json"
    if marketplace_path.exists():
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
        for entry in marketplace.get("plugins", []):
            if isinstance(entry, dict) and entry.get("name") == ZCODE_PLUGIN_NAME:
                entry["version"] = plugin_version
        write_json_lf(marketplace_path, marketplace)

    package_path = plugin_root / "package.json"
    if package_path.exists():
        package = json.loads(package_path.read_text(encoding="utf-8"))
        package["version"] = plugin_version
        write_json_lf(package_path, package)


def build_zcode_plugin() -> Path:
    profile_root = DIST_ROOT / "zcode-plugin"
    clean_dir(profile_root)
    copy_tree(ZCODE_PLUGIN_SOURCE, profile_root / ZCODE_PLUGIN_NAME)
    sync_frontmatter_versions(profile_root)
    assert_frontmatter_versions(profile_root)
    sync_zcode_plugin_metadata(profile_root / ZCODE_PLUGIN_NAME)
    write_indexes(profile_root, "engineering-calculation-system-zcode-plugin")
    return profile_root


def build_ui_client() -> Path:
    """Build the one-click deployment console as a Windows single-file exe.

    Driven by the ``ui_client`` block in release_config.json. Uses PyInstaller
    ``--onefile`` so the result is a self-contained exe that needs no Python on
    the target machine. If PyInstaller is not installed, this is a soft failure:
    we emit a README explaining how to install it, so the rest of the release
    build is not blocked.
    """
    profile_root = DIST_ROOT / "ui-client"
    clean_dir(profile_root)

    if not UI_CLIENT_CONFIG:
        raise RuntimeError("ui_client config missing from release_config.json")

    exe_name = UI_CLIENT_CONFIG["exe_name_template"].format(version=VERSION)
    entry_module = UI_CLIENT_CONFIG["entry_module"]            # e.g. tools.installer_gui.app
    collect_all = tuple(UI_CLIENT_CONFIG.get("collect_all", ()))
    collect_submodules = tuple(UI_CLIENT_CONFIG.get("collect_submodules", ()))
    onefile = bool(UI_CLIENT_CONFIG.get("onefile", True))
    windowed = bool(UI_CLIENT_CONFIG.get("windowed", True))
    icon = UI_CLIENT_CONFIG.get("icon")
    data_files = tuple(UI_CLIENT_CONFIG.get("data_files", ()))

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        readme = profile_root / "README.md"
        readme.write_text(
            "# UI client not built\n\n"
            "PyInstaller is not installed in this environment, so the deployment\n"
            "console exe was skipped. Install it and re-run:\n\n"
            "```bash\npip install pyinstaller\npython tools/build_release.py --profile ui-client\n```\n",
            encoding="utf-8",
        )
        print(f"ui-client: PyInstaller not installed; wrote {readme.relative_to(REPO_ROOT)}")
        return profile_root

    # PyInstaller must import the installer_gui package, which lives under
    # tools/ (not an installed distribution). We give it an entry script that
    # puts tools/ on sys.path before importing the real entry module.
    tools_dir = REPO_ROOT / "tools"
    bootstrap = profile_root / "_entry_bootstrap.py"
    bootstrap.write_text(
        f"from {entry_module} import main\n"
        "main()\n",
        encoding="utf-8",
    )

    argv: list[str] = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(bootstrap),
        f"--name={exe_name}",
        f"--distpath={profile_root}",
        f"--workpath={(profile_root / '_build').as_posix()}",
        f"--specpath={(profile_root / '_spec').as_posix()}",
        f"--paths={tools_dir}",
        "--noconfirm",
        "--clean",
    ]
    if onefile:
        argv.append("--onefile")
    if windowed:
        argv.append("--windowed")
    if icon:
        icon_path = REPO_ROOT / str(icon)
        if not icon_path.exists():
            raise RuntimeError(f"ui-client icon not found: {icon_path}")
        validate_windows_icon(icon_path)
        argv.append(f"--icon={icon_path}")
    for pkg in collect_all:
        argv.append(f"--collect-all={pkg}")
    for mod in collect_submodules:
        argv.append(f"--collect-submodules={mod}")
    for item in data_files:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise RuntimeError(f"ui-client data_files entries must be [source, target], got: {item!r}")
        source = REPO_ROOT / str(item[0])
        target = str(item[1])
        if not source.exists():
            raise RuntimeError(f"ui-client data file not found: {source}")
        argv.append(f"--add-data={source}{os.pathsep}{target}")

    print(f"ui-client: running PyInstaller -> {exe_name}")
    result = subprocess.run(argv, cwd=str(REPO_ROOT))
    # Clean up build scratch dirs PyInstaller leaves behind.
    for scratch in ("_build", "_spec"):
        scratch_dir = profile_root / scratch
        if scratch_dir.exists():
            shutil.rmtree(scratch_dir, ignore_errors=True)
    bootstrap.unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(f"PyInstaller failed (exit {result.returncode})")

    exe_path = profile_root / (exe_name + ".exe")
    if not exe_path.exists():
        raise RuntimeError(f"PyInstaller reported success but {exe_path} was not produced")

    write_indexes(profile_root, "engineering-calculation-system-ui-client")
    return profile_root


def build_profile(profile: str) -> Path:
    builders = {
        "core": build_core,
        "adapters-light": build_adapters_light,
        "qoder-addon": build_qoder_addon,
        "qoder-plugin": build_qoder_plugin,
        "qoderworkcn-plugin": build_qoderworkcn_plugin,
        "singlefile": build_singlefile,
        "source-dev": build_source_dev,
        "zcode-plugin": build_zcode_plugin,
        "ui-client": build_ui_client,
    }
    return builders[profile]()


def archive_name(profile: str) -> str:
    return f"engineering-calculation-system-{profile}-v{VERSION}.zip"


def target_slug(name: str) -> str:
    return "".join(char if char.isalnum() else "-" for char in name).strip("-")


def release_archive_name(target: BundleTarget) -> str:
    return f"{PACKAGE_PREFIX}-{target_slug(target.name)}-v{VERSION}.zip"


def release_package_root_name(target: BundleTarget) -> str:
    return f"{PACKAGE_PREFIX}-{target_slug(target.name)}-v{VERSION}"


def target_install_folder(target: BundleTarget) -> str:
    if target.payload_at_root:
        return "."
    return Path(target.path).name


def write_zip(source_root: Path, archive_path: Path, *, archive_root_name: str | None = None) -> None:
    files = iter_files(source_root, include_indexes=True)
    with zipfile.ZipFile(archive_path, "w") as archive:
        for file in files:
            rel = file.relative_to(source_root).as_posix()
            if archive_root_name:
                rel = f"{archive_root_name}/{rel}"
            info = zipfile.ZipInfo(rel, date_time=(2026, 6, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, file.read_bytes())


def bundle_path(root: Path, rel: str) -> Path:
    return root / Path(rel)


def profile_path(profile_roots: dict[str, Path], copy: BundleCopy) -> Path:
    base = profile_roots[copy.profile]
    if copy.source == ".":
        return base
    return base / copy.source


def apply_bundle_copy(profile_roots: dict[str, Path], copy: BundleCopy, dst_root: Path) -> None:
    src = profile_path(profile_roots, copy)
    dst = bundle_path(dst_root, copy.target)
    if copy.is_file:
        copy_file(src, dst)
    else:
        copy_tree(src, dst)


def published_targets() -> tuple[BundleTarget, ...]:
    by_name = {target.name: target for target in CLASSIFIED_TARGETS}
    return tuple(by_name[name] for name in PUBLISH_TARGET_NAMES)


def write_target_install_guide(package_root: Path, target: BundleTarget, install_folder: str) -> None:
    lines = [
        f"# Engineering Calculation System v{VERSION} - {target.name}",
        "",
        f"This package is prepared for {target.name}.",
        "",
        target.install_text,
        "",
        "```text",
        f"{install_folder}/",
        "```",
        "",
    ]
    for note in target.notes:
        lines.extend([note, ""])
    (package_root / "INSTALL.md").write_text("\n".join(lines), encoding="utf-8")


def write_minimax_readmes(payload_root: Path) -> None:
    """Write repo-root guides for MiniMax Code local and Github import flows."""
    readme = f"""# Engineering Calculation System for MiniMax Code

This package is prepared as a MiniMax Code skills repository.

## Local Install

For a local MiniMax Code / Mavis install on Windows:

1. Unzip this archive.
2. Copy `skills/engineering-calculation-system/` to:

```text
%USERPROFILE%\\.mavis\\skills\\engineering-calculation-system\\
```

3. Restart MiniMax Code, or verify from PowerShell:

```powershell
& "$env:USERPROFILE\\.mavis\\bin\\mavis.cmd" skill list
& "$env:USERPROFILE\\.mavis\\bin\\mavis.cmd" skill show engineering-calculation-system
```

If your MiniMax Code / Mavis build reports a different user skill root, use the reported root.

## Delivery Contract

For implementation or release work, the skill must use:

```text
shared/lifecycle.md
shared/execution-discipline.md
shared/planning-discipline.md
shared/review-feedback-discipline.md
shared/version-control-discipline.md
shared/completion-evidence.md
shared/systematic-debugging.md
```

Use route cards, gate cards, artifact contracts, validation evidence, and the
completion evidence matrix before making completion claims. Long tasks should
resume from `.engineering-calc/work/progress.md` when available.

`web-complete` means dual closure: a readable print-ready A4 HTML calculation
book with real input, non-empty `BookResult.checks`, and useful charts when
chartable values exist, plus a complete web system with API/UI, import/export,
batch, deployment artifacts, and smoke tests. The MiniMaxCode entrypoint must
use the full core package, project template, and validator before making a
production completion claim.

## Import from Github

1. Unzip this archive.
2. Publish the unzipped contents as a Github repository root.
3. In MiniMax Code, open Skills, choose Create, then Import from Github.
4. Paste the repository URL.

The skill entry is:

```text
skills/engineering-calculation-system/SKILL.md
```

## Smoke Prompt

After import, start a task with:

```text
Use engineering-calculation-system to create a web-complete engineering calculation scaffold with capability detection, Marimo optional review, and HTML/LaTeX report export.
```

## Validation

When the package is available on disk, validate it with:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core
```
"""
    readme_zh = f"""# MiniMax Code Engineering Calculation System

This ASCII guide replaces the previous encoded Chinese fallback to avoid mojibake in strict package validation.

Use `skills/engineering-calculation-system/SKILL.md` as the skill entrypoint. For implementation or release work, load `shared/lifecycle.md`, `shared/execution-discipline.md`, `shared/planning-discipline.md`, `shared/review-feedback-discipline.md`, `shared/version-control-discipline.md`, `shared/completion-evidence.md`, and `shared/systematic-debugging.md`.

Use route cards, gate cards, artifact contracts, validation evidence, and `.engineering-calc/work/progress.md` for long-task resume.

`web-complete` means dual closure: a readable print-ready A4 HTML calculation book with real input, non-empty `BookResult.checks`, and useful charts when chartable values exist, plus a complete web system with API/UI, import/export, batch, deployment artifacts, and smoke tests.

Validate before completion:

```bash
python skills/engineering-calculation-system/scripts/validate_artifacts.py --package-root skills/engineering-calculation-system --profile core
```
"""
    (payload_root / "README.md").write_text(readme, encoding="utf-8")
    (payload_root / "README_zh.md").write_text(readme_zh, encoding="utf-8")


def merge_core_into(dst: Path, profile_roots: dict[str, Path]) -> None:
    copy_tree(profile_roots["core"] / "engineering-calculation-system", dst)


def merge_adapter_docs_into(dst: Path, profile_roots: dict[str, Path]) -> None:
    copy_tree(profile_roots["adapters-light"] / "adapters", dst / "adapters")


def stage_target_payload(profile_roots: dict[str, Path], target: BundleTarget, payload_root: Path) -> None:
    if target.include_core:
        merge_core_into(payload_root, profile_roots)
    if target.include_adapter_docs:
        merge_adapter_docs_into(payload_root, profile_roots)
    for copy in target.copies:
        apply_bundle_copy(profile_roots, copy, payload_root)
    if target.name == "MiniMaxCode":
        write_minimax_readmes(payload_root)


def validate_target_payload(target: BundleTarget, payload_root: Path) -> None:
    context = f"{target.name} payload"
    if target.name in {"QODER", "QoderCN Cloud Agents"}:
        require_paths(
            payload_root,
            [
                "SKILL.md",
                "reference.md",
                "qoder_quickstart.md",
                "assets/lifecycle-console.html",
            ],
            context=context,
        )
        require_text(
            payload_root / "SKILL.md",
            [
                "QODER-Project",
                "web-complete",
                "Stable ASCII Contract",
                "shared/lifecycle.md",
                "shared/execution-discipline.md",
                "shared/planning-discipline.md",
                "shared/review-feedback-discipline.md",
                "shared/version-control-discipline.md",
                "shared/completion-evidence.md",
                "shared/systematic-debugging.md",
                "dual closure",
                "qoder_quickstart.md",
            ],
            context=context,
        )
        require_text(
            payload_root / "qoder_quickstart.md",
            [
                "Qoder Package Self-Check",
                "Direct QODER Skill",
                "QODER Project overlay",
                "Complete core project",
                "Behavior Engineering Layer",
                "shared/execution-discipline.md",
                "shared/planning-discipline.md",
                "shared/review-feedback-discipline.md",
                "shared/version-control-discipline.md",
                "shared/completion-evidence.md",
                "Static Report Triage",
                "static_report_or_cli_only",
                "A4 HTML First",
                "print-ready A4 HTML",
            ],
            context=context,
        )
        require_text(
                payload_root / "assets" / "lifecycle-console.html",
                [
                f"v{VERSION}",
                "12a",
                "12b",
                "12c",
                "14",
            ],
            context=context,
        )
        return

    if target.name == "MiniMaxCode":
        require_paths(
            payload_root,
            [
                "README.md",
                "README_zh.md",
                "skills/engineering-calculation-system/SKILL.md",
                "skills/engineering-calculation-system/shared/lifecycle.md",
                "skills/engineering-calculation-system/shared/execution-discipline.md",
                "skills/engineering-calculation-system/shared/planning-discipline.md",
                "skills/engineering-calculation-system/shared/review-feedback-discipline.md",
                "skills/engineering-calculation-system/shared/version-control-discipline.md",
                "skills/engineering-calculation-system/shared/completion-evidence.md",
                "skills/engineering-calculation-system/shared/systematic-debugging.md",
                "skills/engineering-calculation-system/templates/orchestration/task_brief.md",
                "skills/engineering-calculation-system/templates/orchestration/task_review.md",
                "skills/engineering-calculation-system/templates/orchestration/progress_ledger.md",
                "skills/engineering-calculation-system/scripts/validate_artifacts.py",
                "skills/engineering-calculation-system/scripts/ecs_execution.py",
                "skills/engineering-calculation-system/project_template/engineering_calc_project/src/pkg/core/capabilities.py",
            ],
            context=context,
        )
        require_text(
            payload_root / "skills/engineering-calculation-system/SKILL.md",
            [
                "name: engineering-calculation-system",
                "shared/lifecycle.md",
                "shared/execution-discipline.md",
                "shared/planning-discipline.md",
                "shared/review-feedback-discipline.md",
                "shared/version-control-discipline.md",
                "shared/completion-evidence.md",
                "dual closure",
                "run_book(BookInput) -> BookResult",
            ],
            context=context,
        )
        require_text(
            payload_root / "README.md",
            [
                "Local Install",
                "Import from Github",
                "%USERPROFILE%\\.mavis\\skills\\engineering-calculation-system\\",
                "skills/engineering-calculation-system/SKILL.md",
                "shared/lifecycle.md",
                "shared/execution-discipline.md",
                "shared/planning-discipline.md",
                "shared/review-feedback-discipline.md",
                "shared/version-control-discipline.md",
                "shared/completion-evidence.md",
                "dual closure",
                "BookResult.checks",
            ],
            context=context,
        )
        return

    if target.name == "ZCode":
        require_paths(payload_root, ZCODE_PLUGIN_REQUIRED_PATHS, context=context)
        require_text(
            payload_root / ".zcode-plugin" / "plugin.json",
            [
                ZCODE_PLUGIN_NAME,
                "\"skills\": \"skills\"",
                f"\"entrypoint\": \"{ZCODE_SKILL_ENTRYPOINT}\"",
            ],
            context=context,
        )
        require_text(
            payload_root / "marketplace.json",
            [
                "\"source\": \".\"",
                ZCODE_PLUGIN_NAME,
            ],
            context=context,
        )
        require_text(
            payload_root / Path(ZCODE_SKILL_ENTRYPOINT),
            ZCODE_SKILL_REQUIRED_PHRASES,
            context=context,
        )
        require_text(
            payload_root / Path(ZCODE_SKILL_ROOT) / "shared" / "zcode-plugin-adapter.md",
            ZCODE_ADAPTER_REQUIRED_PHRASES,
            context=context,
        )
        return

    if target.name == "Qoder CLI Plugin":
        validate_qoder_plugin(payload_root, context=context)
        return

    if target.name in {"QoderWorkCN", "WorkBuddy"}:
        validate_qoderworkcn_plugin(payload_root, context=context)
        return

    if target.include_core:
        require_paths(
            payload_root,
            [
                "SKILL.md",
                "skills/00-engineering-calculation-router.skill.md",
                "shared/lifecycle.md",
                "shared/execution-discipline.md",
                "shared/planning-discipline.md",
                "shared/review-feedback-discipline.md",
                "shared/version-control-discipline.md",
                "shared/completion-evidence.md",
                "shared/systematic-debugging.md",
                "templates/orchestration/task_brief.md",
                "templates/orchestration/task_review.md",
                "templates/orchestration/progress_ledger.md",
                "templates/implementation/ui_layout_spec.md",
                "schemas/artifact_contracts.json",
                "scripts/validate_artifacts.py",
                "scripts/ecs_execution.py",
                "project_template/engineering_calc_project/webapp/routes.py",
                "project_template/engineering_calc_project/webapp/i18n.py",
                "project_template/engineering_calc_project/webapp/templates/base.html",
                "project_template/engineering_calc_project/webapp/templates/partials/_topbar.html",
                "project_template/engineering_calc_project/webapp/static/js/i18n.js",
                "project_template/engineering_calc_project/deploy/one_click_deploy.sh",
                "project_template/engineering_calc_project/deploy/Dockerfile",
                "project_template/engineering_calc_project/release/runbook.md",
                "project_template/engineering_calc_project/tests/smoke/test_web_routes.py",
            ],
            context=context,
        )
        require_text(
            payload_root / "SKILL.md",
            [
                "shared/lifecycle.md",
                "shared/execution-discipline.md",
                "shared/planning-discipline.md",
                "shared/review-feedback-discipline.md",
                "shared/version-control-discipline.md",
                "shared/completion-evidence.md",
                "dual closure",
            ],
            context=context,
        )
        require_text(
            payload_root / "shared/lifecycle.md",
            [
                "Engineering Calculation Lifecycle",
                "Web-Complete Exit Gate",
                "BookResult.checks",
            ],
            context=context,
        )
        require_text(
            payload_root / "shared/execution-discipline.md",
            [
                "Route Card",
                "Gate Card",
                "Artifact Contract",
                "Validation Evidence",
            ],
            context=context,
        )
        require_text(
            payload_root / "shared/planning-discipline.md",
            [
                "Planning Discipline",
                "exact_files",
                "stop_conditions",
            ],
            context=context,
        )
        require_text(
            payload_root / "shared/review-feedback-discipline.md",
            [
                "Review Feedback Discipline",
                "source_authority_impact",
                "route_upstream",
            ],
            context=context,
        )
        require_text(
            payload_root / "shared/version-control-discipline.md",
            [
                "Version Control Discipline",
                "baseline_validation",
                "platform acceptance report",
            ],
            context=context,
        )
        require_text(
            payload_root / "shared/completion-evidence.md",
            [
                "Evidence Matrix",
                "`web-complete`",
                "`bug fixed`",
            ],
            context=context,
        )
        require_text(
            payload_root / "project_template/engineering_calc_project/webapp/templates/partials/_topbar.html",
            [
                "id=\"langToggle\"",
                "data-lang=\"en\"",
                "data-lang=\"zh\"",
            ],
            context=context,
        )
        require_text(
            payload_root / "project_template/engineering_calc_project/deploy/one_click_deploy.sh",
            [
                "docker compose up -d --build",
                "ADMIN_REVIEW_PASSWORD",
                "marimo run apps/review/admin_formula_review.py",
            ],
            context=context,
        )
        require_text(
            payload_root / "project_template/engineering_calc_project/webapp/static/js/i18n.js",
            [
                "localStorage",
                "document.documentElement.lang",
                "setLanguage",
            ],
            context=context,
        )

    platform_required = {
        "QODER Project": [
            ".qoder/skills/engineering-calc-system/SKILL.md",
            ".qoder/skills/engineering-calc-system/reference.md",
            ".qoder/skills/engineering-calc-system/qoder_quickstart.md",
            ".qoder/skills/engineering-calc-system/assets/lifecycle-console.html",
            ".qoder/agents/engineering-calc-system.md",
            ".qoder/agents/engineering-calc-reference-acquirer.md",
            ".qoder/agents/engineering-calc-source-intake.md",
            ".qoder/agents/engineering-calc-logic-extractor.md",
            ".qoder/agents/engineering-calc-module-worker.md",
            ".qoder/agents/engineering-calc-interface-worker.md",
            ".qoder/agents/engineering-calc-verification-worker.md",
            ".qoder/agents/engineering-calc-release-worker.md",
            ".qoder/references/engineering-calc-system.md",
        ],
        "QoderCN": [
            "skills/engineering-calc-system/SKILL.md",
            "skills/engineering-calc-system/reference.md",
            "skills/engineering-calc-system/qoder_quickstart.md",
            "skills/engineering-calc-system/assets/lifecycle-console.html",
            "agents/engineering-calc-system.md",
            "agents/engineering-calc-reference-acquirer.md",
            "agents/engineering-calc-source-intake.md",
            "agents/engineering-calc-logic-extractor.md",
            "agents/engineering-calc-module-worker.md",
            "agents/engineering-calc-interface-worker.md",
            "agents/engineering-calc-verification-worker.md",
            "agents/engineering-calc-release-worker.md",
            "references/engineering-calc-system.md",
        ],
        "QoderCN Project": [
            ".lingma/skills/engineering-calc-system/SKILL.md",
            ".lingma/skills/engineering-calc-system/reference.md",
            ".lingma/skills/engineering-calc-system/qoder_quickstart.md",
            ".lingma/skills/engineering-calc-system/assets/lifecycle-console.html",
            ".lingma/agents/engineering-calc-system.md",
            ".lingma/agents/engineering-calc-reference-acquirer.md",
            ".lingma/agents/engineering-calc-source-intake.md",
            ".lingma/agents/engineering-calc-logic-extractor.md",
            ".lingma/agents/engineering-calc-module-worker.md",
            ".lingma/agents/engineering-calc-interface-worker.md",
            ".lingma/agents/engineering-calc-verification-worker.md",
            ".lingma/agents/engineering-calc-release-worker.md",
            ".lingma/references/engineering-calc-system.md",
        ],
        "QoderCN CLI": [
            ".qoder-cn/skills/engineering-calc-system/SKILL.md",
            ".qoder-cn/skills/engineering-calc-system/reference.md",
            ".qoder-cn/skills/engineering-calc-system/qoder_quickstart.md",
            ".qoder-cn/skills/engineering-calc-system/assets/lifecycle-console.html",
            ".qodercn/agents/engineering-calc-system.md",
            ".qodercn/agents/engineering-calc-reference-acquirer.md",
            ".qodercn/agents/engineering-calc-source-intake.md",
            ".qodercn/agents/engineering-calc-logic-extractor.md",
            ".qodercn/agents/engineering-calc-module-worker.md",
            ".qodercn/agents/engineering-calc-interface-worker.md",
            ".qodercn/agents/engineering-calc-verification-worker.md",
            ".qodercn/agents/engineering-calc-release-worker.md",
            ".qodercn/references/engineering-calc-system.md",
        ],
        "QoderCN CLI Project": [
            ".qoder/skills/engineering-calc-system/SKILL.md",
            ".qoder/skills/engineering-calc-system/reference.md",
            ".qoder/skills/engineering-calc-system/qoder_quickstart.md",
            ".qoder/skills/engineering-calc-system/assets/lifecycle-console.html",
            ".qodercn/agents/engineering-calc-system.md",
            ".qodercn/agents/engineering-calc-reference-acquirer.md",
            ".qodercn/agents/engineering-calc-source-intake.md",
            ".qodercn/agents/engineering-calc-logic-extractor.md",
            ".qodercn/agents/engineering-calc-module-worker.md",
            ".qodercn/agents/engineering-calc-interface-worker.md",
            ".qodercn/agents/engineering-calc-verification-worker.md",
            ".qodercn/agents/engineering-calc-release-worker.md",
            ".qodercn/references/engineering-calc-system.md",
        ],
        "TRAE": [
            ".trae/project_rules.md",
            ".trae/rules/engineering-calc-system.md",
        ],
        "OpenCode": [
            ".opencode/skills/engineering-calc-system/SKILL.md",
        ],
        "AGENTS Generic": [
            "AGENTS.md",
            ".agents/skills/engineering-calc-system/SKILL.md",
        ],
    }
    if target.name in platform_required:
        require_paths(payload_root, platform_required[target.name], context=context)
        if target.name == "QODER Project":
            require_text(
                payload_root / ".qoder" / "skills" / "engineering-calc-system" / "assets" / "lifecycle-console.html",
                [f"v{VERSION}", "12a", "12b", "12c", "14"],
                context=context,
            )
            require_text(
                payload_root / ".qoder" / "agents" / "engineering-calc-system.md",
                ["Behavior Engineering Layer", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md", "static_report_or_cli_only", "reports/*.html"],
                context=context,
            )
            require_text(
                payload_root / ".qoder" / "skills" / "engineering-calc-system" / "qoder_quickstart.md",
                [
                    "Behavior Engineering Layer",
                    "shared/execution-discipline.md",
                    "shared/planning-discipline.md",
                    "shared/review-feedback-discipline.md",
                    "shared/version-control-discipline.md",
                    "shared/completion-evidence.md",
                    "Static Report Triage",
                    "static_report_or_cli_only",
                    "A4 HTML First",
                    "print-ready A4 HTML",
                ],
                context=context,
            )
        if target.name == "QoderCN":
            require_text(
                payload_root / "skills" / "engineering-calc-system" / "assets" / "lifecycle-console.html",
                [f"v{VERSION}", "12a", "12b", "12c", "14"],
                context=context,
            )
            require_text(
                payload_root / "skills" / "engineering-calc-system" / "qoder_quickstart.md",
                ["Behavior Engineering Layer", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md"],
                context=context,
            )
            require_text(
                payload_root / "agents" / "engineering-calc-system.md",
                ["Behavior Engineering Layer", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md", "static_report_or_cli_only", "reports/*.html"],
                context=context,
            )
        if target.name == "QoderCN Project":
            require_text(
                payload_root / ".lingma" / "skills" / "engineering-calc-system" / "assets" / "lifecycle-console.html",
                [f"v{VERSION}", "12a", "12b", "12c", "14"],
                context=context,
            )
            require_text(
                payload_root / ".lingma" / "skills" / "engineering-calc-system" / "qoder_quickstart.md",
                ["Behavior Engineering Layer", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md"],
                context=context,
            )
            require_text(
                payload_root / ".lingma" / "agents" / "engineering-calc-system.md",
                ["Behavior Engineering Layer", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md", "static_report_or_cli_only", "reports/*.html"],
                context=context,
            )
        if target.name == "QoderCN CLI":
            require_text(
                payload_root / ".qoder-cn" / "skills" / "engineering-calc-system" / "assets" / "lifecycle-console.html",
                [f"v{VERSION}", "12a", "12b", "12c", "14"],
                context=context,
            )
            require_text(
                payload_root / ".qoder-cn" / "skills" / "engineering-calc-system" / "qoder_quickstart.md",
                ["Behavior Engineering Layer", "QoderCN CLI", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md"],
                context=context,
            )
            require_text(
                payload_root / ".qodercn" / "agents" / "engineering-calc-system.md",
                ["Behavior Engineering Layer", "QoderCN CLI", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md", "static_report_or_cli_only", "reports/*.html"],
                context=context,
            )
        if target.name == "QoderCN CLI Project":
            require_text(
                payload_root / ".qoder" / "skills" / "engineering-calc-system" / "assets" / "lifecycle-console.html",
                [f"v{VERSION}", "12a", "12b", "12c", "14"],
                context=context,
            )
            require_text(
                payload_root / ".qoder" / "skills" / "engineering-calc-system" / "qoder_quickstart.md",
                ["Behavior Engineering Layer", "QoderCN CLI", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md"],
                context=context,
            )
            require_text(
                payload_root / ".qodercn" / "agents" / "engineering-calc-system.md",
                ["Behavior Engineering Layer", "QoderCN CLI", "shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "progress.md", "static_report_or_cli_only", "reports/*.html"],
                context=context,
            )

    if target.include_adapter_docs:
        require_paths(
            payload_root,
            [
                "adapters/agent-entrypoints.md",
                "adapters/mcp-recommendations.md",
            ],
            context=context,
        )
        require_text(
            payload_root / "adapters" / "agent-entrypoints.md",
            [
                "shared/execution-discipline.md",
                "shared/planning-discipline.md",
                "shared/review-feedback-discipline.md",
                "shared/version-control-discipline.md",
                "shared/completion-evidence.md",
                "shared/systematic-debugging.md",
                "progress_ledger.md",
            ],
            context=context,
        )

    platform_text_checks = {
        "TRAE": [
            (".trae/project_rules.md", ["shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "shared/systematic-debugging.md", "progress.md"]),
            (".trae/rules/engineering-calc-system.md", ["shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "shared/systematic-debugging.md", "progress.md"]),
        ],
        "OpenCode": [
            (".opencode/skills/engineering-calc-system/SKILL.md", ["shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "systematic-debugging.md", "progress.md"]),
        ],
        "AGENTS Generic": [
            ("AGENTS.md", ["shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "shared/systematic-debugging.md", "progress.md"]),
            (".agents/skills/engineering-calc-system/SKILL.md", ["shared/execution-discipline.md", "shared/planning-discipline.md", "shared/review-feedback-discipline.md", "shared/version-control-discipline.md", "shared/completion-evidence.md", "systematic-debugging.md", "progress.md"]),
        ],
    }
    for rel_path, phrases in platform_text_checks.get(target.name, []):
        require_text(payload_root / rel_path, phrases, context=context)


def build_platform_package(profile_roots: dict[str, Path], target: BundleTarget, package_root: Path) -> Path:
    missing = [profile for profile in RELEASE_REQUIRED_PROFILES if profile not in profile_roots]
    if missing:
        raise RuntimeError(f"release package requires profiles: {', '.join(missing)}")

    if package_root.exists():
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True, exist_ok=True)

    install_folder = target_install_folder(target)
    payload_root = package_root if target.payload_at_root else package_root / install_folder
    stage_target_payload(profile_roots, target, payload_root)
    sync_frontmatter_versions(package_root)
    assert_frontmatter_versions(package_root)
    validate_target_payload(target, payload_root)
    if target.include_install_guide:
        write_target_install_guide(package_root, target, install_folder)
    return package_root


def write_release_index(archives: list[ReleaseArchive]) -> None:
    lines = [
        "# Engineering Calculation System Release Bundles",
        "",
        f"Version: {VERSION}",
        f"Created at: {CREATED_AT}",
        "",
        "## Publish Files",
        "",
        "| Target | Archive | Install Folder | Files | Size KB | SHA256 |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for item in archives:
        lines.append(
            f"| {item.target.name} | `{item.archive_path.name}` | "
            f"`{item.install_folder}/` | {item.file_count} | "
            f"{item.archive_path.stat().st_size / 1024:.1f} | `{sha256(item.archive_path)}` |"
        )
    lines.extend(
        [
            "",
            "## Install",
            "",
        ]
    )
    for item in archives:
        lines.extend(
            [
                f"### {item.target.name}",
                "",
                item.target.install_text,
                "",
                "```text",
                f"{item.install_folder}/",
                "```",
                "",
            ]
        )
        for note in item.target.notes:
            lines.extend([note, ""])
    lines.extend(
        [
            "## Non-Published Build Outputs",
            "",
            "`dist/singlefile/` and `dist/source-dev/` are still generated for fallback and development use, but they are not part of the default platform publish packages.",
            "",
        ]
    )
    (RELEASE_ROOT / "RELEASE_INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def canonical_docs_summary(target: BundleTarget) -> str:
    if target.name in {"QODER", "QoderCN Cloud Agents"}:
        return "Text reminders only; direct skill must route to QODER Project or complete core package."
    if target.name in {"QoderCN", "QoderCN CLI"}:
        return "Text reminders only in user-level overlay; project/core package required for web-complete."
    if target.name in {"Qoder CLI Plugin", "QoderWorkCN", "WorkBuddy"}:
        return "Bundled under skills/engineering-calculation-system/shared/."
    if target.name == "MiniMaxCode":
        return "Bundled under skills/engineering-calculation-system/shared/."
    if target.name == "ZCode":
        return "Bundled under plugin skills/engineering-calculation-system/shared/."
    return "Bundled at package root under shared/."


def write_platform_acceptance_report(archives: list[ReleaseArchive]) -> None:
    lines = [
        "# Platform Acceptance Matrix",
        "",
        f"Version: {VERSION}",
        f"Created at: {CREATED_AT}",
        "",
        "This report records the platform entrypoint, canonical behavior docs, adapter reminder, and fallback path for each published archive.",
        "",
        "## Canonical Behavior Docs",
        "",
        *[f"- `{doc}`" for doc in CANONICAL_BEHAVIOR_DOCS],
        "",
        "## Published Platforms",
        "",
        "| Target | Archive | Entrypoint | Canonical Docs | Adapter Reminder | Missing Capability Fallback |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in archives:
        target = item.target
        entrypoint = PLATFORM_ENTRYPOINTS.get(target.name, "SKILL.md")
        adapter = "Use platform entrypoint, then root SKILL/router and canonical shared docs."
        if target.name in {"QODER Project", "QoderCN Project", "QoderCN CLI Project"}:
            adapter = "Agent-first supervisor; skill wrapper is the resource layer."
        elif target.name in {"QODER", "QoderCN", "QoderCN CLI", "QoderCN Cloud Agents"}:
            adapter = "Lightweight skill/resource entrypoint; do not claim web-complete alone."
        elif target.name == "Qoder CLI Plugin":
            adapter = "Official .qoder-plugin layout for Qoder CLI; bundled full core skill is the production layer."
        elif target.name == "QoderWorkCN":
            adapter = "Official .qoder-plugin expert-kit layout with QoderWork CN-native agents, skills, references, and quick-entry docs."
        elif target.name == "WorkBuddy":
            adapter = "WorkBuddy-ready .qoder-plugin expert-kit layout with skills, expert agents, references, and quick-entry docs."
        elif target.name == "MiniMaxCode":
            adapter = "Repository skill layout under skills/engineering-calculation-system."
        elif target.name == "ZCode":
            adapter = "Plugin-managed skill component; enable from ZCode Plugins, then use plugin skills."
        fallback = PLATFORM_FALLBACKS.get(
            target.name,
            "Use dist/singlefile/engineering-calculation-system.all-in-one.md if multi-file loading is unavailable.",
        )
        lines.append(
            f"| {target.name} | `{item.archive_path.name}` | `{entrypoint}` | "
            f"{canonical_docs_summary(target)} | {adapter} | {fallback} |"
        )
    lines.append("")
    (RELEASE_ROOT / "PLATFORM_ACCEPTANCE.md").write_text("\n".join(lines), encoding="utf-8")


def build_split_archives(built_profiles: dict[str, Path]) -> list[Path]:
    split_root = RELEASE_ROOT / "split-archives"
    split_root.mkdir(parents=True, exist_ok=True)
    archives: list[Path] = []
    for profile, profile_root in built_profiles.items():
        archive_path = split_root / archive_name(profile)
        write_zip(profile_root, archive_path)
        archives.append(archive_path)
    return archives


def build_release_packages(
    built_profiles: dict[str, Path],
    *,
    split_archives: bool = False,
) -> list[ReleaseArchive]:
    clean_dir(RELEASE_ROOT)
    archives: list[ReleaseArchive] = []
    with tempfile.TemporaryDirectory(prefix="ecs-release-") as temp_dir:
        temp_root = Path(temp_dir)
        for target in published_targets():
            package_name = release_package_root_name(target)
            package_root = build_platform_package(built_profiles, target, temp_root / package_name)
            archive_path = RELEASE_ROOT / release_archive_name(target)
            archive_root_name = None if target.payload_at_root else package_root.name
            write_zip(package_root, archive_path, archive_root_name=archive_root_name)
            archives.append(
                ReleaseArchive(
                    target=target,
                    archive_path=archive_path,
                    install_folder=target_install_folder(target),
                    file_count=len(iter_files(package_root, include_indexes=True)),
                )
            )

    checksum_lines = [f"{sha256(item.archive_path)}  {item.archive_path.name}" for item in archives]
    if split_archives:
        for archive in build_split_archives(built_profiles):
            checksum_lines.append(f"{sha256(archive)}  split-archives/{archive.name}")
    (RELEASE_ROOT / "CHECKSUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    write_release_index(archives)
    write_platform_acceptance_report(archives)
    return archives


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        choices=PROFILE_CHOICES,
        action="append",
        help="Release profile to build. May be passed more than once.",
    )
    parser.add_argument("--all", action="store_true", help="Build every release profile")
    parser.add_argument(
        "--archives",
        action="store_true",
        help="Also create platform release zip packages under dist/release",
    )
    parser.add_argument(
        "--no-archives",
        action="store_true",
        help="Do not create platform release zip packages when building every profile",
    )
    parser.add_argument(
        "--split-archives",
        action="store_true",
        help="Also create legacy per-profile zip archives under dist/release/split-archives",
    )
    parser.add_argument(
        "--no-ui-client",
        action="store_true",
        help="Skip the ui-client profile (the PyInstaller exe build) when building all profiles. "
        "Has no effect when --profile ui-client is passed explicitly.",
    )
    args = parser.parse_args(argv)

    if args.profile and args.all:
        parser.error("use either --profile or --all, not both")
    if args.archives and args.no_archives:
        parser.error("use either --archives or --no-archives, not both")

    default_publish = not args.profile and not args.all
    profiles = DEFAULT_ALL_PROFILES if args.all or default_publish else tuple(args.profile or ())
    # --no-ui-client drops the (slow, PyInstaller-dependent) exe build from the
    # default all-profiles set, but never blocks an explicit --profile ui-client.
    if args.no_ui_client and not args.profile:
        profiles = tuple(p for p in profiles if p != "ui-client")
    create_archives = args.archives or ((args.all or default_publish) and not args.no_archives)

    if default_publish:
        print("no profile specified; building all profiles and platform release packages")

    built: dict[str, Path] = {}
    for profile in profiles:
        built[profile] = build_profile(profile)

    for path in built.values():
        files = iter_files(path)
        total_kb = sum(file.stat().st_size for file in files) / 1024
        print(f"built {path.relative_to(REPO_ROOT).as_posix()} ({len(files)} files, {total_kb:.1f} KB)")

    if create_archives:
        if set(RELEASE_REQUIRED_PROFILES) - set(built):
            missing = ", ".join(sorted(set(RELEASE_REQUIRED_PROFILES) - set(built)))
            raise RuntimeError(f"platform release packages require all profiles; missing: {missing}")
        archives = build_release_packages(built, split_archives=args.split_archives)
        print(f"built {RELEASE_ROOT.relative_to(REPO_ROOT).as_posix()} ({len(archives)} platform archives)")
        for archive in archives:
            print(
                f"  {archive.archive_path.name} "
                f"({archive.file_count} files, {archive.archive_path.stat().st_size / 1024:.1f} KB)"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
