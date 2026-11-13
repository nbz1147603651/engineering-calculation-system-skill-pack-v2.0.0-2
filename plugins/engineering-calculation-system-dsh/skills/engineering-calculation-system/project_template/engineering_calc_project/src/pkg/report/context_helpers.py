"""Format-independent report context helpers over computed inputs/results."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


def to_plain(value: Any) -> Any:
    """Convert dataclasses and enums into Jinja-friendly plain values."""
    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_plain(item) for item in value]
    return value



def report_sources_from_checks(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Summarize source references already present in formula traces."""
    sources: dict[str, dict[str, Any]] = {}
    for check in checks:
        check_id = str(check.get("check_id") or "check")
        for trace in check.get("formula_traces", []) or []:
            source_reference = str(trace.get("source_reference") or "").strip()
            if not source_reference:
                continue
            formula_id = str(trace.get("formula_id") or "formula")
            record = sources.setdefault(
                source_reference,
                {
                    "source_reference": source_reference,
                    "role": "formula_trace_source",
                    "used_in": [],
                },
            )
            record["used_in"].append(f"{check_id}:{formula_id}")
    return list(sources.values())



def report_assumptions_from_context(
    plain_input: dict[str, Any],
    plain_report: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return report assumptions without inventing engineering logic."""
    explicit = plain_report.get("assumptions")
    if isinstance(explicit, list) and explicit:
        return explicit

    design_options = plain_input.get("design_options", {})
    input_assumptions = design_options.get("assumptions") if isinstance(design_options, dict) else None
    if isinstance(input_assumptions, list) and input_assumptions:
        return input_assumptions

    return [
        {
            "assumption_id": "A001",
            "assumption": "Demand and capacity are supplied in the same unit for the template demonstration check.",
            "source_reference": "S01",
            "program_handling": "The template reports the unit and evaluates utilization only.",
        }
    ]



def report_figures_from_context(
    plain_report: dict[str, Any],
    plain_result: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return report-only figure records without changing calculation results."""
    raw_figures = (
        plain_report.get("figures")
        or plain_report.get("report_figures")
        or plain_result.get("figures")
        or []
    )
    if not isinstance(raw_figures, list):
        return []

    figures: list[dict[str, Any]] = []
    for index, raw_item in enumerate(raw_figures, start=1):
        if isinstance(raw_item, str):
            item: dict[str, Any] = {"src": raw_item}
        elif isinstance(raw_item, dict):
            item = dict(raw_item)
        else:
            continue

        figure_id = str(item.get("figure_id") or item.get("id") or f"FIG-{index:03d}")
        title = item.get("title") or item.get("caption") or figure_id
        location = (
            item.get("recommended_report_location")
            or item.get("placement")
            or item.get("location")
            or "after_input_summary"
        )
        item["figure_id"] = figure_id
        item["title"] = title
        item["alt"] = item.get("alt") or title
        item["recommended_report_location"] = str(location)
        figures.append(item)
    return figures

