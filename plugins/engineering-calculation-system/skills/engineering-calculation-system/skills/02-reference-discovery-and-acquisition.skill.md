---
name: reference-discovery-and-acquisition
description: Discover, search, screen, and select candidate engineering references to fill gaps identified by the reference adequacy assessment. Use when materials are absent or insufficient and the model should find authoritative codes, manuals, examples, tables, public guidance, or project-relevant references before analysis.
---

# Reference Discovery and Acquisition

Use this skill after `01-reference-adequacy-and-gap-assessment` identifies gaps.

## Goal

Find candidate references that can support a traceable engineering calculation analysis.

Required transformation:

```text
acquisition_plan.yaml
-> search strategy
-> search log
-> candidate source list
-> authority and relevance screening
-> retrieval decisions
-> updated source coverage matrix
```

## Source Priority

Prefer sources in this order unless the user states a different authority hierarchy:

```text
1. project-specific contractual requirements and design basis
2. governing codes, standards, national annexes, client standards
3. official code commentaries or recognized agency design manuals
4. official technical guidance from ministries, agencies, institutes, or standards bodies
5. approved historical calculation books or verified legacy spreadsheets
6. published worked examples from reliable technical sources
7. textbooks, peer-reviewed papers, university notes, manufacturer technical manuals
8. independent hand calculations
9. internal design notes
10. unverified web pages, forums, AI summaries, or unknown sources
```

## Search Strategy

For each gap, define:

```text
search objective
required facts or tables
jurisdiction and language
preferred publisher or authority
essential keywords
alternative keywords
source acceptance criteria
rejection criteria
```

## Web Search Tool Requirement

When an internet search or browser/search tool is available, use it actively for this stage. Do not rely only on model memory, embedded knowledge, or the user's short description when references are absent, incomplete, stale, jurisdiction-specific, or version-sensitive.

For each critical or high-importance gap:

```text
run targeted web searches
try multiple query formulations
prefer official domains, standards bodies, agencies, ministries, publishers, or recognized technical institutions
open and inspect promising primary sources when the tool supports it
cross-check candidate authority, version/year, jurisdiction, and applicability
record every meaningful search in search_log.csv
record selected and rejected candidates in candidate_sources.csv
record retrieval decisions before persistence
```

If the internet search tool is unavailable, explicitly state that limitation, use only local/user-provided materials, and keep the evidence gate at `search_required` or `partial_analysis_allowed` unless the local evidence is already sufficient.

Prefer targeted queries such as:

```text
<engineering object> <check> design manual pdf official
<standard/code name> <clause/table/equation> <topic>
<agency/ministry> <topic> design guide
<calculation type> worked example <code/version>
```

Use iterative search. After finding a candidate source, search again by its title, publisher, clause/table/equation identifiers, version/year, and related official manuals to find better primary sources or worked examples.

## Screening Criteria

For each candidate source, record:

```text
candidate_id
title
publisher / author
source_type
url_or_location
access_date
version_or_date
jurisdiction
relevance_score
authority_level
coverage_tags
gaps_covered
limitations
license_or_access_notes
recommended_action
```

Recommended actions:

```text
persist_raw
persist_source_card_only
use_for_background_only
reject
needs_user_access
needs_purchase_or_license
needs_confirmation
```

## Copyright and Access Rules

Do not bypass paywalls, login requirements, copy protection, subscription systems, or licensing restrictions.

Do not save full copyrighted standards, textbooks, or papers unless the user provides them or explicitly confirms authorization.

For restricted sources, save only:

```text
bibliographic information
source card
short compliant excerpt if needed
clause/table/equation identifiers
summary of relevance
access instructions
```

## Required Output Artifacts

```text
references/acquisition/search_log.csv
references/acquisition/candidate_sources.csv
references/acquisition/retrieval_decisions.csv
references/acquisition/source_coverage_matrix.csv
references/acquisition/acquisition_notes.md
```

## Search Log Columns

```text
search_id,gap_id,query,tool_or_location,date,results_reviewed,candidates_selected,notes
```

## Candidate Source Columns

```text
candidate_id,title,publisher,source_type,version_or_date,jurisdiction,url_or_location,access_date,authority_level,relevance_score,gaps_covered,recommended_action,limitations,license_or_access_notes
```

## Retrieval Decision Columns

```text
decision_id,candidate_id,decision,reason,local_target,raw_allowed,source_card_required,extraction_required,follow_up
```

## Required Final Response

Provide:

```text
searches performed
best sources found
sources rejected and why
which gaps are now covered
which gaps remain
what will be persisted locally
whether analysis can proceed
```
