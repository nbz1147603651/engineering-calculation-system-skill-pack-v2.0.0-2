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
- Codex-specific adapter and quickstart guidance

The plugin currently exposes skills only. It intentionally does not declare MCP
servers, hooks, or apps until those integrations exist.

## Codex Adaptation

This folder is self-contained. All Codex-specific changes live here:

```text
.codex-plugin/plugin.json
docs/ADAPTATION.md
docs/CODEX_QUICKSTART.md
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
docs/CODEX_QUICKSTART.md
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

The plugin doctor checks the manifest, local marketplace discoverability,
required Codex adapter files, overlay synchronization, bundled-source drift,
the bundled core skill package, the bundled web-complete project template, and
the executable golden-case runner.

The same doctor can run from an installed Codex plugin cache. In that packaged
context it skips source-checkout-only marketplace and bundled-source drift
checks, but still validates the manifest, bundled skill, web-complete template,
and golden-case runner.

## Codex Quickstart

See `docs/CODEX_QUICKSTART.md` for Codex-first prompts, workspace rules, and
validation commands. The shortest smoke path is:

```bash
python scripts/validate_plugin.py
```

For the generated project template specifically:

```bash
cd skills/engineering-calculation-system/project_template/engineering_calc_project
python scripts/verify_golden_cases.py --project-root .
python -m pytest
```

## Refresh From Core

When the source skill pack changes, refresh the bundled copy and reapply the
Codex overlay:

```bash
python scripts/sync_from_core.py
```

This script reads from the repository source package by default and writes only
inside this plugin folder.
