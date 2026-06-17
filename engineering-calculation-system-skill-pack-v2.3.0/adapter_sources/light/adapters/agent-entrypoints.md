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

The supervisor must keep gate decisions, source authority, ID allocation,
handoff freeze, `run_book()` public contracts, and final acceptance serial.

If the target agent can only accept one instruction file, load:

```text
dist/singlefile/engineering-calculation-system.all-in-one.md
```

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

## Qoder

Preferred setup:

1. Apply `dist/qoder-addon/` on top of the core package.
2. Use `.qoder/skills/engineering-calc-system/SKILL.md` as the project skill.
3. Use `.qoder/agents/engineering-calc-system.md` when the environment supports custom agents.
4. Keep `.qoder/skills/engineering-calc-system/reference.md` and assets with the Qoder skill wrapper.

Behavior:

- Qoder should still route to the package router rather than reading every child file.
- Widget or custom UI features are optional. If unavailable, continue with text artifacts and validation scripts.
- Qoder custom agents should use the roles in `shared/multi-agent-orchestration.md`: supervisor, reference-acquirer, source-intake, logic-extractor, module-worker, interface-worker, and verification-worker.

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
For explicit multi-agent or parallel work, read shared/multi-agent-orchestration.md and use templates/orchestration/.
Split work only by disjoint owned paths. Workers return agent_result_packet.yaml fields, and the supervisor accepts output only after merge_review.md checks.
Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
Do not start production implementation unless handoff/implementation_handoff.yaml and handoff/coding_go_no_go.md allow it.
Keep formulas out of UI, report templates, frontend JavaScript, review notebooks, batch scripts, and CSV/XLSX input files.
Official calculations must flow through run_book(BookInput) -> BookResult.
Do not delegate evidence gates, coding gates, source authority, ID allocation, handoff freeze, public runner contract changes, production labels, or release acceptance.
```

## MCP Guidance

MCP servers are optional. Read `adapters/mcp-recommendations.md` before enabling MCPs.

Short version:

- Borrow the MCP capability pattern from curated agent stacks such as oh-my-openagent.
- Do not bundle a full MCP stack as mandatory package behavior.
- Enable only task-scoped MCPs for search/fetch, documentation lookup, public code search, LSP/diagnostics, authorized document extraction, or browser testing.
- Keep credentials and user data outside this package.
- Never use MCPs to bypass paywalls, login walls, license limits, or access controls.
