---
name: engineering-calculation-book
description: Parent/orchestrator skill for building, refactoring, extending, reviewing, testing, packaging, or deploying reusable engineering calculation book software from a validated Implementation Handoff Contract. Use for typed inputs/results, decoupled reusable formula modules, module asset accumulation, official book runners, report contexts, unified production frontends, Marimo module review apps, import/export packages, batch workflows, traceability, regression tests, local runnable web clients, and Linux cloud deployment.
---

# Engineering Calculation Book — Parent Orchestrator

Use this parent skill after a valid implementation handoff exists, or when the user explicitly requests a prototype with clearly recorded assumptions.

This skill builds engineering calculation books as reusable, auditable software systems, not disposable scripts.

## Core Principle

Correctness and traceability come first. Reuse comes second. Presentation comes third.

Never place engineering formulas in:

```text
UI code
frontend code
review apps
report templates
batch scripts
CSV/Excel input files
presentation-only code
```

All official calculation paths must call:

```python
def run_book(book_input: BookInput) -> BookResult:
    ...
```

Operational interfaces should use the shared layout pattern from Skill 12:

```text
top bar for case/status/import/export/report preview
left panel for grouped BookInput forms
right workbench for governing summary, warnings/errors, results, charts, and traces
modal/drawer for report preview, imported report comparison, source trace, formula trace, and package validation
status strip for hashes, versions, package id, and timestamp
```

## Child Skills to Use

Use these child skills in order:

```text
08-calculation-book-architecture
09-core-and-data-models
10-reusable-calculation-modules
11-book-runner-and-governing-summary
12-report-review-batch-interfaces
12a-report-context-and-rendering when reports or report previews are needed
12b-frontend-and-review-interfaces when production UI, API, charts, i18n, or Marimo review is needed
12c-batch-import-export-packages when import/export, upload packages, or batch execution is needed
13-verification-regression-traceability
14-cloud-web-release-deployment when the result must be a runnable local or Linux-cloud deployable web calculator
```

If implementation handoff is missing, incomplete, or not source-backed, route upstream:

```text
01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07
```

## Dependency Direction

Use only this direction:

```text
presentation / report / review / batch / API
  -> books
    -> libraries
      -> core
```

Forbidden reverse dependencies:

```text
core imports libraries/books/UI/report
libraries import books/UI/report/batch
books import UI pages or report templates
reports/templates recalculate engineering results
batch runner implements separate formula logic
```

## Required Implementation Flow

1. Read `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md`.
2. Classify requested features by layer.
3. Define project structure and dependency rules.
4. Define core statuses, errors, metadata, units, validators, hash and serialization utilities.
5. Define typed `BookInput`, `BookResult`, module input/result models, and result paths.
6. Implement reusable calculation modules with formula traces.
7. Implement official `run_book()` orchestration.
8. Implement governing summary and warnings/errors aggregation.
9. Use Skill 12 to select required interface subskills, then build report context, unified frontend, Marimo module review app, API, CLI, import/export package flow, or batch only as thin interfaces over `run_book()`.
10. Add unit, branch, lookup, regression, integration, and smoke tests.
11. Package local and cloud Linux web release artifacts when final delivery is expected.
12. Record acceptance status.

## Required Final Output

For new calculation book systems, provide:

```text
feature classification table
project structure
input schemas and typed models
unit system and status semantics
reusable module interfaces
module asset registry
book runner design
governing summary design
result path registry
report context design when needed
unified review/frontend/batch flow when needed
Marimo review app design when needed
data package import/export contract when needed
test plan and skeletons
run commands
local and cloud Linux deployment commands when final delivery is expected
acceptance checklist
```
