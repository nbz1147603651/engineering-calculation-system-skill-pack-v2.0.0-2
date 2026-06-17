---
name: engineering-calculation-system
description: Full lifecycle workflow for engineering calculation software. Use when Codex or another coding agent must assess missing engineering references, acquire and persist source evidence, transform references into a Calculation Logic Blueprint, create an implementation handoff, build decoupled reusable calculation modules, build auditable web calculation software, verify formulas, reports, batch flows, and traceability, or package a runnable local and Linux-cloud deployable online calculator.
---

# Engineering Calculation System

Start with `skills/00-engineering-calculation-router.skill.md` for any non-trivial request. The router decides whether the task belongs to reference acquisition, source analysis, implementation, interface work, or verification.

## Load Order

Use progressive disclosure:

1. Read the router.
2. Read one parent orchestrator when the task spans a phase:
   - `parent/engineering-calculation-reference-acquisition.skill.md`
   - `parent/engineering-calculation-logic-architecture.skill.md`
   - `parent/engineering-calculation-book.skill.md`
3. Read only the child skill files named by the router or parent.
4. Use templates from `templates/` and shared contracts from `shared/` only when generating or validating artifacts.

Install the default runtime skill from `dist/core/engineering-calculation-system/` when using a built release. For environments that cannot load multiple files reliably, use the generated single-file fallback from `dist/singlefile/engineering-calculation-system.all-in-one.md`.

Agent-specific loading paths are optional overlays from `dist/adapters-light/` or `dist/qoder-addon/`. MCPs are accelerators, not required dependencies.

## Non-Negotiable Gates

Optimize for engineering operation quality and reviewer convenience first. Keep the stack as simple as possible only after the workflow is complete, clear, traceable, and pleasant to use.

Default implementation stack is Python-first:

```text
primary runtime: Python 3.9+
calculation modules: Python package under src/<pkg>/libraries/
official runner: Python run_book(BookInput) -> BookResult
backend/API: Flask or FastAPI thin route layer
frontend: browser web app served from webapp/
review/admin: Marimo when Python-native module review or formula publishing is needed
```

Use another calculation runtime only when the user explicitly requests it and the handoff defines an adapter plan. Marimo review is Python-native and cannot directly inspect non-Python modules without a Python wrapper, CLI, or API adapter.

Do not remove useful interface capabilities just to reduce dependencies. Input validation, import/export, report preview, trace review, formula/source visibility, status clarity, and repeatable deployment are part of the product quality bar.

Do not invent engineering formulas, lookup rules, units, coefficients, or branch logic when the source basis is missing.

Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.

Keep formulas out of UI, report templates, CSV/Excel inputs, batch scripts, and presentation-only code. Official calculations must flow through `run_book(BookInput) -> BookResult`.

Do not label a system complete unless reusable calculation modules are decoupled, traceable, independently testable, and recorded for future reuse.

Do not label a web calculation system production-ready unless it has local run instructions, a Linux cloud deployment path, environment-based configuration, smoke tests, and release artifacts.

Do not label a web calculation system complete when the deliverable is only a static `.html` file, exported report HTML, or visual mockup. Production web delivery must include the calculation modules, official runner, backend API/application entrypoint, frontend assets, tests, and deployment path unless the user explicitly requests a static prototype.

When formula rules must be reviewed or changed after deployment, use a declaration-based formula registry plus a token-protected Marimo admin review app under `/admin/review/`; publish changes only after validation and smoke tests pass.

## Artifact Validation

When this package is available on disk, run:

```bash
python3 scripts/validate_artifacts.py --package-root .
```

For layered v2.3 releases, prefer:

```bash
python3 scripts/validate_artifacts.py --package-root . --profile core
```

For generated engineering calculation projects, also run:

```bash
python3 scripts/validate_artifacts.py --package-root <skill-pack-root> --profile core --project <project-root>
```

Treat validation failures as blocking unless the user explicitly asks for a draft or prototype.
