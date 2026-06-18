# Web-Complete Delivery Contract

This contract applies to every adapter entrypoint: Codex, MiniMaxCode, Qoder,
OpenCode, Trae, AGENTS-compatible rules agents, and the generated single-file
fallback.

## Delivery Mode Declaration

Before implementation work starts, declare one delivery mode in the working
notes or final handoff:

```text
core-only
report-only
prototype-web
web-complete
```

Default to `web-complete` whenever the user asks for a calculation system,
calculation-book software, web app, online calculator, deployable tool, reusable
software package, batch workflow, or does not explicitly request a narrower
prototype.

Only use `core-only`, `report-only`, or `prototype-web` when the user explicitly
asks for that reduced scope. Reduced-scope work must be labeled as not complete
and not deployable.

## Web-Complete Minimum

A `web-complete` engineering calculation delivery must include all of these:

- reusable calculation modules and the official `run_book(BookInput) -> BookResult`
  path
- typed input/result models and traceable governing status
- backend application entrypoint and thin API routes
- `/health` health endpoint and `POST /api/calculate`
- report preview or download route that consumes `BookResult`
- automatic final calculation-book route `POST /api/report/final` that chooses LaTeX/PDF when a local compiler exists and A4 HTML otherwise
- LaTeX/Overleaf-compatible report package export when calculation-book export is in scope, including template interaction, `GET /api/report/decision`, `GET /api/report/templates`, `latex_template_id`, compile validation, and default fallback
- import/export route for JSON configuration
- batch route or documented batch interface that calls `run_book()` once per case
- browser frontend assets under `webapp/` or an explicitly documented equivalent
- reusable UI kit assets: shared partials, `tokens.css`, `components.css`, and
  book-specific additions in `style.css`
- interactive Chinese/English UI switching with `data-i18n` bindings,
  `/api/i18n/<lang>`, persisted language preference, and report/API calls using
  the selected language
- managed input, normalized result, upload package, report, batch summary, and log
  directories
- release/deployment files for Docker or systemd/nginx plus environment examples
- smoke tests for health, calculate, Chinese/English i18n, import, export,
  report, and batch paths
- release checklist with local run, API smoke, deployment smoke, and remaining
  assumptions
- successful artifact validation before any claim of completion

## Completion Guard

Do not describe a delivery as complete, production-ready, deployable, or
web-complete if it is only:

- a CLI runner such as `run_book.py`
- `outputs/book_result.json`
- static HTML
- exported report HTML
- a UI mockup
- a notebook-only demo

Those artifacts may be valid outputs or prototypes, but they are not a deployable
web calculation system.

## Default Full Implementation Path

For `web-complete`, use this default implementation path unless the user
explicitly narrows scope:

```text
08 architecture
-> 09 core/data models
-> 10 reusable modules
-> 11 book runner
-> 12a report context/rendering
-> 12b frontend/review interfaces
-> 12c batch import/export packages
-> 13 verification/regression/traceability
-> 14 cloud web release/deployment
```

If a project already has a tested calculation core, preserve it and complete the
missing web, batch, report, deployment, and smoke-test layers.

## Installation Shape Check

At the start of work, inspect the installed package shape:

```text
SKILL.md
skills/
shared/
templates/
schemas/
scripts/validate_artifacts.py
project_template/
```

If only a lightweight wrapper is present, such as a Qoder direct skill with only
`SKILL.md`, `reference.md`, and assets, state that the current install is a
lightweight entrypoint, not the complete project template. Use the full
project/root package or the generated single-file fallback before claiming
web-complete delivery.

## Validation

For generated projects, run artifact validation before final acceptance:

```bash
python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete
```

When the validator is available only from the source checkout, run the same
command with `--package-root` pointed at the installed core package.
