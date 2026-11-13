# Engineering Calculation System ZCode Plugin

NIMO Engineering / skill pack `0.0.1` is a local preview and has not been
formally released. Its product version was intentionally reset from historical
`2.6.0`. Existing `2.6.0` users must manually install the verified `0.0.1` preview
and matching host adapter; version comparison and automatic updates cannot
perform this migration. Preserve configuration, business data, and the `2.6.0`
rollback package. Host adapter package versions may be independent of the skill pack.

This plugin packages the Engineering Calculation System skill pack for ZCode.
The skill pack remains the core runtime; the plugin is the installation and
discovery boundary for ZCode's Codex-like plugin manager.

## Why Plugin, Not Only Skill

Use the raw skill directly only when ZCode is configured for legacy
`~/.zcode/skills/<skill-name>/` discovery. Use this plugin when ZCode can
install plugins from Settings -> Plugins or an imported marketplace source,
because the package includes:

- a ZCode plugin manifest
- a local marketplace descriptor for path-based import
- official-style `package.json` metadata for cache/package tooling
- a root `SKILL.md` entrypoint inside `skills/engineering-calculation-system/`
- parent-layer ZCode entrypoint skills for reference acquisition, logic
  architecture, and calculation-book delivery
- lifecycle-phase ZCode entrypoint skills for router, 01-14 child workflows,
  and 12a/12b/12c interface subflows
- shared contracts and quality gates
- artifact templates and schemas
- validation scripts
- a runnable project scaffold

The plugin currently exposes skills only. It intentionally does not declare
hooks, MCP servers, or apps until ZCode-native implementations exist.

ZCode's current plugin management is Beta. The package follows the documented
component layout: a plugin can bundle skills, commands, subagents, MCP servers,
hooks, and LSP integrations, while this plugin starts with the skill component
only.

## ZCode Adaptation

This folder is self-contained. All ZCode-specific changes live here:

```text
marketplace.json
.zcode-plugin/plugin.json
docs/ADAPTATION.md
overlays/
scripts/
skills/
```

The bundled skill entrypoint loads
`skills/engineering-calculation-system/shared/zcode-plugin-adapter.md` before
the router. That adapter maps the platform-neutral engineering workflow onto
ZCode workspace editing, file references, review panels, plugin discovery, and
long-task continuation boundaries.

`marketplace.json` is the local marketplace manifest ZCode can add from the
Discover tab. `.zcode-plugin/plugin.json` is the plugin manifest ZCode probes
after the plugin is selected from that marketplace. The manifest intentionally
declares `"skills": "skills"`, matching ZCode's native plugin component form
used by current official plugins.

ZCode only lists directories that contain `SKILL.md` as plugin skills. The
canonical package remains under `skills/engineering-calculation-system/`; the
additional top-level entries are thin ZCode launch points that route into the
canonical parent and child files. This mirrors the current official-plugin
pattern used by packages such as `superpowers`: keep the plugin manifest simple,
then expose task-sized skills as first-class `skills/<name>/SKILL.md`
directories.

## Install And Discovery Notes

ZCode currently requires the client-side marketplace flow after local staging:
open Settings -> Plugins -> Discover -> +, add this folder, click Get on the
plugin card, and keep it enabled.

If an older copy was already imported and Settings -> Skills does not show the
skill under Plugin skills, uninstall the old plugin entry from ZCode's
Installed tab, refresh the marketplace, then click Get again. ZCode may keep a
cached plugin copy by source/version, so reusing a stale cache can leave the old
`"skills": "./skills/"` manifest in effect even after the staged folder changes.

## Layout

```text
marketplace.json
package.json
.zcode-plugin/plugin.json
docs/ADAPTATION.md
overlays/engineering-calculation-system/shared/zcode-plugin-adapter.md
scripts/sync_from_core.py
scripts/validate_plugin.py
skills/engineering-calculation-system/SKILL.md
skills/engineering-calculation-reference-acquisition/SKILL.md
skills/engineering-calculation-logic-architecture/SKILL.md
skills/engineering-calculation-book-delivery/SKILL.md
skills/engineering-calculation-*/SKILL.md
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

The plugin doctor checks the manifest, ZCode adapter files, overlay
synchronization, bundled-source drift, and the bundled core skill package.

It also runs from a standalone delivered plugin folder. Version checks use the
bundled artifact contract and plugin metadata; a source checkout additionally
checks the canonical release config, installer integration, and source drift.

## Refresh From Core

When the source skill pack changes, refresh the bundled copy and reapply the
ZCode overlay:

```bash
python scripts/sync_from_core.py
```

This script reads from the repository source package by default and writes only
inside this plugin folder.
