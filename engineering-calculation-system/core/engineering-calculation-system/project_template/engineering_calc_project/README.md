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
Official runner: src/pkg/books/example_book/book_runner.py::run_book
Backend/API: Flask application factory at webapp.app:create_app()
Frontend format: Jinja2 templates + Bootstrap 5 + vanilla JavaScript modules
Frontend files: webapp/templates/, webapp/templates/partials/, and webapp/static/
UI kit: tokens.css + components.css + book-specific style.css
UI language: Chinese/English switch via webapp/i18n.py, /api/i18n/<lang>, and webapp/static/js/i18n.js
Report export: print-ready A4 HTML final report at /api/report/final, HTML preview/download, and Overleaf-compatible LaTeX zip at /api/report/latex
Report decision: /api/report/decision defaults to html_a4; LaTeX/PDF is an explicit export/request path
LaTeX templates: list via /api/report/templates; send latex_template_id when downloading, or omit it to use the default template
Charts: structured BookResult.charts from src/pkg/books/example_book/charts.py, rendered by reports and UI without recalculating engineering results
Figures: optional ReportContext.figures or BookResult.figures with source references and report placement metadata
Review/admin: Marimo calculation review when enabled; formula rule publishing remains a separate admin flow
Admin gate: `/admin/` requires `ADMIN_REVIEW_PASSWORD`; Marimo review at `/admin/review/` and formula publishing at `/admin/formulas/` require `ADMIN_REVIEW_TOKEN`
One-click Linux deploy: `bash deploy/one_click_deploy.sh`
```

The browser UI is a web application served by the Python backend. It is not a standalone static HTML deliverable, and it must not contain engineering formulas.

Delivery mode: `web-complete` unless the user explicitly requests `core-only`,
`report-only`, or `prototype-web`. A CLI runner, static HTML, exported report
HTML, notebook demo, or UI mockup is not a deployable web calculation system.

When migrating an existing static calculation book, treat `reports/*.html` and
legacy `report_generator.py` files as imported comparison evidence. Move the
calculation path into `run_book(BookInput) -> BookResult`, then rebuild reports,
UI, Marimo review, import/export, and deployment around that runner.

Operational quality and reviewer convenience take priority over minimal dependencies. Keep the implementation maintainable, but do not remove validation, traces, chart capability, report preview, import/export, or review tooling when they make engineering work safer or faster.

The default calculation book is a rigorous formal A4 HTML report from `src/pkg/report/html_renderer.py`, with a cover page, table of contents, formula logic traces, report figures when supplied, chart data tables when charts are emitted, and `@page size: A4` print CSS. Treat report styles as a template library: LaTeX templates live under `latex/templates/<template_id>/`, with `default_engineering_calcbook` as the built-in style. If a client or company template is supplied, add it as a separate folder with `main.tex.j2` and `template_manifest.yaml`. The UI lists available templates from `/api/report/templates` and sends `latex_template_id` to `/api/report/latex`; a missing or empty value falls back to `default_engineering_calcbook`. Keep `src/pkg/report/{html_renderer,latex_renderer}.py` as presentation-only renderers over trusted `BookResult` and `ReportContext` data. When PDF is explicitly requested and local LaTeX is available, `src/pkg/report/latex_renderer.py` must compile without errors and produce `main.pdf`.

## Validate

From this directory:

```bash
python3 -B -m pytest -q -p no:cacheprovider
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
# edit deploy/.env or let the script create it from deploy/env.example
bash deploy/one_click_deploy.sh compose
```

Main app: `http://127.0.0.1:5000/`

Review setup shell: `http://127.0.0.1:5000/admin/`

Marimo calculation review: `http://127.0.0.1:2718/`

Marimo formula publisher: `http://127.0.0.1:2719/`

Behind nginx, expose the review app at `https://example.com/admin/review/` and the formula publisher at `https://example.com/admin/formulas/`.

systemd/gunicorn path:

```bash
gunicorn "webapp.app:create_app()" --bind 127.0.0.1:5000 --workers 2
```

One-click local fallback:

```bash
bash deploy/one_click_deploy.sh local
```

Formula registry:

```text
data/formula_registry/active_versions.yaml
data/formula_registry/modules/<module_id>/versions/<version_id>.yaml
outputs/logs/formula_publish_log.csv
```

The browser can create a Marimo review session through `/api/review/session`, which saves BookInput, BookResult, ReportContext, and FormulaTrace data under `outputs/review/`. The Marimo calculation review app reads those sessions for live Python review and appends decisions to `outputs/review/review_decisions.jsonl`.

The separate Formula Review Admin may publish declaration-based formulas only after validation passes. The browser UI and report templates must not contain engineering formulas.

If Marimo is not installed on the Linux host, the main calculator still runs and `/admin/` shows the Marimo install prompt instead of pretending review is available.

From the skill pack root:

```bash
python3 scripts/validate_artifacts.py --package-root . --profile core --project project_template/engineering_calc_project --delivery web-complete
```
