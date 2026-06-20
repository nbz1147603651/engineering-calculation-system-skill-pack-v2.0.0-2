---
name: source-intake-and-authority
description: Intake engineering source materials or a local evidence library, assign stable source IDs, classify authority, record source conflicts, and prepare source inventory for calculation logic analysis. Use after reference persistence or when user-provided materials are already available.
---

# Source Intake and Authority

## When to use

First analysis-stage skill, after evidence acquisition or direct user upload. Turn references into
a reliable source inventory that downstream logic extraction can cite.

## Inputs

Prefer reading `references/source_registry.yaml`, `evidence_library_manifest.yaml`,
`acquisition/acquisition_handoff.yaml`, `references/raw/`, `references/extracted/`,
`references/source_cards/`. If no local evidence library exists, use uploaded materials directly
and create equivalent inventory artifacts.

## Steps

1. Assign or verify stable source IDs (`shared/id-convention.md`).
2. For each source, record in `source_inventory.yaml`: source_id, source_name, source_type,
   version_or_date, jurisdiction_or_project, role_in_analysis, priority, authority_level,
   reliability_notes, scope_of_applicability, known_limitations, local_path_or_source_card.
3. Rank by authority hierarchy (canonical — referenced by skills 02 etc., not redefined there):
   1 project-specific contractual requirement; 2 governing design code/standard; 3 official code
   commentary or nationally recognized design manual; 4 project-approved calculation basis;
   5 published worked example from reliable source; 6 verified historical calculation report;
   7 legacy spreadsheet; 8 internal design note; 9 engineering assumption; 10 unknown/unverified.
   Follow a user-specified order if given.
4. Record conflicts in `source_conflicts.csv`: conflict_id, affected formula/coefficient/branch/
   assumption, source A method, source B method, engineering consequence, recommended resolution,
   whether it blocks analysis or coding.
5. Write intake notes in `templates/analysis/source_intake_notes.md`.

## Artifacts

```text
analysis/01_source_inventory/source_inventory.yaml
analysis/01_source_inventory/source_authority_table.csv
analysis/01_source_inventory/source_conflicts.csv
analysis/01_source_inventory/source_intake_notes.md   (templates/analysis/source_intake_notes.md)
```

## Exit gate

Sources are trusted or conflicts block work; authority ranking is explicit; source IDs are stable.
See `shared/lifecycle.md` row 04. Next path: 05 for the logic blueprint.
