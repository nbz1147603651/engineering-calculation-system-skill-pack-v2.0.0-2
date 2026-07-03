# Deployment Console (GUI)

A Qt desktop UI to detect target agent programs and deploy the Engineering
Calculation System skill pack / plugin to each of them in one click.

```text
engineering-calculation-system/tools/installer_gui/
|-- app.py        # lightweight entry point and PySide6 dependency check
|-- qt_app.py     # PySide6 main window, QAbstractTableModel, delegates
|-- agents.py     # target agent metadata
|-- detector.py   # program + deployment detection
|-- deployer.py   # build + copy + backup + verify
|-- workers.py    # background thread + event queue
|-- styles.py     # palette + typography tokens
`-- launch.bat    # Windows double-click launcher
```

## Run

```bash
# from the repo root
python engineering-calculation-system/tools/installer_gui/app.py
# or double-click engineering-calculation-system/tools/installer_gui/launch.bat
```

Requires Python 3.9+ and `PySide6`. If `PySide6` is missing the console offers
to install it on first run (`pip install PySide6`).

## UI architecture

The console uses Qt's model/view stack:

- `AgentTableModel` subclasses `QAbstractTableModel` and owns the product rows,
  selected deployment mode, roots, detection state, and busy state.
- `AgentFilterProxyModel` provides search plus all/needs-action filtering
  without rebuilding widgets.
- A compact `QTableView` replaces the old card grid. The selected row drives a
  details panel with deployment mode, deploy, verify, folder, open-root, and
  remove actions.
- Worker events are drained by a `QTimer`; completion refreshes only the affected
  agent row when possible.
- The activity log keeps a bounded in-memory tail so long deploy output does not
  make the UI progressively heavier.

## Run from the distributable exe

A self-contained Windows exe is built as a release profile:

```bash
python tools/build_release.py --profile ui-client
```

This produces `dist/ui-client/engineering-calc-system-installer-v<version>.exe`.
Double-click to run, or copy it to any Windows machine and run there.

Because the exe is a deployment tool and does not bundle the skill source, it
needs the skill-pack repository folder (the one containing
`tools/build_release.py`) before it can build release profiles. On startup it
honors `ECS_REPO_ROOT`, searches parent folders near the exe, then uses any
saved repo path. If none is valid, it starts without a popup and creates a local
`workspace/` placeholder; use the **Repo...** button to select the real repo
before building or deploying. The exe still needs a system Python 3.9+ on `PATH`
to run `build_release.py` for skill-pack builds.

```powershell
$env:ECS_REPO_ROOT = "C:\path\to\engineering-calculation-system"
.\engineering-calc-system-installer-v2.6.0.exe
```

To rebuild the whole release (skill packs + UI exe) in one command, drop the
`--profile` flag. Use `--no-ui-client` to skip the PyInstaller step during fast
iteration:

```bash
python tools/build_release.py
python tools/build_release.py --no-ui-client
```

If PyInstaller is not installed, the `ui-client` profile writes a README
explaining `pip install pyinstaller` instead of failing the whole release.

## What it does

The console lists eight agent products. Qoder and Qoder CN expose their user
folder / selected project deployment choice in the details panel instead of
duplicating table rows. Each row shows the currently selected mode:

- **program**: whether the agent CLI / home directory is present on this machine
- **deployment**: whether the skill is already installed at that agent root
- **target**: the default install location or the selected project root
- **profiles**: release profiles needed for that target

| Agent | Target location | Verify |
| --- | --- | --- |
| Codex | `~/.codex/skills/engineering-calculation-system/` | `SKILL.md` sentinel |
| MiniMax Code | `~/.mavis/skills/engineering-calculation-system/` | `mavis skill show ...` |
| ZCode | `~/.zcode/plugins/engineering-calculation-system-zcode/` | root `marketplace.json` + `.zcode-plugin/plugin.json` + plugin skill sentinel |
| Qoder | user folder: `QODER_HOME` or `~/.qoder`; selected project: writes `.qoder/` configuration | user audit or `.qoder/agents/engineering-calc-system.md` |
| Qoder CN | user folder: `QODER_CN_HOME`, `QODERCN_HOME`, `LINGMA_HOME`, or `~/.lingma`; selected project: writes `.lingma/` configuration | user audit or `.lingma/agents/engineering-calc-system.md` |
| Trae | selected project root, writes `.trae/` and `AGENTS.md` | `.trae/project_rules.md` |
| OpenCode | selected project root, writes `.opencode/` | `.opencode/skills/.../SKILL.md` |
| AGENTS Generic | selected project root, writes `AGENTS.md` and `.agents/` | `AGENTS.md` + `.agents/skills/...` |

For ZCode, Deploy stages a local marketplace folder. Add that folder in ZCode
Settings -> Plugins -> Discover -> +, then install the plugin card with Get.
The GUI cannot force the ZCode client to replace a previously cached plugin
copy. If the plugin is installed but the skill is absent, uninstall the old
entry in ZCode, refresh the marketplace, click Get again, then refresh
Settings -> Skills and check the Plugin skills group.
The ZCode plugin should list the main `engineering-calculation-system` entry,
three parent-layer entries, and lifecycle phase entries for router, 01-14, and
12a/12b/12c workflows.

## Qoder / Qoder CN modes

For Qoder and Qoder CN, choose both modes when you are setting up real project
work:

```text
User folder       install once per machine/user profile
Selected project  deploy once per serious or production project
```

The user-folder mode installs reusable agents, skills, and references so the IDE
can discover the Engineering Calculation System globally. The selected-project
mode writes the project-local `.qoder/` or `.lingma/` overlay alongside the core
skill package, templates, schemas, validator, and project scaffold. That
project-level layer is required before claiming `web-complete`, deployable, or
production-ready output.

Use only the user-folder mode for lightweight routing, quick skill/resource
availability, or exploratory guidance. Use selected-project mode whenever the
current workspace should receive the full engineering calculation workflow.

## Actions

- **Deploy** builds needed release profiles via `tools/build_release.py`, then
  copies the right overlay into the agent root. Existing files are backed up to
  `<name>.bak.<timestamp>` before being overwritten.
- **Verify** re-checks the sentinel file and any supported CLI/audit command.
- **Choose user folder... / Choose project root...** changes the install location or
  selects the concrete project root for project overlays. If a project overlay
  has no selected project root, **Deploy** opens the picker first.
- **Open target** opens the selected install/project location in the OS file manager.
- **Remove** uninstalls only this package's managed files.
- **Build all profiles** runs every release profile in `release_config.json`.
- **Re-scan** re-runs detection for all visible targets.
- **Stop** requests a cooperative cancel of the running job.

## Safety

- No file is silently overwritten; the previous copy is renamed to
  `<name>.bak.<YYYYMMDD-HHMMSS>`.
- Uninstall removes only files this package owns.
- Long-running work happens on a background thread, so the window stays
  responsive while output streams into the log panel.
