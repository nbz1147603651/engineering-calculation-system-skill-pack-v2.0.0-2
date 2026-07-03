# ZCode Plugin Adaptation

This plugin keeps the Engineering Calculation System as a skill-first package
and adds a ZCode-specific distribution boundary around it.

## Adaptation Decision

The core package is still a skill pack because the primary value is procedural
expertise: routing, source gates, handoffs, templates, validation, and project
scaffolding. A ZCode plugin is the better installation shape because the pack is
multi-file, versioned, and easier to manage from a plugin registry or import UI
than from a bare user skill directory.

The chosen architecture is:

```text
plugin wrapper
  manifest and ZCode UI metadata
  maintenance scripts
  ZCode adapter overlay
  bundled skill pack
```

## What Is ZCode-Specific

- `.zcode-plugin/plugin.json` exposes the package to ZCode as one plugin.
- The plugin manifest declares the skill component as `"skills": "skills"`,
  the directory-name form used by current ZCode plugin discovery.
- Root `marketplace.json` lets a local path or Git source enumerate the
  plugin when ZCode is using marketplace-style import.
- `shared/zcode-plugin-adapter.md` maps the skill pack to ZCode workspace,
  file-reference, review-panel, continuation, and plugin-discovery conventions.
- `scripts/validate_plugin.py` validates the plugin wrapper, overlay
  synchronization, bundled-source drift, and bundled core skill package.
- `scripts/sync_from_core.py` refreshes the bundled skill from the source core
  package and reapplies the ZCode overlay.
- `overlays/` stores plugin-only additions so future syncs do not lose them.

## What Is Not ZCode-Specific

The lifecycle router, parent skills, child skills, shared engineering
contracts, artifact templates, project scaffold, and validation logic remain
the same core package material. This avoids maintaining a divergent ZCode fork
of the engineering workflow.

## No Synthetic Integrations

ZCode plugins can bundle skills, commands, subagents, MCP servers, hooks, and
LSP integrations. This plugin currently declares skills only because there are
no ZCode-native command, subagent, MCP, hook, or LSP implementations for this
package yet. They can be added later without changing the bundled skill root.
