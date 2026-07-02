---
name: reference-persistence-and-local-library
description: Persist acquired engineering references, source cards, metadata, search logs, extracted notes, coverage matrices, and acquisition handoff files into a local evidence library. Use after reference discovery or whenever found資料 must be made durable and traceable for downstream analysis.
---

# Reference Persistence and Local Library

## When to use

After candidate sources are selected (skill 02), or when the user asks to save found references
locally. Convert ephemeral search results and user-provided files into a stable, traceable local
evidence library.

## Inputs

`candidate_sources.csv`, `retrieval_decisions.csv`, and acquired files from skill 02.

## Steps

1. Assign stable source IDs (`shared/id-convention.md`: S01, S02, CODE-01, MANUAL-01, EXAMPLE-01,
   EXCEL-01, REPORT-01). Do not change IDs once downstream analysis has started.
2. Persist raw files to `references/raw/S01_<short_source_name>.<ext>` only when allowed
   (`shared/copyright-and-access-policy.md`: user-uploaded, user-authorized, openly downloadable
   with acceptable use, or public-domain/permissively licensed). Otherwise create a source card.
3. Create a source card per source in `references/source_cards/` using
   `templates/acquisition/source_card_template.md` (every source gets a card, even when raw is
   saved). Extract text/tables/workbook logic to `references/extracted/` where appropriate,
   recording extraction date, tool, page/sheet ranges, OCR/uncertainty risks, and avoiding long
   copyrighted passages. For spreadsheets record workbook/sheet names, named ranges,
   visible/hidden sheets, formula map, input/output/intermediate cells, external links/macros.
4. Compute SHA256 for each raw/extracted file and record in
   `references/evidence_library_manifest.yaml` (path, sha256, created_at, source_id, file_role,
   notes).
5. Register all sources in `references/source_registry.yaml`.
6. Write `references/acquisition/acquisition_handoff.yaml` (project_or_calculation_name,
   acquisition_status, source_ids, coverage_summary, remaining_gaps, recommended_analysis_path,
   sources_to_use_as_governing, sources_to_use_as_examples, sources_to_use_as_background,
   copyright_or_access_limitations).

## Directory contract

```text
references/
  acquisition/   gap_assessment.md, acquisition_plan.yaml, search_log.csv,
                 candidate_sources.csv, retrieval_decisions.csv, source_coverage_matrix.csv,
                 acquisition_notes.md, acquisition_handoff.yaml
  raw/           S01_<name>.pdf, S02_<name>.xlsx
  extracted/     S01_text.md, S01_tables/, notes/S01_source_notes.md
  source_cards/  S01_source_card.md, S02_source_card.md
  snapshots/     README.md
  source_registry.yaml
  evidence_library_manifest.yaml
```

## Artifacts

```text
references/raw/...
references/extracted/...
references/source_cards/...
references/source_registry.yaml
references/evidence_library_manifest.yaml
references/acquisition/acquisition_handoff.yaml
```

## Exit gate

Evidence gate is `analysis_allowed` or an explicit blocker is recorded. See
`shared/lifecycle.md` row 03. Next path: 04 for source intake & authority, or back to 02 if gaps
remain.
