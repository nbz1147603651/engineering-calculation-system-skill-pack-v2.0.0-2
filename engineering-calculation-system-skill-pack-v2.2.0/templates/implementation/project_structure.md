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
    reports_pdf/
    reports_docx/
    upload_packages/
    logs/
```

## Placement Rules

Record where each feature class belongs and which files own formulas, runner orchestration, reports, interfaces, and tests.

Use `webapp/` or `src/<pkg>/interfaces/webapp/` for the unified production frontend. Use `apps/review/` for Marimo review apps. Use `data/` for user-provided, imported, staging, normalized, and package-managed data. Use `outputs/` only for generated artifacts. Use `deploy/` for Linux/cloud runtime files and `release/` for final delivery checklists or runbooks.

Reusable calculation assets belong under `src/<pkg>/libraries/` and must be registered in `implementation/02_modules/module_asset_registry.csv`.
