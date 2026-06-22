# Agent Entrypoints

Use this file after installing `dist/core/engineering-calculation-system/` and, when needed, applying the `dist/adapters-light/` overlay to the same folder.

## Universal Loading Rule

The root package entrypoint is:

```text
SKILL.md
```

The first task-specific file is always:

```text
skills/00-engineering-calculation-router.skill.md
```

Do not load all child skills at once. Let the router select one parent orchestrator and only the child skills needed for the task.

For explicit multi-agent, subagent, delegated, or parallel work, also load:

```text
shared/multi-agent-orchestration.md
templates/orchestration/parallel_work_plan.yaml
templates/orchestration/agent_result_packet.yaml
templates/orchestration/merge_review.md
```

For implementation or release work, also load:

```text
shared/lifecycle.md
```

Before implementing, declare `core-only`, `report-only`, `prototype-web`, or
`web-complete`. Default to `web-complete` unless the user explicitly requests a
reduced scope. The default `web-complete` path is:

```text
08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14
```

`web-complete` means dual closure: a readable A4/LaTeX calculation book with
real input and non-empty `BookResult.checks`, plus a complete web system with
API/UI, import/export, batch, deployment artifacts, and smoke tests. Lightweight
entrypoints must call into the complete core package, project template, and
validator before making a production completion claim.

For `web-complete`, the interactive UI must include Chinese/English switching:
`/api/i18n/<lang>`, `data-i18n` bindings, persisted language preference, and
selected-language report preview/download calls.

For production UI, use `templates/implementation/ui_design_system.md`,
`webapp/templates/partials/`, `webapp/static/css/tokens.css`, and
`webapp/static/css/components.css` before adding book-specific fields or result
cards.

For calculation-book export, use `templates/implementation/latex_report_spec.md`
and `templates/implementation/html_report_spec.md`. Choose LaTeX/PDF when
`latexmk` or `pdflatex` is installed and require successful compilation to
`main.pdf`; otherwise use A4 HTML with `@page size: A4`. Ask whether the user
has a preferred LaTeX/Overleaf template before project initialization or first
export; if none is supplied, use `latex/templates/default_engineering_calcbook/`.
Generated web apps must expose `GET /api/report/decision`,
`POST /api/report/final`, `GET /api/report/templates`, and send
`latex_template_id` to `/api/report/latex` with default fallback unless the user
explicitly chooses another report workflow.

The supervisor must keep gate decisions, source authority, ID allocation,
handoff freeze, `run_book()` public contracts, and final acceptance serial.

If the target agent can only accept one instruction file, load:

```text
dist/singlefile/engineering-calculation-system.all-in-one.md
```

If an install lacks `skills/`, `shared/`, `templates/`, `schemas/`,
`scripts/validate_artifacts.py`, or `project_template/`, treat it as a
lightweight entrypoint and use the full project/root package or single-file
fallback before claiming `web-complete`.

## Codex

Preferred setup:

1. Install or expose `dist/core/engineering-calculation-system/` as a Codex skill folder.
2. Use root `SKILL.md` as the primary trigger and entrypoint.
3. Keep `agents/openai.yaml` with the package so Codex-compatible skill UIs can show metadata.

Fallback:

- Paste or attach `dist/singlefile/engineering-calculation-system.all-in-one.md` when file-by-file progressive disclosure is unavailable.
- If only repository rules are available, use `AGENTS.md` plus the root `SKILL.md`.

Multi-agent note:

- Use Codex subagents only for bounded sidecar tasks with disjoint write paths.
- Do not delegate lifecycle routing, gate decisions, ID control, handoff freeze, runner contract changes, or final acceptance.
- Have each worker return an agent result packet and merge through supervisor review.

## MiniMaxCode

Preferred setup:

1. Use `dist/release/engineering-calculation-system-MiniMaxCode-v2.4.2.zip`, or expose `dist/core/engineering-calculation-system/` as a standard `SKILL.md` skill folder.
2. Let MiniMax Code import or auto-discover the root `SKILL.md`.
3. Start with `SKILL.md` and `skills/00-engineering-calculation-router.skill.md`.

Behavior:

- Use the same lifecycle routing, evidence gates, handoff gates, and validation rules as the Codex/core package.
- Do not require a MiniMaxCode-specific hidden project folder unless the target installation explicitly provides one.
- For explicit multi-agent work, use `shared/multi-agent-orchestration.md` and keep supervisor-owned gate decisions serial.

Fallback:

- Use `dist/singlefile/engineering-calculation-system.all-in-one.md` when the environment cannot traverse the multi-file skill package.

## ZCode

Preferred setup:

