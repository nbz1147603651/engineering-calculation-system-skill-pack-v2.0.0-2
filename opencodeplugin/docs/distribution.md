# Distribution and Registration

This plugin supports two registration paths for OpenCode. The installer
configures both transparently; this document explains how they work and
when to choose each.

## Path A — Local plugin (auto-loaded, default)

OpenCode auto-loads JavaScript / TypeScript files from
`.opencode/plugins/` (project) and `~/.config/opencode/plugins/`
(global). The installer writes a small shim:

```text
.opencode/plugins/engineering-calc-system.ts
```

The shim re-exports the built plugin entry:

```ts
// engineering-calc-opencode-managed
export { default } from "../../opencodeplugin/dist/index.js";
```

The installer also adds `@opencode-ai/plugin` to `.opencode/package.json`
only when that dependency is not already present, so OpenCode can resolve
the local TypeScript plugin. Plugin-specific config uses strict JSON;
OpenCode's own `opencode.json` / `opencode.jsonc` remains handled by
OpenCode.

Use this path when:
- The plugin is shipped as part of the skill-pack repository
  (this repo's default layout).
- You want zero configuration beyond running the installer.

## Path B — opencode.json registration (npm-style)

Add the plugin and recommended permissions to `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "engineering-calculation-system-opencode-plugin"
  ],
  "permission": {
    "edit": {
      "*": "ask",
      "plugins/engineering-calculation-system/*": "deny",
      "engineering-calculation-system/core/*": "deny"
    },
    "bash": "ask",
    "external_directory": "ask",
    "task": "ask",
    "skill": {
      "engineering-calc-system": "allow"
    }
  }
}
```

The CLI can print or merge the snippet for you:

```bash
# Print the snippet for the local-file path.
engineering-calc-opencode opencode-json --target /path/to/project

# Print the snippet for the npm package name.
engineering-calc-opencode opencode-json --target /path/to/project --mode npm

# Merge plugin registration and recommended permissions into opencode.json.
engineering-calc-opencode opencode-json --target /path/to/project --mode npm --write

# Include disabled optional MCP examples.
engineering-calc-opencode opencode-json --target /path/to/project --include-mcp

# Print profile recommendations.
engineering-calc-opencode profiles

# Emit profile-recommended MCPs as enabled entries.
engineering-calc-opencode opencode-json --target /path/to/project --profile implementation --mcp recommended
```

OpenCode installs npm plugins automatically at startup
(`bun install` against `~/.cache/opencode/node_modules/`). Use this path
when:
- The plugin is published to npm and consumed by many projects.
- You want a single source of truth in `opencode.json`.

## Optional MCP presets

MCP config is generated only when requested:

- `--mcp none` is the default and emits no MCP config.
- `--mcp catalog` emits the full catalog with every MCP set to
  `enabled: false`.
- `--mcp recommended` emits the selected profile's recommendations and
  sets them to `enabled: true`.
- `--include-mcp` is retained as a compatibility alias for
  `--mcp catalog`.

Built-in MCP entries are `context7`, `gh_grep`, `playwright`, and
`sentry`. `sentry` is OAuth-bearing and is never enabled by a profile;
it appears only as a disabled catalog example. Existing user MCP
settings in `opencode.json` are preserved when `--write` merges a
snippet.

See [mcp-presets.md](mcp-presets.md) for the profile mapping and risk
notes.

## Cross-platform safety

The installer refuses targets inside the Codex plugin
(`plugins/engineering-calculation-system/...`) or the shared skill pack
(`engineering-calculation-system/core/...`). Runtime gate blocking is
experimental and disabled by default; normal guardrails come from
OpenCode permissions, the core skill workflow, and doctor/status
diagnostics.

This separation lets OpenCode and Codex coexist in the same skill pack
without one adapter overwriting the other.

## Uninstall guarantees

`uninstall` is safe to re-run for managed OpenCode assets. It:
- removes managed template files listed in the install manifest,
- removes every file carrying the `engineering-calc-opencode-managed`
  marker,
- copies each removed file to `.opencode/.engineering-calc-backup/`
  before deletion (so a manual rollback is possible),
- removes `@opencode-ai/plugin` only when the installer added it,
- removes the `engineeringCalcOpenCodeManaged` key from
  `.opencode/package.json`,
- leaves any user-created file in `.opencode/` untouched.

If `uninstall` is interrupted, re-running it is idempotent: missing
files are skipped, the manifest is re-read, and the backup directory is
reused.
