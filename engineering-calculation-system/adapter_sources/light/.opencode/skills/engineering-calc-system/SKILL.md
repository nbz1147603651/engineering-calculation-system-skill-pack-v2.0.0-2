---
name: engineering-calc-system
description: Full lifecycle engineering calculation system workflow. Use for engineering calculation reference discovery, formula/lookup/branch extraction, calculation logic blueprints, implementation handoff, auditable calculation-book software, reports, batch flows, verification, traceability, and deployable web calculators.
compatibility: opencode
metadata:
  package: engineering-calculation-system-skill-pack
  entrypoint: ../../../SKILL.md
version: 2.6.0
---

# Engineering Calculation System

This is an OpenCode wrapper for the root Engineering Calculation System skill pack.

## Load Order

1. Read `../../../SKILL.md`.
2. Read `../../../skills/00-engineering-calculation-router.skill.md`.
3. For non-trivial tasks, read `../../../shared/execution-discipline.md` and create route/gate/artifact/validation cards.
4. For multi-step planning, review feedback, or large release/platform work, read `../../../shared/planning-discipline.md`, `../../../shared/review-feedback-discipline.md`, or `../../../shared/version-control-discipline.md` as applicable.
5. Read only the parent and child skill files selected by the router.
6. For explicit multi-agent or parallel work, read `../../../shared/multi-agent-orchestration.md` and use task briefs, result packets, task reviews, review packages, and progress ledgers from `../../../templates/orchestration/`.
7. Before implementation or release work, read `../../../shared/lifecycle.md`.
8. Before completion, production, deployable, or `web-complete` claims, read `../../../shared/completion-evidence.md`.
9. For bug fixes or regressions, read `../../../shared/systematic-debugging.md`.
10. Use `../../../templates/`, `../../../shared/`, and `../../../schemas/` only when generating or validating artifacts.

If relative file loading is unavailable, load the generated `dist/singlefile/engineering-calculation-system.all-in-one.md` release artifact.

If the package shape lacks `skills/`, `shared/`, `templates/`, `schemas/`,
`scripts/validate_artifacts.py`, or `project_template/`, treat the install as a
lightweight entrypoint and use the full project/root package or single-file
fallback before claiming `web-complete`.

## Non-Negotiable Rules

- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Produce route card, gate card, artifact contract, and validation evidence before implementation action.
- Multi-step plans must name concrete files, interfaces, artifact outputs, validation commands, expected outputs, and stop conditions from `shared/planning-discipline.md`.
- Review feedback must be classified through source authority, unit semantics, formula boundary, and lifecycle gate impact from `shared/review-feedback-discipline.md`.
- Large release or platform packaging work must record workspace isolation, baseline validation, dirty state, sync targets, and finishing options from `shared/version-control-discipline.md`.
- Completion claims must map to `shared/completion-evidence.md`; static HTML, visible UI, old output, or agent assertion is not enough.
- Bug fixes must trace the lowest correct layer before patching UI/report symptoms.
- Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.
- Keep formulas out of UI, report templates, frontend JavaScript, review notebooks, batch scripts, and CSV/XLSX input files.
- Route official calculations through `run_book(BookInput) -> BookResult`.
- Declare delivery mode before implementation: `core-only`, `report-only`, `prototype-web`, or `web-complete`.
- Default to `web-complete`; its path is `08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14`.
- `web-complete` means dual closure: a readable A4/LaTeX calculation book with real input and non-empty `BookResult.checks`, plus a complete web system with API/UI, Marimo review/admin pages, import/export, batch, deployment artifacts, and smoke tests.
- Lightweight wrappers must use the complete core package, project template, and validator before making a production completion claim.
- For `web-complete`, include a Chinese/English interactive UI switch with `/api/i18n/<lang>`, `data-i18n`, persisted language preference, and selected-language report calls.
- For `web-complete`, include `/admin/`, `/admin/review/`, `/admin/formulas/`, `/api/review/session`, `/api/review/state/<session_id>`, `apps/review/calculation_review.py`, `apps/review/admin_formula_review.py`, `src/<pkg>/review/bridge.py`, `ADMIN_REVIEW_PASSWORD`, and `ADMIN_REVIEW_TOKEN`; if Marimo is missing, show the install/config prompt and keep the main calculator usable.
- For production UI, use `templates/implementation/ui_design_system.md`, `webapp/templates/partials/`, `webapp/static/css/tokens.css`, and `webapp/static/css/components.css`.
- For calculation-book export, use `templates/implementation/latex_report_spec.md` and `templates/implementation/html_report_spec.md`; choose LaTeX/PDF when `latexmk` or `pdflatex` is installed and require successful compilation to `main.pdf`, otherwise use A4 HTML with `@page size: A4`; expose `GET /api/report/decision`, `POST /api/report/final`, `GET /api/report/templates`, and `/api/report/latex`.
- Do not call CLI runners, static HTML, exported report HTML, notebooks, or UI mockups complete or deployable.
- Parallel workers must have disjoint `owned_paths`, return an agent result packet, and wait for supervisor merge review before their output is accepted.
- Long or compacted work resumes from `.engineering-calc/work/progress.md`, not memory alone.
- Do not delegate evidence gates, coding gates, source authority, ID allocation, handoff freeze, public runner contracts, or final acceptance.
- Run `python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete` before calling a generated project complete.

## Optional MCPs

Before enabling MCP servers, read `../../../adapters/mcp-recommendations.md`. Use MCPs as optional tools for search, docs lookup, public code search, diagnostics, and UI testing; never treat MCP output as authoritative engineering source material without citation and validation.
