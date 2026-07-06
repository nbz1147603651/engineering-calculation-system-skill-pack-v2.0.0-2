# Codex Quickstart

Use this plugin when the task needs source-backed engineering calculation software, not just a
one-off script. The plugin exposes the Engineering Calculation System skill pack as a Codex
installable component while keeping the lifecycle contracts inside the bundled skill root.

## Start A Task

Good first prompts:

```text
Use Engineering Calculation System to route this project and produce gate cards.
Build a web-complete source-backed engineering calculator with reports.
Verify this calculation book with golden cases and artifact validation.
```

For non-trivial work, Codex should load:

```text
skills/engineering-calculation-system/SKILL.md
skills/engineering-calculation-system/shared/codex-plugin-adapter.md
skills/engineering-calculation-system/skills/00-engineering-calculation-router.skill.md
```

Then it should follow the routed parent and child skills rather than jumping directly into code.

## Codex Workspace Pattern

- If the target repository has `.codegraph/`, use CodeGraph before broad text search.
- Keep plugin package edits inside `plugins/engineering-calculation-system/`.
- Put generated project artifacts in the user's workspace, not inside the plugin package, unless
  the user is explicitly maintaining this plugin.
- For frontend or report-preview work, run the local web app and verify API/report/chart behavior
  with tests or browser automation.
- For source-backed claims, preserve source IDs, formula traces, stable result paths, and golden
  case evidence in artifacts.

## Validation Commands

From the Codex plugin folder:

```bash
python scripts/validate_plugin.py
```

This command also works from an installed Codex plugin cache. Source-checkout
checks such as local marketplace discovery and bundled-source drift run only
when the source repository is present.

For the bundled generated project template:

```bash
cd skills/engineering-calculation-system/project_template/engineering_calc_project
python scripts/verify_golden_cases.py --project-root .
python -m pytest
```

From the bundled skill root:

```bash
python scripts/validate_artifacts.py --package-root . --profile core \
  --project project_template/engineering_calc_project --delivery web-complete
```

## Maintenance Flow

When the core skill changes, refresh the bundled Codex skill copy with:

```bash
python scripts/sync_from_core.py --dry-run
python scripts/sync_from_core.py --force
```

The sync script reapplies `overlays/engineering-calculation-system/shared/codex-plugin-adapter.md`
and then runs the plugin doctor.
