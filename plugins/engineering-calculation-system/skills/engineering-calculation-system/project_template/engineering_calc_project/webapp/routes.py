"""Flask route handlers for the engineering calculation web app.

Scaffold: customize routes for each calculation book.
All route handlers are thin: parse → build model → call runner → convert → return.
"""

from __future__ import annotations

import json
import re
import traceback
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from flask import (
    Blueprint, jsonify, render_template, request,
    Response, send_file,
)

from . import config as cfg
from .form_utils import build_case_input_from_form, case_result_to_ui
from .i18n import get_translations

bp = Blueprint("main", __name__)
LATEX_TEMPLATE_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")


def _available_latex_templates() -> list[dict[str, object]]:
    """List importable LaTeX templates. A template is a folder with main.tex.j2."""
    if not cfg.LATEX_TEMPLATE_DIR.exists():
        return []

    templates: list[dict[str, object]] = []
    for path in sorted(cfg.LATEX_TEMPLATE_DIR.iterdir()):
        if not path.is_dir() or not (path / "main.tex.j2").exists():
            continue
        template_id = path.name
        label = (
            "Default engineering calculation book"
            if template_id == cfg.DEFAULT_LATEX_TEMPLATE_ID
            else template_id.replace("_", " ").replace("-", " ").title()
        )
        templates.append({
            "id": template_id,
            "label": label,
            "is_default": template_id == cfg.DEFAULT_LATEX_TEMPLATE_ID,
        })
    return templates


def _resolve_latex_template_dir(template_id: str | None) -> tuple[str, Path]:
    """Resolve a user-selected template ID, falling back to the default template."""
    selected = (template_id or "").strip() or cfg.DEFAULT_LATEX_TEMPLATE_ID
    if not LATEX_TEMPLATE_ID_PATTERN.match(selected):
        raise ValueError("Invalid LaTeX template id.")

    template_dir = cfg.LATEX_TEMPLATE_DIR / selected
    if not template_dir.exists() or not (template_dir / "main.tex.j2").exists():
        raise FileNotFoundError(f"LaTeX template not found or incomplete: {selected}")
    return selected, template_dir


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


@bp.route("/api/capabilities")
def api_capabilities():
    """Return optional runtime capability status without installing anything."""
    from pkg.core.capabilities import detect_capabilities

    return jsonify(detect_capabilities())


@bp.route("/api/report/templates")
def api_report_templates():
    """Return available LaTeX/Overleaf report templates for user selection."""
    return jsonify({
        "status": "ok",
        "default_template_id": cfg.DEFAULT_LATEX_TEMPLATE_ID,
        "templates": _available_latex_templates(),
    })


@bp.route("/api/report/decision")
def api_report_decision():
    """Return the automatic calculation-book renderer decision for this host."""
    from pkg.report.report_selector import select_report_output

    return jsonify({
        "status": "ok",
        "decision": select_report_output().to_dict(),
    })


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
        from pkg.books.book_name.report_context import build_report_context
        from pkg.report.html_renderer import build_html_report_context, render_a4_html_report

        result = run_book(book_input)
        report_context = build_report_context(result)
        html_context = build_html_report_context(
            book_input,
            result,
            report_context,
            lang=lang,
        )
        html = render_a4_html_report(html_context)

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


@bp.route("/api/report/latex", methods=["POST"])
def api_report_latex():
    """Generate an Overleaf-compatible LaTeX calculation report package."""
    try:
        data = request.get_json(force=True)
        lang = data.pop("lang", "en")
        template_request = data.pop("latex_template_id", None) or data.pop(
            "latexTemplateId", None
        )
        template_id, template_dir = _resolve_latex_template_dir(template_request)
        book_input = build_case_input_from_form(data)

        from pkg.books.book_name.book_runner import run_book
        from pkg.books.book_name.report_context import build_report_context
        from pkg.report.latex_renderer import build_latex_report_context, render_latex_project_zip

        result = run_book(book_input)
        report_context = build_report_context(result)
        latex_context = build_latex_report_context(
            book_input,
            result,
            report_context,
            lang=lang,
            template_version=f"{template_id}-v1",
        )
        package_bytes = render_latex_project_zip(latex_context, template_dir)

        return Response(
            package_bytes,
            mimetype="application/zip",
            headers={
                "Content-Disposition": (
                    f"attachment; filename=latex_report_{book_input.project.project_id}.zip"
                )
            },
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "LaTeX report generation failed.",
        }), 400


