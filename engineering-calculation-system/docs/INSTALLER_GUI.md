# Deployment Console (GUI)

A clean desktop UI to detect target agent programs and deploy the Engineering
Calculation System skill pack / plugin to each of them in one click.

```text
engineering-calculation-system/tools/installer_gui/
├── app.py        # main window (entry point)
├── agents.py     # 7 target agents metadata (single source of truth)
├── detector.py   # program + deployment detection
├── deployer.py   # build + copy + backup + verify (reuses build_release.py)
├── workers.py    # background thread + event queue
├── widgets.py    # agent card / log panel / progress bar
├── styles.py     # palette + typography
└── launch.bat    # Windows double-click launcher
```

## Run

```bash
# from the repo root
python engineering-calculation-system/tools/installer_gui/app.py
# or double-click engineering-calculation-system/tools/installer_gui/launch.bat
```

Requires Python 3.9+ and `customtkinter`. If `customtkinter` is missing the
console offers to install it on first run (`pip install customtkinter`).

### Run from the distributable exe

A self-contained Windows exe (no Python needed on the target machine) is built
as a release profile:

```bash
python tools/build_release.py --profile ui-client
```

This produces `dist/ui-client/engineering-calc-system-installer-v<version>.exe`
(~28 MB). Double-click to run, or copy it to any Windows machine and run there.

Because the exe is a *deployment tool* and does not bundle the skill source, the
first launch prompts for the **skill-pack repository folder** (the one containing
`tools/build_release.py`). Pick it once; use the **Repo…** button to change it
later. The exe still needs a system Python 3.9+ on `PATH` to run
`build_release.py` for skill-pack builds (the exe itself only orchestrates
copies/deploys). Set `ECS_REPO_ROOT` to pre-fill the repo path and skip the
prompt:

```powershell
$env:ECS_REPO_ROOT = "C:\path\to\engineering-calculation-system"
.\engineering-calc-system-installer-v2.4.1.exe
```

To rebuild the whole release (skill packs + UI exe) in one command, drop the
`--profile` flag. Use `--no-ui-client` to skip the ~40s PyInstaller step during
fast iteration:

```bash
python tools/build_release.py             # everything, including the exe
python tools/build_release.py --no-ui-client   # skip the exe build
```

If PyInstaller is not installed, the `ui-client` profile writes a README
explaining `pip install pyinstaller` instead of failing the whole release.

## What it does

The console targets seven agents. Each is shown as a card with two status dots:

- **program** — is the agent's CLI / home directory present on this machine?
- **deployed** — is the skill already installed at that agent's root?

| Agent | Kind | Default install root | Verify |
| --- | --- | --- | --- |
| Codex | user | `~/.codex/skills/engineering-calculation-system/` | `SKILL.md` sentinel |
| MiniMax Code | user | `~/.mavis/skills/engineering-calculation-system/` | `mavis skill show …` |
| Qoder (user) | user | `QODER_HOME` or `~/.qoder` | `install_qoder_user.py --audit` |
| Qoder Project | project | pick a project root | `.qoder/agents/engineering-calc-system.md` |
| Trae | project | pick a project root | `.trae/project_rules.md` |
| OpenCode | project | pick a project root | `.opencode/skills/.../SKILL.md` |
| AGENTS Generic | project | pick a project root | `AGENTS.md` + `.agents/skills/...` |

### Buttons

- **Deploy** — builds the needed release profile(s) via `tools/build_release.py`,
  then copies the right overlay into the agent's install root. Existing files
  are backed up to `<name>.bak.<timestamp>` before being overwritten.
- **Verify** — re-checks the sentinel file (and runs `mavis skill show` for
  MiniMax, or `install_qoder_user.py --audit` for Qoder user-level).
- **Remove** — uninstalls only this package's managed files (Qoder user-level
  delegates to `install_qoder_user.py --uninstall`).
- **Folder…** (project agents) — choose the project root to overlay into.
- **Build all profiles** — runs every release profile in `release_config.json`
  so subsequent deploys skip the build step.
- **Re-scan** — re-runs detection for all cards.
- **Stop** — requests a cooperative cancel of the running job.

### Safety

- No file is ever silently overwritten; the previous copy is renamed to
  `<name>.bak.<YYYYMMDD-HHMMSS>`.
- Uninstall removes only files this package owns (known overlay tree +
  sentinels); user content is untouched.
- All long-running work happens on a background thread, so the window stays
  responsive. Output streams into the log panel at the bottom.

## How it reuses existing tooling

The console does **not** reimplement build or install logic:

- `deployer.build_profiles()` shells out to `python tools/build_release.py
  --profile <p>` for each required profile.
- The Qoder user-level deploy/verify/uninstall shells out to
  `python tools/install_qoder_user.py` with `--build` / `--audit` / `--uninstall`.
- Version and profile list are read from `tools/release_config.json`.

So any change to `release_config.json`, `build_release.py`, or
`install_qoder_user.py` is picked up automatically — no GUI changes needed.
