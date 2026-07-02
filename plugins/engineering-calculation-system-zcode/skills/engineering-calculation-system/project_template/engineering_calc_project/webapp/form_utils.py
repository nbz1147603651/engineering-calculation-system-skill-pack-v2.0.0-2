"""Form data -> BookInput builder and BookResult -> UI dict converter.

Scaffold: customize for each calculation book's BookInput / BookResult models.

This module is the SINGLE source of truth for form -> model mapping.
Never put mapping logic in route handlers or template renderers.
"""

from __future__ import annotations

import math
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Optional

from pkg.books.example_book.book_models import BookInput, BookResult, ProjectInfo


# ---------------------------------------------------------------------------
# JSON Sanitization
# ---------------------------------------------------------------------------

def _sanitize_json(obj: Any, _path: str = "") -> tuple[Any, list[dict]]:
    """Recursively replace non-finite floats (inf, -inf, nan) with None.

    Python's float('inf') serializes as ``Infinity`` which is not valid JSON
    and causes ``JSON.parse`` to throw on the browser side.

    Returns:
        Tuple of (sanitized_object, list_of_warnings).
    """
    warnings: list[dict] = []

    if isinstance(obj, float):
        if math.isfinite(obj):
            return obj, warnings
        reason = "Infinity" if math.isinf(obj) else "NaN"
        warnings.append({"field": _path or "value", "reason": reason})
        return None, warnings

    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            child_path = f"{_path}.{k}" if _path else k
            sanitized, child_warnings = _sanitize_json(v, child_path)
            result[k] = sanitized
            warnings.extend(child_warnings)
        return result, warnings

    if isinstance(obj, (list, tuple)):
        result = []
        for i, v in enumerate(obj):
            child_path = f"{_path}[{i}]"
            sanitized, child_warnings = _sanitize_json(v, child_path)
            result.append(sanitized)
            warnings.extend(child_warnings)
        return result, warnings

    return obj, warnings


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _opt(val: Any, default: Optional[float] = None) -> Optional[float]:
    """Convert to float or return default."""
    if val is None or val == "" or val == "null":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _plain(obj: Any) -> Any:
    """Convert dataclasses and enums into JSON-ready values."""
    if isinstance(obj, Enum):
        return obj.value
    if is_dataclass(obj):
        return {key: _plain(value) for key, value in asdict(obj).items()}
    if isinstance(obj, dict):
        return {str(key): _plain(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(value) for value in obj]
    return obj


def _to_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _default_check_payload() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "DEMO-001",
            "name": "Template demand/capacity check",
            "demand": 45.0,
            "capacity": 90.0,
            "limit": 1.0,
            "unit": "kN",
            "source_reference": "S01",
        }
    ]


# ---------------------------------------------------------------------------
# Form -> BookInput
# ---------------------------------------------------------------------------

def build_case_input_from_form(data: dict) -> BookInput:
    """Build a BookInput from web form JSON data.

    Customize this function for each calculation book.
    Use explicit field-by-field conversion - no reflection or magic.
    """
    data = data if isinstance(data, dict) else {}
    proj = _to_dict(data.get("project", {}))
    inputs = _to_dict(data.get("inputs", {}))
    design_options = _to_dict(data.get("design_options", data.get("options", {})))
    if "checks" in data and "checks" not in inputs:
        inputs["checks"] = data["checks"]
    if "checks" not in inputs:
        inputs["checks"] = _default_check_payload()

    project = ProjectInfo(
        project_id=str(proj.get("project_id", "DEMO_001")).strip() or "DEMO_001",
        case_id=str(proj.get("case_id", "DEMO_CASE_001")).strip() or "DEMO_CASE_001",
        title=proj.get("title") or proj.get("project_name", "Template Demonstration Project"),
    )

    # Scaffold: add book-specific input groups here.
    # foundation = Foundation(...)
    # load_case = LoadCase(...)
    # options = DesignOptions(...)

    return BookInput(
        project=project,
        design_options=design_options,
        inputs=inputs,
    )


# ---------------------------------------------------------------------------
# BookInput -> Form (for import/export)
# ---------------------------------------------------------------------------

def book_input_to_form(bi: BookInput) -> dict:
    """Convert a BookInput back to the web form structure.

    Used for JSON export and populating forms after import.
    """
    return {
        "project": {
            "project_id": bi.project.project_id,
            "case_id": bi.project.case_id,
            "project_name": bi.project.title,
            "title": bi.project.title,
        },
        "design_options": bi.design_options,
        "inputs": bi.inputs,
    }


# ---------------------------------------------------------------------------
# BookResult -> UI dict
# ---------------------------------------------------------------------------

def case_result_to_ui(r: BookResult, bi: BookInput) -> dict:
    """Convert BookResult to a UI-friendly dictionary.

    Customize for each calculation book's result structure.

    Rules:
    - round all floats to display precision (3-4 decimals)
    - convert enums to strings for JSON serialization
    - include governing status, utilization, and status badge text
    - embed SVG charts inline when available (bilingual if i18n active)
    - sanitize NaN/Infinity before returning
    """
    out: dict[str, Any] = {"status": "ok"}

    # Governing summary
    g = r.governing
    out["governing"] = {
        "check": g.governing_check_name or "-",
        "utilization": round(g.governing_utilization_or_margin, 4) if g.governing_utilization_or_margin is not None else None,
        "status": _plain(g.overall_status),
    }

    # Scaffold: add book-specific result sections here.
    # e.g. out["bearing"] = { ... }
    # e.g. out["settlement"] = { ... }
    # e.g. out["sliding"] = { ... }

    # Checks
    out["checks"] = [
        {
            "check_id": c.check_id,
            "name": c.name,
            "status": _plain(c.status),
            "demand": round(c.demand, 3) if c.demand is not None else None,
            "capacity": round(c.capacity, 3) if c.capacity is not None else None,
            "utilization": round(c.utilization, 4) if c.utilization is not None else None,
            "limit": round(c.limit, 4) if c.limit is not None else None,
            "unit": c.unit,
            "warnings": c.warnings,
            "errors": c.errors,
            "formula_traces": _plain(c.formula_traces),
        }
        for c in r.checks
    ]
    out["charts"] = _plain(r.charts)

    # Warnings and errors
    out["warnings"] = r.warnings
    out["errors"] = r.errors
    out["formula_registry"] = {
        "version": r.formula_registry_version,
        "hash": r.formula_hash,
        "published_at": r.formula_published_at,
    }

    # Sanitize non-finite floats
    sanitized, sanitize_warnings = _sanitize_json(out)
    if sanitize_warnings:
        existing = sanitized.get("warnings") or []
        existing.extend(
            f"Sanitized {w['field']}: {w['reason']}" for w in sanitize_warnings
        )
        sanitized["warnings"] = existing

    return sanitized
