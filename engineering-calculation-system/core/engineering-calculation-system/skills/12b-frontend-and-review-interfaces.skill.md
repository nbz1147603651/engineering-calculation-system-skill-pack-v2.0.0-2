---
name: frontend-and-review-interfaces
description: Build production web UIs, API routes, form-to-model mapping, frontend JavaScript modules, i18n, charts, numeric sanitization, and Marimo review apps for engineering calculation books. Use when creating operational review interfaces over run_book(), BookInput, BookResult, and ReportContext while keeping formulas out of presentation and review layers.
---

# Frontend and Review Interfaces

## When to use

When the user needs an operational UI, API, review notebook, or module-review surface. Interfaces
make engineering review efficient while remaining thin over trusted calculation modules. Do not
strip useful workflow features (input grouping/validation, fast feedback, governing status,
trace review, report preview/export, import/export, charts, Marimo review) just to keep the
frontend small — keep formulas out of the UI, but make the UI complete for repeated engineering
use. The static-HTML guard and `run_book()` contract live in `shared/lifecycle.md`.

## Steps

1. Pick the frontend format. Default: browser web app served from `webapp/` — Jinja2 shell, Bootstrap
   5 + `webapp/static/css/style.css`, vanilla JS modules under `webapp/static/js/`, JSON endpoints
   under `/api/`, server-rendered shell with API-driven interactions. Use React/Vue/SPA only when
   interaction complexity justifies it and the handoff records build/routing/API/testing/deployment
   consequences.
   If the current project has only scripts plus `reports/*.html`, create or migrate into the
   project scaffold shape first: `pyproject.toml`, `src/<pkg>/`, `webapp/`, `apps/review/`,
   `latex/templates/`, `outputs/`, `tests/`, `deploy/`, and `release/`. Do not wrap the static
   report as the UI.
2. Make the web app deployment-ready: `webapp/app.py` or application factory, `create_app()` for
   gunicorn, `GET /health`, environment-based host/port/secret/debug/data/output paths, local run
   `python -m webapp.app`, production run `gunicorn "webapp.app:create_app()"`. Report HTML lives
   under report/export outputs — it is never the application runtime. A single `.html`/exported
   report/mockup is not a production system; allowed only as an explicit static prototype labeled
   `prototype`/`draft`/`not_production_ready`.
   Required API surface for a web-complete calculator includes `GET /health`, `GET /`,
   `POST /api/calculate`, `GET /api/report/decision`, `GET /api/report/templates`,
   `POST /api/report/html`, `POST /api/report/preview`, `POST /api/report/latex`,
   `POST /api/report/final`, and review-session endpoints when Marimo review is enabled.
3. Apply the unified frontend layout (`templates/implementation/ui_layout_spec.md`) unless an
   existing product design overrides it: top bar (title, case selector, report status, import/
   export, report preview, language switch); left input panel (grouped BookInput forms, units,
   validation, sticky run/save); right review workbench (governing summary, warnings/errors,
   result tables/cards, charts, source/formula traces); modal/drawer (report preview, imported-
   report comparison, traces, package validation, input/result diff); status strip (input hash,
   result hash, runner version, report-template version, package id, timestamp).
4. Use the low-freedom UI kit (`templates/implementation/ui_design_system.md`) before generating/
   modifying production UI. Keep `webapp/templates/partials/_topbar.html`, `_report_modal.html`,
   `webapp/static/css/{tokens,components,style}.css` stable; vary only BookInput fields, BookResult
   sections, charts, and trace content. Do not replace the standard top bar, input/review split,
   status strip, report modal, language switch, automatic final-report download, or LaTeX template
   selector/export action unless the handoff records a justified override.
   When a reference product site is supplied, inherit its restrained token family in
   `tokens.css` while preserving the low-freedom layout. The default operational style mirrors
   the ZJIC/NHS-like palette: white surfaces, `#005EB8` primary blue, `#003087` dark blue,
   `#FFB81C` warm focus/action color, compact 2-4px radii, and dense engineering tables.
   Result and trace displays must follow `templates/implementation/calculation_review_card_spec.md`:
   check-family icon, engineering explanation, formula box, variable/substitution tables, source
   reference, status, and stable result path from `FormulaTrace`.
5. Build the form/API contract in a dedicated mapping module: `form_to_model(data)->BookInput`,
   `model_to_form(model)->dict`, `result_to_ui(result)->dict`. Keep route handlers thin, map
   field-by-field, validate required fields before runner calls, sanitize NaN/Infinity before JSON
   responses, preserve unit conversion at boundaries only, record decisions in
   `templates/implementation/form_mapping_spec.md` (and `api_route_skeleton.md`).
