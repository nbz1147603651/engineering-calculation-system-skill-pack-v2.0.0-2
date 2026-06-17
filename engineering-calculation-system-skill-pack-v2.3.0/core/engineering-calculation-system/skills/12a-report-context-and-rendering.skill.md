---
name: report-context-and-rendering
description: Design and implement source-backed engineering calculation report context, report production decisions, renderer choices, report templates, report preview, and HTML/PDF/DOCX/XLSX/JSON exports over trusted BookResult data. Use when building reports or report previews while keeping templates free of engineering formulas and independent pass/fail logic.
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
PDF for frozen deliverables
DOCX for editable client/report workflows
XLSX for tabular export or audit appendices
JSON for machine-readable packages
```

The chosen renderer must preserve warnings, limitations, source basis, report status, and traceability metadata.

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
documented run command
```

If any item is missing, label the report `draft`, `review`, `prototype`, or `not_for_construction`.

## Required Final Response

Provide:

```text
ReportContext fields
renderer choice and reason
report status
saved input/result source
template boundary proof
output paths
smoke test
remaining limitations
```
