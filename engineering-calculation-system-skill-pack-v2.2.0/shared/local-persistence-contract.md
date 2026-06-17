# Local Persistence Contract

## Purpose

Make retrieved or user-provided sources durable, auditable, and reusable by downstream skills.

## Raw storage rules

Store full raw files only when:

```text
user provided the file
user explicitly authorized saving
the source is openly downloadable with acceptable use
the source is public-domain or permissively licensed
```

Otherwise store a source card and limited notes.

## Required directories

```text
references/raw/
references/source_cards/
references/extracted/
references/acquisition/
references/snapshots/
```

## Required registries

```text
references/source_registry.yaml
references/evidence_library_manifest.yaml
references/acquisition/acquisition_handoff.yaml
```

## Source card required fields

```text
source_id
title
publisher_or_author
source_type
version_or_date
jurisdiction
url_or_location
access_date
raw_file_path
extracted_file_path
authority_level
coverage_tags
relevance_to_calculation
key_clauses_tables_equations_pages
short_excerpts
paraphrased_notes
limitations
license_or_access_notes
recommended_downstream_use
```

## Hashing

Use SHA256 where practical for raw and extracted files. Record hashes in `evidence_library_manifest.yaml`.
