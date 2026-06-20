# Skill Package Summary

## Package purpose

Create a maintainable skill architecture for engineering calculation systems covering:

```text
1. reference discovery and local persistence
2. reference analysis and calculation logic modeling
3. implementation of auditable calculation book software
4. release of runnable local and Linux-cloud deployable web calculation programs
```

## Design decision

Use parent orchestrators plus specialized child skills:

```text
root SKILL.md entrypoint
3 parent skills
18 child skills
shared contracts
templates
artifact schemas
validation scripts
project scaffold
```

The default v2.4 install target is `dist/core/engineering-calculation-system/`. Examples, workflow diagrams, historical source files, and agent-specific adapters are development or overlay material, not part of the default runtime skill.

## Main gates

```text
evidence gate
analysis gate
implementation handoff gate
coding gate
report production gate
verification gate
release deployment gate
```

## Main artifacts

```text
reference_gap_assessment.md
acquisition_plan.yaml
source_coverage_matrix.csv
source_registry.yaml
acquisition_handoff.yaml
calculation_blueprint.md
formula_inventory.csv
implementation_handoff.yaml
BookInput / BookResult models
run_book()
unified UI layout spec
Marimo review spec
data_package_manifest.yaml
module_asset_registry.csv
cloud_linux_deployment.md
release_checklist.md
test_matrix.csv
```

## Default runtime and frontend

```text
Primary runtime: Python 3.9+
Calculation modules: Python packages under src/<pkg>/libraries/
Official runner: run_book(BookInput) -> BookResult
Backend/API: Flask or FastAPI thin routes
Default frontend: browser web app under webapp/
Default web format: Jinja2 templates + Bootstrap 5 + vanilla JavaScript modules
Review/admin: Marimo when Python-native review or formula publishing is needed
```

## Stack principle

```text
Optimize for engineering operation quality and reviewer convenience first.
Use the simplest stack that still provides complete validation, traceability, review, reporting, import/export, and deployment workflows.
Do not remove useful workflow capability merely to reduce dependencies.
Upgrade the frontend or review stack when the handoff shows clear usability, maintainability, or safety value.
```

## v2.1 hardening

```text
cross-agent entrypoints
closed template coverage for declared artifacts
artifact_contracts.json
scripts/validate_artifacts.py
pytest-ready project_template
separated evidence gate and coding gate semantics
```

## Acquisition rule

```text
reference discovery must actively use available internet search/browser/retrieval tools
every meaningful search must be logged
accepted and rejected candidates must be recorded
tool unavailability must be stated explicitly
```

## Report production rule

```text
report production decisions must be recorded without hard-coding one domain or report structure
report status must match evidence, coding gate, and verification state
final reports must come from saved final input or trusted BookResult
ReportContext must preserve warnings, errors, limitations, source basis, and traceability
templates, UI, and batch flows must not calculate or override engineering status
```

## Interface rule

```text
production frontends should use the unified top-bar / left-input / right-review layout
Marimo review apps should support module-level inspection, editable draft inputs, traces, and review logs
data/report imports should be staged, classified, hashed, and normalized before official calculation
upload/export packages should include manifest, inputs, trusted results, reports, hashes, and versions
final web programs should include local run commands, Linux cloud deployment files, health checks, and release smoke records
calculation modules should be decoupled reusable assets recorded in module_asset_registry.csv
administrator formula edits should use declaration-based formula registry publishing through a protected Marimo review app, not arbitrary Python source editing
static HTML files and exported report HTML are outputs or prototypes, not complete production web calculation systems
```

## v2.4.0 multi-agent orchestration

```text
shared/multi-agent-orchestration.md          optional supervisor/worker contract
templates/orchestration/parallel_work_plan.yaml
templates/orchestration/agent_result_packet.yaml
templates/orchestration/merge_review.md
```

Use multi-agent orchestration only for explicit multi-agent, delegated, or
parallel work. Split work by disjoint owned paths. Keep evidence gates, coding
gates, source authority, ID allocation, handoff freeze, `run_book()` public
contract changes, and final acceptance with the supervisor.

## v2.2.0 interface split

```text
Skill 12 is now a lightweight interface router.
Skill 12a handles ReportContext, renderer choices, report status, and template boundaries.
Skill 12b handles production frontends, API routes, form mapping, i18n, charts, sanitization, and Marimo review.
Skill 12c handles managed data areas, upload packages, import/export, hashes, manifests, and batch runs.
Skill 14 handles local runnable web clients, Linux cloud deployment, release checklists, and deployment smoke tests.
```

## v2.4.0 release layering

```text
dist/core/engineering-calculation-system/    default runtime skill
dist/adapters-light/                         optional AGENTS/OpenCode/Trae/generic overlay
dist/qoder-addon/                            optional Qoder overlay
dist/singlefile/                             generated all-in-one fallback
dist/source-dev/                             development/reference bundle
dist/release/                                platform release zips and checksums
  engineering-calculation-system-CODEX-v2.4.1.zip
  engineering-calculation-system-MiniMaxCode-v2.4.1.zip
  engineering-calculation-system-QODER-v2.4.1.zip
  engineering-calculation-system-QODER-Project-v2.4.1.zip
  engineering-calculation-system-TRAE-v2.4.1.zip
  engineering-calculation-system-OpenCode-v2.4.1.zip

tools/release_config.json                    release metadata and platform publish target config
```

`engineering-calculation-system-MiniMaxCode-v2.4.1.zip` keeps the standard root `SKILL.md` layout for MiniMax Code import or auto-discovery. `engineering-calculation-system-QODER-v2.4.1.zip` is a direct QODER Skill upload package with `SKILL.md` at the zip root. `engineering-calculation-system-QODER-Project-v2.4.1.zip` is the QODER project-root overlay package.

## Best use

1. Start with the router.
2. Let the evidence gate decide whether new references must be gathered.
3. Persist gathered references locally before analysis.
4. Analyze persisted references into a Calculation Logic Blueprint.
5. Freeze the implementation handoff before coding.
6. Implement formulas only inside reusable calculation modules and book runners.
7. Use Skill 12 to select report, frontend/review, or batch/package subskills when interfaces are needed.
8. Verify with unit, branch, lookup, regression, integration, interface, package, and smoke tests.
9. Package final web systems with local run instructions, Linux deployment files, release checklist, deployment smoke evidence, and proof that the delivery is not static-HTML-only.
