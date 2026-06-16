---
name: report-review-batch-interfaces
description: Build polished, review-readable report, frontend, Marimo review, CLI, API, import/export, upload-package, and batch interfaces over a trusted engineering calculation book runner and BookResult. Use when creating production web UIs, module review notebooks, data/report import flows, uploadable calculation packages, report previews, or batch summaries, while keeping formulas and independent pass/fail logic out of presentation layers.
---

# Report, Review, Batch, and Interface Layer

Use this skill after `run_book()` and `BookResult` exist or are specified.

## Goal

Create user-facing, reviewer-facing, and batch-facing interfaces that consume `BookInput`, `BookResult`, or `ReportContext` without implementing engineering calculations.

Interfaces must be:

```text
thin over run_book()
review-readable
consistent across projects
pleasant enough for daily engineering use
able to import/export managed data packages
able to preview or import prior reports for review and comparison
```

This skill is domain-neutral about engineering discipline, but not layout-neutral. Use the unified operational layout below unless the user or existing app gives a stronger local design system.

## Interface Families

Select one or more interface families and record the choice.

```text
production frontend: polished browser UI for daily input, calculation, report preview, import/export, and batch operation
Marimo review app: reactive reviewer page for module-by-module inspection, editing, trace checks, and what-if exploration
report renderer: HTML/PDF/DOCX/XLSX/JSON generated from ReportContext
CLI/API/batch: automation layer for repeatable runs and package processing
```

Use Marimo for interactive engineering review when a Python-native reactive page is useful. Author with `marimo edit`; publish a read-only review app with `marimo run`. Marimo pages may use file upload, file browser, and data editor widgets for managed review workflows, but they must still call trusted modules or `run_book()`.

## Unified Frontend Layout

Use a stable layout so every calculation book is easy to reproduce and manage:

```text
top bar:
  book/project title, case selector, report status, import package, export package, report preview, language switch if needed

left input panel:
  collapsible input cards grouped by BookInput model groups
  compact labels, units, required markers, validation feedback
  sticky run/validate/save controls at the bottom

right review workbench:
  governing summary first
  warnings/errors/unresolved assumptions near the top
  result cards ordered by engineering review sequence
  tables, charts, source traces, formula traces, and report preview links

modal or drawer:
  report preview, imported report preview, source trace, formula trace, data package validation, input/result diff

status strip:
  input hash, result hash, runner version, report template version, data package id, timestamp
```

This layout mirrors a repeatable engineering dashboard pattern: inputs stay on the left, conclusions and audit evidence stay on the right, and import/export/report actions stay in a predictable top-level location.

## Review Readability Contract

A review UI is not complete unless a checker can answer these questions quickly:

```text
What is the overall result?
Which check governs?
What input and source basis produced it?
What warnings, errors, or assumptions block final status?
Which formulas, lookup tables, and branch decisions were used?
What changed from the saved final input, previous result, or imported report?
Can the reviewer export the exact input/result package that generated this view?
```

Required readability rules:

```text
show conclusion before detail
show source basis and design code/version near the top
never hide warnings, errors, unresolved assumptions, or prototype status
use tables for comparable checks and cards only for distinct result groups
make every editable field map to a BookInput path
make every displayed result map to a BookResult or ReportContext path
show units with fields and values
provide trace expansion for critical formulas, lookups, and branch decisions
mark exploratory Marimo edits as draft/prototype until saved and verified
```

## Report Production Decision Protocol

Before designing or rendering a report, decide and record:

```text
report purpose
intended audience
review depth
report status
required output formats
governing source basis
required inputs and saved result source
required traceability metadata
required report sections derived from user needs and BookResult
renderer choice and reason
frontend layout choice and reason
Marimo review app choice if used
data package import/export requirements
verification method
known limitations
```

The agent may choose an appropriate rendering stack, but must preserve the unified frontend layout for operational UIs unless an existing product design overrides it. The choice must be justified by the requested deliverable, environment, review requirements, and data already present in `BookResult` or `ReportContext`.

## Report Status

Use explicit report status labels:

```text
draft
review
final
superseded
prototype
not_for_construction
```

Do not label a report `final` or production-ready unless the coding gate allows production work, the source basis is sufficient, the report is generated from saved final input or a trusted saved `BookResult`, and verification has passed.

## Allowed Responsibilities

Interfaces may:

