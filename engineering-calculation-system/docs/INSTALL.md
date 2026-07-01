# Installation

Build releases from the source checkout:

```bash
python tools/build_release.py
```

With no arguments, the build creates every release profile plus ten publish-ready platform zips under `dist/release/`.

## Version Management

The release version is managed from one source:

```text
tools/release_config.json
```

For a new release, update all derived version fields with:

```bash
python tools/sync_versions.py --version <version> --created-at <YYYY-MM-DD>
python ../plugins/engineering-calculation-system/scripts/sync_from_core.py
```

Do not hand-edit individual schema, skill frontmatter, adapter manifest, or OpenCode metadata versions; the sync command updates those from the release config.

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
  Optional Qoder/Qoder CN overlay. Apply only when the target agent needs Qoder-specific files.

dist/singlefile/engineering-calculation-system.all-in-one.md
  Generated fallback for agents that cannot load multiple files.

dist/source-dev/
  Development/reference source bundle, not the default install target.

dist/ui-client/
  One-click deployment console as a Windows single-file exe (PyInstaller --onefile).
  Produced by `python tools/build_release.py --profile ui-client`. See docs/INSTALLER_GUI.md.

dist/release/
  CODEX, MiniMaxCode, ZCode, QODER Skill, QODER project, QoderCN user/project, TRAE, OpenCode, and AGENTS Generic release zips, checksums, and RELEASE_INDEX.md.
```

The `ui-client` profile builds a self-contained `engineering-calc-system-installer-v<version>.exe`
(~28 MB) that detects installed agents and deploys the skill pack to each in one
click. It is included in the default `build_release.py` run; pass `--no-ui-client`
to skip the PyInstaller step during fast iteration. The exe needs a system Python
3.9+ on PATH (to run build_release.py) and the skill-pack repo path. It honors
`ECS_REPO_ROOT`, searches parent folders near the exe, then uses any saved repo
path; if none is valid, it starts without a popup and creates a local `workspace/`
placeholder until the user chooses the repo with the **Repo...** button. See
`docs/INSTALLER_GUI.md` for full details.

publish files:

```text
dist/release/engineering-calculation-system-CODEX-v2.6.0.zip
dist/release/engineering-calculation-system-MiniMaxCode-v2.6.0.zip
dist/release/engineering-calculation-system-ZCode-v2.6.0.zip
dist/release/engineering-calculation-system-QODER-v2.6.0.zip
dist/release/engineering-calculation-system-QODER-Project-v2.6.0.zip
dist/release/engineering-calculation-system-QoderCN-v2.6.0.zip
dist/release/engineering-calculation-system-QoderCN-Project-v2.6.0.zip
dist/release/engineering-calculation-system-TRAE-v2.6.0.zip
dist/release/engineering-calculation-system-OpenCode-v2.6.0.zip
dist/release/engineering-calculation-system-AGENTS-Generic-v2.6.0.zip
```

Each zip contains one install folder plus `INSTALL.md`, except MiniMaxCode which is packaged as a MiniMax skills repository root:

```text
CODEX zip:         copy engineering-calculation-system/ to the Codex skills directory
MiniMaxCode zip:   local install by copying skills/engineering-calculation-system/ to %USERPROFILE%/.mavis/skills/engineering-calculation-system/; Github import remains supported
ZCode zip:         copy engineering-calculation-system/ to ~/.zcode/skills/engineering-calculation-system/, refresh Settings -> Skills, then invoke with $engineering-calculation-system
QODER zip:         upload the zip directly in QODER Skills / Install Skill; this is a lightweight skill/resource entrypoint
QODER Project zip: copy copy-to-project-root/ contents to the QODER project root; this is the recommended Qoder Smart Agent setup
QoderCN zip:       copy copy-to-user-home/ contents to ~/.lingma/ for Qoder CN IDE user-level Skills and Agents
QoderCN Project zip: copy copy-to-project-root/ contents to the Qoder CN project root; it installs a .lingma/ project overlay
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

ZCode local verification:

```powershell
Test-Path "$env:USERPROFILE\.zcode\skills\engineering-calculation-system\SKILL.md"
```

After copying the folder, refresh ZCode Settings -> Skills and keep the skill
enabled. ZCode project-specific guardrails belong in the workspace `AGENTS.md`;
the reusable engineering-calculation workflow remains in the skill folder.

For QODER web-complete generation, prefer the QODER Project zip. The direct
QODER zip keeps `SKILL.md` at the archive root for QODER skill-import
compatibility, but it does not contain the core templates, schemas, validator,
or project scaffold by itself.

For Qoder CN IDE, use the QoderCN user zip for user-level reusable Skills and
Agents under `~/.lingma/`, or the QoderCN Project zip for project-level
`.lingma/agents` and `.lingma/skills`. Official Qoder CN documentation also
mentions `.qodercn` for the IDE process/cache and `QoderCN.exe`; this package
uses `.lingma` for custom Skill/Agent resources because that is the documented
resource location for Qoder CN IDE custom agents and skills.

