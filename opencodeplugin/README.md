# Engineering Calculation System OpenCode Plugin

This folder turns the Engineering Calculation System skill pack into a dedicated OpenCode plugin project.

Current plugin version: `0.2.0`
Target skill pack schema: `2.4.0`

It complements the existing lightweight adapter at `adapter_sources/light/.opencode/skills/engineering-calc-system/SKILL.md` with:

- a native OpenCode plugin entrypoint in `src/index.ts`
- custom tools: `engineering_calc_route`, `engineering_calc_orchestration`, and `engineering_calc_doctor`
- OpenCode command templates under `.opencode/commands`
- OpenCode role-specific agent templates under `.opencode/agents`
- an OpenCode skill wrapper generated with correct relative paths
- a project installer script
- a short optimization assessment in `docs/optimization-assessment.md`

The orchestration tool is read-only: it returns YAML or Markdown drafts for `parallel_work_plan`, `agent_result_packet`, and `merge_review`, but it never writes files directly.

## Local Development

```bash
cd opencodeplugin
npm install
npm run typecheck
npm run build
npm run smoke
```

## Install Into The Current Project

From this folder:

```bash
npm run install-project -- --target .. --force
```

The installer infers a v2.4.0 skill root by reading `schemas/artifact_contracts.json`. If inference fails, pass `--skill-root` explicitly.

The installer writes:

```text
.opencode/plugins/engineering-calc-system.ts
.opencode/skills/engineering-calc-system/SKILL.md
.opencode/commands/engineering-calc-*.md
.opencode/agents/engineering-calc-*.md
.opencode/package.json
```

OpenCode loads local plugins from `.opencode/plugins/` automatically.

## Publish Path

After the package name and license are finalized, build with:

```bash
npm run build
npm pack
```

Then an OpenCode config can use the npm package:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["engineering-calculation-system-opencode-plugin"]
}
```

For engineering work, keep the skill pack itself available on disk and set `ENGINEERING_CALC_SKILL_ROOT` when OpenCode cannot infer it automatically.

## Orchestration Workflow

Use orchestration only when the user explicitly asks for multiple agents, subagents, delegation, or parallel work.

Recommended flow:

```text
/engineering-calc-orchestrate
@engineering-calc-supervisor
@engineering-calc-module-worker
/engineering-calc-worker-packet
/engineering-calc-merge-review
```

The supervisor owns routing, gates, source authority, ID allocation, handoff freeze, public runner contract changes, production/release labels, validation, and final acceptance. Workers only edit declared `owned_paths` and return result packets.
