# Engineering Calculation System Codex Plugin

This plugin packages the Engineering Calculation System skill pack for Codex.
The skill pack remains the core runtime; the plugin is the installation and
discovery boundary.

## Why Plugin, Not Only Skill

Use the raw skill directly when you only need local prompt/routing behavior.
Use this plugin when you want Codex to install and discover the whole system as
one component, because the package includes:

- a root `SKILL.md` entrypoint
- parent and child phase skills
- shared contracts and quality gates
- artifact templates and schemas
- validation scripts
- a runnable project scaffold

The plugin currently exposes skills only. It intentionally does not declare MCP
servers, hooks, or apps until those integrations exist.

## Codex Adaptation

This folder is self-contained. All Codex-specific changes live here:

```text
.codex-plugin/plugin.json
docs/ADAPTATION.md
overlays/
scripts/
skills/
```

The bundled skill entrypoint loads
`skills/engineering-calculation-system/shared/codex-plugin-adapter.md` before
the router. That adapter maps the platform-neutral engineering workflow onto
Codex workspace editing, CodeGraph discovery, web-based reference acquisition,
validation, and multi-agent boundaries.

## Layout

```text
.codex-plugin/plugin.json
docs/ADAPTATION.md
overlays/engineering-calculation-system/shared/codex-plugin-adapter.md
scripts/sync_from_core.py
scripts/validate_plugin.py
skills/engineering-calculation-system/SKILL.md
skills/engineering-calculation-system/parent/
skills/engineering-calculation-system/skills/
skills/engineering-calculation-system/shared/
skills/engineering-calculation-system/templates/
skills/engineering-calculation-system/scripts/
skills/engineering-calculation-system/project_template/
```

## Source

The bundled skill copy was initialized from:

```text
engineering-calculation-system/core/engineering-calculation-system/
```

## Validate

From this plugin folder:

```bash
python scripts/validate_plugin.py
```

The plugin doctor checks the manifest, required Codex adapter files, and the
bundled core skill package.

## Refresh From Core

When the source skill pack changes, refresh the bundled copy and reapply the
Codex overlay:

```bash
python scripts/sync_from_core.py
```

This script reads from the repository source package by default and writes only
inside this plugin folder.
