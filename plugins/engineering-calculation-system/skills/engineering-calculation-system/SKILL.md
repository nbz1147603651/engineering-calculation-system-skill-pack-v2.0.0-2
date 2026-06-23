---
name: engineering-calculation-system
description: Build, verify, package, or deploy source-backed engineering calculation web apps and calculation books. Use when the user needs to assess or acquire engineering references, turn standards/manuals/PDFs/spreadsheets into a Calculation Logic Blueprint and implementation handoff, build decoupled reusable calculation modules and an official run_book() runner, build an auditable web calculation app with a reusable UI kit and HTML/LaTeX/Overleaf reports, verify formulas/reports/batch/traceability, or package a runnable local and Linux-cloud deployable online calculator — even when "calculation", "engineering", or "calculation book" is not named explicitly.
version: 2.4.3
---

# Engineering Calculation System

## Codex Plugin Adapter

When this package is loaded from the Codex plugin, read
`shared/codex-plugin-adapter.md` before the router. The adapter maps this
platform-neutral skill pack onto Codex tool use, workspace edits, validation,
multi-agent boundaries, and user-facing completion rules.

Full lifecycle for source-backed engineering calculation software. Start with
`skills/00-engineering-calculation-router.skill.md` for any non-trivial request — it classifies
the material state and task intent and routes to the right 01-14 path.

## Load order (progressive disclosure)

1. Read the router.
2. Read one parent orchestrator when a task spans a phase:
   `parent/engineering-calculation-reference-acquisition.skill.md` (skills 01-03),
   `parent/engineering-calculation-logic-architecture.skill.md` (skills 04-07), or
   `parent/engineering-calculation-book.skill.md` (skills 08-14).
3. Read only the child skills named by the router or parent.
4. For implementation/release/validation, read `shared/lifecycle.md` (the single source for the
   01-14 gates, delivery-mode bar, and quality checks).
5. For explicit multi-agent/parallel work, read `shared/multi-agent-orchestration.md`.
6. Load `templates/` and `shared/` contracts only when generating or validating artifacts.

Install the runtime skill from `dist/core/engineering-calculation-system/` for a built release; use
`dist/singlefile/engineering-calculation-system.all-in-one.md` when an environment cannot load
multiple files. Adapter overlays live in `dist/adapters-light/` or `dist/qoder-addon/`. MCPs are
accelerators, not required dependencies.

## Delivery mode

Before implementation starts, declare one mode: `core-only | report-only | prototype-web | web-complete`.
Default to `web-complete` for calculation systems, calculation-book software, web apps, online
calculators, reusable packages, batch workflows, or any request that does not explicitly ask for a
narrower prototype. In this skill, `web-complete` means dual closure: a readable, traceable
calculation book AND a complete web calculation system. For `web-complete` the default path is
`08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14`.
The default calculation-book output is print-ready A4 HTML; LaTeX/Overleaf/PDF are explicit
exports or client-specific additions, not the default replacement for the A4 HTML book.

If an existing project has calculation scripts and exported HTML reports but lacks the complete
project scaffold (`run_book`, `webapp/`, `apps/review/`, report renderers, import/export,
deployment files, and smoke tests), classify it as `report-only` or `static_report_or_cli_only`.
Do not polish the report and call it done; route remediation through the full web-complete path.

## Non-negotiable gates

The full gate vocabulary, the step/gate matrix, and the web-complete exit gate live in
`shared/lifecycle.md` (single source). The rules below are the highest-level restatement; do not
duplicate them elsewhere:

- Engineering formulas, lookups, branches, and load-combination logic live ONLY in reusable
  calculation modules and the official book runner.
- The one official calculation path is `run_book(book_input: BookInput) -> BookResult`
  (shorthand: `run_book(BookInput) -> BookResult`); every interface calls it, none reimplements it.
- Production work requires calculation semantic closure across calculation intent, method
  selection, input semantics, computation graph coverage, runner closure, and golden-case
  verification; UI/report completeness cannot compensate for an open calculation core.
- Do not invent formulas/coefficients/units/lookups/branches when the source basis is missing.
- Do not start production implementation unless `handoff/implementation_handoff.yaml` and
  `handoff/coding_go_no_go.md` allow it.
- Default stack is Python-first (Python 3.9+, `src/<pkg>/libraries/`, Flask/FastAPI thin routes,
  `webapp/` browser UI, Marimo review when Python-native module review is needed). Use another
  runtime only when the user explicitly requests it and the handoff defines an adapter plan.
- Do not call a delivery complete/production-ready/deployable/web-complete when it is only a CLI
  runner, static `.html`, exported report HTML, notebook demo, or UI mockup.
- For Qoder or other lightweight entrypoints, run an install-shape check first. If `skills/`,
  `shared/`, `templates/`, `schemas/`, `scripts/validate_artifacts.py`, or `project_template/`
  are absent, use the complete core or QODER Project package before attempting web-complete work.
- Use the shared UI design system (`templates/implementation/ui_design_system.md`,
  `webapp/templates/partials/`, `webapp/static/css/{tokens,components}.css`) for production UI.
- Prefer A4 HTML calculation books with `@page size: A4`, print-safe margins, browser preview,
  and chart data tables for printing when charts are emitted; add LaTeX/PDF only when requested
  or required.
- When formula rules must change after deployment, use a declaration-based formula registry, the
  password-gated Flask admin shell under `/admin/`, and token-protected Marimo apps under
  `/admin/review/` and `/admin/formulas/`; publish only after validation and smoke tests pass.

## Artifact validation

```bash
python3 scripts/validate_artifacts.py --package-root .                         # skill pack
python3 scripts/validate_artifacts.py --package-root . --profile core          # layered release
python3 scripts/validate_artifacts.py --package-root <skill-pack-root> --profile core \
  --project <project-root> --delivery web-complete                             # generated project
```

Treat validation failures as blocking unless the user explicitly asks for a draft or prototype. On
Windows use `python`/`py` if `python3` is unavailable; quote paths with spaces.

## Codex plugin adapter

Keep worker tasks bounded and sidecar-only in Codex-compatible environments; do not delegate lifecycle routing, evidence-gate decisions, source-authority ranking, ID-namespace control, handoff freeze, `run_book()` public-contract changes, or final acceptance.
