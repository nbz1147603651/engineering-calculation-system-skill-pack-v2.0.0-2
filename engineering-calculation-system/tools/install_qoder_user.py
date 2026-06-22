#!/usr/bin/env python3
"""Install or uninstall the Qoder overlay in the current user's .qoder directory."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_QODER = REPO_ROOT / "dist" / "qoder-addon" / ".qoder"
EXPECTED_AGENT_FILES = (
    "engineering-calc-system.md",
    "engineering-calc-reference-acquirer.md",
    "engineering-calc-source-intake.md",
    "engineering-calc-logic-extractor.md",
    "engineering-calc-module-worker.md",
    "engineering-calc-interface-worker.md",
    "engineering-calc-verification-worker.md",
    "engineering-calc-release-worker.md",
)
EXPECTED_SKILL_FILES = (
    "SKILL.md",
    "reference.md",
    "qoder_quickstart.md",
    "assets/lifecycle-console.html",
)
EXPECTED_REFERENCE_FILES = (
    "engineering-calc-system.md",
)
MANAGED_SKILL_DIR = "engineering-calc-system"
MANAGED_REFERENCE_FILE = "engineering-calc-system.md"
DEPRECATED_AGENT_FILES = ("reference.md",)
DEPRECATED_SKILL_DIRS = ("engineering-calculation-system",)


def default_qoder_home() -> Path:
    configured = os.environ.get("QODER_HOME")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".qoder"


def build_qoder_addon() -> None:
    subprocess.run(
        [sys.executable, "tools/build_release.py", "--profile", "qoder-addon"],
        cwd=REPO_ROOT,
        check=True,
    )


def install_qoder_overlay(source: Path, target: Path, *, dry_run: bool) -> None:
    if not source.exists():
        raise FileNotFoundError(
            f"Qoder overlay not found: {source}. Run with --build or build releases first."
        )
    for name in ("agents", "skills", "references"):
        src_dir = source / name
        if not src_dir.exists():
            continue
        dst_dir = target / name
        print(f"{'would copy' if dry_run else 'copy'} {src_dir} -> {dst_dir}")
        if not dry_run:
            dst_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

    for name in DEPRECATED_AGENT_FILES:
        deprecated = target / "agents" / name
        print(f"{'would remove' if dry_run else 'remove if present'} {deprecated}")
        if not dry_run and deprecated.exists():
            deprecated.unlink()
    for name in DEPRECATED_SKILL_DIRS:
        deprecated = target / "skills" / name
        print(f"{'would remove tree' if dry_run else 'remove tree if present'} {deprecated}")
        if not dry_run and deprecated.exists():
            shutil.rmtree(deprecated)


def verify_qoder_overlay(target: Path, *, dry_run: bool) -> None:
    agents_dir = target / "agents"
    skill_dir = target / "skills" / MANAGED_SKILL_DIR
    references_dir = target / "references"
    missing = [name for name in EXPECTED_AGENT_FILES if not (agents_dir / name).exists()]
    missing_skill_files = [name for name in EXPECTED_SKILL_FILES if not (skill_dir / name).exists()]
    missing_reference_files = [name for name in EXPECTED_REFERENCE_FILES if not (references_dir / name).exists()]
    if dry_run:
        print("expected Qoder agents:")
        for name in EXPECTED_AGENT_FILES:
            print(f"  {name}")
        print("expected Qoder skill files:")
        for name in EXPECTED_SKILL_FILES:
            print(f"  skills/{MANAGED_SKILL_DIR}/{name}")
        print("expected Qoder reference files:")
        for name in EXPECTED_REFERENCE_FILES:
            print(f"  references/{name}")
        return
    if missing:
        missing_text = ", ".join(missing)
        raise FileNotFoundError(f"Qoder install is incomplete; missing agents: {missing_text}")
    if missing_skill_files:
        missing_text = ", ".join(missing_skill_files)
        raise FileNotFoundError(f"Qoder install is incomplete; missing skill files: {missing_text}")
    if missing_reference_files:
        missing_text = ", ".join(missing_reference_files)
        raise FileNotFoundError(f"Qoder install is incomplete; missing references: {missing_text}")
    for name in DEPRECATED_AGENT_FILES:
        deprecated = agents_dir / name
        if deprecated.exists():
            raise RuntimeError(f"Deprecated Qoder agent reference remains: {deprecated}")
    print(f"installed {len(EXPECTED_AGENT_FILES)} Qoder agents into {agents_dir}")
    print(f"verified {len(EXPECTED_SKILL_FILES)} Qoder skill files under {skill_dir}")
    print(f"verified {len(EXPECTED_REFERENCE_FILES)} Qoder reference files under {references_dir}")


def remove_empty_directory(path: Path, *, dry_run: bool) -> None:
    if not path.exists() or not path.is_dir():
        return
    try:
        next(path.iterdir())
    except StopIteration:
        print(f"{'would remove empty dir' if dry_run else 'remove empty dir'} {path}")
        if not dry_run:
            path.rmdir()


def uninstall_qoder_overlay(target: Path, *, dry_run: bool) -> None:
    removed = 0
    for name in (*EXPECTED_AGENT_FILES, *DEPRECATED_AGENT_FILES):
        path = target / "agents" / name
        if not path.exists():
            continue
        print(f"{'would remove' if dry_run else 'remove'} {path}")
        removed += 1
        if not dry_run:
            path.unlink()

    skill_dir = target / "skills" / MANAGED_SKILL_DIR
    if skill_dir.exists():
        print(f"{'would remove tree' if dry_run else 'remove tree'} {skill_dir}")
        removed += 1
        if not dry_run:
            shutil.rmtree(skill_dir)
    for name in DEPRECATED_SKILL_DIRS:
        deprecated = target / "skills" / name
        if not deprecated.exists():
            continue
        print(f"{'would remove tree' if dry_run else 'remove tree'} {deprecated}")
        removed += 1
        if not dry_run:
            shutil.rmtree(deprecated)

    reference = target / "references" / MANAGED_REFERENCE_FILE
    if reference.exists():
        print(f"{'would remove' if dry_run else 'remove'} {reference}")
        removed += 1
        if not dry_run:
            reference.unlink()

    for name in ("agents", "skills", "references"):
        remove_empty_directory(target / name, dry_run=dry_run)

    print(f"{'would remove' if dry_run else 'removed'} {removed} managed Qoder entries")


def audit_qoder_overlay(target: Path) -> int:
    agents_dir = target / "agents"
    skills_dir = target / "skills"
    references_dir = target / "references"

    missing_agents = [name for name in EXPECTED_AGENT_FILES if not (agents_dir / name).exists()]
    missing_skill_files = [
        name for name in EXPECTED_SKILL_FILES
        if not (skills_dir / MANAGED_SKILL_DIR / name).exists()
    ]
    missing_reference_files = [
        name for name in EXPECTED_REFERENCE_FILES
        if not (references_dir / name).exists()
    ]
    expected_agents = set(EXPECTED_AGENT_FILES)
    extra_calc_agents = []
    if agents_dir.exists():
        extra_calc_agents = sorted(
            path.name
            for path in agents_dir.glob("engineering-calc*.md")
            if path.name not in expected_agents
        )
    deprecated_agents = [name for name in DEPRECATED_AGENT_FILES if (agents_dir / name).exists()]
    deprecated_skills = [name for name in DEPRECATED_SKILL_DIRS if (skills_dir / name).exists()]

    print(f"Qoder home: {target}")
    print(f"expected agents installed: {len(EXPECTED_AGENT_FILES) - len(missing_agents)}/{len(EXPECTED_AGENT_FILES)}")
    print(f"expected skill files installed: {len(EXPECTED_SKILL_FILES) - len(missing_skill_files)}/{len(EXPECTED_SKILL_FILES)}")
    print(f"expected reference files installed: {len(EXPECTED_REFERENCE_FILES) - len(missing_reference_files)}/{len(EXPECTED_REFERENCE_FILES)}")
    if missing_agents:
        print("missing agents:")
        for name in missing_agents:
            print(f"  {name}")
    if missing_skill_files:
        print("missing skill files:")
        for name in missing_skill_files:
            print(f"  skills/{MANAGED_SKILL_DIR}/{name}")
    if missing_reference_files:
        print("missing reference files:")
        for name in missing_reference_files:
            print(f"  references/{name}")
    if extra_calc_agents:
        print("extra engineering calculation agents:")
        for name in extra_calc_agents:
            print(f"  {name}")
    if deprecated_agents:
        print("deprecated agent files:")
        for name in deprecated_agents:
            print(f"  {name}")
    if deprecated_skills:
        print("deprecated skill directories:")
        for name in deprecated_skills:
            print(f"  {name}")
    clean = not any(
        (
            missing_agents,
            missing_skill_files,
            missing_reference_files,
            extra_calc_agents,
            deprecated_agents,
            deprecated_skills,
        )
    )
    print("audit: clean" if clean else "audit: issues found")
    return 0 if clean else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--qoder-home",
        type=Path,
        default=default_qoder_home(),
        help="Target Qoder user directory. Defaults to QODER_HOME or ~/.qoder.",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build dist/qoder-addon before installing. Ignored with --uninstall.",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove only this package's managed Qoder agents, skill, reference, and deprecated agent reference.",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Check this package's Qoder files for missing entries or redundant legacy files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned filesystem changes without writing.",
    )
    args = parser.parse_args(argv)

    if args.audit:
        return audit_qoder_overlay(args.qoder_home.expanduser())

    if args.uninstall:
        uninstall_qoder_overlay(args.qoder_home.expanduser(), dry_run=args.dry_run)
        return 0

    if args.build:
        build_qoder_addon()
    install_qoder_overlay(DIST_QODER, args.qoder_home.expanduser(), dry_run=args.dry_run)
    verify_qoder_overlay(args.qoder_home.expanduser(), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
