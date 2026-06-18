from __future__ import annotations

from .book_models import BookResult


def build_report_context(result: BookResult) -> dict:
    """Build presentation data from BookResult without recalculating engineering logic."""
    return {
        "project": result.project,
        "governing": result.governing,
        "checks": result.checks,
        "warnings": result.warnings,
        "errors": result.errors,
    }
