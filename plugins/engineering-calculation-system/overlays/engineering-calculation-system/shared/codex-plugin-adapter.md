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
- If a target repository has `.codegraph/`, use CodeGraph before text search
  when locating or understanding code.
- Use `rg` or CodeGraph for code discovery before broad filesystem reads.
- Use `apply_patch` for manual edits and keep changes scoped to the requested
  workspace paths.
- Run the relevant project tests and this package's validation script before
  calling implementation, verification, or release work complete.
- Reference real local files with absolute paths in final responses when
  pointing the user to artifacts.

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

## Completion Summary

When finishing user work, report:

- lifecycle route and gate status when relevant
- delivery mode
- files or artifacts changed
- validation commands run and results
- any source, handoff, or deployment blockers that remain

