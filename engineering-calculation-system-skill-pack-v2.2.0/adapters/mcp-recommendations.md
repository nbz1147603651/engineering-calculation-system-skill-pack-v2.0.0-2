# Optional MCP Recommendations

Use this file when adapting the Engineering Calculation System skill pack to agents with MCP support, including Codex-like environments, Qoder, OpenCode, Trae, and generic MCP clients.

MCP servers are optional accelerators. The skill pack must remain useful without MCP. Do not make evidence gates, handoff gates, formula correctness, or validation depend on one vendor-specific MCP server.

## Recommendation

Borrow the MCP idea pattern from curated agent stacks such as oh-my-openagent, but do not vendor their full MCP set into this skill pack.

Use MCPs in three layers:

1. **Baseline native tools**: file read/write, shell, search, tests, and git from the host agent.
2. **Task-scoped MCPs**: enable only the MCPs needed for the current phase.
3. **Project-approved MCPs**: use secret-bearing or external-system MCPs only after the user confirms scope, credentials, and data boundary.

## Good MCP Fits

| MCP capability | Use in this skill pack | Phase | Notes |
| --- | --- | --- | --- |
| Web search / fetch | Find official standards pages, errata, public manuals, jurisdiction pages, and source metadata | 01-04, 06 | Search results are candidates, not authority. Log meaningful searches. |
| Browser automation | Verify frontend flows, report preview, charts, upload/download, and smoke behavior | 12b, 12c, 14 | Prefer local app testing and screenshots over blind DOM assumptions. |
| Documentation lookup | Check current library/framework APIs for Flask, FastAPI, Pydantic, Marimo, plotting, packaging, or deployment tooling | 08-14 | Use for software docs, not as engineering code authority. |
| Public code search | Compare implementation patterns, package layouts, or test structures | 08-14 | Never copy unvetted formulas or licensed code. |
| LSP / diagnostics | Navigate symbols, catch type or import errors, run code actions where safe | 08-14 | Useful for large generated projects. |
| PDF / document extraction | Extract tables, clause references, and page-level notes from user-provided or authorized files | 04-06 | Respect copyright and access rules. |
| GitHub / issue tools | Work on PRs, CI failures, release notes, or repository review | 13-14 | Enable only when the project is actually on GitHub. |

## Avoid by Default

Do not enable these as default bundled MCPs:

- database MCPs, unless a calculation project explicitly stores cases or audit records in a DB
- email, calendar, CRM, or cloud-drive MCPs, unless the task is explicitly about those systems
- broad browser/login automation for paywalled standards or restricted documents
- scraping MCPs that bypass robots, authentication, paywalls, license limits, or access controls
- finance, trading, or production infrastructure MCPs unrelated to engineering calculation delivery
- any MCP that requires API keys, tokens, private network access, or user data before the user approves it

## Phase Presets

Use these presets as mental models, not as mandatory configuration.

### Reference Acquisition

Enable:

- web search / web fetch
- browser, if pages require inspection
- PDF/document extraction for authorized local files

Keep disabled:

- code search unless looking for open-source implementation patterns after evidence is established
- GitHub unless the user points to a repository

### Logic Blueprint

Enable:

- PDF/document extraction
- spreadsheet/table tooling if source data is tabular
- web search/fetch for errata, official versions, and cross-checking public source metadata

Keep disabled:

- browser automation unless manual page inspection is needed

### Implementation

Enable:

- documentation lookup
- LSP/diagnostics
- public code search for patterns
- test runner integration through native shell tools

Keep disabled:

- web search for formulas unless resolving an explicitly logged source gap

### Interface and Release

Enable:

- browser automation for local UI smoke tests
- documentation lookup for deployment/runtime APIs
- GitHub/CI tools only for PR or workflow tasks

Keep disabled:

- secret-bearing deployment MCPs until the release target and credentials are approved

## Authority Rules

- Treat MCP outputs as leads, diagnostics, or convenience data.
- Record durable evidence in the package artifacts, not in transient MCP chat state.
- For engineering formulas, prefer source cards, clause identifiers, official publications, authorized user documents, and reproducible regression references.
- When MCP output conflicts with local evidence, log the conflict and resolve it through the source authority workflow.

## Minimal Config Examples

The following examples are intentionally conservative. Copy only the parts supported by the target agent.

### OpenCode-style sketch

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

### Generic stdio sketch

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

For search MCPs that require API keys, keep credentials outside the repository and use environment variables from the target agent's secure settings.
