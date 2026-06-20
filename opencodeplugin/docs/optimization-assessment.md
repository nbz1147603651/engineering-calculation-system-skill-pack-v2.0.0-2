# OpenCode-Specific Optimization Assessment

The current skill pack can be optimized for OpenCode. Its core workflow is already strong: it has a root `SKILL.md`, router, parent orchestrators, child skills, templates, schemas, validation scripts, v2.4.0 multi-agent orchestration contracts, and lightweight `.opencode/skills` adapter files. That is enough for file-based skill discovery.

The gap is that the current OpenCode support is an adapter overlay, not a dedicated OpenCode plugin. A professional OpenCode plugin should add these layers:

1. Native plugin entrypoint: `src/index.ts` with OpenCode hooks and custom tools.
2. Installable package shape: `package.json`, `tsconfig.json`, `dist/`, and npm/local plugin support.
3. Diagnostic tools: a doctor tool that checks the skill root and runs `validate_artifacts.py`.
4. Routing tools: a route tool that tells OpenCode which phase, gate, and skill files to load.
5. Orchestration tools: read-only draft generation for `parallel_work_plan`, `agent_result_packet`, and `merge_review`.
6. Project templates: `.opencode/skills`, `.opencode/commands`, and role-specific `.opencode/agents` generated with correct relative paths.
7. Conservative MCP posture: recommend task-scoped MCPs, but do not bundle broad or secret-bearing MCPs by default.
8. Compaction support: preserve evidence gates, source authority decisions, handoff status, validation state, changed artifacts, active plan IDs, worker task IDs, owned paths, result packet status, merge conflicts, and gate decisions across long OpenCode sessions.
9. **Advisory gate diagnostics**: expose handoff, owned path, registry, presentation-layer formula, and cross-platform boundary risks without making the plugin a second governance kernel.
10. **Managed template lifecycle**: track managed OpenCode assets so `update` can show a diff and `uninstall` can clean up plugin-owned templates.
11. **Cross-platform safety**: refuse installation targets inside the Codex plugin or the shared skill pack.
12. **OpenCode-native permissions**: generate `opencode.json` snippets that use OpenCode's own permission model for edit, bash, task, external directory, and skill access.

This `opencodeplugin` directory implements that bridge while keeping the existing core skill pack untouched and staying independent from `tools/build_release.py`. Version `0.5.0` adds profile-driven optional MCP output while preserving the boundary between core skill rules and OpenCode-native adaptation:

- **0.3.0** — productization layer: config loading, schema generation, doctor
  checks, CLI install/update/uninstall/status, managed asset markers, and a
  testable plugin factory.
- **0.4.0** — initial runtime enforcement and lifecycle hardening.
- **0.4.1** — OpenCode-native correction: strict JSON plugin config,
  advisory gate diagnostics by default, experimental runtime hook behind
  `gates.runtimeHook`, target-level cross-platform install guards,
  safer `.opencode/package.json` ownership, and richer `opencode-json`
  permission snippets.
- **0.5.0** — OpenCode-native profile presets and MCP catalog output:
  `opencode-json --profile ... --mcp ...`, `profiles` inspection, disabled
  catalog mode, profile-recommended MCP enablement, and merge behavior
  that preserves existing user MCP config.

## v2.4.0 orchestration posture

The plugin should treat multi-agent work as supervisor-owned coordination, not as unconstrained parallel editing. Plugin tools return draft text only; OpenCode agents write files through normal permissions after the user or supervisor accepts the draft.

The required v2.4.0 runtime files are:

```text
shared/multi-agent-orchestration.md
templates/orchestration/parallel_work_plan.yaml
templates/orchestration/agent_result_packet.yaml
templates/orchestration/merge_review.md
```

The doctor and smoke checks should fail when these files are missing, even if the older v2.3.0 skill paths are present.

## Why not only copy `.opencode/skills`

OpenCode skills are discovered from project or global skill folders and loaded on demand. That is useful, but it does not provide runtime diagnostics, environment injection, custom tools, or compaction behavior. The plugin layer adds those capabilities.

## Why not bundle a large MCP stack

Frameworks such as oh-my-openagent are useful references for plugin orchestration, agent presets, MCP presets, and repeatable installation. For this engineering calculation package, MCPs should stay optional because engineering source authority cannot depend on transient MCP output. Search, fetch, docs lookup, browser testing, PDF extraction, and diagnostics are accelerators, not authorities.

## Universal vs platform-personal scope

This `opencodeplugin/` is **platform-personal**: it adapts the
**universal** skill pack (the `engineering-calculation-system` core) to
OpenCode. The two are kept strictly separate:

- The **universal** layer is the skill pack under
  `engineering-calculation-system/core/engineering-calculation-system/`
  (router, parent orchestrators, child skills, shared contracts,
  schemas, validation scripts). It must remain platform-agnostic.
- The **platform-personal** layer is everything under
  `opencodeplugin/` plus the managed assets written into `.opencode/`.
  It encodes OpenCode-specific behavior: hooks, tool arg shapes, plugin
  shim, commands, agents, permission snippets, advisory diagnostics, and
  installer lifecycle.

A cross-platform safety invariant is enforced at install time: the
OpenCode installer refuses targets inside
`plugins/engineering-calculation-system/` (the Codex adapter) or
`engineering-calculation-system/core/` (the universal skill pack). This
keeps the Codex plugin and the shared skill pack untouched during normal
OpenCode plugin install, update, and uninstall workflows. Runtime
blocking remains an explicit experimental option, not the default
guardrail.
