# Installation

Build releases from the source checkout:

```bash
python tools/build_release.py
```

With no arguments, the build creates every release profile plus sixteen publish-ready platform zips under `dist/release/`.

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

dist/qoder-plugin/
  Qoder CLI plugin package source with .qoder-plugin/plugin.json, agents/, skills/, references/, and adapters/.

dist/zcode-plugin/
  ZCode plugin package source. The published ZCode zip installs this plugin instead of a bare skill folder.

dist/singlefile/engineering-calculation-system.all-in-one.md
  Generated fallback for agents that cannot load multiple files.

dist/source-dev/
  Development/reference source bundle, not the default install target.

dist/ui-client/
  One-click deployment console as a Windows single-file exe (PyInstaller --onefile).
  Produced by `python tools/build_release.py --profile ui-client`. See docs/INSTALLER_GUI.md.

dist/release/
  CODEX, MiniMaxCode, ZCode, QODER Skill/project/plugin, QoderCN IDE/CLI/Cloud Agents, QoderWorkCN, WorkBuddy, TRAE, OpenCode, and AGENTS Generic release zips, checksums, and RELEASE_INDEX.md.
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
dist/release/engineering-calculation-system-Qoder-CLI-Plugin-v2.6.0.zip
dist/release/engineering-calculation-system-QoderCN-v2.6.0.zip
dist/release/engineering-calculation-system-QoderCN-Project-v2.6.0.zip
dist/release/engineering-calculation-system-QoderCN-CLI-v2.6.0.zip
dist/release/engineering-calculation-system-QoderCN-CLI-Project-v2.6.0.zip
dist/release/engineering-calculation-system-QoderCN-Cloud-Agents-v2.6.0.zip
dist/release/engineering-calculation-system-QoderWorkCN-v2.6.0.zip
dist/release/engineering-calculation-system-WorkBuddy-v2.6.0.zip
dist/release/engineering-calculation-system-TRAE-v2.6.0.zip
dist/release/engineering-calculation-system-OpenCode-v2.6.0.zip
dist/release/engineering-calculation-system-AGENTS-Generic-v2.6.0.zip
```

Each zip contains one install folder plus `INSTALL.md`, except MiniMaxCode which is packaged as a MiniMax skills repository root:

```text
CODEX zip:         install engineering-calculation-system/ as the Codex plugin root through the local marketplace; .codex-plugin/plugin.json is the sentinel
MiniMaxCode zip:   local install by copying skills/engineering-calculation-system/ to %USERPROFILE%/.mavis/skills/engineering-calculation-system/; Github import remains supported
ZCode zip:         add engineering-calculation-system-zcode/ as a local marketplace source from Settings -> Plugins -> Discover -> +, then click Get on the plugin card
QODER zip:         upload the zip directly in QODER Skills / Install Skill; this is a lightweight skill/resource entrypoint
QODER Project zip: copy copy-to-project-root/ contents to the QODER project root; this is the recommended Qoder Smart Agent setup
Qoder CLI Plugin zip: install through Qoder CLI plugin management; .qoder-plugin/plugin.json is at the zip root
QoderCN zip:       copy copy-to-user-home/ contents to ~/.lingma/ for Qoder CN IDE user-level Skills and Agents
QoderCN Project zip: copy copy-to-project-root/ contents to the Qoder CN project root; it installs a .lingma/ project overlay
QoderCN CLI zip:   copy copy-to-user-home/ contents to the user home, preserving .qoder-cn/ and .qodercn/
QoderCN CLI Project zip: copy copy-to-project-root/ contents to the QoderCN CLI project root; it installs .qoder/skills and .qodercn/agents
QoderCN Cloud Agents zip: upload the zip as a Cloud Agents custom Skill; SKILL.md is at the zip root
QoderWorkCN zip:   upload the zip through QoderWork CN Expert Kits; .qoder-plugin/plugin.json is at the zip root
WorkBuddy zip:     upload through WorkBuddy Skills Marketplace / Expert Center import when available; .qoder-plugin/plugin.json is at the zip root
TRAE zip:          copy copy-to-project-root/ contents to the TRAE project root
OpenCode zip:      copy copy-to-project-root/ contents to the OpenCode project root
AGENTS Generic zip: copy copy-to-project-root/ contents to an AGENTS.md-compatible project root
```

## Qoder Product Deployment Choice

For Qoder and Qoder CN-family products, the recommended setup is:

```text
user-level install: once per machine/user profile
project-level install: once per serious or production project
```

Use the user-level install to make reusable agents, skills, and references
available globally in the IDE. Use the project-level package to give the current
workspace the complete core skill, shared contracts, templates, schemas,
validator, project scaffold, and project-local `.qoder/` or `.lingma/` overlay.

If you only want a lightweight router or a quick skill import, the direct QODER
Skill zip or the QoderCN user zip is enough. If the task must produce
`web-complete`, production-ready, deployable, or source-backed calculation
software, deploy the project package as well:

```text
Qoder:   user-level once + QODER Project zip per project
QoderCN IDE: user-level once + QoderCN Project zip per project
QoderCN CLI: user-level once + QoderCN CLI Project zip per project
```

Product-specific paths:

| Product | User/global layer | Project layer | Recommended release zip |
| --- | --- | --- | --- |
| Qoder direct Skill | root `SKILL.md` upload | use QODER Project for production | `engineering-calculation-system-QODER-v2.6.0.zip` |
| Qoder Project | `~/.qoder/skills`, `~/.qoder/agents` via `install_qoder_user.py` | `.qoder/skills`, `.qoder/agents` | `engineering-calculation-system-QODER-Project-v2.6.0.zip` |
| Qoder CLI Plugin | plugin root `.qoder-plugin/plugin.json` | plugin-managed `skills/` and `agents/` | `engineering-calculation-system-Qoder-CLI-Plugin-v2.6.0.zip` |
| QoderCN IDE | `~/.lingma/skills`, `~/.lingma/agents` | `.lingma/skills`, `.lingma/agents` | `engineering-calculation-system-QoderCN-v2.6.0.zip`, `engineering-calculation-system-QoderCN-Project-v2.6.0.zip` |
| QoderCN CLI | `~/.qoder-cn/skills`, `~/.qodercn/agents` | `.qoder/skills`, `.qodercn/agents` | `engineering-calculation-system-QoderCN-CLI-v2.6.0.zip`, `engineering-calculation-system-QoderCN-CLI-Project-v2.6.0.zip` |
| QoderCN Cloud Agents | uploaded Skill zip, then bind to Agent | cloud Agent skill list | `engineering-calculation-system-QoderCN-Cloud-Agents-v2.6.0.zip` |
| QoderWorkCN | Expert Kit upload | kit-managed | `engineering-calculation-system-QoderWorkCN-v2.6.0.zip` |

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
Test-Path "$env:USERPROFILE\.zcode\plugins\engineering-calculation-system-zcode\marketplace.json"
Test-Path "$env:USERPROFILE\.zcode\plugins\engineering-calculation-system-zcode\.zcode-plugin\plugin.json"
Test-Path "$env:USERPROFILE\.zcode\plugins\engineering-calculation-system-zcode\skills\engineering-calculation-system\SKILL.md"
Select-String "$env:USERPROFILE\.zcode\plugins\engineering-calculation-system-zcode\.zcode-plugin\plugin.json" -Pattern '"skills": "skills"'
```

