---
name: engineering-calculation-system
description: Full lifecycle workflow for engineering calculation software. Use when Codex or another coding agent must assess missing engineering references, acquire and persist source evidence, transform references into a Calculation Logic Blueprint, create an implementation handoff, build auditable calculation book software, or verify formulas, reports, batch flows, and traceability.
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

For environments that cannot load multiple files reliably, use `engineering-calculation-system.all-in-one.md`.

## Non-Negotiable Gates

Do not invent engineering formulas, lookup rules, units, coefficients, or branch logic when the source basis is missing.

Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.

Keep formulas out of UI, report templates, CSV/Excel inputs, batch scripts, and presentation-only code. Official calculations must flow through `run_book(BookInput) -> BookResult`.

## Artifact Validation

When this package is available on disk, run:

```bash
python3 scripts/validate_artifacts.py --package-root .
```

For generated engineering calculation projects, also run:

```bash
python3 scripts/validate_artifacts.py --package-root <skill-pack-root> --project <project-root>
```

Treat validation failures as blocking unless the user explicitly asks for a draft or prototype.