```text
parse CSV / JSON / YAML / XLSX / ZIP / API input
import prior reports as review artifacts
map fields to BookInput
validate input before runner call
call run_book()
call trusted reusable modules for module-level Marimo review
display inputs and results
build ReportContext from BookResult
render reports
run batch cases
save normalized input JSON
save BookResult JSON
write batch summaries
write data package manifests and hashes
export uploadable calculation packages
```

## Forbidden Responsibilities

Interfaces must not:

```text
implement engineering formulas
perform unit conversion for official calculations except at input/output boundaries
calculate capacity, settlement, reinforcement, hydraulic results, or load combinations independently
recalculate pass/fail status
hide warnings/errors
treat imported reports as calculation truth unless converted through a source-backed BookInput/BookResult path
overwrite final inputs or results from exploratory UI edits without an explicit save, hash, and verification step
```

## Form ↔ Model Bidirectional Mapping

Every production frontend needs two conversion functions that form the bridge between web forms and typed models:

```text
form_to_model(data: dict) -> BookInput    # parse web form JSON into typed BookInput
model_to_form(model: BookInput) -> dict    # serialize BookInput back to form JSON
result_to_ui(result: BookResult) -> dict   # flatten BookResult into UI-friendly dict
```

Rules:

```text
place all mapping logic in one module (e.g. webapp/form_utils.py)
never put mapping logic in route handlers or template renderers
use explicit field-by-field conversion, not reflection or magic
default every optional field to a safe value (0.0, None, empty list)
validate required fields and raise clear errors before runner call
sanitize output for JSON: replace NaN/Infinity with null before response
preserve units during conversion — convert only at boundaries
record mapping decisions in implementation/04_interfaces/form_mapping_spec.md
```

The result-to-UI converter should:

```text
round all floats to display precision (3–4 decimals)
convert enums to strings for JSON serialization
include governing status, utilization, and status badge text
embed SVG charts inline when available
include bilingual chart variants when i18n is active
flag sanitized (Infinity/NaN) fields with warnings
```

## API Route Pattern

Use a single Blueprint or router module with these standard endpoints:

```text
GET  /                          serve main page
GET  /api/defaults              return default calculation parameters
GET  /api/i18n/<lang>           return i18n translations
POST /api/calculate             accept form JSON → run_book() → return result UI dict
POST /api/report/html           generate and download HTML report
POST /api/report/preview        generate HTML report and return as inline preview string
POST /api/import/json           import CaseInput/BookInput JSON file
GET  /api/export/json           export current config as JSON download
POST /api/optimize              auto-optimize parameters if applicable
```

Route handler rules:

```text
keep handlers thin: parse → build model → call runner → convert result → return
use try/except with structured error JSON response
delegate all conversion to the form mapping module
never call calculation modules directly from route handlers
support both file upload and raw JSON body for import endpoints
return Content-Disposition header for all download responses
```

Error response contract:

```json
{"status": "error", "message": "human-readable description"}
```

In debug mode, include traceback. In production, return generic error message.

## Frontend Architecture Pattern

Use a lightweight frontend stack that stays close to the server:

```text
recommended stack: Jinja2 templates + Bootstrap 5 + vanilla JS
alternative stack: React/Vue + Flask/FastAPI backend
review stack: Marimo for interactive engineering review
```

Separate frontend JS into focused modules:

```text
forms.js     form interaction, dynamic lists (e.g. soil layers), validation feedback
results.js   render result cards, status badges, utilization bars, trace expansion
i18n.js      language toggle, data-i18n attribute replacement, bilingual content
main.js      API calls, event binding, orchestration, loading states
```

HTML template structure:

```text
base.html                layout shell: navbar, modal, script includes
index.html               extends base, defines left-input / right-result grid
partials/_project_form   project info input card
partials/_soil_form      soil profile with dynamic layer list
partials/_foundation_form  geometry input card
partials/_loads_form     load case input card
partials/_options_form   design options input card
partials/_results_panel  governing box + result cards (collapsible)
```

Interaction flow:

```text
page load → fetch /api/defaults → populate forms
click calculate → POST /api/calculate → render results panel
click preview → POST /api/report/preview → show in modal iframe
click import → file upload → POST /api/import/json → populate forms
click export → GET /api/export/json → browser download
click optimize → POST /api/optimize → show suggestion dialog → apply
toggle language → fetch /api/i18n/<lang> → replace all data-i18n elements
```

## Internationalization (i18n)

For projects that serve multilingual engineers or international clients:

