# Installation

## Build the plugin

```bash
cd opencodeplugin
npm install
npm run build
```

## Install project-local OpenCode assets

```bash
node dist/cli/index.js install --target .. --force
```

If the skill root cannot be inferred from schema version `2.4.1`, pass it explicitly:

```bash
node dist/cli/index.js install --target .. --skill-root ../engineering-calculation-system/core/engineering-calculation-system --force
```

Preview without writing:

```bash
node dist/cli/index.js install --target .. --dry-run
```

The installer writes OpenCode-native assets only: skills, agents,
commands, the local plugin shim, and a minimal `.opencode/package.json`
dependency when needed. It also writes
`.opencode/.engineering-calc-manifest.json` so updates can report which
managed templates changed.

The installer refuses targets inside the Codex plugin or the shared
skill pack. Install at a project root, not under
`plugins/engineering-calculation-system/` or
`engineering-calculation-system/core/`.

## Update managed assets

```bash
node dist/cli/index.js update --target ..
```

`update` refreshes the managed OpenCode templates and reports a diff
(`added`, `modified`, `removed`) compared to the previous manifest. It
does not modify the shared core skill pack or the Codex plugin.

## Remove managed assets

```bash
node dist/cli/index.js uninstall --target ..
```

`uninstall` removes managed OpenCode template files that carry the
`engineering-calc-opencode-managed` marker or are listed in the
manifest. Before removing, it copies those files into
`.opencode/.engineering-calc-backup/`.

If the installer added `@opencode-ai/plugin` to `.opencode/package.json`,
uninstall removes that dependency. If the dependency already existed, it
is left in place.

## Inspect installation

```bash
node dist/cli/index.js status --target ..
node dist/cli/index.js assets --target ..
node dist/cli/index.js doctor --target .. --verbose
```

## Register with opencode.json (optional)

If you prefer the project-level `opencode.json` registration path
instead of relying on the auto-loaded `.opencode/plugins/` shim, see
[distribution.md](./distribution.md).

## Versioning

The CLI `--version` and the install report both read the version from
`opencodeplugin/package.json`. Do not hardcode the version elsewhere.
