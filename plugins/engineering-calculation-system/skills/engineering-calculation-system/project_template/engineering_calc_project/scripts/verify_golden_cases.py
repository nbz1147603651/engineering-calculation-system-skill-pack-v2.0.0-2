#!/usr/bin/env python3
"""Execute golden-case rows against the official run_book() path.

The registry remains intentionally simple CSV so it can be reviewed alongside
source and handoff artifacts. This runner gives the CSV teeth: each active row
loads the recorded input, calls the project form mapper, calls run_book(), and
compares the recorded result path against the expected value and tolerance.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
import importlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any


sys.dont_write_bytecode = True

PASS_STATUSES = {"accepted", "approved", "verified", "pass", "passed"}
SKIP_STATUSES = {"draft", "deferred", "not_applicable", "not-applicable"}


@dataclass(frozen=True)
class GoldenCaseResult:
    case_id: str
    status: str
    message: str
    expected_result_path: str = ""
    expected: Any = None
    actual: Any = None
    tolerance: str = ""


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_import_path(root: Path) -> None:
    for candidate in (root, root / "src"):
        text = str(candidate)
        if text not in sys.path:
            sys.path.insert(0, text)


def _top_level_yaml_scalar(path: Path, key: str) -> str:
    if not path.exists():
        return ""
    prefix = f"{key}:"
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip().strip('"').strip("'")
    return ""


def _book_name(root: Path) -> str:
    from_handoff = _top_level_yaml_scalar(root / "handoff" / "implementation_handoff.yaml", "book_name")
    if from_handoff:
        return from_handoff

    books_root = root / "src" / "pkg" / "books"
    for candidate in sorted(books_root.iterdir() if books_root.exists() else []):
        if (candidate / "book_runner.py").exists():
            return candidate.name
    raise RuntimeError("could not determine book_name for golden-case verification")


def _plain(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _plain(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _field(value: Any, name: str) -> Any:
    if isinstance(value, dict):
        return value[name]
    return getattr(value, name)


def resolve_result_path(value: Any, result_path: str) -> Any:
    """Resolve paths such as checks[0].utilization from dataclasses or dicts."""
    current = value
    for segment in result_path.split("."):
        if not segment:
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)(.*)$", segment)
        if not match:
            raise KeyError(f"invalid result path segment: {segment}")
        current = _field(current, match.group(1))
        remainder = match.group(2)
        for raw_index in re.findall(r"\[(\d+)\]", remainder):
            current = current[int(raw_index)]
    return current


def _parse_expected_behavior(text: str) -> dict[str, str]:
    pairs = {
        key.strip().lower(): value.strip()
        for key, value in re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([^;]+)", text or "")
    }
    if "expected_value" not in pairs:
        fallback = re.search(r"(?<![A-Za-z0-9_.-])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", text or "")
        if fallback:
            pairs["expected_value"] = fallback.group(0)
    return pairs


def _coerce_scalar(value: str) -> Any:
    text = str(value).strip()
    if text.lower() in {"true", "false"}:
        return text.lower() == "true"
    try:
        return float(text)
    except ValueError:
        return text


def _tolerance_values(text: str) -> tuple[float, float]:
    raw = (text or "").strip().lower()
    if raw in {"", "exact"}:
        return 0.0, 0.0
    if raw.startswith("abs:"):
        return float(raw.split(":", 1)[1]), 0.0
    if raw.startswith("rel:"):
        return 0.0, float(raw.split(":", 1)[1])
    values = {
        key: float(value)
        for key, value in re.findall(r"(abs|atol|rel|rtol)\s*=\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)", raw)
    }
    if values:
        return values.get("abs", values.get("atol", 0.0)), values.get("rel", values.get("rtol", 0.0))
    return float(raw), 0.0


def _matches_expected(actual: Any, expected: Any, tolerance: str) -> bool:
    if isinstance(actual, Enum):
        actual = actual.value
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        abs_tol, rel_tol = _tolerance_values(tolerance)
        return math.isclose(float(actual), float(expected), abs_tol=abs_tol, rel_tol=rel_tol)
    return str(actual).strip().lower() == str(expected).strip().lower()


def _default_status_path(result_path: str) -> str:
    match = re.match(r"^(checks\[\d+\])\.", result_path)
    return f"{match.group(1)}.status" if match else ""


def _is_truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def _run_case(root: Path, row: dict[str, str]) -> GoldenCaseResult:
    case_id = row.get("case_id", "<missing>")
    result_path = row.get("expected_result_path", "").strip()
    expected = _parse_expected_behavior(row.get("expected_behavior", ""))
    if not result_path:
        return GoldenCaseResult(case_id, "fail", "missing expected_result_path")
    if "expected_value" not in expected:
        return GoldenCaseResult(case_id, "fail", "expected_behavior must include expected_value=<value>", result_path)

    input_path = root / row.get("input_path", "")
    if not input_path.exists():
        return GoldenCaseResult(case_id, "fail", f"input file does not exist: {input_path}", result_path)

    form_utils = importlib.import_module("webapp.form_utils")
    book_runner = importlib.import_module(f"pkg.books.{_book_name(root)}.book_runner")
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    book_input = form_utils.build_case_input_from_form(payload)
    book_result = book_runner.run_book(book_input)

    actual = resolve_result_path(book_result, result_path)
    expected_value = _coerce_scalar(expected["expected_value"])
    tolerance = row.get("tolerance", "")
    if not _matches_expected(actual, expected_value, tolerance):
        return GoldenCaseResult(
            case_id,
            "fail",
            "result value mismatch",
            result_path,
            expected_value,
            _plain(actual),
            tolerance,
        )

    status_path = expected.get("status_path") or _default_status_path(result_path)
    if expected.get("expected_status") and status_path:
        status_actual = resolve_result_path(book_result, status_path)
        if isinstance(status_actual, Enum):
            status_actual = status_actual.value
        if str(status_actual).strip().lower() != expected["expected_status"].strip().lower():
            return GoldenCaseResult(
                case_id,
                "fail",
                f"status mismatch at {status_path}",
                status_path,
                expected["expected_status"],
                _plain(status_actual),
                tolerance,
            )

    return GoldenCaseResult(case_id, "pass", "golden case matched", result_path, expected_value, _plain(actual), tolerance)


def run_golden_cases(root: Path | None = None, registry_path: Path | None = None) -> list[GoldenCaseResult]:
    root = (root or project_root()).resolve()
    _ensure_import_path(root)
    registry_path = registry_path or root / "verification" / "golden_case_registry.csv"
    rows = list(csv.DictReader(registry_path.read_text(encoding="utf-8").splitlines()))
    results: list[GoldenCaseResult] = []
    for row in rows:
        case_id = row.get("case_id", "<missing>")
        row_status = str(row.get("status", "")).strip().lower()
        if row_status in SKIP_STATUSES and not _is_truthy(row.get("blocks_production")):
            results.append(GoldenCaseResult(case_id, "skip", f"row status is {row_status}"))
            continue
        if row_status and row_status not in PASS_STATUSES:
            results.append(GoldenCaseResult(case_id, "fail", f"row status is not production-accepted: {row_status}"))
            continue
        results.append(_run_case(root, row))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=project_root())
    parser.add_argument("--registry", type=Path, help="Override golden_case_registry.csv path")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results")
    args = parser.parse_args(argv)

    results = run_golden_cases(args.project_root, args.registry)
    failures = [result for result in results if result.status == "fail"]
    if args.json:
        print(json.dumps([asdict(result) for result in results], indent=2, sort_keys=True))
    else:
        for result in results:
            detail = f" expected={result.expected!r} actual={result.actual!r}" if result.status != "skip" else ""
            print(f"[{result.status.upper()}] {result.case_id}: {result.message}{detail}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