After copying the plugin folder, add that folder as a local marketplace source
from ZCode Settings -> Plugins -> Discover -> +, click Get on the plugin card,
refresh Settings -> Plugins, and keep the plugin enabled. Then refresh
Settings -> Skills and confirm the plugin skills appear under
Plugin skills. If an older imported copy remains installed and the skill is
missing, uninstall that plugin entry from ZCode's Installed tab, refresh the
marketplace, and click Get again so ZCode replaces the cached manifest. ZCode
project-specific guardrails belong in the
workspace `AGENTS.md`; reusable engineering-calculation workflow rules remain
inside the plugin skill. If plugin import is unavailable, copy the plugin's
`skills/engineering-calculation-system/` folder to
`~/.zcode/skills/engineering-calculation-system/` as a legacy fallback.

For QODER web-complete generation, use the QODER Project zip in the target
project. The direct QODER zip keeps `SKILL.md` at the archive root for QODER
skill-import compatibility, but it does not contain the core templates, schemas,
validator, or project scaffold by itself.

For Qoder CN IDE, use the QoderCN user zip for user-level reusable Skills and
Agents under `~/.lingma/`, and use the QoderCN Project zip for project-level
`.lingma/agents` and `.lingma/skills` when the current workspace needs full
project capability. Official Qoder CN documentation also mentions `.qodercn`
for the IDE process/cache and `QoderCN.exe`; this package uses `.lingma` for
custom Skill/Agent resources because that is the documented resource location
for Qoder CN IDE custom agents and skills.

