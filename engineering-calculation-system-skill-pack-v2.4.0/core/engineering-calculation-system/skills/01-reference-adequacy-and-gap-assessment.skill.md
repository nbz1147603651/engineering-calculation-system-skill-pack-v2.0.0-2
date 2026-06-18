---
name: reference-adequacy-and-gap-assessment
description: Assess whether available engineering materials are sufficient for calculation logic extraction or software implementation. Use when no materials are provided, materials look incomplete, source authority is unclear, the user asks whether資料足够, or before deciding whether to search for additional references.
---

# Reference Adequacy and Gap Assessment

Use this skill before searching, analyzing, or coding when source sufficiency is unclear.

## Goal

Determine whether the available references are enough to support:

```text
conceptual outline
traceable calculation blueprint
implementation handoff
prototype code
production-grade calculation book software
```

## Do Not

Do not invent missing formulas, factors, units, load combinations, coefficients, or branch rules.

Do not treat a user description as a governing source unless it is explicitly a project assumption.

Do not send work to coding if the source basis is not sufficient for formulas, units, and checks.

## Inputs to Inspect

```text
user request
uploaded documents
local evidence library if present
references/source_registry.yaml if present
references/acquisition/acquisition_handoff.yaml if present
handoff/implementation_handoff.yaml if present
```

## Adequacy Dimensions

Evaluate coverage for:

```text
engineering domain and calculation object
governing code / standard / manual
jurisdiction and version/year
project-specific design basis
load cases and load combinations
geometry definitions
material / soil / hydraulic / structural parameters
formula sources
lookup tables / charts / interpolation rules
branch and applicability rules
unit and sign conventions
safety factors / partial factors / resistance factors
worked examples or regression references
reporting requirements
review / approval requirements
```

## Required Output Artifacts

```text
references/acquisition/reference_gap_assessment.md
references/acquisition/source_coverage_matrix.csv
references/acquisition/acquisition_plan.yaml
references/acquisition/open_reference_questions.md
```

## Coverage Matrix

Use this structure:

| Requirement ID | Requirement | Importance | Covered? | Current Source ID | Gap | Needed Source Type | Blocks Analysis? | Blocks Coding? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Importance values:

```text
critical
high
medium
low
```

Coverage values:

```text
covered
partially_covered
not_covered
conflicting
unknown
```

## Acquisition Plan

For each gap, define:

```text
gap_id
needed_information
why_it_matters
preferred_source_type
authority_priority
target_jurisdiction_or_standard
search_keywords
candidate_domains_or_publishers
minimum_acceptance_criteria
fallback_if_not_found
```

## Gate Decision

Return one evidence gate status:

```text
evidence_no_go
search_required
partial_analysis_allowed
analysis_allowed
```

Default decisions:

```text
No governing source and formulas needed -> search_required
No formulas, lookup rules, or units -> search_required
Enough for rough structure only -> partial_analysis_allowed
Enough for traceable blueprint but not tests -> analysis_allowed
```

If the user asks for implementation, also state whether the downstream coding gate is likely `no_go`, `prototype_allowed`, or `production_allowed`, but do not use coding gate statuses as the evidence gate result.

## Required Final Response

Provide:

```text
material sufficiency judgment
blocking gaps
non-blocking gaps
recommended sources to find
whether web/file-library/user upload search should be used
local artifacts to create
next skill path
```
