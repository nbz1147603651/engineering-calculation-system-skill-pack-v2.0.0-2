---
name: engineering-calculation-reference-acquisition
description: Parent/orchestrator skill for finding, screening, acquiring, and locally persisting engineering references before analysis. Use when the user has no materials, insufficient materials, stale or conflicting materials, unclear code basis, or asks the model to find references for an engineering calculation workflow before building a Calculation Logic Blueprint or software implementation.
---

# Engineering Calculation Reference Acquisition - Parent Orchestrator

Use this parent when source materials are missing, incomplete, stale, contradictory, or not
authoritative enough to analyze. It does NOT extract formulas or implement code. It builds a local
evidence library that downstream analysis can trust and cite.

## Entry condition

The router routes here when the material state is `no_materials`, `insufficient_materials`, or
`materials_available_untrusted`. If a usable `references/acquisition/acquisition_handoff.yaml`
already exists and the user asks for analysis or implementation, skip this phase and route to the
logic-architecture parent instead. For non-trivial work, use `shared/execution-discipline.md` to
keep the route card, gate card, artifact contract, and validation evidence current.

## Child skills (run in order)

```text
01-reference-adequacy-and-gap-assessment   classify gaps, set evidence gate
02-reference-discovery-and-acquisition     search, screen, record retrieval decisions
03-reference-persistence-and-local-library persist allowed materials + source cards + handoff
```

## Phase exit gate

Hand off to analysis only when the evidence gate is `analysis_allowed` (or an explicit blocker is
recorded). The required handoff artifact is `references/acquisition/acquisition_handoff.yaml`. See
`shared/lifecycle.md` rows 01-03 for the per-step entry/exit gates and the End-of-Step Rule. Use
`shared/completion-evidence.md` before making any `source-backed` or `analysis_allowed` claim.

## Cross-cutting rules (loaded on demand, not restated here)

- Copyright and access limits: `shared/copyright-and-access-policy.md`.
- Multi-agent / parallel acquisition: `shared/multi-agent-orchestration.md` (only if the user
  explicitly requests parallel work). Serial items - source ID assignment, access decisions,
  authority ranking, acquisition-handoff finalization - stay with the supervisor.
