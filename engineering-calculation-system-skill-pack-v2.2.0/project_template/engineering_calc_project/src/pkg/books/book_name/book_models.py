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
class BookResult:
    project: ProjectInfo
    governing: GoverningSummary
    checks: list[CheckResult]
    intermediate_values: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
