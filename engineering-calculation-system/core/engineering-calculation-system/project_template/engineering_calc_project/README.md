# Engineering Calculation Project Scaffold

This scaffold supports the full v2 lifecycle:

```text
references -> analysis -> handoff -> implementation -> src -> tests -> deploy -> release
```

Start with `references/acquisition/` when materials are missing or insufficient.

## Default Stack

```text
Primary runtime: Python 3.9+
Calculation modules: Python package under src/pkg/libraries/
Official runner: src/pkg/books/book_name/book_runner.py::run_book
Backend/API: Flask application factory at webapp.app:create_app()
Frontend format: Jinja2 templates + Bootstrap 5 + vanilla JavaScript modules
Frontend files: webapp/templates/, webapp/templates/partials/, and webapp/static/
UI kit: tokens.css + components.css + book-specific style.css
UI language: Chinese/English switch via webapp/i18n.py, /api/i18n/<lang>, and webapp/static/js/i18n.js
Report export: automatic final report at /api/report/final, HTML preview/download, and Overleaf-compatible LaTeX zip at /api/report/latex
Report decision: /api/report/decision selects latex_pdf when latexmk or pdflatex is available, otherwise html_a4
LaTeX templates: list via /api/report/templates; send latex_template_id when downloading, or omit it to use the default template
Review/admin: Marimo when enabled
```

The browser UI is a web application served by the Python backend. It is not a standalone static HTML deliverable, and it must not contain engineering formulas.

Delivery mode: `web-complete` unless the user explicitly requests `core-only`,
`report-only`, or `prototype-web`. A CLI runner, static HTML, exported report
HTML, notebook demo, or UI mockup is not a deployable web calculation system.

Operational quality and reviewer convenience take priority over minimal dependencies. Keep the implementation maintainable, but do not remove validation, traces, report preview, import/export, or review tooling when they make engineering work safer or faster.

LaTeX report templates live under `latex/templates/default_engineering_calcbook/`. If a client or company template is supplied, add it as a separate folder under `latex/templates/<template_id>/` with `main.tex.j2`. The UI lists available templates from `/api/report/templates` and sends `latex_template_id` to `/api/report/latex`; a missing or empty value falls back to `default_engineering_calcbook`. Keep `src/pkg/report/latex_renderer.py` as a presentation-only renderer over trusted `BookResult` and `ReportContext` data. Final report generation uses `src/pkg/report/report_selector.py`: if local LaTeX is available, `src/pkg/report/latex_renderer.py` must compile without errors and produce `main.pdf`; otherwise `src/pkg/report/html_renderer.py` renders a rigorous A4 HTML calculation report with formula logic traces and `@page size: A4`.

## Validate

From this directory:

```bash
python3 -m pytest -q
```

## Run Locally

```bash
python3 -m pip install "flask>=3.0" "gunicorn>=21.2" "marimo>=0.8"
python3 -m webapp.app
```

Health check:

```bash
curl -fsS http://127.0.0.1:5000/health
```

## Deploy on Linux

Docker Compose path:

```bash
cd deploy
# edit SECRET_KEY and ADMIN_REVIEW_TOKEN before production use
docker compose up -d --build
```

Main app: `http://127.0.0.1:5000/`

Marimo admin review: `http://127.0.0.1:2718/`

Behind nginx, expose the admin page at `https://example.com/admin/review/`.

systemd/gunicorn path:

```bash
gunicorn "webapp.app:create_app()" --bind 127.0.0.1:5000 --workers 2
```

Formula registry:

```text
data/formula_registry/active_versions.yaml
data/formula_registry/modules/<module_id>/versions/<version_id>.yaml
outputs/logs/formula_publish_log.csv
```

The Marimo admin app may publish declaration-based formulas only after validation passes. The browser UI and report templates must not contain engineering formulas.

From the skill pack root:

```bash
python3 scripts/validate_artifacts.py --package-root . --profile core --project project_template/engineering_calc_project --delivery web-complete
```
