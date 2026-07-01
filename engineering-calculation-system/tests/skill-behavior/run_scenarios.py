#!/usr/bin/env python3
"""Static behavior-scenario asset runner for the engineering calculation skill."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = ROOT.parents[1] / "core" / "engineering-calculation-system"
SCENARIO_DIR = ROOT / "scenarios"
RUBRIC_DIR = ROOT / "rubrics"
FIXTURE_DIR = ROOT / "fixtures"

REQUIRED_TOP_LEVEL = {
    "id": str,
    "prompt": str,
    "required_skill_paths": list,
    "expected_decision": dict,
    "forbidden_decisions": list,
    "rubric": str,
}

REQUIRED_DECISION_KEYS = {
    "route_card",
    "gate_card",
    "artifact_contract",
    "validation_evidence",
    "completion_evidence_category",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_scenario(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path}: scenario files are YAML-compatible JSON in this runner: {exc}")
    if not isinstance(data, dict):
        fail(f"{path}: scenario must be an object")
    return data


def require_type(path: Path, data: dict[str, Any], key: str, expected_type: type) -> Any:
    if key not in data:
        fail(f"{path}: missing required key '{key}'")
    value = data[key]
    if not isinstance(value, expected_type):
        fail(f"{path}: key '{key}' must be {expected_type.__name__}")
    return value


def validate_scenario(path: Path, seen_ids: set[str]) -> None:
    data = read_scenario(path)
    for key, expected_type in REQUIRED_TOP_LEVEL.items():
        require_type(path, data, key, expected_type)

    scenario_id = data["id"]
    if scenario_id in seen_ids:
        fail(f"{path}: duplicate scenario id '{scenario_id}'")
    seen_ids.add(scenario_id)
    if scenario_id != path.stem:
        fail(f"{path}: id must match filename stem")

    required_skill_paths = data["required_skill_paths"]
    if not required_skill_paths:
        fail(f"{path}: required_skill_paths must not be empty")
    for rel in required_skill_paths:
        if not isinstance(rel, str):
            fail(f"{path}: required_skill_paths entries must be strings")
        if not (PACKAGE_ROOT / rel).exists():
            fail(f"{path}: required skill path does not exist: {rel}")

    decision = data["expected_decision"]
    missing = sorted(REQUIRED_DECISION_KEYS - set(decision))
    if missing:
        fail(f"{path}: expected_decision missing keys: {', '.join(missing)}")

    if not isinstance(data["forbidden_decisions"], list) or not data["forbidden_decisions"]:
        fail(f"{path}: forbidden_decisions must be a non-empty list")

    rubric_path = RUBRIC_DIR / data["rubric"]
    if not rubric_path.exists():
        fail(f"{path}: rubric not found: {data['rubric']}")

    for rel in data.get("fixtures", []):
        if not isinstance(rel, str):
            fail(f"{path}: fixture entries must be strings")
        if not (FIXTURE_DIR / rel).exists():
            fail(f"{path}: fixture not found: {rel}")


def main() -> int:
    if not SCENARIO_DIR.exists():
        fail(f"scenario directory missing: {SCENARIO_DIR}")
    paths = sorted(SCENARIO_DIR.glob("*.yaml"))
    if not paths:
        fail("no behavior scenarios found")

    seen_ids: set[str] = set()
    for path in paths:
        validate_scenario(path, seen_ids)

    print(f"PASS: {len(paths)} behavior scenarios validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
