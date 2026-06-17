# Source Acquisition Contract

## Purpose

Standardize how missing engineering references are searched, screened, and prepared for downstream analysis.

## Minimum acquisition outputs

```text
reference_gap_assessment.md
acquisition_plan.yaml
search_log.csv
candidate_sources.csv
retrieval_decisions.csv
source_coverage_matrix.csv
source_registry.yaml
evidence_library_manifest.yaml
acquisition_handoff.yaml
```

## Source decision statuses

```text
persist_raw
persist_source_card_only
use_for_background_only
reject
needs_user_access
needs_purchase_or_license
needs_confirmation
```

## Search log requirement

Every meaningful search attempt should be logged with:

```text
search_id
gap_id
query
tool_or_location
date
results_reviewed
candidates_selected
notes
```

## Internet search tool requirement

When an agent has access to internet search, browser, or retrieval tools, reference discovery must use them for missing, incomplete, stale, or jurisdiction-specific source bases.

Minimum behavior:

```text
search each critical/high gap with multiple targeted queries
prefer primary and official sources over summaries
inspect promising results when opening pages/files is possible
cross-check version/year, jurisdiction, publisher, and applicability
log the tool used in tool_or_location
record both accepted and rejected candidates
state explicitly when search tools are unavailable or blocked
```

## Candidate source requirement

Each candidate source must have:

```text
candidate_id
title
publisher
source_type
version_or_date
jurisdiction
url_or_location
access_date
authority_level
relevance_score
gaps_covered
recommended_action
limitations
license_or_access_notes
```