6. Structure frontend JS (`webapp/static/js/`): `forms.js` (collect/populate/reset/validate/
   dynamic lists), `results.js` (summaries, status badges, utilization bars, trace expansion,
   formula review cards from trace data using KaTeX/MathJax with plain-text fallback),
   `i18n.js` (language switching, `data-i18n` replacement), `main.js` (API calls, events, loading,
   orchestration). Do not calculate engineering results in JS.
7. Add i18n when multilingual engineers/clients are served (`templates/implementation/i18n_pattern.md`):
   single translation dictionary, `data-i18n` attributes, `/api/i18n/<lang>`, visible
   Chinese/English toggle, persisted preference, `document.documentElement.lang` + `data-lang`
   update on switch, selected lang included in calculate/report-preview/report-download calls,
   bilingual chart variants when needed. Use a recursive sanitizer for non-finite numerics
   (`src/<pkg>/core/sanitize.py`) — display as `--`/`N/A`, preserve warnings.
8. Generate useful engineering charts from already-computed `BookResult` values
   (`templates/implementation/chart_integration.md`, `src/<pkg>/books/<book_name>/charts.py`).
   Drive chart selection from the book's result-path registry, `ReportContext`, and review needs,
   not from a universal hardcoded list. When useful chartable data exists, expose structured
   `BookResult.charts`/`ChartSpec` with source result paths, data tables, and recommended UI/report
   locations; when it does not, record charts as not applicable. Charts visualize; they never
   calculate, override pass/fail, choose governing cases, or do official unit conversion.
9. Add a Marimo review app when reviewers need module-level inspection, under
   `apps/review/<book_name>_review.py` and `apps/review/modules/<module_name>_review.py`
   (`templates/implementation/marimo_review_spec.md`). For frontend-connected review, add the
   generic bridge from `templates/implementation/marimo_frontend_bridge_spec.md`: `/api/review/session`,
   `/api/review/state/<session_id>`, `src/<pkg>/review/bridge.py`, and
   `apps/review/calculation_review.py`. The Marimo app loads saved BookInput/BookResult/
   ReportContext sessions from `outputs/review/`, then supports live Python review in
   `marimo edit` and controlled token-protected `marimo run` behind `/admin/review/`.
   The interactive UI must include an obvious entry into review from the top bar. The Flask
   admin shell at `/admin/` must require an environment-provided `ADMIN_REVIEW_PASSWORD`
   before exposing review or formula-publishing controls; the Marimo services under
   `/admin/review/` and `/admin/formulas/` must also use `ADMIN_REVIEW_TOKEN` and bind to
   localhost or an internal network. If Marimo is unavailable, the admin shell must display the
   install prompt and leave the main calculator usable.
   Module review pages include: case/package loader, module selector,
   editable draft inputs, run module or full `run_book()`, governing result + warnings/errors,
   input/result diff, formula/source traces with the same formula-card fields used by web/report,
   review notes/decision, save draft or module-review
   log. Label exploratory edits `draft`/`review`/`prototype` until rerun through the official path
   and verified. Embedded admin review (`templates/implementation/admin_marimo_review_spec.md`):
   main app at `/`, Flask admin shell at `/admin/`, Marimo at `/admin/review/` as a separate service behind nginx/proxy, shared
   `data/formula_registry/`, run with `marimo run` (not `edit`), env-provided admin password,
   admin token + HTTPS, declaration-based formula rules only (no arbitrary Python editing),
   publish only after validation + smoke tests pass. Formula publishing updates
   `active_versions.yaml`; the next `/api/calculate` must expose the active registry version/hash
   in the interactive UI status strip.

## Artifacts

```text
webapp/{app.py, routes.py, config.py, form_utils.py}
webapp/templates/{base.html,index.html,partials/_topbar.html,partials/_report_modal.html}
webapp/static/js/{main,forms,results,i18n}.js
webapp/static/css/{tokens,components,style}.css
src/<pkg>/core/sanitize.py
apps/review/...
implementation/04_interfaces/{ui_layout_spec,ui_design_system,form_mapping_spec,
  api_route_skeleton,i18n_pattern,chart_integration,marimo_review_spec,
  admin_marimo_review_spec,formula_registry_spec}.md  (templates/implementation/)
```

## Exit gate

API/UI calculate through `run_book` and render real results; delivery is not static-HTML-only when
production delivery is expected. See `shared/lifecycle.md` row 12b. Next path: 12c if batch/
import-export is needed, else 13.
