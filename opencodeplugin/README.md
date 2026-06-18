# Engineering Calculation System OpenCode Plugin

Standalone OpenCode plugin for the Engineering Calculation System skill pack.

Current plugin version: `0.3.0`
Target skill pack schema: `2.4.0`

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
```

Managed files contain an `engineering-calc-opencode-managed` marker so `uninstall` can remove only this plugin's files.

## Common Commands

```bash
engineering-calc-opencode install --target <project> --skill-root <skill-root> --force
engineering-calc-opencode update --target <project>
engineering-calc-opencode doctor --target <project> --verbose
engineering-calc-opencode status --target <project>
engineering-calc-opencode schema --write
engineering-calc-opencode config-example --full
engineering-calc-opencode uninstall --target <project>
```

## OpenCode Tools

- `engineering_calc_route`
- `engineering_calc_orchestration`
- `engineering_calc_doctor`
- `engineering_calc_status`
- `engineering_calc_config_example`

The orchestration tool is read-only: it returns YAML or Markdown drafts for `parallel_work_plan`, `agent_result_packet`, and `merge_review`, but never writes files directly.

## Configuration

Project config lives at:

```text
.opencode/engineering-calc-system.jsonc
```

User config lives at:

```text
%APPDATA%/opencode/engineering-calc-system.jsonc
~/.config/opencode/engineering-calc-system.jsonc
```

See [configuration.md](docs/configuration.md).

## More

- [Installation](docs/installation.md)
- [Configuration](docs/configuration.md)
- [Doctor](docs/doctor.md)
- [Orchestration Guide](docs/orchestration-guide.md)
- [Optimization Assessment](docs/optimization-assessment.md)
