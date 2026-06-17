# Marimo Review Specification

Use Marimo for Python-native, reactive engineering review pages when module-level checking, editable inputs, or exploratory scenarios are useful.

## App Locations

```text
apps/review/<book_name>_review.py
apps/review/modules/<module_name>_review.py
```

## Launch Commands

```bash
marimo edit apps/review/<book_name>_review.py
marimo run apps/review/<book_name>_review.py
```

Use `marimo edit` for authoring and engineering development. Use `marimo run` for a read-only review app.

## Standard Review Page

| Section | Required content |
| --- | --- |
| Header | project, case, package id, report status, source basis, runner version |
| Package loader | file upload or file browser for data packages and final inputs |
| Module selector | module list from handoff/module registry |
| Editable input | BookInput group or module input model using form controls or data editor |
| Run cell | call selected trusted module or run_book() |
| Result summary | status, governing value, warnings/errors |
| Trace review | formula ids, source references, lookup ids, branch decisions |
| Diff review | current draft vs final input/result/imported report |
| Notes and decision | reviewer notes, accepted/rejected/needs change |
| Save/export | draft input, review log row, BookResult JSON, upload package |

## Module Review Rules

- Each editable field must map to a typed input field.
- Each result value must map to a module result path or BookResult path.
- Exploratory edits must be labeled draft/review/prototype.
- Saving an edit must write a new draft input or review artifact; do not overwrite final input silently.
- Module pages may call reusable modules directly for review, but official report generation must use `run_book()`.
- The page must display warnings/errors and traceability before export.

## Suggested Widgets

Use the available Marimo UI widgets that fit the project:

```text
file upload for local user-provided packages
file browser for server-side package selection
data editor for tabular module inputs
dropdown or tabs for module selection
forms and sliders for scenario exploration
tables/dataframes for check summaries and diffs
download controls for JSON/report/package artifacts
```

## Review Log

Write review decisions to:

```text
implementation/04_interfaces/module_review_log.csv
outputs/logs/module_review_log.csv
```

Do not use the review log as calculation input. It is an audit record.

