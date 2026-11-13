from webapp.app import create_app
from webapp import config as cfg


def test_health_and_calculate_routes():
    client = create_app().test_client()

    assert client.get("/health").status_code == 200
    response = client.post(
        "/api/calculate",
        json=cfg.DEFAULTS,
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["formula_registry"]["version"]
    assert payload["governing"]["status"] == "PASS"
    assert isinstance(payload["checks"], list)
    assert payload["checks"]
    assert isinstance(payload["charts"], list)
    assert payload["charts"]
    assert payload["checks"][0]["status"] == "PASS"
    assert payload["checks"][0]["formula_traces"]
    assert isinstance(payload["warnings"], list)
    assert isinstance(payload["errors"], list)


def test_capabilities_route_and_review_shell(monkeypatch):
    monkeypatch.setattr(cfg, "ADMIN_REVIEW_PASSWORD", "")
    monkeypatch.setattr(cfg, "ADMIN_REVIEW_TOKEN", "")
    client = create_app().test_client()

    response = client.get("/api/capabilities")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert "python" in payload["capabilities"]
    assert "marimo_review" in payload["capabilities"]
    assert "latex" in payload["capabilities"]

    page = client.get("/admin/")
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert 'id="adminReviewPage"' in html
    assert "Marimo Calculation Review" in html
    assert "Admin password is not configured" in html
    assert "ADMIN_REVIEW_TOKEN" in html
    assert "ADMIN_REVIEW_PASSWORD" in html
    assert "/static/js/i18n.js" in html

    monkeypatch.setattr(cfg, "ADMIN_REVIEW_PASSWORD", "let-me-in")
    bad_login = client.post("/admin/", data={"admin_password": "wrong"})
    assert bad_login.status_code == 401
    assert "Invalid admin password" in bad_login.get_data(as_text=True)

    good_login = client.post("/admin/", data={"admin_password": "let-me-in"})
    assert good_login.status_code == 200
    authed_html = good_login.get_data(as_text=True)
    assert "marimo run apps/review/calculation_review.py" in authed_html
    assert "marimo run apps/review/admin_formula_review.py" in authed_html
    assert "/api/review/session" in authed_html
    assert "/admin/formulas" in authed_html


def test_import_report_and_batch_routes(monkeypatch, tmp_path):
    monkeypatch.setattr(cfg, "REVIEW_SESSION_DIR", tmp_path / "review")
    client = create_app().test_client()
    case = cfg.DEFAULTS

    import_response = client.post("/api/import/json", json=case)
    assert import_response.status_code == 200
    assert import_response.get_json()["status"] == "ok"

    preview_response = client.post("/api/report/preview", json=case)
    assert preview_response.status_code == 200
    assert preview_response.get_json()["status"] == "ok"

    html_response = client.post("/api/report/html", json=case)
    assert html_response.status_code == 200
    assert html_response.headers["Content-Type"].startswith("text/html")
    html = html_response.get_data(as_text=True)
    assert "@page" in html
    assert "size: A4" in html
    assert "print-color-adjust" in html
    assert "Engineering Calculation Book" in html
    assert "Table of Contents" in html
    assert "cover-page" in html
    assert "Engineering Charts" in html
    assert "chart-data" in html
    assert "Formula Logic Trace" in html
    assert "Sources" in html
    assert "Assumptions" in html
    assert "Template Boundary Statement" in html

    decision_response = client.get("/api/report/decision")
    assert decision_response.status_code == 200
    decision = decision_response.get_json()["decision"]
    assert decision["output_format"] == "html_a4"
    assert "print-ready A4 HTML" in decision["reason"]

    review_response = client.post("/api/review/session", json=case)
    assert review_response.status_code == 200
    review = review_response.get_json()["review"]
    assert review["session_id"]
    assert review["admin_url"].startswith("/admin/?session_id=")
    assert review["review_url"].startswith("/admin/review/?session_id=")

    state_response = client.get(f"/api/review/state/{review['session_id']}")
    assert state_response.status_code == 200
    assert state_response.get_json()["review"]["status"] == "ready_for_review"

    batch_response = client.post("/api/batch/run", json={"cases": [case, case]})
    assert batch_response.status_code == 200
    payload = batch_response.get_json()
    assert payload["status"] == "ok"
    assert payload["count"] == 2


def test_i18n_api_and_language_toggle_shell():
    client = create_app().test_client()

    en_response = client.get("/api/i18n/en")
    assert en_response.status_code == 200
    assert en_response.get_json()["btn_calculate"] == "Run Calculation"
    assert en_response.get_json()["language_chinese"] == "Chinese"

    zh_response = client.get("/api/i18n/zh")
    assert zh_response.status_code == 200
    assert zh_response.get_json()["btn_calculate"] == "执行计算"
    assert zh_response.get_json()["language_english"] == "英文"

    page = client.get("/")
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert 'id="langToggle"' in html
    assert 'id="latexTemplateSelect"' in html
    assert 'id="capabilityStrip"' in html
    assert 'id="chartsSection"' in html
    assert 'id="checksSection"' in html
    assert 'id="traceSection"' in html
    assert 'id="btnAdminReview"' in html
    assert 'id="adminReviewStatus"' in html
    assert 'data-lang="en"' in html
    assert 'data-lang="zh"' in html
    assert 'data-i18n-title="language_label"' in html
    assert "static/js/i18n.js" in html


def test_deploy_artifacts_present():
    project_root = cfg.PROJECT_ROOT
    deploy_script = project_root / "deploy" / "one_click_deploy.sh"
    runbook = project_root / "release" / "runbook.md"
    compose = project_root / "deploy" / "docker-compose.yml"
    nginx = project_root / "deploy" / "nginx" / "engineering-calc.conf"

    assert deploy_script.exists()
    assert "docker compose up -d --build" in deploy_script.read_text(encoding="utf-8")
    assert 'ECS_ENV_FILE="$ENV_FILE"' in deploy_script.read_text(encoding="utf-8")
    assert "ADMIN_REVIEW_PASSWORD" in deploy_script.read_text(encoding="utf-8")
    assert runbook.exists()
    assert "bash deploy/one_click_deploy.sh" in runbook.read_text(encoding="utf-8")
    assert "marimo-formula-admin" in compose.read_text(encoding="utf-8")
    assert "127.0.0.1:2718:2718" in compose.read_text(encoding="utf-8")
    assert "127.0.0.1:2719:2719" in compose.read_text(encoding="utf-8")
    assert "/admin/formulas/" in nginx.read_text(encoding="utf-8")


def test_export_json_accepts_posted_form_data():
    client = create_app().test_client()

    response = client.post(
        "/api/export/json",
        json={"project": {"project_id": "P002", "case_id": "C002", "title": "Export"}},
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")


def test_import_export_preserves_design_options():
    client = create_app().test_client()
    case = {
        "project": {"project_id": "P004", "case_id": "C004", "title": "Options"},
        "design_options": {"method": "LRFD", "gamma": 1.25},
    }

    import_response = client.post("/api/import/json", json=case)
    assert import_response.status_code == 200
    imported = import_response.get_json()["data"]
    assert imported["design_options"] == case["design_options"]

    export_response = client.post("/api/export/json", json=imported)
    assert export_response.status_code == 200
    exported = export_response.get_json()
    assert exported["design_options"] == case["design_options"]
