---
name: frontend-and-review-interfaces
description: Build production web UIs, API routes, form-to-model mapping, frontend JavaScript modules, i18n, charts, numeric sanitization, and Marimo review apps for engineering calculation books. Use when creating operational review interfaces over run_book(), BookInput, BookResult, and ReportContext while keeping formulas out of presentation and review layers.
---

# Frontend and Review Interfaces

Use this skill when the user needs an operational UI, API, review notebook, or module review surface.

## Goal

Create interfaces that make engineering review efficient while remaining thin over trusted calculation modules.

Prioritize operator quality and convenience:

```text
clear input grouping and validation
fast calculation feedback
visible governing status, warnings, and errors
source and formula trace review
report preview and export
import/export packages for repeatable work
charts only when they improve engineering judgment
Marimo review when module-level inspection or formula publishing is valuable
```

Do not strip useful workflow features just to keep the frontend small. Keep formulas out of the UI, but make the UI comfortable and complete for repeated engineering use.

Recommended interface families:

```text
production frontend: browser UI for inputs, calculation, report preview, import/export, and review
Marimo review app: Python-native module inspection, draft edits, traces, and what-if review
API route layer: thin parse -> model -> run_book -> UI/result conversion endpoints
```

## Primary Frontend Format

The default frontend is a browser web app served from `webapp/`:

```text
page shell: Jinja2 templates in webapp/templates/
styling: Bootstrap 5 plus webapp/static/css/style.css
JavaScript: vanilla modules in webapp/static/js/
API style: JSON endpoints under /api/
interaction model: server-rendered shell with API-driven calculation/review interactions
```

Use this default format for most calculation books. Use React, Vue, a separate SPA build, or another frontend format when interaction complexity, maintainability, or operator convenience justifies it and the handoff records the build, routing, API, testing, and deployment consequences.

## Deployment-Ready Web App Minimum

For production web delivery, include:

```text
webapp/app.py or equivalent application factory
create_app() entrypoint for gunicorn or platform runtime
GET /health endpoint for deployment smoke tests
environment-based host, port, secret, debug, data, and output paths
local run command such as python -m webapp.app
production run command such as gunicorn "webapp.app:create_app()"
```

## Static HTML Delivery Guard

A single `.html` file, exported report HTML, or static mockup is not a production web calculation system. It may be delivered only when the user explicitly asks for a static prototype, and then it must be labeled `prototype`, `draft`, or `not_production_ready`.

For production frontend work, the browser page must be backed by the same backend/API path used in tests and deployment: form data maps to `BookInput`, API routes call `run_book()`, and the frontend renders returned `BookResult`/UI data.

Report HTML belongs under report/export outputs. It must not be treated as the application runtime.

## Unified Frontend Layout

Use this layout unless an existing product design overrides it:

```text
top bar:
  book/project title, case selector, report status, import/export, report preview, Chinese/English language switch

left input panel:
  grouped BookInput forms, units, validation feedback, sticky run/save controls

right review workbench:
  governing summary, warnings/errors, result tables/cards, charts, source traces, formula traces

modal or drawer:
  report preview, imported report comparison, source trace, formula trace, package validation, input/result diff

status strip:
  input hash, result hash, runner version, report template version, package id, timestamp
```

Use `templates/implementation/ui_layout_spec.md`.

## Low-Freedom UI Kit

Use `templates/implementation/ui_design_system.md` before generating or modifying production UI. This is the default constraint layer for Qoder and other code generators.

Keep the global structure, token files, shared partials, and action placement stable. Vary only the BookInput fields, BookResult sections, charts, and trace content required by the calculation book.

Required UI kit assets:

```text
webapp/templates/partials/_topbar.html
webapp/templates/partials/_report_modal.html
webapp/static/css/tokens.css
webapp/static/css/components.css
webapp/static/css/style.css
```

Do not replace the standard top bar, input/review split, status strip, report modal, language switch, automatic final report download, or LaTeX template selector/export action unless the implementation handoff explicitly records a justified design-system override.

## Form and API Contract

Create explicit conversion functions:

```text
form_to_model(data: dict) -> BookInput
model_to_form(model: BookInput) -> dict
result_to_ui(result: BookResult) -> dict
```

Rules:

```text
place conversion in a dedicated mapping module
keep route handlers thin
use explicit field-by-field mapping
validate required fields before runner calls
sanitize NaN and Infinity before JSON responses
preserve unit conversion at input/output boundaries only
record mapping decisions in form_mapping_spec.md
```

Use `templates/implementation/form_mapping_spec.md` and `templates/implementation/api_route_skeleton.md`.

## Frontend JavaScript

Keep JavaScript focused:

```text
forms.js: collect, populate, reset, validate, dynamic lists
results.js: render summaries, status badges, utilization bars, trace expansion
i18n.js: language switching and data-i18n replacement
main.js: API calls, event binding, loading states, orchestration
```

Do not calculate engineering results in JavaScript.

## i18n, Sanitization, and Charts

Use i18n when the project serves multilingual engineers or clients:

```text
single translation dictionary
data-i18n attributes
/api/i18n/<lang> endpoint
visible Chinese/English toggle in the interactive UI
localStorage or equivalent persisted language preference
document.documentElement.lang and data-lang update on every switch
selected lang included in calculate/report preview/report download calls when backend text can vary
bilingual chart variants when needed
```

Use a recursive sanitizer for non-finite numeric values. Display sanitized values as `--` or `N/A` and preserve warnings.

Generate charts from already-computed `BookResult` values. Charts visualize; they do not calculate.

Use:

```text
templates/implementation/i18n_pattern.md
templates/implementation/chart_integration.md
src/<pkg>/core/sanitize.py or equivalent
```

## Marimo Review Apps

Use Marimo when reviewers need interactive module-level inspection.

Create apps under:

```text
apps/review/<book_name>_review.py
apps/review/modules/<module_name>_review.py
```

Each review app should expose:

```text
case/package loader
module selector
editable draft inputs
run selected module or full run_book()
governing result and warnings/errors
input/result diff
formula traces and source references
review notes and decision
save draft input or module review log
```

Label exploratory edits as `draft`, `review`, or `prototype` until saved, rerun through the official path, and verified.

Use `templates/implementation/marimo_review_spec.md`.

## Embedded Admin Review

When Marimo is embedded in the main deployed site, use this production shape:

```text
main web app at /
Marimo admin review at /admin/review/
Marimo runs as a separate service behind nginx or the platform proxy
shared formula registry at data/formula_registry/
```

Run Marimo with `marimo run`, not `marimo edit`, in production. Protect it with an environment-provided admin token/password and HTTPS. The admin page may edit declaration-based formula rules, but it must not provide arbitrary Python source editing. Publishing may update production only after validation and smoke tests pass.

Use:

```text
templates/implementation/admin_marimo_review_spec.md
templates/implementation/formula_registry_spec.md
templates/implementation/formula_rule_schema.yaml
templates/implementation/formula_publish_log.csv
```

## Required Final Response

Provide:

```text
layout summary
UI design system files used
operator convenience and review-quality decisions
mapping module and functions
API route table
frontend module breakdown
frontend format and file layout
i18n/sanitization/chart decisions
Marimo review scope if used
embedded admin review route and token strategy if used
proof that UI and review layers do not calculate
proof that the delivery is not static-HTML-only when production delivery is expected
smoke test
run command
deployment-ready entrypoint when final delivery is expected
```
