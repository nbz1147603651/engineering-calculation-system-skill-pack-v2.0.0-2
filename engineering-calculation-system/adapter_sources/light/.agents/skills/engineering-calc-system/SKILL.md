---
name: engineering-calc-system
description: Portable engineering calculation system skill wrapper for agents that support .agents/skills. Use for reference acquisition, engineering formula extraction, calculation logic blueprints, implementation handoff, auditable calculation software, reports, batch execution, verification, and deployment.
compatibility: generic-agent
metadata:
  package: engineering-calculation-system-skill-pack
  entrypoint: ../../../SKILL.md
version: 2.4.3
---

# Engineering Calculation System

This is a portable wrapper for agents that discover skills from `.agents/skills`.

## Start Here

Read the root package entrypoint:

```text
../../../SKILL.md
../../../skills/00-engineering-calculation-router.skill.md
```

Then read only the parent and child skill files selected by the router.

Before implementation or release work, also read:

```text
../../../shared/lifecycle.md
```

If the package shape does not include `skills/`, `shared/`, `templates/`,
`schemas/`, `scripts/validate_artifacts.py`, and `project_template/`, treat the
current install as a lightweight entrypoint and use the full project/root package
or single-file fallback before claiming `web-complete` delivery.

For explicit multi-agent or parallel work, also read:

```text
../../../shared/multi-agent-orchestration.md
../../../templates/orchestration/parallel_work_plan.yaml
../../../templates/orchestration/agent_result_packet.yaml
../../../templates/orchestration/merge_review.md
```

If the target agent cannot access multiple files reliably, use:

```text
the generated dist/singlefile/engineering-calculation-system.all-in-one.md release artifact
```

## Hard Rules

- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Do not skip evidence and handoff gates.
- Keep all official calculations in reusable calculation modules and `run_book(BookInput) -> BookResult`.
- Keep UI, reports, batch scripts, and review tools as thin consumers of trusted results.
- Declare delivery mode before implementation: `core-only`, `report-only`, `prototype-web`, or `web-complete`.
- Default to `web-complete`; its path is `08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14`.
- `web-complete` means dual closure: a readable A4/LaTeX calculation book with real input and non-empty `BookResult.checks`, plus a complete web system with API/UI, import/export, batch, deployment artifacts, and smoke tests.
- Lightweight wrappers must use the complete core package, project template, and validator before making a production completion claim.
- For `web-complete`, include a Chinese/English interactive UI switch with `/api/i18n/<lang>`, `data-i18n`, persisted language preference, and selected-language report calls.
- For production UI, use `templates/implementation/ui_design_system.md`, `webapp/templates/partials/`, `webapp/static/css/tokens.css`, and `webapp/static/css/components.css`.
- For calculation-book export, use `templates/implementation/latex_report_spec.md` and `templates/implementation/html_report_spec.md`; choose LaTeX/PDF when `latexmk` or `pdflatex` is installed and require successful compilation to `main.pdf`, otherwise use A4 HTML with `@page size: A4`; expose `GET /api/report/decision`, `POST /api/report/final`, `GET /api/report/templates`, and `/api/report/latex`.
- Do not call CLI runners, static HTML, exported report HTML, notebooks, or UI mockups complete or deployable.
- Split parallel work only by disjoint owned paths.
- Keep gate decisions, source authority, ID allocation, handoff freeze, public runner contracts, and final acceptance with the supervisor.
- Validate generated project artifacts with `scripts/validate_artifacts.py --profile core --delivery web-complete`.

## Tooling

MCP servers are optional. Read `../../../adapters/mcp-recommendations.md` before enabling them, and keep source authority, copyright, and access-control rules above tool convenience.