@bp.route("/api/report/final", methods=["POST"])
def api_report_final():
    """Generate the strictest available calculation-book report for this host."""
    try:
        data = request.get_json(force=True)
        lang = data.pop("lang", "en")
        template_request = data.pop("latex_template_id", None) or data.pop(
            "latexTemplateId", None
        )
        book_input = build_case_input_from_form(data)

        from pkg.books.book_name.book_runner import run_book
        from pkg.books.book_name.report_context import build_report_context
        from pkg.report.html_renderer import build_html_report_context, render_a4_html_report
        from pkg.report.latex_renderer import build_latex_report_context, compile_latex_project
        from pkg.report.report_selector import select_report_output

        result = run_book(book_input)
        report_context = build_report_context(result)
        decision = select_report_output()

        if decision.output_format == "latex_pdf":
            template_id, template_dir = _resolve_latex_template_dir(template_request)
            latex_context = build_latex_report_context(
                book_input,
                result,
                report_context,
                lang=lang,
                template_version=f"{template_id}-v1",
            )
            with TemporaryDirectory(prefix="engineering_calc_latex_") as tmp:
                compiled = compile_latex_project(latex_context, template_dir, Path(tmp))
                pdf_bytes = Path(compiled["pdf_path"]).read_bytes()
            return Response(
                pdf_bytes,
                mimetype="application/pdf",
                headers={
                    "Content-Disposition": (
                        f"attachment; filename=calculation_report_{book_input.project.project_id}.pdf"
                    ),
                    "X-Report-Renderer": "latex_pdf",
                    "X-Report-Compiler": str(decision.latex_tool),
                    "X-Report-Decision": decision.reason,
                },
            )

        html_context = build_html_report_context(
            book_input,
            result,
            report_context,
            lang=lang,
        )
        html = render_a4_html_report(html_context)
        return Response(
            html,
            mimetype="text/html",
            headers={
                "Content-Disposition": (
                    f"attachment; filename=calculation_report_{book_input.project.project_id}.html"
                ),
                "X-Report-Renderer": "html_a4",
                "X-Report-Decision": decision.reason,
            },
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "Final report generation failed.",
        }), 400


@bp.route("/api/report/preview", methods=["POST"])
def api_report_preview():
    """Generate HTML report and return it as a string for inline preview."""
    try:
        data = request.get_json(force=True)
        lang = data.pop("lang", "en")
        book_input = build_case_input_from_form(data)

        from pkg.books.book_name.book_runner import run_book
        from pkg.books.book_name.report_context import build_report_context
        from pkg.report.html_renderer import build_html_report_context, render_a4_html_report

        result = run_book(book_input)
        report_context = build_report_context(result)
        html_context = build_html_report_context(
            book_input,
            result,
            report_context,
            lang=lang,
        )
        html = render_a4_html_report(html_context)

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


@bp.route("/api/export/json", methods=["GET", "POST"])
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


@bp.route("/api/batch/run", methods=["POST"])
def api_batch_run():
    """Run a JSON batch through the official book runner, one case at a time."""
    try:
        payload = request.get_json(force=True) or {}
        cases = payload.get("cases")
        if cases is None and "project" in payload:
            cases = [payload]
        if not isinstance(cases, list) or not cases:
            return jsonify({
                "status": "error",
                "message": "Batch payload must contain a non-empty cases list.",
            }), 400

        from pkg.books.book_name.book_runner import run_book

        results = []
        for index, case_data in enumerate(cases, start=1):
            if not isinstance(case_data, dict):
                return jsonify({
                    "status": "error",
                    "message": f"Case {index} must be a JSON object.",
                }), 400

            book_input = build_case_input_from_form(case_data)
            result = run_book(book_input)
            results.append({
                "case_index": index,
                "project_id": book_input.project.project_id,
                "case_id": book_input.project.case_id,
                "status": "ok",
                "result": case_result_to_ui(result, book_input),
            })

        return jsonify({
            "status": "ok",
            "count": len(results),
            "results": results,
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "Batch run failed.",
        }), 400


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@bp.app_errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Not found"}), 404


@bp.app_errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "message": "Internal server error"}), 500
