from __future__ import annotations

from pkg.core.checks import CheckResult

from .book_models import (
    BookResult,
    ChartAxis,
    ChartSeries,
    ChartSpec,
    ChartThreshold,
)


def build_book_charts(result: BookResult) -> list[ChartSpec]:
    """Create engineering-review charts from already-computed BookResult values."""
    charts: list[ChartSpec] = []
    utilization_chart = build_check_utilization_chart(result.checks)
    if utilization_chart is not None:
        charts.append(utilization_chart)

    demand_capacity_chart = build_demand_capacity_chart(result.checks)
    if demand_capacity_chart is not None:
        charts.append(demand_capacity_chart)

    return charts


def build_check_utilization_chart(checks: list[CheckResult]) -> ChartSpec | None:
    indexed_checks = [
        (index, check)
        for index, check in enumerate(checks)
        if check.utilization is not None
    ]
    if not indexed_checks:
        return None

    categories = [_check_label(check) for _, check in indexed_checks]
    result_paths = [f"checks[{index}].utilization" for index, _ in indexed_checks]
    thresholds = _common_limit_threshold(indexed_checks)

    return ChartSpec(
        chart_id="check_utilization_summary",
        title="Check Utilization Summary",
        chart_type="bar",
        purpose=(
            "Compare already-computed utilization values so the reviewer can "
            "see which checks are closest to their recorded limits."
        ),
        categories=categories,
        series=[
            ChartSeries(
                label="Utilization",
                values=[check.utilization for _, check in indexed_checks],
                unit="ratio",
                result_paths=result_paths,
                color="#2563eb",
            )
        ],
        x_axis=ChartAxis(label="Check"),
        y_axis=ChartAxis(label="Utilization", unit="ratio"),
        thresholds=thresholds,
        source_result_paths=result_paths,
        notes=[
            "Generated from CheckResult.utilization values only.",
            "The chart does not recalculate pass/fail status or utilization.",
        ],
    )


def build_demand_capacity_chart(checks: list[CheckResult]) -> ChartSpec | None:
    indexed_checks = [
        (index, check)
        for index, check in enumerate(checks)
        if check.demand is not None and check.capacity is not None
    ]
    if not indexed_checks:
        return None

    unit = _common_unit([check for _, check in indexed_checks])
    demand_paths = [f"checks[{index}].demand" for index, _ in indexed_checks]
    capacity_paths = [f"checks[{index}].capacity" for index, _ in indexed_checks]

    return ChartSpec(
        chart_id="demand_capacity_comparison",
        title="Demand and Capacity Comparison",
        chart_type="grouped_bar",
        purpose=(
            "Place already-computed demand and capacity values side by side "
            "for quick audit of governing checks."
        ),
        categories=[_check_label(check) for _, check in indexed_checks],
        series=[
            ChartSeries(
                label="Demand",
                values=[check.demand for _, check in indexed_checks],
                unit=unit,
                result_paths=demand_paths,
                color="#dc2626",
            ),
            ChartSeries(
                label="Capacity",
                values=[check.capacity for _, check in indexed_checks],
                unit=unit,
                result_paths=capacity_paths,
                color="#16a34a",
            ),
        ],
        x_axis=ChartAxis(label="Check"),
        y_axis=ChartAxis(label="Demand / Capacity", unit=unit),
        source_result_paths=[*demand_paths, *capacity_paths],
        notes=[
            "Generated from CheckResult.demand and CheckResult.capacity values only.",
            "Mixed units are shown as 'varies'; see the check table for each row unit.",
        ] if unit == "varies" else [
            "Generated from CheckResult.demand and CheckResult.capacity values only.",
        ],
    )


def _check_label(check: CheckResult) -> str:
    return check.name or check.check_id


def _common_unit(checks: list[CheckResult]) -> str | None:
    units = {check.unit for check in checks if check.unit}
    if not units:
        return None
    if len(units) == 1:
        return next(iter(units))
    return "varies"


def _common_limit_threshold(
    indexed_checks: list[tuple[int, CheckResult]]
) -> list[ChartThreshold]:
    limits = [
        (index, check.limit)
        for index, check in indexed_checks
        if check.limit is not None
    ]
    if len(limits) != len(indexed_checks):
        return []

    unique_limits = {limit for _, limit in limits}
    if len(unique_limits) != 1:
        return []

    index, limit = limits[0]
    return [
        ChartThreshold(
            label="Recorded limit",
            value=limit,
            unit="ratio",
            source_result_path=f"checks[{index}].limit",
        )
    ]
