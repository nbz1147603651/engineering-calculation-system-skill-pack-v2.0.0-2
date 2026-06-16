---
name: engineering-calculation-logic-architecture
description: Parent/orchestrator skill for transforming a local engineering evidence library or user-provided engineering references into an implementation-ready Calculation Logic Blueprint and Implementation Handoff Contract. Use before coding when analyzing engineering codes, manuals, PDFs, spreadsheets, reports, design notes, test reports, soil reports, existing scripts, or legacy calculation books.
---

# Engineering Calculation Logic Architecture — Parent Orchestrator

Use this parent skill after the evidence gate has enough material to analyze. If no material exists or the source basis is too weak, route upstream to `engineering-calculation-reference-acquisition` first.

This skill does not primarily write production code. It orchestrates child skills that turn references into a traceable, implementation-ready calculation architecture.

## Core Principle

Mermaid diagrams are views, not the product.

The product is a reviewable, traceable, implementation-ready `Calculation Logic Blueprint`, followed by a formal `Implementation Handoff Contract`.

Required transformation:

```text
local evidence library / user references
-> source inventory and authority ranking
-> engineering concept map
-> normalized calculation logic
-> formula / lookup / branch inventory
-> Mermaid views
-> software module mapping
-> verification plan
-> implementation_handoff.yaml
```

## Child Skills to Use

Use these child skills in order:

```text
04-source-intake-and-authority
05-engineering-logic-blueprint
06-formula-lookup-branch-extraction
07-implementation-handoff-contract
```

If `references/acquisition/acquisition_handoff.yaml` does not exist and source sufficiency is doubtful, run:

```text
01-reference-adequacy-and-gap-assessment
02-reference-discovery-and-acquisition
03-reference-persistence-and-local-library
```

before this analysis sequence.

## Required Artifact Flow

```text
references/source_registry.yaml
references/evidence_library_manifest.yaml
analysis/01_source_inventory/
analysis/02_logic_blueprint/
analysis/03_logic_details/
analysis/04_diagrams/
analysis/05_risks_and_questions/
handoff/
```

## Workflow

1. Confirm that sources are available and adequate enough for analysis.
2. Run source intake and authority classification.
3. Build engineering concept map and normalized calculation node inventory.
4. Extract formulas, lookup tables, interpolation rules, branch logic, unit/sign conventions, assumptions, and applicability limits.
5. Generate Mermaid views from the normalized logic, not from raw prose.
6. Map nodes to future software modules, input models, result models, report context, and tests.
7. Create `implementation_handoff.yaml`, `artifact_index.yaml`, and `coding_go_no_go.md`.
8. Stop before production coding unless the user explicitly asks for implementation and the handoff gate allows it.

## Required Final Output

For substantial analysis tasks, provide:

```text
1. Evidence basis and source sufficiency status
2. Source summary and authority ranking
3. Engineering concept map
4. Calculation logic summary
5. Normalized calculation node inventory
6. Formula / method / lookup / branch inventory
7. Mermaid global flowchart
8. Mermaid data flow diagram when useful
9. Mermaid branch logic diagram when useful
10. Mermaid module dependency diagram when useful
11. Input, intermediate, and output inventories
12. Software module mapping
13. Suggested data model groups
14. Validation rules
15. Verification plan
16. Risks, ambiguities, assumptions, and open questions
17. Implementation handoff package
18. Coding gate recommendation
```

## Quality Gate

Before handoff, verify:

```text
source IDs are stable
source authority is explicit
conflicts are recorded
major concepts are identified
major formulas and lookup rules are traced
branch logic is explicit
unit and sign conventions are recorded
inputs and outputs are model-ready
risks are not hidden
open questions are classified by coding impact
handoff status is explicit: no_go, prototype_allowed, or production_allowed
```
