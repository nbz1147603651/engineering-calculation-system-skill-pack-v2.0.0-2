"""Flask application configuration.

Scaffold: customize DEFAULTS and settings for each project.
"""

from __future__ import annotations

import os
from pathlib import Path

# Project root: one level up from webapp/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

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

# Default calculation parameters — served on page load so the user
# can calculate immediately without filling every field.
# Customize these defaults for each engineering calculation book.
DEFAULTS: dict = {
    "project": {
        "project_id": "EXAMPLE_001",
        "project_name": "Example Project",
    },
    "foundation": {
        # Add book-specific geometry fields here.
        # e.g. "B_m": 1.0, "L_m": 1.0, "D_m": 1.2,
    },
    "loads": {
        # Add book-specific load fields here.
        # e.g. "Fx_kN": 0.0, "Fy_kN": 0.0, "Fz_kN": 100.0,
    },
    "options": {
        # Add book-specific design options here.
        # e.g. "fos_bearing": 3.0,
    },
    # Add soil_layers, water_table, or other book-specific sections as needed.
}
