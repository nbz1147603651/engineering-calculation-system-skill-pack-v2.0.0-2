# Configuration

The plugin reads JSONC config from user and project scopes.

User config:

```text
%APPDATA%/opencode/engineering-calc-system.jsonc
~/.config/opencode/engineering-calc-system.jsonc
```

Project config:

```text
.opencode/engineering-calc-system.jsonc
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

```jsonc
{
  "$schema": "./engineering-calc-system.schema.json",
  "strictGateMode": true,
  "defaultPhase": "router"
}
```

