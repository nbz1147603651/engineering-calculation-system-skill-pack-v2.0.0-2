from __future__ import annotations

from .book_models import BookInput, BookResult, GoverningSummary
from pkg.core.enums import Status


def run_book(book_input: BookInput) -> BookResult:
    """Official calculation entry point. Interfaces, reports, and batch must call this."""
    checks = []
    governing = GoverningSummary(
        overall_status=Status.NOT_EVALUATED,
        warnings_count=0,
        errors_count=0,
    )
    return BookResult(project=book_input.project, governing=governing, checks=checks)
