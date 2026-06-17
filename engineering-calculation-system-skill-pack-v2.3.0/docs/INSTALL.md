# Installation

Build releases from the source checkout:

```bash
python tools/build_release.py
```

With no arguments, the build creates every release profile and publish-ready zip archives under `dist/release/`.

The default runtime package is:

```text
dist/core/engineering-calculation-system/
```

Install that folder as the skill root in Codex-compatible or generic multi-file skill environments. It contains only the runtime skill entrypoint, routing skills, shared contracts, templates, schema, validation script, and project scaffold.

## Release Profiles

```text
dist/core/engineering-calculation-system/
  Default Codex/core runtime skill.

dist/adapters-light/
  Optional overlay for AGENTS.md, .agents, .opencode, .trae, and adapter guidance.

dist/qoder-addon/
  Optional Qoder overlay. Apply only when the target agent needs Qoder-specific files.

dist/singlefile/engineering-calculation-system.all-in-one.md
  Generated fallback for agents that cannot load multiple files.

dist/source-dev/
  Development/reference source bundle, not the default install target.

dist/release/
  Publish-ready zip archives, checksums, and RELEASE_INDEX.md.
```

To build only one layer during development:

```bash
python tools/build_release.py --profile core
python tools/build_release.py --profile adapters-light
python tools/build_release.py --profile qoder-addon
python tools/build_release.py --profile singlefile
```

## Overlay Usage

Install core first. If the target agent needs adapter entrypoints, copy the chosen overlay on top of the installed core folder:

```text
core install root: dist/core/engineering-calculation-system/
overlay source:    dist/adapters-light/ or dist/qoder-addon/
```

The light adapter overlay provides:

```text
AGENTS.md
adapters/
.agents/
.opencode/
.trae/
```

The Qoder addon provides:

```text
.qoder/
```

Do not merge Qoder files into the default core package unless the target environment specifically needs them.

## Validate

Validate the core source or installed core release:

```bash
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root core/engineering-calculation-system --profile core
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core
```

Validate optional release profiles:

```bash
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/adapters-light --profile adapters-light
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/qoder-addon --profile qoder-addon
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/singlefile --profile singlefile
```

Validate the included project scaffold:

```bash
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core --project dist/core/engineering-calculation-system/project_template/engineering_calc_project
cd dist/core/engineering-calculation-system/project_template/engineering_calc_project
python -m pytest -q
```
