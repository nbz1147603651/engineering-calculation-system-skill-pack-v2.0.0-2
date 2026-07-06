---
name: engineering-calc-system
description: 工程计算系统全生命周期专家。用于工程计算、计算书、规范/标准、公式提取、查找表、分支逻辑、单位换算、批量计算、在线计算器、报告、验算、部署、Qoder/QoderCN/QoderCN CLI/Cloud Agents 适配。Use when a task involves engineering calculation references, formula/lookup/branch extraction, calculation logic blueprints, implementation handoff, auditable calculation-book software, reports, batch flows, verification, or release.
version: 2.6.0
---

# Engineering Calculation System - Qoder Entry

This file is the compact Qoder skill/resource entrypoint. It intentionally avoids
duplicating the full supervisor and reference manuals. Load only the next file
needed for the current task.

## Stable ASCII Contract

This Qoder skill is a lightweight entrypoint unless the project also contains the
complete core package:

```text
SKILL.md
skills/
shared/
templates/
schemas/
scripts/validate_artifacts.py
project_template/
```

Direct Qoder skill imports can route, explain gates, show assets, and diagnose
missing package shape. They must not claim `production_allowed`, deployable, or
`web-complete` by themselves. For production work, use the QODER Project package
or a complete core package. In release archives this is the
`engineering-calculation-system-QODER-Project-v2.6.0.zip` / `QODER-Project`
copy-to-project-root package, or the single-file fallback when layered loading is
unavailable.

`web-complete` still means dual closure: a readable calculation book and a
complete web calculation system both close before completion is claimed.

## Qoder Architecture

Use an agent-first, skill-backed architecture when Qoder custom agents are
available.

- If `.qoder/agents/engineering-calc-system.md` exists, it is the supervisor.
- This `skills/engineering-calc-system/SKILL.md` file is the lightweight
  reusable skill/resource layer.
- `qoder_quickstart.md` is the first operator file for install-shape checks,
  first prompts, and validation commands.
- `reference.md` and `.qoder/references/engineering-calc-system.md` hold long
  reference material; keep long references outside `.qoder/agents/` so Qoder
  does not list them as disabled custom agents.
- The Qoder CLI plugin layout also includes the complete core skill at
  `skills/engineering-calculation-system/`.

Packaged Qoder worker agents in QODER Project:

| Agent file | Delegation scope |
| --- | --- |
| `.qoder/agents/engineering-calc-reference-acquirer.md` | 01-03 reference acquisition |
| `.qoder/agents/engineering-calc-source-intake.md` | 04 source intake |
| `.qoder/agents/engineering-calc-logic-extractor.md` | 05-07 logic extraction and handoff drafts |
| `.qoder/agents/engineering-calc-module-worker.md` | 08-11 modules and runner support |
| `.qoder/agents/engineering-calc-interface-worker.md` | 12/12a/12b/12c API, report, frontend, batch |
| `.qoder/agents/engineering-calc-verification-worker.md` | 13 verification |
| `.qoder/agents/engineering-calc-release-worker.md` | 14 release/deployment |

## Behavior Engineering Layer

Use this layer to decide what to load, what evidence to record, and when a
completion claim is allowed. The detailed rules remain in the shared contracts;
this section is only the compact Qoder routing anchor.

1. Read `qoder_quickstart.md` at the start of a Qoder task.
2. If the complete core package is present, read
   `skills/00-engineering-calculation-router.skill.md`.
3. For every non-trivial task, read `shared/execution-discipline.md` and produce
   the route card, gate card, artifact contract, and validation evidence frame.
4. Read one parent orchestrator or child skill selected by the router; do not
   load all 01-14 skills at once.
5. For implementation, validation, or release, read `shared/lifecycle.md`.
6. For plans, read `shared/planning-discipline.md`.
7. For user, reviewer, or worker feedback, read
   `shared/review-feedback-discipline.md`.
8. For release, sync, package, or platform work, read
   `shared/version-control-discipline.md`.
9. Before claiming source-backed, production, formula verified, report-ready,
   `web-complete`, deployable, or bug fixed status, read
   `shared/completion-evidence.md`.
10. For defects and regressions, read `shared/systematic-debugging.md`.
11. For delegated work, use `shared/multi-agent-orchestration.md`,
   `templates/orchestration/task_brief.md`, `agent_result_packet.yaml`,
   `merge_review.md`, and `.engineering-calc/work/progress.md`.

## Completion Gates

Do not invent engineering formulas, lookup rules, units, coefficients, branch
logic, or pass/fail criteria. Formula logic belongs only in reusable calculation
modules and the official `run_book(BookInput) -> BookResult` runner. UI, report
templates, frontend code, batch scripts, and CSV/XLSX input files consume
computed results; they do not calculate.

Production work requires calculation semantic closure through the complete
core/project package. Before claiming production correctness, ensure the project
contains and validates `calculation_intent_contract.md`,
`method_selection_matrix.csv`, `input_semantics_ledger.csv`,
`computation_graph_coverage.csv`, `runner_closure_map.csv`, and
`golden_case_registry.csv`.

Validate generated projects with:

```bash
python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete
```

If validation fails, label the result as `prototype`, `incomplete`, or
`not deployable`.

## Static Report Triage

If a project has calculation scripts or exported `reports/*.html` but lacks
`webapp/`, `apps/review/`, `src/pkg/report/`, `latex/templates/`,
`tests/smoke/`, `deploy/`, or `handoff/`, classify it as
`static_report_or_cli_only`. Treat exported HTML as comparison evidence, not the
deployable application runtime.

## Marimo Review Closure

For `web-complete`, create the Marimo review/admin closure instead of only a
static HTML report or UI mockup. Required artifacts and entrypoints include
`/admin/`, `/admin/review/`, `/admin/formulas/`, `/api/review/session`,
`/api/review/state/<session_id>`, `apps/review/calculation_review.py`,
`apps/review/admin_formula_review.py`, `src/pkg/review/bridge.py`,
`ADMIN_REVIEW_PASSWORD`, and `ADMIN_REVIEW_TOKEN`. If Marimo is unavailable, the
admin shell must show the install/config prompt while `/`, `/health`, and
`/api/calculate` stay usable.

## A4 HTML First

Default calculation-book output to print-ready A4 HTML: `@page size: A4`,
print-safe margins, formula traces, source result paths, warnings/errors,
sources, assumptions, traceability, and chart data tables when charts are
emitted. Use LaTeX/Overleaf/PDF only when explicitly requested or required by
the handoff.

## Detailed Reference

Full lifecycle details live in `reference.md` or, in Qoder Project overlays,
`.qoder/references/engineering-calc-system.md`. Complete executable guidance
lives in the core package under `skills/`, `parent/`, `shared/`, `templates/`,
`schemas/`, `scripts/validate_artifacts.py`, and `project_template/`.
