# ZCode Plugin Adapter

Use this file only when the Engineering Calculation System is loaded through
the ZCode plugin package. It maps ZCode's plugin boundary to the platform-neutral
skill workflow; it does not replace the lifecycle router, parent orchestrators,
child skills, shared gates, templates, or validators.

## Loading Contract

- Treat `.zcode-plugin/plugin.json` as the install and discovery manifest.
- Keep its skill component declaration as `"skills": "skills"` so ZCode
  registers the plugin `skills/` directory.
- Treat root `marketplace.json` as the local/Git marketplace descriptor
  when ZCode imports this package as a marketplace source.
- Treat `skills/engineering-calculation-system/SKILL.md` as the skill entrypoint
  exposed by the plugin.
- Load `skills/00-engineering-calculation-router.skill.md` after this adapter,
  then load only the parent and child files selected by the router.
- Keep reusable workflow rules in the bundled skill. Keep project-specific
  operating rules in the workspace `AGENTS.md`.

## Workspace Boundaries

- Do not write into the plugin package during normal user project work.
- Generated projects, evidence libraries, reports, and validation outputs belong
  in the active ZCode workspace.
- For plugin maintenance tasks, keep ZCode-specific changes inside
  `plugins/engineering-calculation-system-zcode/`.
- If the repository has `.codegraph/`, use CodeGraph before broad text search
  when locating code for package, release, or adapter work.

## ZCode Conveniences

- Use ZCode file references, workspace context, review panels, Goal Mode,
  subagents, and model or execution controls as accelerators, not as sources of
  engineering authority.
- For long tasks or continuation flows, maintain
  `.engineering-calc/work/progress.md` and resume from the ledger before
  making completion claims.
- Use ZCode's plugin manager to install, enable, update, disable, or remove the
  plugin. Legacy `~/.zcode/skills/<skill-name>/` installs are a fallback only.
- Once enabled, the plugin's skill component should appear under ZCode's plugin
  skills surface and can be selected from the input skill/command picker.

## Safety Gates

- Use `shared/execution-discipline.md` before implementation action.
- Use `shared/planning-discipline.md` for multi-step plans.
- Use `shared/review-feedback-discipline.md` before acting on review or user
  feedback.
- Use `shared/version-control-discipline.md` for package, plugin, adapter, or
  release work.
- Use `shared/completion-evidence.md` before any completion, deployable,
  source-backed, report-ready, formula-verified, or web-complete claim.
- Keep lifecycle routing, evidence gate decisions, source-authority ranking, ID
  namespace control, handoff freeze, `run_book()` public-contract changes, and
  final acceptance serial.

## Plugin Maintenance

For plugin package maintenance, run the plugin-level doctor:

```bash
python scripts/validate_plugin.py
```

Refresh the bundled skill from the core package with:

```bash
python scripts/sync_from_core.py --dry-run
python scripts/sync_from_core.py
```

The sync script may overwrite the bundled skill folder after checking for dirty
destination changes. Keep overlay-only files under `overlays/` so they are
reapplied after every core refresh.
