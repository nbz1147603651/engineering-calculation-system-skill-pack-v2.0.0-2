# Engineering Calculation System OpenCode Plugin

Standalone OpenCode plugin for the Engineering Calculation System skill pack.

Current plugin version: `0.5.0`
Target skill pack schema: `2.6.0`

This package is the OpenCode-specific adapter layer. The shared skill
pack under `engineering-calculation-system/core/` remains the workflow
source of truth; the Codex plugin under `plugins/engineering-calculation-system/`
remains a separate platform wrapper.

## Quick Install

```bash
cd opencodeplugin
npm install
npm run build
node dist/cli/index.js install --target .. --force
node dist/cli/index.js doctor --target ..
```

The installer writes managed project-local assets under:

```text
.opencode/AGENTS.md
.opencode/plugins/engineering-calc-system.ts
.opencode/skills/engineering-calc-system/SKILL.md
.opencode/commands/engineering-calc-*.md
.opencode/agents/engineering-calc-*.md
.opencode/package.json
.opencode/.engineering-calc-manifest.json
```

Managed files contain an `engineering-calc-opencode-managed` marker so `uninstall` can remove only this plugin's files.

## Common Commands

```bash
engineering-calc-opencode install --target <project> --skill-root <skill-root> --force
engineering-calc-opencode update --target <project>
engineering-calc-opencode doctor --target <project> --verbose
engineering-calc-opencode status --target <project>
engineering-calc-opencode assets --target <project>
engineering-calc-opencode schema --write
engineering-calc-opencode config-example --full
engineering-calc-opencode profiles
engineering-calc-opencode opencode-json --target <project> --write
engineering-calc-opencode opencode-json --profile implementation --mcp recommended
engineering-calc-opencode uninstall --target <project>
```

## OpenCode Tools

- `engineering_calc_route` — phase-aware routing prompt and load order.
- `engineering_calc_orchestration` — read-only draft of `parallel_work_plan`,
  `agent_result_packet`, or `merge_review`.
- `engineering_calc_doctor` — runs the doctor checks (including
  `validate_artifacts.py`).
- `engineering_calc_status` — reports skill root, config, assets, and
  advisory gate diagnostic state.
- `engineering_calc_config_example` — returns a minimal or full JSON
  config example.
- `engineering_calc_gate_status` — reports current advisory diagnostics,
  handoff freeze, and active plan.

The orchestration tool is read-only: it returns YAML or Markdown drafts
for `parallel_work_plan`, `agent_result_packet`, and `merge_review`,
but never writes files directly.

## OpenCode-Native Guardrails

The plugin does not replace the core skill pack's engineering workflow
rules with a second governance engine. It uses OpenCode-native surfaces:

- `.opencode/skills/` for skill discovery.
- `.opencode/agents/` for supervisor and worker roles.
- `.opencode/commands/` for repeatable workflows.
- `opencode.json` permission recommendations for edit, bash, task,
  external directory, and skill access.
- doctor/status/route tools for diagnostics and load guidance.

The deterministic gate checks remain available as advisory diagnostics.
The `tool.execute.before` runtime hook is experimental and disabled by
default; enable it only with `gates.runtimeHook: true`.

MCP presets are optional OpenCode accelerators exposed through
`opencode-json`; they are not installed automatically and do not replace
source authority, handoff, validation, or merge review.

See [gates.md](docs/gates.md) for configuration,
[distribution.md](docs/distribution.md) for the `opencode.json`
registration path, and [mcp-presets.md](docs/mcp-presets.md) for MCP
profiles.

## Configuration

Project config lives at:

```text
.opencode/engineering-calc-system.json
```

User config lives at:

```text
%APPDATA%/opencode/engineering-calc-system.json
~/.config/opencode/engineering-calc-system.json
```

See [configuration.md](docs/configuration.md).

## Runtime Dependencies

Plugin-specific config uses strict JSON. OpenCode's own `opencode.json`
or `opencode.jsonc` remains handled by OpenCode itself. Local plugin
shims keep the minimal `.opencode/package.json` dependency needed for
OpenCode TypeScript plugin loading.

## More

- [Installation](docs/installation.md)
- [Configuration](docs/configuration.md)
- [Distribution](docs/distribution.md)
- [MCP Presets](docs/mcp-presets.md)
- [Doctor](docs/doctor.md)
- [Gates](docs/gates.md)
- [Orchestration Guide](docs/orchestration-guide.md)
- [Optimization Assessment](docs/optimization-assessment.md)
