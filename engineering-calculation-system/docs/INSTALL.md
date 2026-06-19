# Installation

Build releases from the source checkout:

```bash
python tools/build_release.py
```

With no arguments, the build creates every release profile plus seven publish-ready platform zips under `dist/release/`.

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
  CODEX, MiniMaxCode, QODER Skill, QODER project, TRAE, OpenCode, and AGENTS Generic release zips, checksums, and RELEASE_INDEX.md.
```

Publish files:

```text
dist/release/engineering-calculation-system-CODEX-v2.4.0.zip
dist/release/engineering-calculation-system-MiniMaxCode-v2.4.0.zip
dist/release/engineering-calculation-system-QODER-v2.4.0.zip
dist/release/engineering-calculation-system-QODER-Project-v2.4.0.zip
dist/release/engineering-calculation-system-TRAE-v2.4.0.zip
dist/release/engineering-calculation-system-OpenCode-v2.4.0.zip
dist/release/engineering-calculation-system-AGENTS-Generic-v2.4.0.zip
```

Each zip contains one install folder plus `INSTALL.md`, except MiniMaxCode which is packaged as a MiniMax skills repository root:

```text
CODEX zip:         copy engineering-calculation-system/ to the Codex skills directory
MiniMaxCode zip:   local install by copying skills/engineering-calculation-system/ to %USERPROFILE%/.mavis/skills/engineering-calculation-system/; Github import remains supported
QODER zip:         upload the zip directly in QODER Skills / Install Skill; this is a lightweight entrypoint
QODER Project zip: copy copy-to-project-root/ contents to the QODER project root
TRAE zip:          copy copy-to-project-root/ contents to the TRAE project root
OpenCode zip:      copy copy-to-project-root/ contents to the OpenCode project root
AGENTS Generic zip: copy copy-to-project-root/ contents to an AGENTS.md-compatible project root
```

MiniMax Code local verification on Windows:

```powershell
& "$env:USERPROFILE\.mavis\bin\mavis.cmd" skill list
& "$env:USERPROFILE\.mavis\bin\mavis.cmd" skill show engineering-calculation-system
```

If a future MiniMax Code / Mavis build reports a different user skill root, copy
the skill folder to the reported root. The repository-style layout
`skills/engineering-calculation-system/SKILL.md` is still used when importing
from Github.

For QODER web-complete generation, prefer the QODER Project zip. The direct
QODER zip keeps `SKILL.md` at the archive root for QODER skill-import
compatibility, but it does not contain the core templates, schemas, validator,
or project scaffold by itself.

To build only one layer during development:

```bash
python tools/build_release.py --profile core
python tools/build_release.py --profile adapters-light
python tools/build_release.py --profile qoder-addon
python tools/build_release.py --profile singlefile
```

## Maintenance

Release metadata and classified install targets are configured in:

```text
tools/release_config.json
```

Update that file first when changing the package version, release date, publish targets, single-file inclusion rules, source-dev contents, or adding another agent environment. The build script validates this configuration before creating release zips.

## Overlay Usage

The platform release zips are the recommended install path. Use the MiniMaxCode zip for MiniMax Code standard skill import or discovery. Use the QODER zip for direct QODER Skill upload; use the QODER Project, TRAE, and OpenCode packages when copying an overlay into a project root. Use raw overlays only when developing or debugging a release profile:

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

## Optional Multi-Agent Orchestration

v2.4 includes optional orchestration guidance for explicit multi-agent,
delegated, or parallel work:

```text
shared/multi-agent-orchestration.md
templates/orchestration/
```

Use these files only when a platform supports worker agents or the user asks to
split work. Workers must have disjoint owned paths and return result packets;
the supervisor performs merge review and keeps all gate decisions serial.

## Web-Complete Delivery Contract

All platform packages share `shared/delivery-contract.md`. Generated projects
that are intended to be complete web systems must validate with:

```bash
python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete
```

Do not mark CLI runners, static HTML, exported report HTML, notebooks, or UI
mockups as deployable web systems.

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
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core --project dist/core/engineering-calculation-system/project_template/engineering_calc_project --delivery web-complete
cd dist/core/engineering-calculation-system/project_template/engineering_calc_project
python -m pytest -q
```