```text
use a single master dictionary: key -> (english, chinese)
expose via /api/i18n/<lang> endpoint
use data-i18n="key" attributes in HTML elements
replace text content on language toggle via JS
generate bilingual charts (one SVG per language) and toggle via CSS classes
include i18n for: form labels, buttons, result titles, status text, error messages, chart labels
do not hard-code display text in templates — always use i18n keys
```

i18n dictionary categories:

```text
navigation and layout (title, subtitle, buttons)
section titles (project, soil, foundation, loads, options, results)
form field labels and help text
result display labels (governing, bearing, settlement, sliding, uplift)
status text (PASS, FAIL, warnings, errors)
error and warning messages
report sections
```

Record the i18n strategy in `implementation/04_interfaces/i18n_pattern.md`.

## Numeric Sanitization

Engineering calculations frequently produce non-finite floats (Infinity from division by zero, NaN from invalid parameters). These values break JSON serialization and frontend rendering.

```text
implement a recursive sanitizer that walks dicts/lists/tuples
replace float('inf'), float('-inf'), float('nan') with None
record sanitization warnings with field path and reason
attach warnings to the API response under a "warnings" key
frontend should display '--' or 'N/A' for null numeric values
show a non-blocking warning banner when sanitization occurred
```

Place the sanitizer in the form mapping module or core utilities. Call it as the last step before `jsonify()` in every API response that contains calculation results.

## Chart and Visualization Integration

Charts improve engineering review when they reveal patterns that tables cannot.

```text
generate charts server-side using matplotlib or plotly
render as SVG strings for inline embedding in HTML responses
support bilingual chart labels when i18n is active
embed charts in the result-to-UI dict as {zh: svg_zh, en: svg_en}
frontend toggles visibility via CSS classes (bi-zh / bi-en)
```

Recommended chart types for geotechnical and structural calculations:

```text
result breakdown (bar chart showing component contributions)
stress or force distribution (line chart over depth)
influence factor distribution (line chart)
time-dependent curve (consolidation, creep)
soil or member profile (schematic diagram)
utilization summary (horizontal bar chart for all checks)
```

Rules:

```text
charts must not calculate — they visualize already-computed BookResult values
label axes with units
use consistent color coding for PASS (green) / FAIL (red) / WARNING (amber)
keep SVG size reasonable (< 50KB per chart)
provide chart data as structured dicts alongside SVG for accessibility
```

Record chart strategy in `implementation/04_interfaces/chart_integration.md`.

## Default Configuration and Error Handling

Every production frontend should load with sensible defaults so the user can calculate immediately:

```text
define a DEFAULTS dict in webapp/config.py with all form fields populated
serve defaults via GET /api/defaults on page load
allow user to reset to defaults via a button
```

Error handling strategy:

```text
API errors return structured JSON: {status: "error", message: "..."}
HTTP 400 for bad input or calculation failure
HTTP 404 for missing resources
HTTP 500 for unexpected server errors
in debug mode, include full traceback in the message
in production, log full traceback server-side, return generic message to client
frontend shows error in a dismissible alert banner
never lose user input on error — preserve form state
```

## Import, Report Import, and Upload Packages

Use a managed data area:

```text
data/input/                  user-provided source inputs
data/imported/reports/       prior HTML/PDF/DOCX/XLSX/context reports used for review or comparison
data/imported/references/    project-provided reference files allowed by access rules
data/staging/                uploaded but not yet accepted files
data/normalized/cases/       normalized BookInput JSON per case
data/packages/               unpacked upload/export packages with manifest
outputs/results_json/        trusted BookResult JSON
outputs/reports_html/        generated HTML reports
outputs/reports_pdf/         generated PDF reports
outputs/reports_docx/        generated DOCX reports
outputs/upload_packages/     ZIP or folder packages ready to share/upload
```

Upload package flow:

```text
upload ZIP or files
-> store in data/staging/
-> compute hashes and inspect manifest
-> classify inputs, reports, references, and outputs
-> normalize accepted inputs into BookInput JSON
-> show validation and diff summary
-> run_book only after user selects case or batch
-> save BookResult and export package
```

Imported reports are review artifacts. They may support visual comparison, regression evidence, or client review, but must not inject formulas or override official status.

## Marimo Module Review Pattern

Create Marimo apps under:

```text
apps/review/<book_name>_review.py
apps/review/modules/<module_name>_review.py
```

Each Marimo review page should include:

