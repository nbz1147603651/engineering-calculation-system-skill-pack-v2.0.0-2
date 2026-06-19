from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import Status


@dataclass(frozen=True)
class FormulaTrace:
    formula_id: str
    formula_name: str
    source_reference: str
    inputs: dict[str, Any]
    intermediates: dict[str, Any]
    result_symbol: str
    result_value: Any
    unit: str | None = None
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    name: str
    status: Status
    demand: float | None = None
    capacity: float | None = None
    utilization: float | None = None
    limit: float | None = None
    unit: str | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    formula_traces: list[FormulaTrace] = field(default_factory=list)
