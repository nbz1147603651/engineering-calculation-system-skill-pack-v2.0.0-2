---
name: calculation-book-architecture
description: Design the project and package architecture for a reusable engineering calculation book system from a validated implementation handoff, including feature classification, dependency rules, package layout, and file placement.
---

# Calculation Book Architecture

Use this skill as the first implementation-stage skill.

## Goal

Design the software architecture before writing formulas or interfaces.

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
  tests/
  verification/
```

## Required Output Artifacts

```text
implementation/00_architecture/project_structure.md
implementation/00_architecture/feature_classification.csv
implementation/00_architecture/dependency_rules.md
implementation/00_architecture/package_layout.md
```

## Required Final Response

Provide:

```text
architecture decision
feature classification
project tree
layer placement
forbidden dependencies
implementation order
```
