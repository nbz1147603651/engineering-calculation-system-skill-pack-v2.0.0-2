from pkg.books.book_name.book_models import BookInput, ProjectInfo
from pkg.books.book_name.book_runner import run_book


def test_run_book_returns_result():
    book_input = BookInput(project=ProjectInfo(project_id="P001", case_id="C001", title="Example"))
    result = run_book(book_input)
    assert result.project.case_id == "C001"
    assert result.governing is not None
