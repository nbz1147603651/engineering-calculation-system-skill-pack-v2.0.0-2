---
name: frontend-and-review-interfaces
description: Build production web UIs, API routes, form-to-model mapping, frontend JavaScript modules, i18n, charts, numeric sanitization, and Marimo review apps for engineering calculation books. Use when creating operational review interfaces over run_book(), BookInput, BookResult, and ReportContext while keeping formulas out of presentation and review layers.
---

# Frontend and Review Interfaces

Use this skill when the user needs an operational UI, API, review notebook, or module review surface.

## Goal

Create interfaces that make engineering review efficient while remaining thin over trusted calculation modules.

Recommended interface families:

```text
production frontend: browser UI for inputs, calculation, report preview, import/export, and review
Marimo review app: Python-native module inspection, draft edits, traces, and what-if review
API route layer: thin parse -> model -> run_book -> UI/result conversion endpoints
```

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

## Unified Frontend Layout

Use this layout unless an existing product design overrides it:

```text
top bar:
  book/project title, case selector, report status, import/export, report preview, language switch

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

## Required Final Response

Provide:

```text
layout summary
mapping module and functions
API route table
frontend module breakdown
i18n/sanitization/chart decisions
Marimo review scope if used
proof that UI and review layers do not calculate
smoke test
run command
deployment-ready entrypoint when final delivery is expected
```
