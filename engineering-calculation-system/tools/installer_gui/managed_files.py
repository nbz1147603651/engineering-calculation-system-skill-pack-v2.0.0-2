"""Track exact project-overlay ownership and retain user files on uninstall."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import uuid
from pathlib import Path
from typing import Callable


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_path(root: Path, agent: str) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", agent):
        raise ValueError(f"Invalid managed agent ID: {agent}")
    return root / ".engineering-calc" / "installs" / f"{agent}.json"


def child(root: Path, relative: str) -> Path:
    base = root.resolve()
    if Path(relative).is_absolute():
        raise ValueError(f"Managed path must be relative: {relative}")
    target = (base / relative).resolve()
    if target == base or not target.is_relative_to(base):
        raise ValueError(f"Managed path leaves the project: {relative}")
    return target


def read_manifest(root: Path, agent: str) -> dict:
    path = child(root, manifest_path(root, agent).relative_to(root).as_posix())
    if not path.exists():
        return {"schema": 1, "agent": agent, "files": {}}
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema") != 1 or manifest.get("agent") != agent or not isinstance(manifest.get("files"), dict):
        raise ValueError(f"Invalid deployment manifest: {path}")
    for relative, entry in manifest["files"].items():
        child(root, relative)
        if not isinstance(entry, dict) or not re.fullmatch(r"[a-f0-9]{64}", str(entry.get("sha256", ""))):
            raise ValueError(f"Invalid file entry in deployment manifest: {relative}")
        if entry.get("backup"):
            child(root, entry["backup"])
    return manifest


def install(root: Path, agent: str, copies: list[tuple[Path, Path]], log: Callable[[str], None]) -> None:
    root = root.expanduser().resolve()
    manifest = read_manifest(root, agent)
    entries = manifest["files"]
    directory = child(root, manifest_path(root, agent).relative_to(root).as_posix()).parent
    other_manifests = {candidate.stem: read_manifest(root, candidate.stem)
                       for candidate in directory.glob("*.json") if candidate.stem != agent}
    for source, relative_target in copies:
        if not source.exists():
            raise ValueError(f"Missing deployment source: {source}")
        sources = sorted(path for path in source.rglob("*") if path.is_file()) if source.is_dir() else [source]
        for path in sources:
            relative = (relative_target / path.relative_to(source)).as_posix() if source.is_dir() else relative_target.as_posix()
            destination = child(root, relative)
            previous = entries.get(relative, {})
            source_hash = digest(path)
            current_hash = digest(destination) if destination.exists() else None
            if current_hash == source_hash:
                # Identical pre-existing files are borrowed, never claimed as ours.
                if relative not in entries:
                    entries[relative] = {"sha256": source_hash, "borrowed": True}
                continue
            # A different host may own the current version of this same path.
            # Keep its original pre-install baseline rather than treating a
            # managed upgrade as a user edit and backing up an intermediate version.
            owners = [previous, *(other["files"].get(relative, {}) for other in other_manifests.values())]
            owner = next((entry for entry in owners if entry and not entry.get("borrowed")
                          and entry.get("sha256") == current_hash), None)
            backup = owner.get("backup") if owner else previous.get("backup")
            if destination.exists():
                backup_path = destination.with_name(destination.name + ".bak.nimo-" + uuid.uuid4().hex[:12])
                shutil.copy2(destination, backup_path)
                # Keep the original pre-install baseline across unchanged redeploys.
                if owner is None:
                    backup = backup_path.relative_to(root).as_posix()
                log(f"[backup] {destination} -> {backup_path}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            entries[relative] = {"sha256": source_hash, "backup": backup, "borrowed": False}
            # Persist ownership after each successful copy so interrupted installs are recoverable.
            save_manifest(root, agent, manifest)
            # Every installed host uses the actual shared version. Record it
            # with the same baseline so either uninstall order is recoverable.
            for name, other in other_manifests.items():
                if relative in other["files"]:
                    other["files"][relative].update(entries[relative])
                    save_manifest(root, name, other)
            log(f"[copy] {path} -> {destination}")
    save_manifest(root, agent, manifest)


def save_manifest(root: Path, agent: str, manifest: dict) -> None:
    path = child(root, manifest_path(root, agent).relative_to(root).as_posix())
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def uninstall(root: Path, agent: str, log: Callable[[str], None]) -> None:
    root = root.expanduser().resolve()
    path = child(root, manifest_path(root, agent).relative_to(root).as_posix())
    if not path.is_file():
        raise ValueError(f"No ownership manifest at {path}; legacy files were retained. Deploy once to record exact ownership before uninstalling.")
    manifest = read_manifest(root, agent)
    other_manifests = {candidate.stem: read_manifest(root, candidate.stem)
                       for candidate in path.parent.glob("*.json") if candidate.stem != agent}
    retained = {}
    for relative, entry in manifest["files"].items():
        destination = child(root, relative)
        if entry.get("borrowed"):
            log(f"[keep] pre-existing file: {destination}")
            continue
        if destination.exists() and digest(destination) != entry.get("sha256"):
            log(f"[keep] modified after installation: {destination}")
            retained[relative] = entry
            continue
        shared = next(((name, other) for name, other in other_manifests.items()
                       if other["files"].get(relative, {}).get("sha256") == entry["sha256"]), None)
        if shared:
            name, other = shared
            shared_entry = other["files"][relative]
            if shared_entry.get("borrowed"):
                # Transfer ownership and the true pre-install baseline so the
                # final remaining host can later remove/restore this shared file.
                shared_entry.update({"borrowed": False, "backup": entry.get("backup")})
                save_manifest(root, name, other)
            log(f"[keep] shared with {name}: {destination}")
            continue
        backup = child(root, entry["backup"]) if entry.get("backup") else None
        if backup and backup.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup, destination)
            log(f"[restore] {backup} -> {destination}; backup retained")
        elif destination.is_file():
            destination.unlink()
            log(f"[remove] {destination}")
    if retained:
        manifest["files"] = retained
        save_manifest(root, agent, manifest)
    else:
        path.unlink()
