---
name: reference-persistence-and-local-library
description: Persist acquired engineering references, source cards, metadata, search logs, extracted notes, coverage matrices, and acquisition handoff files into a local evidence library. Use after reference discovery or whenever found資料 must be made durable and traceable for downstream analysis.
---

# Reference Persistence and Local Library

Use this skill after candidate sources have been selected or when the user asks to save found references locally.

## Goal

Convert ephemeral search results and user-provided files into a stable local evidence library.

Required transformation:

```text
candidate_sources.csv + retrieval_decisions.csv + acquired files
-> stable source IDs
-> raw files where allowed
-> source cards where raw persistence is not allowed
-> extracted notes / text where appropriate
-> source_registry.yaml
-> evidence_library_manifest.yaml
-> acquisition_handoff.yaml
```

## Directory Contract

Use this structure:

```text
references/
  acquisition/
    reference_gap_assessment.md
    acquisition_plan.yaml
    search_log.csv
    candidate_sources.csv
    retrieval_decisions.csv
    source_coverage_matrix.csv
    acquisition_notes.md
    acquisition_handoff.yaml
  raw/
    S01_<short_source_name>.pdf
    S02_<short_source_name>.xlsx
  extracted/
    S01_text.md
    S01_tables/
    S02_workbook_formula_map.md
    notes/
      S01_source_notes.md
  source_cards/
    S01_source_card.md
    S02_source_card.md
  snapshots/
    README.md
  source_registry.yaml
  evidence_library_manifest.yaml
```

## Stable Source IDs

Assign source IDs such as:

```text
S01, S02, S03
CODE-01
MANUAL-01
EXAMPLE-01
EXCEL-01
REPORT-01
```

Do not change existing IDs once downstream analysis has started.

## Raw Persistence Rules

Save raw files only when:

```text
the user uploaded the file
the user explicitly authorized saving it
it is openly downloadable and permitted for local use
it is public-domain or permissively licensed
```

If raw saving is not allowed or uncertain, create a source card instead.

## Source Card Contract

Every source should have a source card, even when raw is saved.

Each source card should include:

```text
source_id
title
publisher / author
source_type
version_or_date
jurisdiction
url_or_location
access_date
raw_file_path if any
extracted_file_path if any
authority_level
coverage_tags
relevance_to_calculation
key clauses / tables / equations / pages
short compliant excerpts if necessary
paraphrased notes
limitations
license_or_access_notes
recommended downstream use
```

## Extraction Rules

When extracting text, tables, or workbook logic:

```text
record extraction date
record extraction tool or method if relevant
record page/sheet/range references
record uncertainty and OCR risks
preserve table identifiers
avoid long copyrighted passages
prefer structured summaries and identifiers
```

For spreadsheets, record:

```text
workbook name
sheet names
named ranges
visible/hidden sheets
formula map if available
input cells
output cells
important intermediate cells
external links/macros if present
```

## Hash and Manifest

For every local raw or extracted file, record where practical:

```text
path
sha256
created_at
source_id
file_role
notes
```

## Acquisition Handoff

Create:

```text
references/acquisition/acquisition_handoff.yaml
```

It should include:

```text
project_or_calculation_name
acquisition_status
source_ids
coverage_summary
remaining_gaps
recommended_analysis_path
sources_to_use_as_governing
sources_to_use_as_examples
sources_to_use_as_background
copyright_or_access_limitations
```

## Required Final Response

Provide:

```text
local evidence library summary
files persisted
source cards created
coverage status
remaining gaps
next skill path: 04-source-intake-and-authority or back to 02-reference-discovery-and-acquisition
```
