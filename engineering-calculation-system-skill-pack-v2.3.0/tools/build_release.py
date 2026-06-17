#!/usr/bin/env python3
"""Build layered release artifacts for the engineering calculation skill pack."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_SOURCE = REPO_ROOT / "core" / "engineering-calculation-system"
LIGHT_ADAPTER_SOURCE = REPO_ROOT / "adapter_sources" / "light"
QODER_ADAPTER_SOURCE = REPO_ROOT / "adapter_sources" / "qoder"
DIST_ROOT = REPO_ROOT / "dist"
RELEASE_ROOT = DIST_ROOT / "release"
RELEASE_CONFIG_PATH = REPO_ROOT / "tools" / "release_config.json"

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
    copies: tuple[BundleCopy, ...] = ()
    notes: tuple[str, ...] = ()


def load_release_config() -> dict:
    with RELEASE_CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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
    extra_copies: tuple[BundleCopy, ...],
) -> None:
    profiles = set(config["profiles"])
    for field in ("default_all_profiles", "release_required_profiles"):
        unknown = set(config.get(field, ())) - profiles
        if unknown:
            raise ValueError(f"{field} references unknown profile(s): {', '.join(sorted(unknown))}")

    seen_paths: set[str] = set()
    for target in targets:
        validate_rel_path(target.path, f"classified target {target.name} path")
        if target.path in seen_paths:
            raise ValueError(f"duplicate classified target path: {target.path}")
        seen_paths.add(target.path)
        for copy in target.copies:
            validate_bundle_copy(copy, profiles, f"classified target {target.name}")

    for copy in extra_copies:
        validate_bundle_copy(copy, profiles, "extra bundle copy")

    if not config.get("singlefile_prefixes"):
        raise ValueError("singlefile_prefixes must not be empty")
    if not config.get("source_dev_includes"):
        raise ValueError("source_dev_includes must not be empty")


def validate_bundle_copy(copy: BundleCopy, profiles: set[str], context: str) -> None:
    if copy.profile not in profiles:
        raise ValueError(f"{context} references unknown profile: {copy.profile}")
    validate_rel_path(copy.source, f"{context} source", allow_dot=True)
    validate_rel_path(copy.target, f"{context} target")


CONFIG = load_release_config()
VERSION = CONFIG["version"]
CREATED_AT = CONFIG["created_at"]
BUNDLE_NAME = CONFIG.get("bundle_name", f"engineering-calculation-system-release-v{VERSION}")
PROFILE_CHOICES = tuple(CONFIG["profiles"])
DEFAULT_ALL_PROFILES = tuple(CONFIG.get("default_all_profiles", PROFILE_CHOICES))
RELEASE_REQUIRED_PROFILES = tuple(CONFIG.get("release_required_profiles", PROFILE_CHOICES))
SINGLEFILE_PREFIXES = tuple(CONFIG["singlefile_prefixes"])
SOURCE_DEV_INCLUDES = tuple(CONFIG["source_dev_includes"])
CLASSIFIED_TARGETS = tuple(parse_bundle_target(target) for target in CONFIG["classified_targets"])
EXTRA_BUNDLE_COPIES = tuple(parse_bundle_copy(copy) for copy in CONFIG["extra_bundle_copies"])
validate_release_config(CONFIG, CLASSIFIED_TARGETS, EXTRA_BUNDLE_COPIES)


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
    write_indexes(profile_root, "engineering-calculation-system-core")
    return profile_root


def build_adapters_light() -> Path:
    profile_root = DIST_ROOT / "adapters-light"
    clean_dir(profile_root)
    copy_tree(LIGHT_ADAPTER_SOURCE, profile_root)
    write_indexes(profile_root, "engineering-calculation-system-adapters-light")
    return profile_root


def build_qoder_addon() -> Path:
    profile_root = DIST_ROOT / "qoder-addon"
    clean_dir(profile_root)
    copy_tree(QODER_ADAPTER_SOURCE, profile_root)
    write_indexes(profile_root, "engineering-calculation-system-qoder-addon")
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
    write_indexes(profile_root, "engineering-calculation-system-source-dev")
    return profile_root


def build_profile(profile: str) -> Path:
    builders = {
        "core": build_core,
        "adapters-light": build_adapters_light,
        "qoder-addon": build_qoder_addon,
        "singlefile": build_singlefile,
        "source-dev": build_source_dev,
    }
    return builders[profile]()


def archive_name(profile: str) -> str:
    return f"engineering-calculation-system-{profile}-v{VERSION}.zip"


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


def write_install_guide(bundle_root: Path) -> None:
    lines = [
        "# Engineering Calculation System v2.3.0 Release",
        "",
        "This bundle is organized by target agent software. Copy only the folder for the tool you are installing.",
        "",
    ]
    for target in CLASSIFIED_TARGETS:
        lines.extend(
            [
                f"## {target.name}",
                "",
                target.install_text,
                "",
                "```text",
                f"{target.path}/",
                "```",
                "",
            ]
        )
        for note in target.notes:
            lines.extend([note, ""])

    lines.extend(
        [
            "## Singlefile",
            "",
            "Use `Singlefile/engineering-calculation-system.all-in-one.md` only when an agent cannot load a multi-file skill folder.",
            "",
            "## SourceDev",
            "",
            "Use `SourceDev/source-dev/` for repository review or downstream packaging. It is not the default runtime install target.",
            "",
        ]
    )
    (bundle_root / "INSTALL.md").write_text("\n".join(lines), encoding="utf-8")


def merge_core_into(dst: Path, profile_roots: dict[str, Path]) -> None:
    copy_tree(profile_roots["core"] / "engineering-calculation-system", dst)


def merge_adapter_docs_into(dst: Path, profile_roots: dict[str, Path]) -> None:
    copy_tree(profile_roots["adapters-light"] / "adapters", dst / "adapters")


def build_classified_bundle(profile_roots: dict[str, Path], bundle_root: Path) -> Path:
    missing = [profile for profile in RELEASE_REQUIRED_PROFILES if profile not in profile_roots]
    if missing:
        raise RuntimeError(f"classified release requires profiles: {', '.join(missing)}")

    if bundle_root.exists():
        shutil.rmtree(bundle_root)
    bundle_root.mkdir(parents=True, exist_ok=True)

    for target in CLASSIFIED_TARGETS:
        target_root = bundle_path(bundle_root, target.path)
        if target.include_core:
            merge_core_into(target_root, profile_roots)
        if target.include_adapter_docs:
            merge_adapter_docs_into(target_root, profile_roots)
        for copy in target.copies:
            apply_bundle_copy(profile_roots, copy, target_root)

    for copy in EXTRA_BUNDLE_COPIES:
        apply_bundle_copy(profile_roots, copy, bundle_root)

    write_install_guide(bundle_root)
    return bundle_root


def write_release_index(bundle_zip: Path, bundle_file_count: int) -> None:
    layout_lines = [f"  {target.path}/" for target in CLASSIFIED_TARGETS]
    layout_lines.extend(
        [
            "  Singlefile/engineering-calculation-system.all-in-one.md",
            "  SourceDev/source-dev/",
        ]
    )
    install_lines = [
        f"{target.name}: {target.install_text} Use `{target.path}/`."
        for target in CLASSIFIED_TARGETS
    ]
    install_lines.extend(
        [
            "Singlefile: use only when multi-file skill loading is unavailable.",
            "SourceDev: use for repository review or downstream packaging, not runtime installation.",
        ]
    )
    lines = [
        "# Engineering Calculation System Release Bundles",
        "",
        f"Version: {VERSION}",
        f"Created at: {CREATED_AT}",
        "",
        "## Publish File",
        "",
        "| Archive | Size KB | SHA256 |",
        "| --- | ---: | --- |",
        f"| `{bundle_zip.name}` | {bundle_zip.stat().st_size / 1024:.1f} | `{sha256(bundle_zip)}` |",
        "",
        "## Bundle Layout",
        "",
        "```text",
        f"{BUNDLE_NAME}/",
        *layout_lines,
        "```",
        "",
        f"Bundle file count: {bundle_file_count}",
        "",
        "## Install Order",
        "",
        *install_lines,
        "",
    ]
    (RELEASE_ROOT / "RELEASE_INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def build_split_archives(built_profiles: dict[str, Path]) -> list[Path]:
    split_root = RELEASE_ROOT / "split-archives"
    split_root.mkdir(parents=True, exist_ok=True)
    archives: list[Path] = []
    for profile, profile_root in built_profiles.items():
        archive_path = split_root / archive_name(profile)
        write_zip(profile_root, archive_path)
        archives.append(archive_path)
    return archives


def build_release_bundle(built_profiles: dict[str, Path], *, split_archives: bool = False) -> tuple[Path, int]:
    clean_dir(RELEASE_ROOT)
    bundle_zip = RELEASE_ROOT / f"{BUNDLE_NAME}.zip"
    with tempfile.TemporaryDirectory(prefix="ecs-release-") as temp_dir:
        bundle_root = build_classified_bundle(built_profiles, Path(temp_dir) / BUNDLE_NAME)
        bundle_file_count = len(iter_files(bundle_root, include_indexes=True))
        write_zip(bundle_root, bundle_zip, archive_root_name=bundle_root.name)

    checksum_lines = [f"{sha256(bundle_zip)}  {bundle_zip.name}"]
    if split_archives:
        for archive in build_split_archives(built_profiles):
            checksum_lines.append(f"{sha256(archive)}  split-archives/{archive.name}")
    (RELEASE_ROOT / "CHECKSUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    write_release_index(bundle_zip, bundle_file_count)
    return bundle_zip, bundle_file_count


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
        help="Also create a classified release zip under dist/release",
    )
    parser.add_argument(
        "--no-archives",
        action="store_true",
        help="Do not create the classified release zip when building every profile",
    )
    parser.add_argument(
        "--split-archives",
        action="store_true",
        help="Also create legacy per-profile zip archives under dist/release/split-archives",
    )
    args = parser.parse_args(argv)

    if args.profile and args.all:
        parser.error("use either --profile or --all, not both")
    if args.archives and args.no_archives:
        parser.error("use either --archives or --no-archives, not both")

    default_publish = not args.profile and not args.all
    profiles = DEFAULT_ALL_PROFILES if args.all or default_publish else tuple(args.profile or ())
    create_archives = args.archives or ((args.all or default_publish) and not args.no_archives)

    if default_publish:
        print("no profile specified; building all profiles and the classified release bundle")

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
            raise RuntimeError(f"classified release bundle requires all profiles; missing: {missing}")
        bundle_zip, bundle_file_count = build_release_bundle(built, split_archives=args.split_archives)
        print(f"staged classified bundle ({bundle_file_count} files)")
        print(
            f"built {bundle_zip.relative_to(REPO_ROOT).as_posix()} "
            f"({bundle_zip.stat().st_size / 1024:.1f} KB)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
