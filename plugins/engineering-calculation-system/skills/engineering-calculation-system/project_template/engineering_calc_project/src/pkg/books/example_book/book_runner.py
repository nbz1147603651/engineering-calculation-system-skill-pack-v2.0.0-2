from __future__ import annotations

from dataclasses import replace
import math
from typing import Any

from .book_models import BookInput, BookResult, GoverningSummary
from .charts import build_book_charts
from pkg.core.checks import CheckResult, FormulaTrace
from pkg.core.enums import Status
from pkg.core.formula_registry import active_registry_metadata, get_formula_display


def _safe_float(value: Any, default: float | None = None) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return number


def _status_from_utilization(utilization: float | None, limit: float | None) -> Status:
    if utilization is None or limit is None:
        return Status.NOT_EVALUATED
    return Status.PASS if utilization <= limit else Status.FAIL


def _build_check(index: int, payload: dict[str, Any]) -> CheckResult:
    demand = _safe_float(payload.get("demand"), 0.0)
    capacity = _safe_float(payload.get("capacity"), 0.0)
    limit = _safe_float(payload.get("limit"), 1.0)
    utilization = None
    if demand is not None and capacity is not None and abs(capacity) > 1e-12:
        utilization = abs(demand) / abs(capacity)
    status = _status_from_utilization(utilization, limit)
    check_id = str(payload.get("check_id") or f"DEMO-{index:03d}")
    name = str(payload.get("name") or "Template demand/capacity check")
    unit = payload.get("unit") or "unit"
    source_reference = str(payload.get("source_reference") or "S01")
    formula_display = get_formula_display("example_module", "F-EXAMPLE-001")
    trace = FormulaTrace(
        formula_id=str(formula_display["formula_id"]),
        formula_name=str(formula_display["formula_name"]),
        source_reference=source_reference or str(formula_display["source_reference"]),
        inputs={"demand": demand, "capacity": capacity, "limit": limit},
        intermediates={"abs_demand": abs(demand or 0.0), "abs_capacity": abs(capacity or 0.0)},
        result_symbol="utilization",
        result_value=utilization,
        unit="ratio",
        expression_tex=formula_display.get("expression_tex"),
        expression_plain=formula_display.get("expression_plain"),
        engineering_explanation=formula_display.get("engineering_explanation"),
        variable_definitions=formula_display.get("variable_definitions") or {},
        substitutions={"D": demand, "C": capacity, "eta": utilization},
        result_path=f"checks[{index - 1}].utilization",
        display_icon=formula_display.get("display_icon"),
        notes=[
            "Template demonstration logic for validation closure.",
            "Replace this example module with source-backed engineering formulas before project use.",
        ],
    )
    return CheckResult(
        check_id=check_id,
        name=name,
        status=status,
        demand=demand,
        capacity=capacity,
        utilization=utilization,
        limit=limit,
        unit=str(unit),
        formula_traces=[trace],
    )


def _checks_from_input(book_input: BookInput) -> list[CheckResult]:
    raw_checks = book_input.inputs.get("checks")
    if isinstance(raw_checks, list) and raw_checks:
        return [
            _build_check(index, item if isinstance(item, dict) else {})
            for index, item in enumerate(raw_checks, start=1)
        ]
    return []


def _governing_from_checks(checks: list[CheckResult]) -> GoverningSummary:
    if not checks:
        return GoverningSummary(
            overall_status=Status.NOT_EVALUATED,
            warnings_count=1,
            errors_count=0,
        )
    failing = [check for check in checks if check.status == Status.FAIL]
    if failing:
        governing = max(failing, key=lambda item: item.utilization or 0.0)
        return GoverningSummary(
            overall_status=Status.FAIL,
            governing_check_id=governing.check_id,
            governing_check_name=governing.name,
            governing_utilization_or_margin=governing.utilization,
            governing_limit=governing.limit,
        )
    assessed = [check for check in checks if check.utilization is not None]
    governing = max(assessed, key=lambda item: item.utilization or 0.0, default=checks[0])
    return GoverningSummary(
        overall_status=Status.PASS,
        governing_check_id=governing.check_id,
        governing_check_name=governing.name,
        governing_utilization_or_margin=governing.utilization,
        governing_limit=governing.limit,
    )


def run_book(book_input: BookInput) -> BookResult:
    """Official calculation entry point. Interfaces, reports, and batch must call this."""
    formula_metadata = active_registry_metadata()
    checks = _checks_from_input(book_input)
    governing = _governing_from_checks(checks)
    result = BookResult(
        project=book_input.project,
        governing=governing,
        checks=checks,
        intermediate_values={
            "input_check_count": len(book_input.inputs.get("checks", []) or []),
            "template_module": "pkg.books.example_book.book_runner",
            "calculation_boundary": "run_book(BookInput) -> BookResult",
        },
        warnings=[] if checks else ["No input checks were provided to the example book."],
        formula_registry_version=formula_metadata["formula_registry_version"],
        formula_hash=formula_metadata["formula_hash"],
        formula_published_at=formula_metadata["formula_published_at"],
    )
    return replace(result, charts=build_book_charts(result))
