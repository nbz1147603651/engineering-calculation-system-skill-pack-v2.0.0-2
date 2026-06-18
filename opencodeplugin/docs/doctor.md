# Doctor

Run:

```bash
engineering-calc-opencode doctor --target <project> --verbose
```

Checks:

- `skill-root`
- `schema-version`
- `required-files`
- `orchestration-templates`
- `opencode-assets`
- `config`
- `mcp-policy`
- `python-validation`
- `project-template-validation`

Output modes:

```bash
engineering-calc-opencode doctor --target <project>
engineering-calc-opencode doctor --target <project> --verbose
engineering-calc-opencode doctor --target <project> --json
engineering-calc-opencode doctor --target <project> --no-validation
```

Failed root, schema, required-file, orchestration, Python validation, and project-template checks are blockers for production work.

