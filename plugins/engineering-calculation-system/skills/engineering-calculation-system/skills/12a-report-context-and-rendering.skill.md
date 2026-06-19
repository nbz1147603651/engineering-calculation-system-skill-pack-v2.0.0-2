---
name: report-context-and-rendering
description: Design and implement source-backed engineering calculation report context, report production decisions, renderer choices, report templates, report preview, and HTML/LaTeX/PDF/DOCX/XLSX/JSON exports over trusted BookResult data. Use when building reports, calculation books, LaTeX/Overleaf-compatible exports, or report previews while keeping templates free of engineering formulas and independent pass/fail logic.
---

# Report Context and Rendering

Use this skill for report production after `run_book()` and `BookResult` exist or are specified.

## Goal

Create reports from a structured `ReportContext` that wraps trusted calculation results without recalculating engineering outcomes.

Required flow:

```text
saved final input or trusted saved BookResult
-> build_report_context()
-> renderer/template
-> report output
-> optional preview or package export
```

## Report Production Decision

Before rendering, record:

```text
report purpose
intended audience
review depth
report status
required output formats
governing source basis
saved input/result source
required traceability metadata
renderer choice and reason
required report sections
verification method
known limitations
```

Use `templates/implementation/report_context_spec.md`.

## Report Status

Use explicit report status labels from Skill 12. Do not mark reports `final` until source basis, coding gate, saved input/result, and verification state all support production use.

## ReportContext Contents

Include when applicable:

```text
project and case metadata
report production decision
report status and output target
design basis and source references
input summary
assumptions and limitations
module summaries
governing summary
checks and stable result paths
chart specifications and recommended report locations
intermediate values selected for audit
warnings and errors
formula traces or source trace references
imported report comparison metadata
data package metadata
appendix data
traceability metadata
```

## Template Boundaries

Templates may contain:

```text
value references
loops and conditionals
formatting filters
section visibility logic
unit display formatting
cross-references
```

Templates must not contain:

```text
engineering formulas
lookup rules
load-combination generation
optimization logic
independent unit conversion for official calculations
independent pass/fail logic
```

## Renderer Choice

Choose the simplest renderer that satisfies the output requirement:

```text
HTML for preview and browser-native review
LaTeX project zip for Overleaf-compatible calculation books and PDF-ready workflows
PDF for frozen deliverables
DOCX for editable client/report workflows
XLSX for tabular export or audit appendices
JSON for machine-readable packages
```

The chosen renderer must preserve warnings, limitations, source basis, report status, and traceability metadata.

## Automatic Report Output Decision

For final calculation-book output, make one automatic environment-based decision before claiming completion:

```text
if latexmk or pdflatex is available locally:
  choose latex_pdf
  render the selected LaTeX template
  compile locally
  completion requires exit code 0 and main.pdf exists
else:
  choose html_a4
  render the A4 HTML calculation report
```

Use `templates/implementation/html_report_spec.md` for the HTML fallback. Generated web apps should expose `GET /api/report/decision` and `POST /api/report/final`. A failed LaTeX compilation is a blocking report failure, not a reason to silently downgrade to HTML.

## LaTeX and Overleaf-Compatible Export

Use `templates/implementation/latex_report_spec.md` when the user asks for LaTeX, Overleaf, PDF-ready calculation books, or reusable calculation-book templates.

Before first report generation or project initialization, ask whether the user has a preferred LaTeX/Overleaf template, `.cls/.sty` file, company cover, page format, or section order. If no template is supplied, use the default template:

```text
latex/templates/default_engineering_calcbook/
```

Record the interaction result in the report production decision as `user_selected`, `user_declined`, or `no_response_default`. Generated web apps should expose `GET /api/report/templates` and send the selected value as `latex_template_id` to `POST /api/report/latex`; if the value is missing or empty, the backend must use `default_engineering_calcbook`.

Generate an Overleaf-compatible zip package by default. Do not require a self-hosted Overleaf server for normal exports.

Required implementation shape:

```text
src/pkg/report/latex_renderer.py
src/pkg/report/html_renderer.py
src/pkg/report/report_selector.py
GET /api/report/templates
POST /api/report/latex
POST /api/report/final
latex/templates/default_engineering_calcbook/main.tex.j2
latex/templates/default_engineering_calcbook/cover.tex.j2
latex/templates/default_engineering_calcbook/page_style.sty
latex/templates/default_engineering_calcbook/sections/
outputs/reports_latex/
tests/smoke/test_latex_report.py
```

LaTeX templates follow the same template boundary rules as HTML/DOCX/PDF templates: display already-computed values and traces only; never calculate engineering outcomes.

## A4 HTML Calculation Report

When no local LaTeX compiler is available, render HTML as a formal A4 calculation book, not a loose web page. The HTML must include `@page size: A4`, print-safe margins, cover/title block, governing summary, input summary, engineering charts when `BookResult.charts` is present, calculation checks, formula logic trace, warnings/errors, traceability metadata, and a template boundary statement. Formula logic must be shown from stored traces; the HTML must not calculate or override status.

When `BookResult.charts` is present, place engineering charts after the governing/input summary and before detailed check tables unless the handoff specifies another review order. Charts must display stored values and source result paths only.

## Production Minimum

A production report workflow must have:

```text
recorded report production decision
explicit report status
saved final input or trusted saved BookResult
clear source basis and limitations
structured ReportContext
template boundary proof
warnings and errors preserved in output
traceability metadata preserved
smoke test for each renderer or export path
LaTeX compile test or explicit no-LaTeX HTML fallback record
documented run command
```

If any item is missing, label the report `draft`, `review`, `prototype`, or `not_for_construction`.

## Required Final Response

Provide:

```text
ReportContext fields
renderer choice and reason
LaTeX/Overleaf template decision when applicable
report status
saved input/result source
template boundary proof
output paths
smoke test
remaining limitations
```
