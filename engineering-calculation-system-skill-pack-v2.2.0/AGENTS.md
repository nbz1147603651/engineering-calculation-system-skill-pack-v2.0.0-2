# Engineering Calculation System Agent Rules

Use these repository rules for OpenCode and other AGENTS.md-compatible coding agents.

## Entrypoint

This repository is an engineering calculation skill pack, not a normal application repository.

For engineering calculation work, start with:

```text
SKILL.md
skills/00-engineering-calculation-router.skill.md
```

Do not load every child skill at startup. Read the router first, then load only the parent and child skill files selected by the router.

## Required Behavior

- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.
- Keep formulas out of UI, report templates, frontend JavaScript, review notebooks, batch scripts, and CSV/XLSX input files.
- Route official calculations through `run_book(BookInput) -> BookResult`.
- Use templates from `templates/` and shared contracts from `shared/` when generating artifacts.
- Run `python scripts/validate_artifacts.py --package-root .` before calling the package complete.

## Platform Notes

- OpenCode should discover the wrapper skill at `.opencode/skills/engineering-calc-system/SKILL.md`.
- Cross-tool skill clients may use `.agents/skills/engineering-calc-system/SKILL.md`.
- Qoder-specific files live under `.qoder/`.
- Trae-compatible rules live under `.trae/`.
- Agent-specific loading notes live in `adapters/agent-entrypoints.md`.

## MCP Guidance

MCP servers are optional accelerators. Use `adapters/mcp-recommendations.md` before enabling MCPs.

Prefer a small, task-scoped MCP set:

- web search or fetch tools for reference discovery and source freshness
- documentation lookup for implementation libraries and frameworks
- public code search for implementation patterns, not engineering authority
- LSP or diagnostics tools for code navigation and verification
- browser automation only for UI smoke tests and frontend checks

Do not enable secret-bearing, database, browser, GitHub, or broad filesystem MCPs unless the task requires them and the user has approved the access boundary.
