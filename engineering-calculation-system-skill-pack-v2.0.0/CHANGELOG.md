# Changelog

## v2.1.1 — 2026-06-16

### Added

- Added a domain-neutral report production decision protocol for report, review, export, and batch interfaces.
- Added report status, production eligibility, traceability, and template-boundary requirements to the report context template.
- Added package validation checks for the required report production protocol sections.
- Added a unified frontend layout contract based on a top bar, left input panel, right review workbench, modal/drawer reviews, and status strip.
- Added Marimo review app guidance for module-level review, editable draft inputs, formula/source traces, review logs, and `marimo edit` / `marimo run` workflows.
- Added import/export and upload package contracts for staged data, imported reports, normalized inputs, trusted results, manifests, hashes, and package exports.
- Added project scaffold directories for `webapp/`, `apps/review/`, managed `data/`, and `outputs/upload_packages/`.

### Changed

- Strengthened reference discovery instructions to require active internet search/browser/retrieval tool use when available.
- Required search attempts, accepted candidates, rejected candidates, and retrieval decisions to be logged before analysis proceeds.
- Added explicit fallback behavior when internet search tools are unavailable or blocked.
- Strengthened report/review interface gates so UI, Marimo pages, batch summaries, and upload packages remain traceable thin layers over trusted calculations.

## v2.1.0 — 2026-06-16

### Added

- Root `SKILL.md` entrypoint for Codex-compatible discovery.
- `agents/openai.yaml` UI metadata.
- Cross-agent adapter notes for Codex, Qoder, Trae, opencode, and generic agents.
- Artifact contract schema in `schemas/artifact_contracts.json`.
- Standard-library validator in `scripts/validate_artifacts.py`.
- Missing templates for declared acquisition, analysis, handoff, implementation, and runner artifacts.
- `pyproject.toml`, package `__init__.py` files, and test path configuration for the project scaffold.

### Changed

- Separated evidence gate statuses from coding gate statuses.
- Aligned `calculation_nodes.csv` with the normalized node model fields.
- Expanded `implementation_handoff.yaml` with formula, lookup, branch, and traceability reference fields.
- Lowered scaffold Python compatibility target to Python 3.9+.

### Verified

- `python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project`
- `python3 -m pytest -q` inside `project_template/engineering_calc_project`

## v2.0.0 — 2026-06-16

### Added

- New upstream reference acquisition phase.
- New parent orchestrator: `engineering-calculation-reference-acquisition`.
- New child skills:
  - `01-reference-adequacy-and-gap-assessment`
  - `02-reference-discovery-and-acquisition`
  - `03-reference-persistence-and-local-library`
- New local evidence library contract.
- New acquisition handoff contract connecting source discovery to source intake.
- New templates for search logs, candidate sources, source coverage matrix, source cards, retrieval decisions, and evidence library manifest.
- New quality gates for `evidence_no_go`, `search_required`, `partial_analysis_allowed`, `analysis_allowed`, `prototype_allowed`, and `production_allowed`.

### Changed

- Renumbered downstream analysis and implementation skills to make room for the upstream layer.
- Updated router to detect no-material and insufficient-material cases.
- Updated logic architecture parent to require an evidence gate before analysis.
- Updated calculation book parent to route upstream when a handoff lacks source evidence.

### Preserved

- Calculation Logic Blueprint remains the central analysis artifact.
- Implementation Handoff Contract remains the analysis-to-coding interface.
- `run_book(BookInput) -> BookResult` remains the official calculation entry point.
- Engineering formulas remain forbidden in UI, report templates, batch scripts, and CSV/Excel inputs.
