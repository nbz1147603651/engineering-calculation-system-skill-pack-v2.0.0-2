---
name: engineering-calculation-system
description: Build, verify, package, or deploy source-backed engineering calculation web apps and calculation books. Use when the user needs to assess or acquire engineering references, turn standards/manuals/PDFs/spreadsheets into a Calculation Logic Blueprint and implementation handoff, build decoupled reusable calculation modules and an official run_book() runner, build an auditable web calculation app with a reusable UI kit and HTML/LaTeX/Overleaf reports, verify formulas/reports/batch/traceability, or package a runnable local and Linux-cloud deployable online calculator - even when "calculation", "engineering", or "calculation book" is not named explicitly.
version: 2.6.0
---

# Engineering Calculation System

## Codex Plugin Adapter

When this package is loaded from the Codex plugin, read
`shared/codex-plugin-adapter.md` before the router. The adapter maps this
platform-neutral skill pack onto Codex tool use, workspace edits, validation,
multi-agent boundaries, and user-facing completion rules.

Full lifecycle for source-backed engineering calculation software. Start with
`skills/00-engineering-calculation-router.skill.md` for any non-trivial request. It classifies the
material state and task intent, then routes to the right 01-14 path.

## Load order (progressive disclosure)

1. Read the router.
2. For any non-trivial task, read `shared/execution-discipline.md` and prepare the route card,
   gate card, artifact contract, and validation evidence frame before implementation action.
3. Read one parent orchestrator when a task spans a phase:
   `parent/engineering-calculation-reference-acquisition.skill.md` (skills 01-03),
   `parent/engineering-calculation-logic-architecture.skill.md` (skills 04-07), or
   `parent/engineering-calculation-book.skill.md` (skills 08-14).
4. Read only the child skills named by the router or parent.
5. For implementation/release/validation, read `shared/lifecycle.md` (the single source for the
   01-14 gates, delivery-mode bar, and quality checks).
6. For multi-step plans or plan execution, read `shared/planning-discipline.md`.
7. Before applying user, reviewer, worker, or tool feedback, read
   `shared/review-feedback-discipline.md`.
8. For large package, plugin, adapter, platform, or release work, read
   `shared/version-control-discipline.md`.
9. Before making completion, verification, production, deployable, or web-complete claims, read
   `shared/completion-evidence.md`.
10. For bug fixes or regressions, read `shared/systematic-debugging.md`.
11. For explicit multi-agent/parallel work, read `shared/multi-agent-orchestration.md` plus the
   orchestration task/review templates.
12. Load other `templates/` and `shared/` contracts only when generating or validating artifacts.

Install the runtime skill from `dist/core/engineering-calculation-system/` for a built release; use
`dist/singlefile/engineering-calculation-system.all-in-one.md` when an environment cannot load
multiple files. Adapter overlays live in `dist/adapters-light/` or `dist/qoder-addon/`. MCPs are
accelerators, not required dependencies.

## Canonical Contracts

Do not copy full gate rules into adapters or child skills. Use these files as the single sources:

- `shared/lifecycle.md`: delivery mode, 01-14 gates, formula boundary,
  `run_book(BookInput) -> BookResult`, and web-complete exit gate.
- `shared/execution-discipline.md`: route card, gate card, artifact contract, and validation
  evidence discipline.
- `shared/planning-discipline.md`: plan card, plan quality gate, exact-file/interface validation,
  and stop conditions for multi-step work.
- `shared/review-feedback-discipline.md`: review feedback card and source/formula/gate conflict
  handling before edits.
- `shared/version-control-discipline.md`: workspace isolation, dirty-state handling, platform sync,
  and release closure.
- `shared/completion-evidence.md`: claim-to-evidence matrix for source-backed, production,
  formula verification, report-ready, web-complete, deployable, and bug-fixed claims.
- `shared/systematic-debugging.md`: engineering bug-fix root-cause chain and lowest-correct-layer
  repair rule.
- `shared/multi-agent-orchestration.md`: task brief, owned paths, result packet, review package,
  and ledger contract.

For `web-complete`, the lifecycle's dual closure rule remains mandatory: a readable calculation
book and a complete web calculation system must both close before completion is claimed.

## Artifact validation

```bash
python3 scripts/validate_artifacts.py --package-root .                         # skill pack
python3 scripts/validate_artifacts.py --package-root . --profile core          # layered release
python3 scripts/validate_artifacts.py --package-root <skill-pack-root> --profile core \
  --project <project-root> --delivery web-complete                             # generated project
```

Treat validation failures as blocking unless the user explicitly asks for a draft or prototype. On
Windows use `python`/`py` if `python3` is unavailable; quote paths with spaces.

## Codex plugin adapter

When loaded from the Codex plugin, read `shared/codex-plugin-adapter.md` before the router. Keep
worker tasks bounded and sidecar-only in Codex-compatible environments; do not delegate lifecycle
routing, evidence-gate decisions, source-authority ranking, ID-namespace control, handoff freeze,
`run_book()` public-contract changes, or final acceptance.
