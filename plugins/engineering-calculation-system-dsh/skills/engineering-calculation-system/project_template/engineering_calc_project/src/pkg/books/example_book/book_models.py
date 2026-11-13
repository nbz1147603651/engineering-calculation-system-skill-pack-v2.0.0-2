from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pkg.core.checks import CheckResult
from pkg.core.enums import Status


@dataclass(frozen=True)
class ProjectInfo:
    project_id: str
    case_id: str
    title: str


@dataclass(frozen=True)
class BookInput:
    project: ProjectInfo
    design_options: dict[str, Any] = field(default_factory=dict)
    inputs: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GoverningSummary:
    overall_status: Status
    governing_check_id: str | None = None
    governing_check_name: str | None = None
    governing_utilization_or_margin: float | None = None
    governing_limit: float | None = None
    critical_load_case_or_combination: str | None = None
    warnings_count: int = 0
    errors_count: int = 0


@dataclass(frozen=True)
class ChartAxis:
    label: str
    unit: str | None = None


@dataclass(frozen=True)
class ChartSeries:
    label: str
    values: list[float | None]
    unit: str | None = None
    result_paths: list[str] = field(default_factory=list)
    color: str | None = None


@dataclass(frozen=True)
class ChartThreshold:
    label: str
    value: float
    unit: str | None = None
    source_result_path: str | None = None


@dataclass(frozen=True)
class ChartSpec:
    chart_id: str
    title: str
    chart_type: str
    purpose: str
    categories: list[str]
    series: list[ChartSeries]
    x_axis: ChartAxis
    y_axis: ChartAxis
    recommended_ui_location: str = "after_governing_summary"
    recommended_report_location: str = "after_input_summary"
    thresholds: list[ChartThreshold] = field(default_factory=list)
    source_result_paths: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BookResult:
    project: ProjectInfo
    governing: GoverningSummary
    checks: list[CheckResult]
    charts: list[ChartSpec] = field(default_factory=list)
    intermediate_values: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    formula_registry_version: str = "unversioned"
    formula_hash: str | None = None
    formula_published_at: str | None = None
