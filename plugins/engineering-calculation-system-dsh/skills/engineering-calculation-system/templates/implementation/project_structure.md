# Project Structure

```text
engineering_calc_project/
  references/
  analysis/
  handoff/
  data/
    input/
    imported/
      reports/
      references/
    staging/
    normalized/
      cases/
    packages/
  implementation/
  src/<pkg>/
    core/
    libraries/
    books/<book_name>/
    interfaces/
    report/
  webapp/
  latex/
    templates/
      default_engineering_calcbook/
      <custom_template_id>/
    generated/
    output/
  apps/
    review/
  deploy/
    nginx/
    systemd/
  release/
  tests/
  verification/
  outputs/
    results_json/
    reports_html/
    reports_latex/
    reports_pdf/
    reports_docx/
    upload_packages/
    logs/
```

## Placement Rules

Record where each feature class belongs and which files own formulas, runner orchestration, reports, interfaces, and tests.

Use `webapp/` or `src/<pkg>/interfaces/webapp/` for the unified production frontend. The default web format is Jinja2 templates, Bootstrap 5, and vanilla JavaScript modules served by the Python backend. Use `latex/` for reusable LaTeX/Overleaf-compatible report templates and generated source packages. Treat report styles as a template library: every reusable LaTeX style is a folder under `latex/templates/<template_id>/` with a manifest, and future file-based HTML styles should use the same stable template-ID/version convention. Use `src/pkg/report/html_renderer.py`, `src/pkg/report/latex_renderer.py`, and `src/pkg/report/report_selector.py` for report generation: print-ready A4 HTML is the default final calculation book, while LaTeX/PDF is explicit or handoff-required export. Use `apps/review/` for Marimo review apps. Use `data/` for user-provided, imported, staging, normalized, and package-managed data. Use `outputs/` only for generated artifacts. Use `deploy/` for Linux/cloud runtime files and `release/` for final delivery checklists or runbooks.

Reusable calculation assets belong under `src/<pkg>/libraries/` and must be registered in `implementation/02_modules/module_asset_registry.csv`.
