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


def test_export_json_accepts_posted_form_data():
    client = create_app().test_client()

    response = client.post(
        "/api/export/json",
        json={"project": {"project_id": "P002", "case_id": "C002", "title": "Export"}},
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
