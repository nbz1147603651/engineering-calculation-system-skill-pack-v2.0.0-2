# Migration Notes from v1.0 to v2.0.0

## v2.2.0 to v2.3.0 release layering

The default install target is no longer the source checkout root. Build release profiles first:

```bash
python tools/build_release.py
```

The no-argument build creates every release profile plus five publish-ready platform zips in `dist/release/`:

```text
dist/release/engineering-calculation-system-CODEX-v2.3.0.zip
dist/release/engineering-calculation-system-QODER-v2.3.0.zip
dist/release/engineering-calculation-system-QODER-Project-v2.3.0.zip
dist/release/engineering-calculation-system-TRAE-v2.3.0.zip
dist/release/engineering-calculation-system-OpenCode-v2.3.0.zip
```

Use `engineering-calculation-system-QODER-v2.3.0.zip` for direct QODER Skill upload; it places `SKILL.md` at the zip root. CODEX contains `engineering-calculation-system/`; QODER Project, TRAE, and OpenCode contain `copy-to-project-root/` for project-root installation.

Release metadata and classified install targets now live in:

```text
tools/release_config.json
```

Use that file as the first edit point for future version bumps or target-agent additions.

Install the core runtime skill from:

```text
dist/core/engineering-calculation-system/
```

Use optional overlays only when needed:

```text
dist/adapters-light/
dist/qoder-addon/
dist/singlefile/engineering-calculation-system.all-in-one.md
```

Recommended validation:

```bash
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core --project dist/core/engineering-calculation-system/project_template/engineering_calc_project
```

## v2.0.0 to v2.1.0 hardening

No lifecycle renumbering is required. Existing v2.0 artifacts remain valid.

Recommended additions:

```text
SKILL.md
agents/openai.yaml
adapters/agent-entrypoints.md
schemas/artifact_contracts.json
scripts/validate_artifacts.py
tools/build_release.py
```

Recommended validation:

```bash
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core --project dist/core/engineering-calculation-system/project_template/engineering_calc_project
```

Gate terminology is now separated:

```text
Evidence gate: evidence_no_go | search_required | partial_analysis_allowed | analysis_allowed
Coding gate: no_go | prototype_allowed | production_allowed
```

If an existing v2.0 `implementation_handoff.yaml` lacks these keys, add them before production coding:

```text
formula_inventory_refs
lookup_inventory_refs
branch_inventory_refs
traceability_requirements
```

## Numbering change

```text
v1.0 01-source-intake-and-authority              -> v2.0 04-source-intake-and-authority
v1.0 02-engineering-logic-blueprint              -> v2.0 05-engineering-logic-blueprint
v1.0 03-formula-lookup-branch-extraction         -> v2.0 06-formula-lookup-branch-extraction
v1.0 04-implementation-handoff-contract          -> v2.0 07-implementation-handoff-contract
v1.0 05-calculation-book-architecture            -> v2.0 08-calculation-book-architecture
v1.0 06-core-and-data-models                     -> v2.0 09-core-and-data-models
v1.0 07-reusable-calculation-modules             -> v2.0 10-reusable-calculation-modules
v1.0 08-book-runner-and-governing-summary        -> v2.0 11-book-runner-and-governing-summary
v1.0 09-report-review-batch-interfaces           -> v2.0 12-report-review-batch-interfaces
v1.0 10-verification-regression-traceability     -> v2.0 13-verification-regression-traceability
```

## New upstream artifacts

Add these before analysis when references are missing or insufficient:

```text
references/acquisition/reference_gap_assessment.md
references/acquisition/acquisition_plan.yaml
references/acquisition/search_log.csv
references/acquisition/candidate_sources.csv
references/acquisition/source_coverage_matrix.csv
references/acquisition/retrieval_decisions.csv
references/source_registry.yaml
references/evidence_library_manifest.yaml
references/acquisition/acquisition_handoff.yaml
```

## Compatibility

Existing v1.0 analysis and implementation workflows remain valid when the user already provides enough reliable reference material. The new upstream phase is activated only when materials are absent, incomplete, stale, contradictory, or insufficiently authoritative.
