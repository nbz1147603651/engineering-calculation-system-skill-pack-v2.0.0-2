---
name: report-review-batch-interfaces
description: Route and govern report, frontend, review, API, import/export, upload-package, batch, LaTeX/Overleaf calculation-book export, and deployable-web interface work over a trusted engineering calculation book runner and BookResult. Use when the task needs presentation, review, report rendering, operational UI, data package, API, CLI, batch workflows, or a final runnable online web calculator while keeping formulas and independent pass/fail logic out of interface layers.
---

# Report, Review, Batch, and Interface Router

Use this skill after `run_book()` and `BookResult` exist or are specified.

This skill selects the correct interface subskill and enforces the shared interface rules. Load only the subskill needed by the user request.

When the interface must become a deployable online web calculator, route to Skill 14 after frontend/API verification.

## Core Principle

Interfaces consume trusted calculation outputs. They do not become calculation engines.

Never place engineering formulas, lookup rules, branch decisions, load-combination logic, or independent pass/fail decisions in:

```text
UI code
frontend JavaScript
review notebooks
report templates
batch scripts
CSV/XLSX input files
presentation-only code
```

All official paths must call:

```python
run_book(BookInput) -> BookResult
```

## Interface Subskills

Select one or more:

```text
12a-report-context-and-rendering
  Use for ReportContext design, report production decisions, renderer choice, templates, preview, HTML/LaTeX/PDF/DOCX/XLSX/JSON exports, report status, and template boundaries.

12b-frontend-and-review-interfaces
  Use for production web UI, form-to-model mapping, API route shape, frontend JavaScript structure, i18n, charts, numeric sanitization, and Marimo review apps.

12c-batch-import-export-packages
  Use for managed data areas, report import, upload packages, import/export manifests, hashes, package validation, CLI/API batch runs, and batch summaries.

14-cloud-web-release-deployment
  Use after 12b and 13 when the user expects a runnable local and cloud-deployable online web calculator.
```

If the request spans all three families, read them in this order:

```text
12a -> 12b -> 12c -> 13 -> 14 when final web release is expected
```

## Shared Interface Contract

Every interface family must preserve:

```text
BookInput path mapping
BookResult or ReportContext result paths
source basis and limitations
warnings, errors, assumptions, and prototype status
input hash and result hash when persisted
runner version and report/template version when available
stable export paths
smoke tests for each user-facing path
```

## Report Status Labels

Use explicit status:

```text
draft
review
final
superseded
prototype
not_for_construction
```

Do not label a report or interface output `final` unless the coding gate allows production work, the source basis is sufficient, the output is generated from saved final input or trusted saved `BookResult`, and verification has passed.

## Required Interface Decision Record

Before implementation, record:

```text
requested interface family
consumed BookInput / BookResult / ReportContext
runner entrypoint
source of saved input/result
report or interface status
chosen templates or UI pattern
import/export or batch scope
release/deployment scope when final web delivery is expected
verification method
known limitations
selected subskills
```

Use templates from:

```text
templates/implementation/input_mapping_spec.md
templates/implementation/ui_layout_spec.md
templates/implementation/ui_design_system.md
templates/implementation/report_context_spec.md
templates/implementation/latex_report_spec.md
templates/implementation/import_export_contract.md
templates/implementation/marimo_review_spec.md
templates/implementation/batch_flow.md
templates/implementation/data_package_manifest.yaml
templates/deployment/cloud_linux_deployment.md
templates/deployment/release_checklist.md
```

## Required Final Response

Provide:

```text
selected interface subskills
which runner is called
which BookInput, BookResult, or ReportContext is consumed
status and production eligibility
proof that formulas are not in UI/report/Marimo/batch
created or updated artifact paths
smoke test or validation command
release/deployment command when final web delivery is expected
remaining limitations
```
