# Installation

Build the plugin first:

```bash
cd opencodeplugin
npm install
npm run build
```

Install project-local OpenCode assets:

```bash
node dist/cli/index.js install --target .. --force
```

If the skill root cannot be inferred from schema version `2.4.1`, pass it explicitly:

```bash
node dist/cli/index.js install --target .. --skill-root ../engineering-calculation-system/core/engineering-calculation-system --force
```

Update managed assets:

```bash
node dist/cli/index.js update --target ..
```

Remove managed assets only:

```bash
node dist/cli/index.js uninstall --target ..
```

Uninstall skips files without the `engineering-calc-opencode-managed` marker.
