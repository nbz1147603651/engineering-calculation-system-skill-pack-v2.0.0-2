# Codex Plugin Adapter

Use this adapter when the Engineering Calculation System skill pack is loaded
through the Codex plugin. It does not replace the lifecycle router, parent
skills, child skills, contracts, or templates. It tells Codex how to execute
the same workflow inside a shared workspace.

## Resource Roots

- Treat the directory containing the root `SKILL.md` as the skill root.
- Resolve `skills/`, `parent/`, `shared/`, `templates/`, `schemas/`,
  `scripts/`, and `project_template/` relative to that skill root.
- Do not write into the plugin package during normal user project work.
  Project artifacts belong in the user's target workspace.
- For plugin maintenance tasks, keep all Codex-specific changes inside the
  plugin folder.

## Codex Execution Rules

- Follow the root `SKILL.md` load order: read this adapter, then the router,
  then only the parent/child skills needed for the task.
- Treat this plugin as the Codex distribution boundary. For normal user work,
  the target workspace is the user's repository or generated project; the
  plugin package is read-only unless the user explicitly asks for plugin
  maintenance.
- For multi-step plans, read `shared/planning-discipline.md` before editing.
  For user feedback, external review, or worker reports, read
  `shared/review-feedback-discipline.md` before choosing fix, reject, or
  upstream route. For release, plugin sync, or platform packaging, read
  `shared/version-control-discipline.md`.
- If a target repository has `.codegraph/`, use CodeGraph before text search
  when locating or understanding code.
- Use `rg` or CodeGraph for code discovery before broad filesystem reads.
- When a task involves PDFs, spreadsheets, Word/PowerPoint artifacts, rendered
  reports, or browser-visible web apps, use the relevant Codex-provided tools
  and bundled workspace dependencies when available. Record unavailable tools
  as validation or acquisition limitations instead of silently lowering gates.
- Use `apply_patch` for manual edits and keep changes scoped to the requested
  workspace paths.
- Run the relevant project tests and this package's validation script before
  calling implementation, verification, or release work complete.
- For plugin maintenance, use `scripts/sync_from_core.py --dry-run` before
  overwriting bundled skill files unless the change is already isolated and
  intentional.
- Reference real local files with absolute paths in final responses when
  pointing the user to artifacts.

## Codex Trigger And Routing

Route through this skill pack when the user asks to build, inspect, verify, or
deploy any engineering calculator, calculation book, source-backed report,
formula module, batch calculator, review UI, or online calculation system. Do
not wait for the exact words "engineering calculation" if the work clearly
depends on formulas, standards, checks, capacities, loads, factors, or
traceable calculation outputs.

The first non-trivial response should establish:

```text
task_type:
material_state:
required_skill_path:
delivery_mode:
gate_status:
completion_evidence_category:
```

Use `web-complete` by default for deployable or online calculator requests.
Use narrower modes only when the user explicitly asks for a draft, prototype,
core-only module, or report-only artifact.

## Generated Project Bootstrap

When creating a new calculator project, copy or recreate the scaffold pattern
from `project_template/engineering_calc_project` into the target workspace and
then customize the package, book name, sources, inputs, modules, UI, reports,
and deployment files. Do not run production formulas from the template example
book. Replace example logic with source-backed modules and keep all interfaces
thin over `run_book(BookInput) -> BookResult`.

Before claiming generated-project completion, run the appropriate subset:

```bash
python scripts/verify_golden_cases.py --project-root <project-root>
python -m pytest
python <skill-root>/scripts/validate_artifacts.py --package-root <skill-root> --profile core --project <project-root> --delivery web-complete
```

## Reference Acquisition In Codex

- Engineering standards, product data, laws, current web docs, pricing,
  availability, jurisdiction rules, and other unstable or external facts
  require current source verification.
- Use available web/search/browser tools for reference discovery when the
  lifecycle route reaches acquisition or when the source basis is uncertain.
- Persist accepted and rejected candidates using the acquisition templates
  instead of relying on chat memory.
- If a required retrieval tool is unavailable, state that explicitly in the
  acquisition notes and do not upgrade the evidence gate based on memory.

## Multi-Agent Boundaries

- Use Codex subagents only when the user explicitly asks for multiple agents,
  parallel work, delegation, or a similar split.
- Read `shared/multi-agent-orchestration.md` before assigning any worker task.
- Keep lifecycle routing, evidence gates, source authority, ID allocation,
  handoff freeze, `run_book()` public contract changes, and final acceptance
  with the supervisor.
- Workers should own disjoint paths and return result packets or equivalent
  fields in their final messages.

## Delivery And Validation

- Declare one delivery mode before implementation work:
  `core-only`, `report-only`, `prototype-web`, or `web-complete`.
- Default to `web-complete` for online calculators and calculation systems
  unless the user explicitly asks for a narrower artifact.
- Do not mark formula work production-ready without source-backed handoff
  artifacts and a permissive coding gate.
- For a generated project, run:

```bash
python scripts/validate_artifacts.py --package-root <skill-root> --profile core --project <project-root> --delivery web-complete
```

- For plugin package maintenance, run the plugin-level doctor:

```bash
python scripts/validate_plugin.py
```

The Codex plugin doctor is intentionally stronger than manifest validation: it
also checks bundled-source sync, overlay sync, core artifact validation,
web-complete project-template validation, and executable golden-case smoke.

## Completion Summary

When finishing user work, report:

- lifecycle route and gate status when relevant
- delivery mode
- files or artifacts changed
- validation commands run and results
- any source, handoff, or deployment blockers that remain
