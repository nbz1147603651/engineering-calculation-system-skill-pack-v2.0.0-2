"""Flask route handlers for the engineering calculation web app.

Scaffold: customize routes for each calculation book.
All route handlers are thin: parse → build model → call runner → convert → return.
"""

from __future__ import annotations

import json
import traceback
from io import BytesIO

from flask import (
    Blueprint, jsonify, render_template, request,
    Response, send_file,
)

from . import config as cfg
from .form_utils import build_case_input_from_form, case_result_to_ui
from .i18n import get_translations

bp = Blueprint("main", __name__)


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@bp.route("/")
def index():
    """Serve the main single-page application."""
    return render_template("index.html")


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@bp.route("/api/defaults")
def api_defaults():
    """Return default calculation parameters."""
    return jsonify(cfg.DEFAULTS)


@bp.route("/api/i18n/<lang>")
def api_i18n(lang: str):
    """Return i18n translations for the given language (en or zh)."""
    if lang not in ("en", "zh"):
        lang = "en"
    return jsonify(get_translations(lang))


@bp.route("/api/calculate", methods=["POST"])
def api_calculate():
    """Run engineering calculation and return structured results.

    Flow: form JSON → BookInput → run_book() → BookResult → UI dict
    """
    try:
        data = request.get_json(force=True)
        book_input = build_case_input_from_form(data)

        # Import the book runner — the ONLY official calculation path.
        # Replace with the actual import for your calculation book.
        from pkg.books.book_name.book_runner import run_book
        result = run_book(book_input)

        ui_data = case_result_to_ui(result, book_input)
        return jsonify(ui_data)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "Calculation failed. Please check your inputs.",
        }), 400


@bp.route("/api/report/html", methods=["POST"])
def api_report_html():
    """Generate and download an HTML calculation report."""
    try:
        data = request.get_json(force=True)
        lang = data.pop("lang", "en")
        book_input = build_case_input_from_form(data)

        from pkg.books.book_name.book_runner import run_book
        result = run_book(book_input)

        # Replace with your actual report generator.
        # from pkg.report.html import generate_html_report
        # html = generate_html_report(book_input, result, lang=lang)
        html = f"<h1>Report placeholder for {book_input.project.project_id}</h1>"

        return Response(
            html,
            mimetype="text/html",
            headers={
                "Content-Disposition": f"attachment; filename=report_{book_input.project.project_id}.html"
            },
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "Report generation failed.",
        }), 400


@bp.route("/api/report/preview", methods=["POST"])
def api_report_preview():
    """Generate HTML report and return it as a string for inline preview."""
    try:
        data = request.get_json(force=True)
        lang = data.pop("lang", "en")
        book_input = build_case_input_from_form(data)

        from pkg.books.book_name.book_runner import run_book
        result = run_book(book_input)

        # Replace with your actual report generator.
        html = f"<h1>Report preview for {book_input.project.project_id}</h1>"

        return jsonify({"status": "ok", "html": html})

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "Report preview failed.",
        }), 400


@bp.route("/api/import/json", methods=["POST"])
def api_import_json():
    """Import a BookInput JSON configuration file."""
    try:
        if "file" in request.files:
            f = request.files["file"]
            raw = f.read().decode("utf-8")
        else:
            raw = request.get_data(as_text=True)

        data = json.loads(raw)
        book_input = build_case_input_from_form(data)

        # Convert BookInput back to the web form structure.
        from .form_utils import book_input_to_form
        form_data = book_input_to_form(book_input)
        return jsonify({"status": "ok", "data": form_data})

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


@bp.route("/api/export/json")
def api_export_json():
    """Export current configuration as JSON file."""
    try:
        data = request.get_json(silent=True)
        if data is None:
            data = cfg.DEFAULTS

        book_input = build_case_input_from_form(data)

        # Replace with your actual serialization.
        from .form_utils import book_input_to_form
        json_data = book_input_to_form(book_input)

        return Response(
            json.dumps(json_data, indent=2, ensure_ascii=False),
            mimetype="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=config_{book_input.project.project_id}.json"
            },
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@bp.app_errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Not found"}), 404


@bp.app_errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "message": "Internal server error"}), 500
