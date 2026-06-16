# Agent Entrypoints

Use this file when the target agent cannot automatically discover the root `SKILL.md`.

## Codex

Install the package as a skill folder when possible. The root `SKILL.md` is the primary entrypoint. For a single-file import, use `engineering-calculation-system.all-in-one.md`.

## Qoder / Trae / opencode

Register the package root as project instructions or a reusable prompt bundle. Use this routing prompt:

```text
Use the Engineering Calculation System skill pack.
Start with skills/00-engineering-calculation-router.skill.md.
Do not load all child skills at once. Load only the parent and child skills selected by the router.
During 02-reference-discovery-and-acquisition, use available internet search/browser tools actively for missing or insufficient references, and log searches in references/acquisition/search_log.csv.
Use templates/ for output artifacts and scripts/validate_artifacts.py before considering the work complete.
```

## Generic Agent

If the platform only accepts one instruction file, load `engineering-calculation-system.all-in-one.md`.

If the platform accepts multiple files, expose these directories:

```text
parent/
skills/
shared/
templates/
schemas/
scripts/
project_template/
```
