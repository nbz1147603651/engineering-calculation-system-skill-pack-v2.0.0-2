# Doctor

Run:

```bash
engineering-calc-opencode doctor --target <project> --verbose
```

Checks:

- `skill-root` — the resolved skill pack root exists.
- `schema-version` — matches the target schema declared by this plugin.
- `required-files` — the 12 required files of the skill pack are present.
- `orchestration-templates` — the v2.4.x orchestration files exist.
- `opencode-assets` — the project-level OpenCode assets are fully installed.
- `config` — the strict JSON plugin config loaded cleanly.
- `mcp-policy` — MCP presets are conservative.
- `optional-capabilities` — optional runtime capabilities (marimo, latex, docker).
- `python-validation` — `scripts/validate_artifacts.py` passes.
- `project-template-validation` — `validate_artifacts.py` passes against the
  bundled project template.

Output modes:

```bash
engineering-calc-opencode doctor --target <project>
engineering-calc-opencode doctor --target <project> --verbose
engineering-calc-opencode doctor --target <project> --json
engineering-calc-opencode doctor --target <project> --no-validation
```

Failed `skill-root`, `schema-version`, `required-files`, `orchestration-templates`,
`python-validation`, and `project-template-validation` checks are blockers for
production work. `opencode-assets` warns when assets are missing.
`optional-capabilities` and `mcp-policy` are advisory.
