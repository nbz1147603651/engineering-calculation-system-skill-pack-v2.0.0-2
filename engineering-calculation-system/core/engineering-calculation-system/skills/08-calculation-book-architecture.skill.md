---
name: calculation-book-architecture
description: Design the project and package architecture for a reusable engineering calculation book system from a validated implementation handoff, including feature classification, dependency rules, decoupled reusable module boundaries, module asset registry, package layout, deployment layout, and file placement.
---

# Calculation Book Architecture

## When to use

First implementation-stage skill. Design the software architecture before writing formulas or
interfaces. Plan reusable modules as long-lived assets, not book-local helpers.

## Inputs

`handoff/implementation_handoff.yaml`, `handoff/coding_go_no_go.md`. If the gate is `no_go`,
produce only scaffold or architecture notes — do not implement production formulas.

## Steps

1. Classify every feature by layer (use `templates/implementation/feature_classification.csv`):
   core platform | reusable engineering library | calculation-book runner | report context/
   renderer | review/frontend | batch/CLI/API | verification | release/deployment. For each
   feature record: Existing module? | New module needed? | Reusable? | Location | Notes.
2. Fix the dependency direction (non-negotiable, see `shared/lifecycle.md`):
   `presentation/report/review/batch/API -> books -> libraries -> core`. Define the forbidden
   reverse dependencies in `templates/implementation/dependency_rules.md`.
3. Define reusable module boundaries: library modules must be independent of a specific web page,
   report, batch job, database, or file layout; expose typed input/options/result models; own
   source-backed formulas/lookup behavior/intermediate values; return warnings/errors instead of
   hiding assumptions; be registered in `module_asset_registry.csv`.
4. Define the package layout and default project structure
   (`templates/implementation/package_layout.md`, `templates/implementation/project_structure.md`):
   `src/<pkg>/{core,libraries,books/<book_name>,interfaces,report}`, `webapp/`, `apps/review/`,
   `data/{input,imported,staging,normalized/cases,packages}`, `outputs/{results_json,reports_*,
   upload_packages,logs}`, `deploy/{nginx,systemd}`, `release/`, `tests/`, `verification/`.
5. Seed `implementation/02_modules/module_asset_registry.csv` with the planned module IDs.

## Artifacts

```text
implementation/00_architecture/project_structure.md     (templates/implementation/project_structure.md)
implementation/00_architecture/feature_classification.csv
implementation/00_architecture/dependency_rules.md      (templates/implementation/dependency_rules.md)
implementation/00_architecture/package_layout.md        (templates/implementation/package_layout.md)
implementation/02_modules/module_asset_registry.csv
```

## Exit gate

Architecture prevents formulas in UI/report/batch; dependency direction is fixed. See
`shared/lifecycle.md` row 08. Next path: 09 for core/data models.