For QoderCN CLI, use the QoderCN CLI user zip for the documented split
user-level resource layout:

```text
~/.qoder-cn/skills/engineering-calc-system/SKILL.md
~/.qodercn/agents/engineering-calc-system.md
~/.qodercn/references/engineering-calc-system.md
```

Use the QoderCN CLI Project zip in each serious CLI project:

```text
.qoder/skills/engineering-calc-system/SKILL.md
.qodercn/agents/engineering-calc-system.md
.qodercn/references/engineering-calc-system.md
```

Do not substitute the QoderCN IDE `.lingma` package for the QoderCN CLI
`.qoder-cn` / `.qodercn` package; they target different documented product
surfaces.

For QoderCN Cloud Agents, upload
`engineering-calculation-system-QoderCN-Cloud-Agents-v2.6.0.zip` as a custom
Skill. The archive root contains `SKILL.md`, `reference.md`,
`qoder_quickstart.md`, and `assets/`, and is intentionally small for the Cloud
Agents Skill upload limit. After upload, bind the returned Skill ID/version to
the target Agent. The bind API replaces the Agent's `skills` list, so preserve
existing Agent skill bindings before updating. This cloud Skill is still a
lightweight router; production `web-complete` work must use a complete
core/project package.

For Qoder CLI plugin installs, use
`engineering-calculation-system-Qoder-CLI-Plugin-v2.6.0.zip`. Its root contains
`.qoder-plugin/plugin.json`, `skills/engineering-calculation-system/`,
`skills/engineering-calc-system/`, `agents/`, `references/`, and `adapters/`.
The plugin is the best Qoder CLI packaging shape when you want one installable
bundle with both the supervisor agents and the complete core skill.

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

engineering-calculation-system-Qoder-CLI-Plugin-v2.6.0.zip
  Qoder CLI plugin package with .qoder-plugin/plugin.json at the zip root and
  complete core skill resources under skills/engineering-calculation-system/.

engineering-calculation-system-QoderCN-CLI-v2.6.0.zip
  QoderCN CLI user-level split package for ~/.qoder-cn/skills and
  ~/.qodercn/agents.

engineering-calculation-system-QoderCN-CLI-Project-v2.6.0.zip
  QoderCN CLI project-root package with .qoder/skills, .qodercn/agents,
  complete core templates, schemas, validator, and project scaffold.

engineering-calculation-system-QoderCN-Cloud-Agents-v2.6.0.zip
  QoderCN Cloud Agents Skill upload package with root SKILL.md.
```

Use QODER Project for serious Qoder project work. Use the direct QODER Skill zip
only when the target flow is Qoder Skill import or lightweight routing.

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
python tools/build_release.py --profile qoder-plugin
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

The platform release zips are the recommended install path. Use the MiniMaxCode zip for MiniMax Code standard skill import or discovery. Use the ZCode zip for ZCode plugin installation or custom marketplace import. Use the QODER zip for direct QODER Skill upload; use the QODER Project, QoderCN Project, QoderCN CLI Project, TRAE, and OpenCode packages when copying an overlay into a project root. Use the Qoder CLI Plugin zip for Qoder CLI plugin install, the QoderCN zip for Qoder CN IDE user-level `~/.lingma` install, the QoderCN CLI zip for the CLI split `~/.qoder-cn` / `~/.qodercn` user install, and the QoderCN Cloud Agents zip for custom Skill upload. Use raw overlays only when developing or debugging a release profile:

```text
core install root: dist/core/engineering-calculation-system/
overlay source:    dist/adapters-light/ or dist/qoder-addon/
plugin source:     dist/qoder-plugin/
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

The Qoder CLI plugin source provides:

```text
.qoder-plugin/plugin.json
skills/engineering-calculation-system/
skills/engineering-calc-system/
agents/
references/
adapters/
```

Inside `.qoder/`, the Smart Agent entrypoint is
`.qoder/agents/engineering-calc-system.md`; the skill/resource layer is
`.qoder/skills/engineering-calc-system/`; long non-agent reference material is
stored under `.qoder/references/`.

For Qoder CN release packages, the same internal overlay is remapped to
`agents/`, `skills/`, and `references/` for user-level `~/.lingma` install, or
to project-root `.lingma/` for project-level install.

For QoderCN CLI release packages, the same internal overlay is remapped to
`.qoder-cn/skills/` plus `.qodercn/agents/` for user-level install, or to
project-root `.qoder/skills/` plus `.qodercn/agents/` for project-level install.

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
