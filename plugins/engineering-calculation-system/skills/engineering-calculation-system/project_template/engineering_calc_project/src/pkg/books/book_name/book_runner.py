from __future__ import annotations

from .book_models import BookInput, BookResult, GoverningSummary
from pkg.core.enums import Status
from pkg.core.formula_registry import active_registry_metadata


def run_book(book_input: BookInput) -> BookResult:
    """Official calculation entry point. Interfaces, reports, and batch must call this."""
    formula_metadata = active_registry_metadata()
    checks = []
    governing = GoverningSummary(
        overall_status=Status.NOT_EVALUATED,
        warnings_count=0,
        errors_count=0,
    )
    return BookResult(
        project=book_input.project,
        governing=governing,
        checks=checks,
        formula_registry_version=formula_metadata["formula_registry_version"],
        formula_hash=formula_metadata["formula_hash"],
        formula_published_at=formula_metadata["formula_published_at"],
    )
