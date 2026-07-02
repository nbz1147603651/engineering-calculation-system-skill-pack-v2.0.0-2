---
name: reference-discovery-and-acquisition
description: Discover, search, screen, and select candidate engineering references to fill gaps identified by the reference adequacy assessment. Use when materials are absent or insufficient and the model should find authoritative codes, manuals, examples, tables, public guidance, or project-relevant references before analysis.
---

# Reference Discovery and Acquisition

## When to use

After skill 01 identifies gaps. Find candidate references that can support a traceable engineering
calculation analysis.

## Inputs

`references/acquisition/acquisition_plan.yaml` and `source_coverage_matrix.csv` from skill 01.

## Steps

1. Build a search strategy per gap: search objective, required facts/tables, jurisdiction &
   language, preferred publisher/authority, essential + alternative keywords, source acceptance
   criteria, rejection criteria.
2. Run web/file search. When an internet search or browser tool is available, use it actively for
   each critical/high-importance gap — multiple query formulations, prefer official domains /
   standards bodies / agencies / publishers, open and inspect promising primary sources, cross-check
   authority/version/year/jurisdiction/applicability. If no search tool is available, state that
   limitation explicitly and keep the evidence gate at `search_required` or
   `partial_analysis_allowed` unless local evidence is already sufficient.
3. Log every meaningful search in `templates/acquisition/search_log.csv` (columns:
   search_id,gap_id,query,tool_or_location,date,results_reviewed,candidates_selected,notes).
   Useful query shapes: `<object> <check> design manual pdf official`; `<standard> <clause/table>
   <topic>`; `<agency> <topic> design guide`; `<calc type> worked example <code/version>`. Iterate:
   after a candidate is found, search again by its title/publisher/clause identifiers/version to
   find better primary sources or worked examples.
4. Screen each candidate and record it in `templates/acquisition/candidate_sources.csv` (columns:
   candidate_id,title,publisher,source_type,version_or_date,jurisdiction,url_or_location,
   access_date,authority_level,relevance_score,gaps_covered,recommended_action,limitations,
   license_or_access_notes). Recommended actions: persist_raw | persist_source_card_only |
   use_for_background_only | reject | needs_user_access | needs_purchase_or_license |
   needs_confirmation.
5. Rank by authority hierarchy (canonical list lives in skill 04; reuse it, do not redefine).
6. Record retrieval decisions in `templates/acquisition/retrieval_decisions.csv` (columns:
   decision_id,candidate_id,decision,reason,local_target,raw_allowed,source_card_required,
   extraction_required,follow_up) before any persistence.
7. Update `source_coverage_matrix.csv` with newly covered gaps.

## Copyright & access

Follow `shared/copyright-and-access-policy.md`. Do not bypass paywalls/login/copy-protection/
subscriptions/licensing. Save full copyrighted standards/textbooks/papers only when the user
provides or explicitly authorizes them; otherwise store bibliographic metadata + source card +
short compliant excerpts + clause/table/equation identifiers + access instructions only.

## Artifacts

```text
references/acquisition/search_log.csv             (templates/acquisition/search_log.csv)
references/acquisition/candidate_sources.csv      (templates/acquisition/candidate_sources.csv)
references/acquisition/retrieval_decisions.csv    (templates/acquisition/retrieval_decisions.csv)
references/acquisition/source_coverage_matrix.csv (updated)
references/acquisition/acquisition_notes.md       (templates/acquisition/acquisition_notes.md)
```

## Exit gate

Critical gaps have source candidates or recorded blockers. See `shared/lifecycle.md` row 02. Next
path: 03 to persist the selected sources.