Qoder import mode check:

```text
Shown under Qoder Smart Agents / agents: .qoder/agents/engineering-calc-system.md, agent import
Uploaded through QODER Skills / Install Skill: root SKILL.md, skill import
Copied from QODER Project zip: hybrid project; agent is supervisor, skill is resource layer
```

Recommended Qoder architecture is agent-first and skill-backed. Keep only real
agent files under `.qoder/agents/`. Long references belong in
`.qoder/references/` or `.qoder/skills/engineering-calc-system/reference.md` so
Qoder does not list them as disabled custom agents.

One-click build behavior:

```text
python tools/build_release.py
```

This command builds every platform package (and the UI deployment exe). Pass
`--no-ui-client` to skip the PyInstaller exe build when iterating quickly. For
Qoder, it creates:

```text
engineering-calculation-system-QODER-v2.6.0.zip
  Direct Skill import package with root SKILL.md, reference.md, and assets/.

engineering-calculation-system-QODER-Project-v2.6.0.zip
  Project-root package with the supervisor agent, delegated worker agents,
  skill/resource layer, references, core templates, schemas, validator, and
  project scaffold.
```

Use QODER Project when you want multiple Qoder custom agents installed together.
Use the direct QODER Skill zip only when the target flow is Qoder Skill import.

For a local user-level Qoder install from this source checkout:

```bash
python tools/install_qoder_user.py --build
```

This builds `dist/qoder-addon/`, copies `.qoder/agents`, `.qoder/skills`, and
`.qoder/references` into `QODER_HOME` or `~/.qoder`, removes the deprecated
`.qoder/agents/reference.md` file if present, and verifies that all packaged
Qoder worker agents are installed.

For a local user-level Qoder CN install from this source checkout:

```bash
python tools/install_qoder_user.py --product qodercn --build
```

This builds the same `dist/qoder-addon/` overlay and copies its `agents`,
`skills`, and `references` into `QODER_CN_HOME`, `QODERCN_HOME`, `LINGMA_HOME`,
or `~/.lingma` by default.

Useful local Qoder maintenance commands:

```bash
python tools/install_qoder_user.py --audit
python tools/install_qoder_user.py --uninstall
python tools/install_qoder_user.py --uninstall --dry-run
python tools/install_qoder_user.py --product qodercn --audit
python tools/install_qoder_user.py --product qodercn --uninstall
```

`--audit` checks for missing managed files and redundant legacy files such as
`.qoder/agents/reference.md` or an old `.qoder/skills/engineering-calculation-system/`
directory. `--uninstall` removes only this package's managed Qoder agents,
skill directory, reference file, and deprecated reference-agent file; it does
not remove unrelated Qoder cache, extensions, project history, or other custom
content. Use `--dry-run` to preview filesystem changes without writing.

To build only one layer during development:

```bash
python tools/build_release.py --profile core
python tools/build_release.py --profile adapters-light
python tools/build_release.py --profile qoder-addon
python tools/build_release.py --profile singlefile
python tools/build_release.py --profile ui-client
```

## Maintenance

Release metadata and classified install targets are configured in:

```text
tools/release_config.json
```

Update that file first when changing the package version, release date, publish targets, single-file inclusion rules, source-dev contents, or adding another agent environment. The build script validates this configuration before creating release zips.

## Overlay Usage

The platform release zips are the recommended install path. Use the MiniMaxCode zip for MiniMax Code standard skill import or discovery. Use the ZCode zip for ZCode user-skill installation or Skills UI import. Use the QODER zip for direct QODER Skill upload; use the QODER Project, QoderCN Project, TRAE, and OpenCode packages when copying an overlay into a project root. Use the QoderCN zip for Qoder CN user-level `~/.lingma` install. Use raw overlays only when developing or debugging a release profile:

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

The Qoder/Qoder CN addon provides:

```text
.qoder/
```

Inside `.qoder/`, the Smart Agent entrypoint is
`.qoder/agents/engineering-calc-system.md`; the skill/resource layer is
`.qoder/skills/engineering-calc-system/`; long non-agent reference material is
stored under `.qoder/references/`.

For Qoder CN release packages, the same internal overlay is remapped to
`agents/`, `skills/`, and `references/` for user-level `~/.lingma` install, or
to project-root `.lingma/` for project-level install.

The QODER Project package also includes delegated worker agents:

```text
.qoder/agents/engineering-calc-reference-acquirer.md
.qoder/agents/engineering-calc-source-intake.md
.qoder/agents/engineering-calc-logic-extractor.md
.qoder/agents/engineering-calc-module-worker.md
.qoder/agents/engineering-calc-interface-worker.md
.qoder/agents/engineering-calc-verification-worker.md
.qoder/agents/engineering-calc-release-worker.md
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

All platform packages share `shared/lifecycle.md` as the single source of truth.
The legacy shared contract files are short compatibility redirects. Generated
projects that are intended to be complete web systems must validate with:

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
python -B -m pytest -q -p no:cacheprovider
```