1. Use `dist/release/engineering-calculation-system-ZCode-v2.4.2.zip`, or copy `dist/core/engineering-calculation-system/` to `~/.zcode/skills/engineering-calculation-system/`.
2. In ZCode, open Settings -> Skills, refresh the skill list, and keep `engineering-calculation-system` enabled.
3. Invoke the skill in chat with `$engineering-calculation-system`; use `@` file references and `/goal` for long tasks when useful.
4. Put project-specific operating rules in the workspace `AGENTS.md`. If you need a starter file, copy `dist/adapters-light/AGENTS.md` into the workspace root.

Behavior:

- ZCode skills are standard directories with a `SKILL.md` entrypoint, so the core package is the authoritative skill payload.
- ZCode Agent should still start from `SKILL.md` and `skills/00-engineering-calculation-router.skill.md`, then load only the selected parent and child files.
- Use ZCode's workspace context, file references, review panel, and model/execution controls as platform conveniences; do not bypass evidence gates, coding gates, handoff freeze, or `run_book(BookInput) -> BookResult`.
- ZCode reads user and workspace `AGENTS.md` instructions separately from skills. Keep persistent project guardrails in `AGENTS.md`, and keep reusable engineering-calculation workflow rules in the skill.

Fallback:

- If ZCode cannot traverse the multi-file skill directory, use `dist/singlefile/engineering-calculation-system.all-in-one.md` as the attached/pasted fallback.
- If only project instructions are available, use `AGENTS.md` plus the routing prompt below.

## Qoder

Preferred setup:

1. For project-root installation, use `dist/release/engineering-calculation-system-QODER-Project-v2.4.2.zip`.
2. Apply `dist/qoder-addon/` on top of the core package when composing manually.
3. Use `.qoder/agents/engineering-calc-system.md` as the Smart Agent supervisor when the environment supports custom agents.
4. Use `.qoder/skills/engineering-calc-system/SKILL.md` as the project skill and direct-skill fallback.
5. Keep `.qoder/skills/engineering-calc-system/reference.md`, `.qoder/references/engineering-calc-system.md`, and assets with the Qoder wrapper.

Recommended Qoder architecture:

- Use agent-first routing. The Qoder Smart Agent owns model/tool selection, expert-team orchestration, lifecycle routing, gate decisions, and final acceptance.
- Use the skill wrapper as the reusable knowledge/resource layer, not as the only production template.
- Keep `.qoder/agents/` clean: only real agent Markdown files belong there. Store long references under `.qoder/references/` or `.qoder/skills/engineering-calc-system/reference.md` so Qoder does not list them as disabled custom agents.
- If both agent and skill are present, the agent is the supervisor and the skill is the resource layer. If only the direct QODER Skill zip is installed, treat it as a lightweight entrypoint.
- A single `python tools/build_release.py` run packages all Qoder custom agents into the QODER Project zip. The direct QODER Skill zip remains root-`SKILL.md` only for Skill import compatibility.
- From a source checkout, `python tools/install_qoder_user.py --build` installs the Qoder overlay into `QODER_HOME` or `~/.qoder` and verifies the supervisor plus worker agents. Use `python tools/install_qoder_user.py --audit` to check for redundant legacy files, and `python tools/install_qoder_user.py --uninstall` to remove only this package's managed Qoder files.

Packaged Qoder custom agents:

```text
.qoder/agents/engineering-calc-system.md
.qoder/agents/engineering-calc-reference-acquirer.md
.qoder/agents/engineering-calc-source-intake.md
.qoder/agents/engineering-calc-logic-extractor.md
.qoder/agents/engineering-calc-module-worker.md
.qoder/agents/engineering-calc-interface-worker.md
.qoder/agents/engineering-calc-verification-worker.md
.qoder/agents/engineering-calc-release-worker.md
```

Behavior:

- Qoder should still route to the package router rather than reading every child file.
- Widget or custom UI features are optional. If unavailable, continue with text artifacts and validation scripts.
- The direct QODER Skill zip is a lightweight entrypoint. For web-complete generation, prefer QODER Project because it includes the core skill, templates, schemas, validator, project scaffold, and `.qoder/` overlay.
- Qoder custom agents should map expert-team roles to the roles in `shared/multi-agent-orchestration.md`: supervisor, reference-acquirer, source-intake, logic-extractor, module-worker, interface-worker, and verification-worker.

Fallback:

- Use root `SKILL.md` and `skills/00-engineering-calculation-router.skill.md`.
- Use `dist/singlefile/engineering-calculation-system.all-in-one.md` for single-file import.

## OpenCode

Preferred setup:

