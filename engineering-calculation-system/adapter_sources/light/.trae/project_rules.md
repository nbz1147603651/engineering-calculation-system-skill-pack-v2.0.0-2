# Engineering Calculation System Rules

Use these project rules when working on engineering calculation software in Trae or another rules-based AI IDE.

## Entrypoint

Use the Engineering Calculation System skill pack.

Start with:

```text
SKILL.md
skills/00-engineering-calculation-router.skill.md
```

Do not load every child skill at once. Load only the parent and child skills selected by the router.

For explicit multi-agent, delegated, or parallel work, also load:

```text
shared/multi-agent-orchestration.md
templates/orchestration/parallel_work_plan.yaml
templates/orchestration/agent_result_packet.yaml
templates/orchestration/merge_review.md
```

If Trae cannot read the package as multiple files, load:

```text
engineering-calculation-system.all-in-one.md
```

Before implementation or release work, also read:

```text
shared/lifecycle.md
shared/lifecycle.md
```

If the install lacks `skills/`, `shared/`, `templates/`, `schemas/`,
`scripts/validate_artifacts.py`, or `project_template/`, treat it as a
lightweight entrypoint and use the full project/root package or single-file
fallback before claiming `web-complete`.

## Lifecycle

Route work through:

```text
reference acquisition and persistence
-> reference analysis and Calculation Logic Blueprint
-> implementation, interfaces, verification, traceability, and release
-> default web-complete path: 08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14
```

## Required Gates

Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.

Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.

Do not put formulas in UI, report templates, frontend JavaScript, review notebooks, batch scripts, or CSV/XLSX input files.

Official calculations must flow through:

```text
run_book(BookInput) -> BookResult
```

Declare delivery mode before implementation: `core-only`, `report-only`,
`prototype-web`, or `web-complete`. Default to `web-complete` unless the user
explicitly requests a narrower prototype.

`web-complete` means dual closure: a readable A4/LaTeX calculation book with
real input and non-empty `BookResult.checks`, plus a complete web system with
API/UI, import/export, batch, deployment artifacts, and smoke tests. Lightweight
wrappers must use the complete core package, project template, and validator
before making a production completion claim.

Do not call CLI runners, static HTML, exported report HTML, notebooks, or UI
mockups complete or deployable.

For `web-complete`, include a Chinese/English interactive UI switch with
`/api/i18n/<lang>`, `data-i18n`, persisted language preference, and
selected-language report calls.

For production UI, use `templates/implementation/ui_design_system.md`,
`webapp/templates/partials/`, `webapp/static/css/tokens.css`, and
`webapp/static/css/components.css`.

For calculation-book export, use `templates/implementation/latex_report_spec.md`
and `templates/implementation/html_report_spec.md`; choose LaTeX/PDF when
`latexmk` or `pdflatex` is installed and require successful compilation to
`main.pdf`, otherwise use A4 HTML with `@page size: A4`; expose
`GET /api/report/decision`, `POST /api/report/final`, `GET /api/report/templates`,
and `/api/report/latex`.

## Parallel Work

Parallel work is optional and must use disjoint owned paths.

Do not delegate evidence gates, coding gates, source authority, ID allocation,
handoff freeze, `run_book()` contract changes, production labels, or release
acceptance. Workers return agent result packets; the supervisor accepts output
only after merge review.

## Search and Evidence

During reference discovery, use available internet search or browser tools for missing, insufficient, stale, or jurisdiction-specific references. Log meaningful searches in:

```text
references/acquisition/search_log.csv
```

Record accepted and rejected candidates before analysis proceeds.

## Optional MCPs

MCP servers are optional. Read:

```text
adapters/mcp-recommendations.md
```

Prefer search/fetch, documentation lookup, LSP/diagnostics, authorized PDF extraction, and browser testing. Do not enable secret-bearing or restricted-access MCPs unless the user confirms scope and credentials.

## Completion

Use templates from `templates/` for artifacts.

Run validation before considering the work complete:

```bash
python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete
```
