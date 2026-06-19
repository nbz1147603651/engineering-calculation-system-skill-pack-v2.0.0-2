# Codex Plugin Adaptation

This plugin keeps the Engineering Calculation System as a skill-first package
and adds a Codex-specific distribution boundary around it.

## Adaptation Decision

The core package is still a skill pack because the primary value is procedural
expertise: routing, source gates, handoffs, templates, validation, and project
scaffolding. A Codex plugin is the better installation shape because the pack is
multi-file, versioned, and likely to grow optional tools over time.

The chosen architecture is:

```text
plugin wrapper
  manifest and Codex UI metadata
  maintenance scripts
  Codex adapter overlay
  bundled skill pack
```

## What Is Codex-Specific

- `.codex-plugin/plugin.json` exposes the package to Codex as one plugin.
- `shared/codex-plugin-adapter.md` maps the skill pack to Codex workspace,
  web/search, CodeGraph, edit, validation, and multi-agent conventions.
- `scripts/validate_plugin.py` validates both the plugin wrapper and bundled
  core skill package.
- `scripts/sync_from_core.py` refreshes the bundled skill from the source core
  package and reapplies the Codex overlay.
- `overlays/` stores plugin-only additions so future syncs do not lose them.

## What Is Not Codex-Specific

The lifecycle router, parent skills, child skills, shared engineering
contracts, artifact templates, project scaffold, and validation logic remain
the same core package material. This avoids maintaining a divergent Codex fork
of the engineering workflow.

## No Synthetic Integrations

The plugin currently declares skills only. It does not declare hooks, MCP
servers, or apps because there are no Codex-native implementations for those
integration points yet. They can be added later without changing the bundled
skill root.

