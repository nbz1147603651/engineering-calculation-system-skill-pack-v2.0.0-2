# Engineering Calculation System Agent Rules

Use these repository rules for ZCode, OpenCode, and other AGENTS.md-compatible coding agents.

## Entrypoint

This repository is an engineering calculation skill pack, not a normal application repository.

For engineering calculation work, start with:

```text
SKILL.md
skills/00-engineering-calculation-router.skill.md
shared/execution-discipline.md
```

Do not load every child skill at startup. Read the router first, then load only the parent and child skill files selected by the router.

For multi-step planning, review feedback, or large release/platform work, also read the relevant behavior stabilizer:

```text
shared/planning-discipline.md
shared/review-feedback-discipline.md
shared/version-control-discipline.md
```

For completion, production, deployable, or `web-complete` claims, also read:

```text
shared/completion-evidence.md
```

For bug fixes or regressions, also read:

```text
shared/systematic-debugging.md
```

For explicit multi-agent, subagent, delegated, or parallel work, also read:

```text
shared/multi-agent-orchestration.md
templates/orchestration/parallel_work_plan.yaml
templates/orchestration/task_brief.md
templates/orchestration/agent_result_packet.yaml
templates/orchestration/task_review.md
templates/orchestration/merge_review.md
templates/orchestration/progress_ledger.md
```

For implementation or release work, read:

```text
shared/lifecycle.md
```

If the install lacks `skills/`, `shared/`, `templates/`, `schemas/`,
`scripts/validate_artifacts.py`, or `project_template/`, treat it as a
lightweight entrypoint and use the full project/root package or single-file
fallback before claiming `web-complete`.

## Required Behavior

- For every non-trivial task, produce the execution-discipline route card, gate card, artifact contract, and validation evidence frame before implementation action.
- Multi-step plans must pass `shared/planning-discipline.md`: goal, constraints, exact files, interfaces, artifact outputs, validation commands, expected outputs, and stop conditions must be concrete.
- Review feedback must pass `shared/review-feedback-discipline.md` before editing; source conflicts, unit semantics, formula boundary issues, and lifecycle gate impacts route upstream instead of becoming surface patches.
- Large release or cross-platform packaging work must use `shared/version-control-discipline.md` to record workspace isolation, baseline validation, dirty state, sync targets, and finishing options.
- Any completion-like claim must map to `shared/completion-evidence.md`; static HTML, visible UI, old command output, or agent assertion is not enough.
- Bug fixes must trace the lowest correct layer using `shared/systematic-debugging.md` before editing UI/report symptoms.
- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.
- Keep formulas out of UI, report templates, frontend JavaScript, review notebooks, batch scripts, and CSV/XLSX input files.
- Route official calculations through `run_book(BookInput) -> BookResult`.
- Declare delivery mode before implementation: `core-only`, `report-only`, `prototype-web`, or `web-complete`.
- Default to `web-complete`; its path is `08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14`.
- `web-complete` means dual closure: a readable print-ready A4 HTML calculation book with non-empty `BookResult.checks`, metadata-driven charts when the current book exposes useful chartable values, and a complete web system with API/UI, Marimo review/admin pages, import/export, batch, deployment, and smoke tests.
- Lightweight entrypoints must use the complete core package, project template, and validator before making a production completion claim.
- For `web-complete`, include a Chinese/English interactive UI switch with `/api/i18n/<lang>`, `data-i18n`, persisted language preference, and selected-language report calls.
- For `web-complete`, include the password-gated `/admin/` review shell, proxied Marimo pages at `/admin/review/` and `/admin/formulas/`, `/api/review/session`, `/api/review/state/<session_id>`, `apps/review/calculation_review.py`, `apps/review/admin_formula_review.py`, `src/<pkg>/review/bridge.py`, and `ADMIN_REVIEW_PASSWORD` / `ADMIN_REVIEW_TOKEN` setup. If Marimo is not installed, the admin shell must show the install/config prompt and the calculator must still run.
- For production UI, use `templates/implementation/ui_design_system.md`, `webapp/templates/partials/`, `webapp/static/css/tokens.css`, and `webapp/static/css/components.css`.
- For calculation-book export, use `templates/implementation/html_report_spec.md` as the default final calculation book and `templates/implementation/latex_report_spec.md` for explicit LaTeX/Overleaf/PDF exports; default to A4 HTML with `@page size: A4`, print-safe CSS, source result paths, formula traces, and chart data tables when charts are emitted; expose `GET /api/report/decision`, `POST /api/report/final`, `GET /api/report/templates`, and send `latex_template_id` to `/api/report/latex` with default fallback.
- Do not call CLI runners, static HTML, exported report HTML, notebooks, or UI mockups complete or deployable.
- Use templates from `templates/` and shared contracts from `shared/` when generating artifacts.
- Before parallel implementation, declare disjoint `owned_paths` for each worker and do not overwrite another worker's output.
- Workers must return an agent result packet; a supervisor must run merge review before accepting worker output.
- Long or compacted work resumes from `.engineering-calc/work/progress.md`, not from memory alone.
- Do not delegate evidence gates, coding gates, source authority decisions, ID allocation, handoff freeze, `run_book()` contract changes, or final acceptance.
- Run `python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete` before calling a generated project complete.

## Platform Notes

- OpenCode should discover the wrapper skill at `.opencode/skills/engineering-calc-system/SKILL.md`.
- ZCode should install the core skill folder at `~/.zcode/skills/engineering-calculation-system/` and invoke it with `$engineering-calculation-system`.
- ZCode project-specific guardrails belong in the workspace `AGENTS.md`; keep the root `SKILL.md` as the skill entrypoint.
- MiniMaxCode, ZCode, OpenCode, Trae, and generic AGENTS-style installs all use the same behavior-engineering contracts: `shared/execution-discipline.md`, `shared/planning-discipline.md`, `shared/review-feedback-discipline.md`, `shared/version-control-discipline.md`, `shared/completion-evidence.md`, and `shared/systematic-debugging.md`.
- Cross-tool skill clients may use `.agents/skills/engineering-calc-system/SKILL.md`.
- MiniMax Code can use the `MiniMaxCode` release zip or the standard root `SKILL.md` package.
- Qoder-specific files come from the separate `dist/qoder-addon/` overlay.
- Trae-compatible rules live under `.trae/`.
- Agent-specific loading notes live in `adapters/agent-entrypoints.md`.

## MCP Guidance

MCP servers are optional accelerators. Use `adapters/mcp-recommendations.md` before enabling MCPs.

Prefer a small, task-scoped MCP set:

- web search or fetch tools for reference discovery and source freshness
- documentation lookup for implementation libraries and frameworks
- public code search for implementation patterns, not engineering authority
- LSP or diagnostics tools for code navigation and verification
- browser automation only for UI smoke tests and frontend checks

Do not enable secret-bearing, database, browser, GitHub, or broad filesystem MCPs unless the task requires them and the user has approved the access boundary.
