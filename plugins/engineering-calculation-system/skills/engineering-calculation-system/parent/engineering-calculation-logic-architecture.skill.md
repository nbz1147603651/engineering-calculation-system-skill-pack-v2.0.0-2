---
name: engineering-calculation-logic-architecture
description: Parent/orchestrator skill for transforming a local engineering evidence library or user-provided engineering references into an implementation-ready Calculation Logic Blueprint and Implementation Handoff Contract. Use before coding when analyzing engineering codes, manuals, PDFs, spreadsheets, reports, design notes, test reports, soil reports, existing scripts, or legacy calculation books.
---

# Engineering Calculation Logic Architecture — Parent Orchestrator

Use this parent after the evidence gate has enough material to analyze. If no material exists or
the source basis is too weak, route upstream to the reference-acquisition parent first. This
parent does NOT write production code — it turns references into a traceable, implementation-ready
calculation architecture.

## Entry condition

A local evidence library exists (or user-provided materials are sufficient) and the evidence gate
is `analysis_allowed`. If `references/acquisition/acquisition_handoff.yaml` is missing and source
sufficiency is doubtful, run skills 01-03 first.

## Child skills (run in order)

```text
04-source-intake-and-authority          stable source IDs, authority ranking, conflicts
05-engineering-logic-blueprint          concept map + normalized calculation nodes + diagrams
06-formula-lookup-branch-extraction     freeze formulas, lookups, branches, units, test needs
07-implementation-handoff-contract      freeze public scope, runtime stack, coding gate
```

## Phase exit gate

Hand off to implementation only when `handoff/implementation_handoff.yaml` and
`handoff/coding_go_no_go.md` exist and the coding gate is `production_allowed` (or
`prototype_allowed` for an explicitly requested prototype). The product is the reviewable
Calculation Logic Blueprint, not the Mermaid views — diagrams are views of the deeper node model.
See `shared/lifecycle.md` rows 04-07 for the per-step entry/exit gates.

## Cross-cutting rules (loaded on demand, not restated here)

- ID namespace (source/node/formula/lookup/branch IDs): `shared/id-convention.md`. ID allocation
  is supervisor-only in multi-agent runs.
- Multi-agent / parallel analysis: `shared/multi-agent-orchestration.md` (only if the user
  explicitly requests parallel work). Serial items — authority ranking, conflict resolution,
  normalized node-graph merge, handoff freeze — stay with the supervisor.
