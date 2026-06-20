# MCP Presets

MCP support in this plugin is an optional OpenCode accelerator. It is
not part of the shared skill pack and does not change the source
authority rules, handoff workflow, validation scripts, or merge review
requirements.

MCP entries are emitted only by `opencode-json`; `install` does not
write MCP config automatically.

## Modes

```bash
engineering-calc-opencode opencode-json --mcp none
engineering-calc-opencode opencode-json --mcp catalog
engineering-calc-opencode opencode-json --profile implementation --mcp recommended
```

- `none` is the default. It emits plugin registration and permissions
  only.
- `catalog` emits every built-in MCP example with `enabled: false`.
- `recommended` emits only the MCPs recommended by the selected profile
  and sets them to `enabled: true`.

The legacy `--include-mcp` flag remains available and is equivalent to
`--mcp catalog`.

## Profiles

| Profile | Recommended MCP |
| --- | --- |
| `conservative` | none |
| `reference-acquisition` | none |
| `implementation` | `context7`, `gh_grep` |
| `verification` | `playwright` |
| `web-complete` | `context7`, `playwright` |
| `release` | none |

Use `engineering-calc-opencode profiles` or
`engineering-calc-opencode profiles --json` to inspect the current
profile catalog.

## Built-in MCP catalog

| MCP | Config | Default posture |
| --- | --- | --- |
| `context7` | remote `https://mcp.context7.com/mcp` | Docs lookup accelerator; not an engineering source authority. |
| `gh_grep` | remote `https://mcp.grep.app` | Public code-pattern search; do not copy unreviewed code. |
| `playwright` | local `["npx", "@playwright/mcp@latest"]` | Browser automation for verification profiles. |
| `sentry` | remote `https://mcp.sentry.dev/mcp` with `oauth: {}` | Catalog-only disabled example; never auto-enabled. |

## Non-goals

The catalog intentionally does not include filesystem, generic
"everything", GitHub, email, calendar, cloud-drive, or database MCPs.
Those tools either duplicate OpenCode-native capabilities or introduce
too much authority surface for a default engineering-calculation
adapter.

## Merge behavior

When `opencode-json --write` is used, existing user config wins. The CLI
adds missing plugin/MCP entries but does not overwrite an existing MCP
server's URL, auth, command, or `enabled` value.
