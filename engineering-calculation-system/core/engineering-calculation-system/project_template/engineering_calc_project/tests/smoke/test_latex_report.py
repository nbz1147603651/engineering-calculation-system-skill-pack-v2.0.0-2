from io import BytesIO
from zipfile import ZipFile

from pkg.report.report_selector import ReportRenderDecision
from webapp.app import create_app


def test_latex_report_package_route():
    client = create_app().test_client()
    case = {"project": {"project_id": "P004", "case_id": "C004", "title": "LaTeX"}}

    response = client.post("/api/report/latex", json=case)

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/zip")
    with ZipFile(BytesIO(response.data)) as archive:
        names = set(archive.namelist())
        assert "main.tex" in names
        assert "cover.tex" in names
        assert "page_style.sty" in names
        assert "sections/01_summary.tex" in names


def test_final_report_route_uses_a4_html_when_latex_unavailable(monkeypatch):
    import pkg.report.report_selector as selector

    monkeypatch.setattr(
        selector,
        "select_report_output",
        lambda: ReportRenderDecision(
            output_format="html_a4",
            reason="test fallback",
            latex_available=False,
        ),
    )
    client = create_app().test_client()

    response = client.post(
        "/api/report/final",
        json={"project": {"project_id": "P006", "case_id": "C006", "title": "HTML A4"}},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/html")
    assert response.headers["X-Report-Renderer"] == "html_a4"
    html = response.get_data(as_text=True)
    assert "@page" in html
    assert "size: A4" in html
    assert "Formula Logic Trace" in html


def test_latex_template_listing_and_default_fallback():
    client = create_app().test_client()

    templates_response = client.get("/api/report/templates")
    assert templates_response.status_code == 200
    payload = templates_response.get_json()
    assert payload["default_template_id"] == "default_engineering_calcbook"
    assert any(item["id"] == "default_engineering_calcbook" for item in payload["templates"])

    response = client.post(
        "/api/report/latex",
        json={
            "project": {"project_id": "P005", "case_id": "C005", "title": "LaTeX Default"},
            "latex_template_id": "",
        },
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/zip")
