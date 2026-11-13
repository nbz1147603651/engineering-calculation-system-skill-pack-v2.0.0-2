import importlib.util
from pathlib import Path


def _import_review_app(filename: str):
    path = Path(__file__).resolve().parents[2] / "apps" / "review" / filename
    module_name = filename.removesuffix(".py")
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.__name__ == module_name
    assert hasattr(module, "app")
    if importlib.util.find_spec("marimo") is None:
        assert module.app.message == "Marimo is not installed. Install with: python -m pip install marimo"
    return module


def test_calculation_review_importable():
    _import_review_app("calculation_review.py")


def test_admin_formula_review_importable():
    _import_review_app("admin_formula_review.py")
