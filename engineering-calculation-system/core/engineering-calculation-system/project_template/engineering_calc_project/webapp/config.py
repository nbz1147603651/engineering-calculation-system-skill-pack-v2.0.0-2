"""Flask application configuration."""

from __future__ import annotations

import os
from pathlib import Path

# Project root: one level up from webapp/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
LATEX_TEMPLATE_DIR = PROJECT_ROOT / "latex" / "templates"

# Flask settings
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

# Server settings
HOST = os.environ.get("APP_HOST", "0.0.0.0")
PORT = int(os.environ.get("APP_PORT", "5000"))

# Persistent runtime paths
DATA_DIR = Path(os.environ.get("DATA_DIR", DATA_DIR))
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", OUTPUT_DIR))
FORMULA_REGISTRY_DIR = Path(os.environ.get("FORMULA_REGISTRY_DIR", DATA_DIR / "formula_registry"))
LATEX_TEMPLATE_DIR = Path(os.environ.get("LATEX_TEMPLATE_DIR", LATEX_TEMPLATE_DIR))
DEFAULT_LATEX_TEMPLATE_ID = os.environ.get("DEFAULT_LATEX_TEMPLATE_ID", "default_engineering_calcbook")

# Default calculation parameters served on page load so the user can calculate
# immediately without filling every field. Keep this structure aligned with
# webapp.form_utils.build_case_input_from_form and tests/smoke/example_input.json.
DEFAULTS: dict = {
    "project": {
        "project_id": "DEMO_001",
        "case_id": "DEMO_CASE_001",
        "project_name": "Template Demonstration Project",
        "title": "Template Demonstration Project",
    },
    "inputs": {
        "checks": [
            {
                "check_id": "DEMO-001",
                "name": "Template demand/capacity check",
                "demand": 45.0,
                "capacity": 90.0,
                "limit": 1.0,
                "unit": "kN",
                "source_reference": "S01",
            }
        ]
    },
    "design_options": {
        "calculation_basis": "template_demonstration",
        "report_status": "review",
    },
}