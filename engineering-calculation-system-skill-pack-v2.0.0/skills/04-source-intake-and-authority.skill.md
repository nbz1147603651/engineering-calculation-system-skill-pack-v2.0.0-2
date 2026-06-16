---
name: source-intake-and-authority
description: Intake engineering source materials or a local evidence library, assign stable source IDs, classify authority, record source conflicts, and prepare source inventory for calculation logic analysis. Use after reference persistence or when user-provided materials are already available.
---

# Source Intake and Authority

Use this skill as the first analysis-stage skill after evidence acquisition or direct user upload.

## Goal

Turn references into a reliable source inventory that downstream logic extraction can cite.

## Inputs

Prefer reading these artifacts if available:

```text
references/source_registry.yaml
references/evidence_library_manifest.yaml
references/acquisition/acquisition_handoff.yaml
references/raw/
references/extracted/
references/source_cards/
```

If no local evidence library exists, use uploaded materials directly and create equivalent source inventory artifacts.

## Source Inventory Contract

Assign or verify stable source IDs:

```text
S01, S02, S03
CODE-01
MANUAL-01
EXCEL-01
REPORT-01
NOTE-01
```

For each source, record:

```text
source_id
source_name
source_type
version_or_date
jurisdiction_or_project
role_in_analysis
priority
authority_level
reliability_notes
scope_of_applicability
known_limitations
local_path_or_source_card
```

## Authority Hierarchy

Default priority order:

```text
1. project-specific contractual requirement
2. governing design code or standard
3. official code commentary or nationally recognized design manual
4. project-approved calculation basis
5. published worked example from reliable source
6. verified historical calculation report
7. legacy spreadsheet
8. internal design note
9. engineering assumption
10. unknown source or unverified material
```

If the user specifies a different order, follow it.

## Conflict Inventory

When sources conflict, record:

```text
conflict_id
affected formula, coefficient, branch, or assumption
source A method
source B method
engineering consequence
recommended resolution
whether it blocks analysis or coding
```

## Required Output Artifacts

```text
analysis/01_source_inventory/source_inventory.yaml
analysis/01_source_inventory/source_authority_table.csv
analysis/01_source_inventory/source_conflicts.csv
analysis/01_source_inventory/source_intake_notes.md
```

## Quality Gate

Before passing to logic blueprint, verify:

```text
sources are identified
source IDs are stable
version/year and jurisdiction are captured where available
authority ranking is explicit
project-specific sources are distinguished from generic sources
source cards or local paths are available
conflicts and gaps are visible
```

## Required Final Response

Provide:

```text
source inventory summary
authority ranking
conflicts found
gaps remaining
whether logic blueprint can proceed
```
