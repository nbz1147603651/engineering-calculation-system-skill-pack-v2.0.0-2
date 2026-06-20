# Configuration

The plugin reads strict JSON config from user and project scopes.

User config:

```text
%APPDATA%/opencode/engineering-calc-system.json
~/.config/opencode/engineering-calc-system.json
```

Project config:

```text
.opencode/engineering-calc-system.json
```

Precedence:

```text
defaults < user config < ancestor project configs < current project config < CLI flags
```

Sensitive fields such as `mcpPresets` are user-only. If they appear in project config, they are ignored with a warning.

Generate schema:

```bash
npm run build:schema
```

Minimal config:

```json
{
  "$schema": "./engineering-calc-system.schema.json",
  "defaultPhase": "router"
}
```

Gate diagnostics are advisory by default:

```json
{
  "gates": {
    "enabled": true,
    "enforcement": "warn",
    "runtimeHook": false,
    "disable": []
  }
}
```

OpenCode's own `opencode.json` or `opencode.jsonc` is still parsed by
OpenCode. This file is only for plugin-specific settings.

Optional MCP presets are generated through `opencode-json --mcp ...`,
not through this plugin config file. See [mcp-presets.md](mcp-presets.md).
