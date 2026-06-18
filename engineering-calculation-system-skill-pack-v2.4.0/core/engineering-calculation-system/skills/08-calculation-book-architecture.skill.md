---
name: calculation-book-architecture
description: Design the project and package architecture for a reusable engineering calculation book system from a validated implementation handoff, including feature classification, dependency rules, decoupled reusable module boundaries, module asset registry, package layout, deployment layout, and file placement.
---

# Calculation Book Architecture

Use this skill as the first implementation-stage skill.

## Goal

Design the software architecture before writing formulas or interfaces.

Plan reusable modules as long-lived assets, not book-local helpers.

## Required Inputs

```text
handoff/implementation_handoff.yaml
handoff/coding_go_no_go.md
```

If the gate is `no_go`, produce only scaffold or architecture notes; do not implement production formulas.

## Dependency Direction

```text
presentation / report / review / batch / API
  -> books
    -> libraries
      -> core
```

## Feature Classification

Before implementation, classify every feature:

| Feature | Layer | Existing module? | New module needed? | Reusable? | Location | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Layers:

```text
core platform
reusable engineering library
calculation book runner
report context / renderer
review/frontend
batch / CLI / API
verification
release / deployment
```

## Reusable Module Boundaries

Before coding, define which engineering logic belongs in reusable libraries and which orchestration belongs in book runners.

Reusable library modules must:

```text
be independent from a specific web page, report, batch job, database, or file layout
expose typed input/options/result models
own source-backed formulas, lookup behavior, and intermediate values
return warnings/errors instead of hiding assumptions
be registered in module_asset_registry.csv
```

## Default Project Structure

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
  outputs/
    results_json/
    reports_html/
    reports_pdf/
    reports_docx/
    upload_packages/
    logs/
  deploy/
    nginx/
    systemd/
  release/
  tests/
  verification/
```

## Required Output Artifacts

```text
implementation/00_architecture/project_structure.md
implementation/00_architecture/feature_classification.csv
implementation/00_architecture/dependency_rules.md
implementation/00_architecture/package_layout.md
implementation/02_modules/module_asset_registry.csv
```

## Required Final Response

Provide:

```text
architecture decision
feature classification
project tree
layer placement
forbidden dependencies
module asset boundaries
implementation order
```
