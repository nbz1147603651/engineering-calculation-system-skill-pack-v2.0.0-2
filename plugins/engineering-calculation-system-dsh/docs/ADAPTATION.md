# DeepSeek Harness Adaptation

This plugin keeps the Engineering Calculation System as a skill-first package and
adds a DeepSeek Harness distribution boundary around it.

## Adaptation Decision

The core package is still a skill pack because the primary value is procedural
expertise: routing, source gates, handoffs, templates, validation, and project
scaffolding. A DeepSeek Harness bundle is the better installation shape because
the pack is multi-file, versioned, and easier to manage from a profile's bundle
list than from a bare user skill directory.

The chosen architecture is:

```text
bundle manifest (dsh.bundle.patch)
  cordis composition layer
  Cordis plugin registering a ctx.skills provider
  DSH adapter overlay
  bundled skill pack
```

## What Is DeepSeek Harness-Specific

- `package.json` declares `dsh.bundle.patch`, which is what `dsh plugin add`
  reads to activate a layer instead of installing a plain dependency.
- `cordis.patch.yml` inserts one host row; the row is addressable by id, so a
  profile can override or disable this pack from a later patch layer.
- `lib/index.js` is a Cordis plugin: it registers a skill provider at the
  bundled rank, publishes the pack as source `bundled`, and exposes the bundle
  directory as the skill's resource base.
- `overlays/.../shared/dsh-plugin-adapter.md` maps the pack onto DeepSeek
  Harness skill loading, model-visible tools, sandbox and approval behavior,
  session evidence, delegation boundaries, and user-facing output.
- The sync step drops the core package's Codex-only adapter section and rewrites
  the core package's source-install paragraph, because a DeepSeek Harness bundle
  must not instruct the model to read an overlay or a `dist/` distribution tree
  it does not carry.
- `scripts/validate_plugin.py` validates the wrapper, the bundled frontmatter,
  every path the bundled `SKILL.md` references, references to trees the bundle
  does not carry, and stray build residue.

## What Is Not DeepSeek Harness-Specific

The lifecycle router, parent skills, child skills, shared engineering
contracts, artifact templates, project scaffold, `run_book(BookInput) ->
BookResult` contract, and validation scripts remain the same core package
material. This avoids maintaining a divergent DeepSeek Harness fork of the
engineering workflow.

## No Synthetic Integrations

A DeepSeek Harness bundle can also contribute commands, subagents, MCP servers,
or hooks. This package declares skills only, because there is no DeepSeek
Harness-native command, subagent, MCP server, or hook implementation for this
pack yet. The bundles that do add such rows are the ones that ship the
corresponding implementation; declaring a row without one would put a
non-functional entry into every session of the profile.

## Relationship to the Other Host Plugins

`plugins/engineering-calculation-system` (Codex), the ZCode plugin, and the
light adapters under `adapter_sources/` each package the same core material for
their own host. They share the sync-and-overlay pattern: copy core, apply host
overlays, keep host-specific instructions out of the shared core.