1. Apply `dist/adapters-light/` on top of the core package.
2. Keep root `AGENTS.md` in the installed package.
3. Use `.opencode/skills/engineering-calc-system/SKILL.md` as the project skill wrapper.

Behavior:

- `AGENTS.md` gives repository-level guardrails.
- The OpenCode skill wrapper gives a discoverable tool-style skill.
- Optional MCPs should be configured outside the skill pack or copied from examples after review.
- Parallel workers must declare `owned_paths`, return result packets, and wait for supervisor merge review.

Fallback:

- Use `.agents/skills/engineering-calc-system/SKILL.md` for agents that share the `.agents/skills` convention.
- Use `dist/singlefile/engineering-calculation-system.all-in-one.md` when OpenCode cannot traverse the package files.

## Trae

Preferred setup:

1. Apply `dist/adapters-light/` on top of the core package.
2. Use `.trae/project_rules.md` as project rules when Trae supports project-level rule files.
3. Use `.trae/rules/engineering-calc-system.md` when the environment supports rule folders.

Fallback:

- Paste the routing prompt below into Trae manual instructions.
- Use `dist/singlefile/engineering-calculation-system.all-in-one.md` when only one file can be loaded.
- Keep Trae rules concise: use the shared orchestration file for detailed parallel ownership, packet, and merge requirements.

## Generic Rules Agents

If the platform accepts repository rules, expose:

```text
AGENTS.md
SKILL.md
adapters/
parent/
skills/
shared/
templates/
schemas/
scripts/
project_template/
```

If the platform accepts a skill folder, use one of:

```text
.agents/skills/engineering-calc-system/SKILL.md
.opencode/skills/engineering-calc-system/SKILL.md
SKILL.md
```

If the platform only accepts one instruction file, load:

```text
dist/singlefile/engineering-calculation-system.all-in-one.md
```

## Routing Prompt

Use this prompt for agents that cannot discover adapter files:

```text
Use the Engineering Calculation System skill pack.
Start with SKILL.md and skills/00-engineering-calculation-router.skill.md.
Do not load all child skills at once. Load only the parent and child skills selected by the router.
During 02-reference-discovery-and-acquisition, use available internet search/browser tools actively for missing, insufficient, stale, or jurisdiction-specific references, and log meaningful searches in references/acquisition/search_log.csv.
Use templates/ for output artifacts and scripts/validate_artifacts.py before considering the work complete.
For implementation or release work, read shared/lifecycle.md.
Declare delivery mode before implementation: core-only, report-only, prototype-web, or web-complete. Default to web-complete.
For web-complete, follow 08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14.
For web-complete, deliver both a readable calculation book with non-empty BookResult.checks and a complete web system with API/UI, import/export, batch, deployment, and smoke tests.
For web-complete, include a Chinese/English interactive UI switch with /api/i18n/<lang>, data-i18n, persisted language preference, and selected-language report calls.
For production UI, use templates/implementation/ui_design_system.md plus webapp/templates/partials/, tokens.css, and components.css.
For calculation-book export, use templates/implementation/latex_report_spec.md and templates/implementation/html_report_spec.md; choose LaTeX/PDF when latexmk or pdflatex is installed and require successful compilation to main.pdf, otherwise use A4 HTML with @page size: A4; expose GET /api/report/decision, POST /api/report/final, GET /api/report/templates, and send latex_template_id to /api/report/latex with default fallback.
Do not call CLI runners, static HTML, exported report HTML, notebooks, or UI mockups complete or deployable.
For explicit multi-agent or parallel work, read shared/multi-agent-orchestration.md and use templates/orchestration/.
Split work only by disjoint owned paths. Workers return agent_result_packet.yaml fields, and the supervisor accepts output only after merge_review.md checks.
Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
Do not start production implementation unless handoff/implementation_handoff.yaml and handoff/coding_go_no_go.md allow it.
Keep formulas out of UI, report templates, frontend JavaScript, review notebooks, batch scripts, and CSV/XLSX input files.
Official calculations must flow through run_book(BookInput) -> BookResult.
Do not delegate evidence gates, coding gates, source authority, ID allocation, handoff freeze, public runner contract changes, production labels, or release acceptance.
Before claiming web-complete, run scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete.
```

## MCP Guidance

MCP servers are optional. Read `adapters/mcp-recommendations.md` before enabling MCPs.

Short version:

- Borrow the MCP capability pattern from curated agent stacks such as oh-my-openagent.
- Do not bundle a full MCP stack as mandatory package behavior.
- Enable only task-scoped MCPs for search/fetch, documentation lookup, public code search, LSP/diagnostics, authorized document extraction, or browser testing.
- Keep credentials and user data outside this package.
- Never use MCPs to bypass paywalls, login walls, license limits, or access controls.
