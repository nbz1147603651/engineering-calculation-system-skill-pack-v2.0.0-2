# API Route Skeleton

Use this template to document the API endpoint architecture for engineering calculation web applications.

## Technology Stack

| Item | Selected value | Notes |
| --- | --- | --- |
| Framework | Flask / FastAPI | Flask with Blueprint pattern |
| Server | gunicorn (production) / flask dev (development) | — |
| Serialization | `flask.jsonify` | Structured JSON responses |
| Error format | `{"status": "error", "message": "..."}` | Consistent error contract |

## Endpoint Registry

| Method | Path | Purpose | Input | Output | Auth |
| --- | --- | --- | --- | --- | --- |
| GET | `/` | Serve main SPA page | — | HTML | none |
| GET | `/api/defaults` | Return default parameters | — | JSON (form defaults) | none |
| GET | `/api/i18n/<lang>` | Return i18n translations | lang: "en" or "zh" | JSON (key→text) | none |
| POST | `/api/calculate` | Run calculation | JSON (form data) | JSON (result UI dict) | none |
| POST | `/api/report/html` | Generate downloadable report | JSON (form data + lang) | HTML file download | none |
| POST | `/api/report/preview` | Generate report for inline preview | JSON (form data + lang) | JSON `{status, html}` | none |
| POST | `/api/import/json` | Import configuration | file upload or JSON body | JSON `{status, data}` | none |
| GET | `/api/export/json` | Export configuration | JSON (form data) | JSON file download | none |
| POST | `/api/optimize` | Auto-optimize parameters | JSON (form data + lang) | JSON (optimal result) | none |

## Handler Pattern

```python
@bp.route("/api/calculate", methods=["POST"])
def api_calculate():
    """Thin handler: parse → build model → call runner → convert → return."""
    try:
        data = request.get_json(force=True)
        ci = build_case_input_from_form(data)        # form_utils.py
        result = run_case(ci)                         # runner.py (the only calculation path)
        ui_data = case_result_to_ui(result, ci)       # form_utils.py
        return jsonify(ui_data)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if DEBUG else "Calculation failed.",
        }), 400
```

## Error Handling Strategy

| HTTP code | Trigger | Response body |
| --- | --- | --- |
| 400 | Bad input, validation error, calculation failure | `{"status": "error", "message": "details"}` |
| 404 | Missing resource | `{"status": "error", "message": "Not found"}` |
| 500 | Unexpected server error | `{"status": "error", "message": "Internal server error"}` |

```text
in DEBUG mode: include full traceback in message field
in production: log traceback server-side, return generic message to client
frontend: show error in dismissible alert banner, preserve user input
```

## Application Factory Pattern

```python
# webapp/app.py
def create_app() -> Flask:
    app = Flask(__name__, template_folder="...", static_folder="...")
    app.secret_key = cfg.SECRET_KEY
    app.config["DEBUG"] = cfg.DEBUG
    from .routes import bp
    app.register_blueprint(bp)
    return app

# Development:
#   python -m webapp.app
# Production:
#   gunicorn "webapp.app:create_app()" --bind 0.0.0.0:5000 --workers 2
```

## Rules

```text
route handlers must be thin — no business logic, no formula calls
all model building and result conversion lives in form_utils.py
all calculation lives behind run_book() / run_case() — never in routes
download responses must include Content-Disposition header
import endpoints should accept both file upload and raw JSON body
debug mode controlled by environment variable, not hard-coded
```
