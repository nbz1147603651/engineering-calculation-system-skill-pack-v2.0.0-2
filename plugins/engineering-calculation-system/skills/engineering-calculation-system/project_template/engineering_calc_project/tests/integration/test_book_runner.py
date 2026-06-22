from dataclasses import replace

from pkg.books.example_book.book_models import BookInput, BookResult, GoverningSummary, ProjectInfo
from pkg.books.example_book.charts import build_book_charts
from pkg.books.example_book.book_runner import run_book
from pkg.books.example_book.report_context import build_report_context
from pkg.core.checks import CheckResult
from pkg.core.enums import Status
from pkg.report.html_renderer import build_html_report_context, render_a4_html_report
from pkg.report.latex_renderer import build_latex_report_context


def test_run_book_returns_result():
    book_input = BookInput(
        project=ProjectInfo(project_id="P001", case_id="C001", title="Example"),
        inputs={
            "checks": [
                {
                    "check_id": "DEMO-001",
                    "name": "Template demand/capacity check",
                    "demand": 45,
                    "capacity": 90,
                    "limit": 1,
                    "unit": "kN",
                    "source_reference": "S01",
                }
            ]
        },
    )
    result = run_book(book_input)
    assert result.project.case_id == "C001"
    assert result.governing is not None
    assert result.governing.overall_status == Status.PASS
    assert result.checks
    assert result.checks[0].formula_traces
    assert isinstance(result.charts, list)


def test_check_results_generate_review_charts_and_report_context():
    result = BookResult(
        project=ProjectInfo(project_id="P010", case_id="C010", title="Charted"),
        governing=GoverningSummary(
            overall_status=Status.PASS,
            governing_check_id="CHK-2",
            governing_check_name="Sliding",
            governing_utilization_or_margin=0.82,
            governing_limit=1.0,
        ),
        checks=[
            CheckResult(
                check_id="CHK-1",
                name="Bearing",
                status=Status.PASS,
                demand=120.0,
                capacity=240.0,
                utilization=0.50,
                limit=1.0,
                unit="kN",
            ),
            CheckResult(
                check_id="CHK-2",
                name="Sliding",
                status=Status.PASS,
                demand=82.0,
                capacity=100.0,
                utilization=0.82,
                limit=1.0,
                unit="kN",
            ),
        ],
    )
    result = replace(result, charts=build_book_charts(result))

    assert [chart.chart_id for chart in result.charts] == [
        "check_utilization_summary",
        "demand_capacity_comparison",
    ]
    assert result.charts[0].recommended_report_location == "after_input_summary"
    assert result.charts[0].source_result_paths == [
        "checks[0].utilization",
        "checks[1].utilization",
    ]
    assert result.charts[0].thresholds[0].source_result_path == "checks[0].limit"

    report_context = build_report_context(result)
    assert report_context["charts"] == result.charts
    report_context["figures"] = [
        {
            "figure_id": "FIG-001",
            "title": "Foundation Layout",
            "caption": "Project geometry image supplied for report review.",
            "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3C/svg%3E",
            "recommended_report_location": "after_input_summary",
            "source_reference": "S-FIG",
            "result_path": "report.figures[0]",
        }
    ]

    book_input = BookInput(project=result.project)
    html_context = build_html_report_context(book_input, result, report_context)
    html = render_a4_html_report(html_context)
    latex_context = build_latex_report_context(book_input, result, report_context)
    assert "Engineering Charts" in html
    assert "Engineering Figures" in html
    assert "Foundation Layout" in html
    assert "<img" in html
    assert "Check Utilization Summary" in html
    assert "<svg" in html
    assert "chart-data" in html
    assert "print-color-adjust" in html
    assert "checks[0].utilization" in html
    assert "do not recalculate engineering outcomes" in html
    assert latex_context["figures"][0]["figure_id"] == "FIG-001"
