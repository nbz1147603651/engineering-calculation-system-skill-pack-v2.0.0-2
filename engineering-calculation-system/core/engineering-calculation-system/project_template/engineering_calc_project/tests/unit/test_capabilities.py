import importlib.metadata
import importlib.util

from pkg.core.capabilities import detect_capabilities


def test_capabilities_marimo_missing(monkeypatch):
    real_find_spec = importlib.util.find_spec

    def fake_find_spec(name):
        if name == "marimo":
            return None
        return real_find_spec(name)

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)

    payload = detect_capabilities({})

    assert payload["capabilities"]["marimo"]["status"] == "missing"
    assert payload["capabilities"]["marimo_review"]["status"] == "missing"
    assert payload["capabilities"]["marimo_review"]["install_command"] == "python -m pip install marimo"


def test_capabilities_marimo_configured(monkeypatch):
    class FakeSpec:
        origin = "test-marimo"

    def fake_find_spec(name):
        if name == "marimo":
            return FakeSpec()
        return None

    def fake_version(name):
        if name == "marimo":
            return "1.2.3"
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)
    monkeypatch.setattr(importlib.metadata, "version", fake_version)

    payload = detect_capabilities({
        "ADMIN_REVIEW_TOKEN": "secret",
        "MARIMO_BASE_URL": "/admin/review/",
    })

    assert payload["capabilities"]["marimo"]["status"] == "available"
    assert payload["capabilities"]["marimo"]["version"] == "1.2.3"
    assert payload["capabilities"]["marimo_review"]["status"] == "configured"
    assert payload["capabilities"]["marimo_review"]["admin_url"] == "/admin/review/"
    assert payload["capabilities"]["marimo_review"]["service_url"] == "http://127.0.0.1:2718/"
    assert "apps/review/calculation_review.py" in payload["capabilities"]["marimo_review"]["run_command"]
    assert "--token-password <ADMIN_REVIEW_TOKEN>" in payload["capabilities"]["marimo_review"]["run_command"]
    assert "admin_formula_review.py" in payload["capabilities"]["marimo_review"]["formula_admin_run_command"]


def test_capabilities_marimo_available_without_token(monkeypatch):
    class FakeSpec:
        origin = "test-marimo"

    def fake_find_spec(name):
        if name == "marimo":
            return FakeSpec()
        return None

    monkeypatch.setattr(importlib.util, "find_spec", fake_find_spec)

    payload = detect_capabilities({})

    review = payload["capabilities"]["marimo_review"]
    assert review["status"] == "available"
    assert review["available"] is True
    assert review["configured"] is False
    assert review["shell_url"] == "/admin/review/"
    assert "Set ADMIN_REVIEW_TOKEN" in review["message"]
