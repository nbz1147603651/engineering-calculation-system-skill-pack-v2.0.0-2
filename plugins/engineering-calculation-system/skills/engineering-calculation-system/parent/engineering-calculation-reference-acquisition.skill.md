---
name: engineering-calculation-reference-acquisition
description: Parent/orchestrator skill for finding, screening, acquiring, and locally persisting engineering references before analysis. Use when the user has no materials, insufficient materials, stale or conflicting materials, unclear code basis, or asks the model to find references for an engineering calculation workflow before building a Calculation Logic Blueprint or software implementation.
---

# Engineering Calculation Reference Acquisition — Parent Orchestrator

Use this parent skill before reference analysis when source materials are missing, incomplete, stale, contradictory, or not authoritative enough.

This skill does not extract all formulas and does not implement code. It creates a local evidence library that downstream analysis can trust and cite.

## Core Principle

Do not invent engineering calculation rules when references are missing.

When web search or browser/search tools are available, the acquisition phase must use them. Missing, incomplete, stale, or jurisdiction-specific references require active internet search, source opening/inspection where possible, authority screening, and logged search evidence before analysis proceeds.

Required transformation:

```text
user intent / sparse description
-> reference adequacy assessment
-> gap list and acquisition plan
-> source discovery and authority screening
-> local persistence of allowed materials and source cards
-> acquisition_handoff.yaml
-> downstream source intake and analysis
```

## Parallelization Guidance

When the user explicitly requests multi-agent or parallel work, read
`shared/multi-agent-orchestration.md` and create
`templates/orchestration/parallel_work_plan.yaml`.

Safe parallel slices:

```text
separate source gaps
separate jurisdictions or code families
separate official pages, manuals, examples, and errata searches
separate source card drafts or extraction notes
```

Supervisor-only work:

```text
source ID assignment
access and copyright decisions
authority ranking
coverage matrix merge
evidence gate status
acquisition_handoff.yaml finalization
```

## Child Skills to Use

Use these child skills in order:

```text
01-reference-adequacy-and-gap-assessment
02-reference-discovery-and-acquisition
03-reference-persistence-and-local-library
```

## When to Use

Use when:

```text
no reference materials are provided
only a short user description is provided
uploaded materials omit code basis, equations, tables, examples, or units
provided materials conflict or are obsolete
source authority is unclear
user asks to find design codes, manuals, examples, or calculation references
implementation request arrives without a valid source basis or handoff
```

## Required Artifact Flow

```text
references/acquisition/reference_gap_assessment.md
references/acquisition/acquisition_plan.yaml
references/acquisition/search_log.csv
references/acquisition/candidate_sources.csv
references/acquisition/source_coverage_matrix.csv
references/acquisition/retrieval_decisions.csv
references/raw/
references/source_cards/
references/extracted/
references/source_registry.yaml
references/evidence_library_manifest.yaml
references/acquisition/acquisition_handoff.yaml
```

## Copyright and Access Rules

Never bypass paywalls, login walls, subscription systems, robots restrictions, or license controls.

Persist raw full documents only when they are:

```text
user-provided
explicitly authorized by the user
openly downloadable from an official or public source with acceptable use
public-domain or clearly permissively licensed
```

For copyrighted standards, codes, manuals, papers, or textbooks, prefer:

```text
source cards
bibliographic metadata
clause/table/equation identifiers
short compliant excerpts
paraphrased notes
page references
links or access instructions
```

Do not store long copyrighted passages simply to make downstream work easier.

## Quality Gate

Before handing off to analysis, verify:

```text
minimum source basis is identified
source coverage is mapped to calculation needs
source IDs are stable
search attempts are logged
candidate sources are ranked
retrieval decisions are recorded
local file paths or source cards exist
uncovered gaps remain explicit
evidence gate is stated: evidence_no_go, search_required, partial_analysis_allowed, or analysis_allowed
```

## Required Final Output

Provide:

```text
reference adequacy summary
gaps found
sources searched
candidate sources selected or rejected
local persistence summary
coverage matrix summary
remaining missing evidence
recommended next skill path
acquisition_handoff.yaml summary
```
