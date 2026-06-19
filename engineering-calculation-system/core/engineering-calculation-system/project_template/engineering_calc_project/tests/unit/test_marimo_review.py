import importlib.util
from pathlib import Path


def test_admin_formula_review_importable():
    path = Path(__file__).resolve().parents[2] / "apps" / "review" / "admin_formula_review.py"
    spec = importlib.util.spec_from_file_location("admin_formula_review", path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "app")
