from webapp.app import create_app


def test_health_and_calculate_routes():
    client = create_app().test_client()

    assert client.get("/health").status_code == 200
    response = client.post(
        "/api/calculate",
        json={"project": {"project_id": "P001", "case_id": "C001", "title": "Example"}},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["formula_registry"]["version"]


def test_import_report_and_batch_routes():
    client = create_app().test_client()
    case = {"project": {"project_id": "P003", "case_id": "C003", "title": "Batch"}}

    import_response = client.post("/api/import/json", json=case)
    assert import_response.status_code == 200
    assert import_response.get_json()["status"] == "ok"

    preview_response = client.post("/api/report/preview", json=case)
    assert preview_response.status_code == 200
    assert preview_response.get_json()["status"] == "ok"

    html_response = client.post("/api/report/html", json=case)
    assert html_response.status_code == 200
    assert html_response.headers["Content-Type"].startswith("text/html")

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
    assert 'data-lang="en"' in html
    assert 'data-lang="zh"' in html
    assert 'data-i18n-title="language_label"' in html
    assert "static/js/i18n.js" in html


def test_export_json_accepts_posted_form_data():
    client = create_app().test_client()

    response = client.post(
        "/api/export/json",
        json={"project": {"project_id": "P002", "case_id": "C002", "title": "Export"}},
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