```text
case/package loader
module selector
editable module input fields or data editor
run selected module or full run_book()
governing result and warnings/errors
input/result diff from saved final or imported reference
formula traces and source references
review notes and decision
save draft input, module review log, or export package
```

Marimo review pages may use sliders and editable tables for what-if exploration. Label all such results as `draft`, `review`, or `prototype` until the exact input is saved, re-run through the official path, and verified.

## Report Flow

```text
final_input.json
-> run_book()
-> BookResult
-> save BookResult JSON
-> build_report_context()
-> template/render function
-> report
-> optional upload package
```

## Report Context Contract

Build `ReportContext` as a presentation contract over computed results. It should expose enough structured data for the chosen renderer without forcing a fixed report layout.

Include when applicable:

```text
report production decision
project and case metadata
report status and output target
design basis and source references
input summary
assumptions and limitations
module summaries
governing summary
checks and result paths
intermediate values selected for audit
warnings and errors
formula traces or source trace references
imported report comparison metadata
data package metadata
appendix data
traceability metadata
```

Report sections should be derived from:

```text
user-requested deliverable
calculation scope
BookResult result paths
required review questions
source-backed reporting requirements
warnings, errors, and unresolved assumptions
```

Templates may contain value references, loops, conditionals, formatting filters, section visibility logic, unit display formatting, and cross-references. Templates must not contain engineering formulas, independent unit conversion for official calculations, optimization logic, load-combination generation, or independent pass/fail logic.

## Batch Flow

```text
read batch_control.csv or uploaded package manifest
-> load case input
-> validate
-> run_book()
-> save normalized input JSON
-> save BookResult JSON
-> render report if requested
-> write batch summary CSV/HTML
-> export upload package if requested
-> write logs
```

Batch workflows must preserve per-case report status, warnings, errors, result paths, hashes, and traceability metadata. A batch summary may summarize outcomes, but it must not recalculate or override case-level engineering status.

## Production Report Minimum

A production report workflow must have:

```text
recorded report production decision
explicit report status
saved final input or trusted saved BookResult
clear source basis and limitations
structured ReportContext
unified UI layout spec when frontend exists
Marimo review spec when review notebooks exist
data package manifest when import/export packages exist
renderer or export path selected for the requested deliverable
proof that templates/UI/Marimo/batch do not calculate
warnings and errors preserved in the report output
traceability metadata preserved
smoke test for each report renderer or export path
documented run command
```

If any item is missing, state the report as draft, review, prototype, or blocked according to the gap. Do not silently downgrade production requirements.

## Required Output Artifacts

```text
implementation/04_interfaces/input_mapping_spec.md
implementation/04_interfaces/ui_layout_spec.md
implementation/04_interfaces/import_export_contract.md
implementation/04_interfaces/marimo_review_spec.md
implementation/04_interfaces/report_context_spec.md
implementation/04_interfaces/review_readability_checklist.md
implementation/04_interfaces/review_schema.csv
implementation/04_interfaces/frontend_fields.csv
implementation/04_interfaces/module_review_log.csv
implementation/04_interfaces/data_package_manifest.yaml
implementation/04_interfaces/batch_flow.md
implementation/04_interfaces/form_mapping_spec.md
implementation/04_interfaces/i18n_pattern.md
implementation/04_interfaces/chart_integration.md
implementation/04_interfaces/api_route_skeleton.md
src/<pkg>/books/<book_name>/input_mapping.py
src/<pkg>/books/<book_name>/report_context.py
src/<pkg>/interfaces/
src/<pkg>/report/
src/<pkg>/core/sanitize.py
webapp/ or src/<pkg>/interfaces/webapp/
webapp/config.py
webapp/routes.py
webapp/form_utils.py
webapp/i18n.py
webapp/templates/base.html
webapp/templates/index.html
webapp/templates/partials/
webapp/static/js/
webapp/static/css/
apps/review/ when Marimo review is requested
tests/smoke/test_<report_or_interface>.py
```

## Required Final Response

Provide:

```text
which BookInput or BookResult is consumed
which runner is called
unified UI layout summary
field mapping or display schema
form ↔ model bidirectional mapping module location and key functions
API route table with endpoints, methods, and responsibilities
frontend JS module breakdown
i18n strategy and dictionary scope
numeric sanitization approach
chart types and generation pipeline
import/export and upload package flow
Marimo review pages and module editing scope if used
report context fields
template or UI flow
report production decision and status
proof that formulas are not in template/UI/Marimo/batch
smoke test
run command
```
