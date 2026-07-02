---
name: reference-adequacy-and-gap-assessment
description: Assess whether available engineering materials are sufficient for calculation logic extraction or software implementation. Use when no materials are provided, materials look incomplete, source authority is unclear, the user asks whether資料足够, or before deciding whether to search for additional references.
---

# Reference Adequacy and Gap Assessment

## When to use

Before searching, analyzing, or coding, when source sufficiency is unclear. Determine whether the
available references can support a conceptual outline, a traceable blueprint, an implementation
handoff, prototype code, or production-grade calculation-book software.

## Do not

Invent missing formulas, factors, units, load combinations, coefficients, or branch rules. Treat a
user description as a governing source only if it is explicitly a project assumption. Send work to
coding if the source basis is not sufficient for formulas, units, and checks.

## Inputs to inspect

```text
user request
uploaded documents
local evidence library if present
references/source_registry.yaml if present
references/acquisition/acquisition_handoff.yaml if present
handoff/implementation_handoff.yaml if present
```

## Steps

1. Score coverage across these adequacy dimensions: engineering domain & calculation object;
   governing code/standard/manual; jurisdiction & version/year; project-specific design basis;
   load cases & combinations; geometry; material/soil/hydraulic/structural parameters; formula
   sources; lookup tables/charts/interpolation; branch & applicability rules; unit & sign
   conventions; safety/partial/resistance factors; worked examples or regression references;
   reporting requirements; review/approval requirements.
2. Fill the coverage matrix (`templates/acquisition/source_coverage_matrix.csv`) — one row per
   requirement with columns: Requirement ID | Requirement | Importance (critical/high/medium/low)
   | Covered? (covered/partially_covered/not_covered/conflicting/unknown) | Current Source ID |
   Gap | Needed Source Type | Blocks Analysis? | Blocks Coding?
3. For each gap, write an acquisition-plan row (`templates/acquisition/acquisition_plan.yaml`):
   gap_id, needed_information, why_it_matters, preferred_source_type, authority_priority,
   target_jurisdiction_or_standard, search_keywords, candidate_domains_or_publishers,
   minimum_acceptance_criteria, fallback_if_not_found.
4. Record open reference questions in `templates/acquisition/open_reference_questions.md`.
5. Set the evidence gate: `evidence_no_go` (cannot analyze/code — basis absent/unreliable) |
   `search_required` (references must be found first) | `partial_analysis_allowed` (enough for
   outline only) | `analysis_allowed` (enough for a traceable blueprint). If the user asks for
   implementation, also state the *likely* coding gate (no_go/prototype_allowed/production_allowed)
   but do not use coding-gate values as the evidence-gate result.

## Artifacts

```text
references/acquisition/reference_gap_assessment.md
references/acquisition/source_coverage_matrix.csv   (templates/acquisition/source_coverage_matrix.csv)
references/acquisition/acquisition_plan.yaml         (templates/acquisition/acquisition_plan.yaml)
references/acquisition/open_reference_questions.md   (templates/acquisition/open_reference_questions.md)
```

## Exit gate

Evidence-gate status is set. See `shared/lifecycle.md` row 01. Next path: 02 if `search_required`
or gaps remain; 04 if `analysis_allowed` and analysis is the goal.
