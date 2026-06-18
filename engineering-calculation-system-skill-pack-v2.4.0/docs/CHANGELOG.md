# Changelog

## v2.4.0 multi-agent orchestration - 2026-06-17

### Added - Parallel-Safe Agent Coordination

- Added `shared/multi-agent-orchestration.md` with supervisor duties, parallel-safe work slices, serial gate boundaries, ownership rules, worker result packets, and merge review rules.
- Added orchestration templates for `parallel_work_plan.yaml`, `agent_result_packet.yaml`, and `merge_review.md`.
- Updated the router and parent orchestrators with explicit parallel suitability guidance while keeping lifecycle gates serial.
- Updated Codex, Qoder, OpenCode, Trae, AGENTS-compatible, and single-file entrypoints to reference the shared orchestration contract.
- Updated validation contracts so orchestration files are required package artifacts in the core profile.
- Added a MiniMaxCode publish target that packages the standard root `SKILL.md` skill layout for MiniMax Code import or auto-discovery.

## v2.3.0 release layering - 2026-06-17

### Added - Slim Core and Layered Distribution

- Added `tools/build_release.py` with `core`, `adapters-light`, `qoder-addon`, `singlefile`, and `source-dev` profiles.
- Made `tools/build_release.py` default to a full publish build with separate CODEX, QODER Skill, QODER Project, TRAE, and OpenCode release zips under `dist/release/`.
- Split QODER release output into a direct Skill upload zip with `SKILL.md` at the zip root and a separate QODER project-root overlay zip.
- Added `tools/release_config.json` so version metadata, platform publish targets, single-file contents, and source-dev contents can be maintained without editing build logic.
- Moved the default install target to `dist/core/engineering-calculation-system/`.
- Moved AGENTS/OpenCode/Trae/generic adapter files to the optional `dist/adapters-light/` overlay.
- Moved Qoder-specific files to the optional `dist/qoder-addon/` overlay.
- Moved the all-in-one skill file to generated output at `dist/singlefile/engineering-calculation-system.all-in-one.md`.
- Updated validation to support `--profile core`, reject runtime cache artifacts, and keep generated indexes out of the core skill folder.
- Removed tracked `.pyc` cache files from the project scaffold and added `.gitignore` rules for generated release outputs.

## Agent adapter hardening - 2026-06-17

### Added - Cross-Agent Entrypoints and MCP Guidance

- Added root `AGENTS.md` for OpenCode and AGENTS.md-compatible coding agents.
- Added `.opencode/skills/engineering-calc-system/SKILL.md` as an OpenCode project skill wrapper.
- Added `.agents/skills/engineering-calc-system/SKILL.md` as a portable generic skill wrapper.
- Added `.trae/project_rules.md` and updated `.trae/rules/engineering-calc-system.md` for Trae-compatible project rules.
- Expanded `adapters/agent-entrypoints.md` with Codex, Qoder, OpenCode, Trae, generic rules agents, and single-file fallback guidance.
- Added `adapters/mcp-recommendations.md` to document optional MCP presets inspired by curated agent stacks such as oh-my-openagent without making MCP servers mandatory dependencies.

## v2.2.0 deployment hardening - 2026-06-16

### Added - Cloud Web Release, Deployment, and Module Assets

- Added `14-cloud-web-release-deployment.skill.md` for final local web client packaging and Linux cloud deployment.
- Added deployment templates for cloud Linux runtime planning, release checklists, and runtime environment variables.
- Added project scaffold deployment files for Docker, docker-compose, systemd, nginx, environment configuration, and release checklist.
- Added `webapp/app.py` application factory with `/health` endpoint for local and gunicorn runtime.
- Added `module_asset_registry.csv` to make decoupled calculation modules reusable and auditable assets.
- Strengthened quality gates so final web systems must be runnable, traceable, reviewable, modifiable, and deployable.

## v2.2.0 — 2026-06-16

### Added — Interface Skill Split and Frontend Implementation Layer

- **Skill 12 split** into a lightweight interface router plus three focused subskills:
  - `12a-report-context-and-rendering.skill.md`
  - `12b-frontend-and-review-interfaces.skill.md`
  - `12c-batch-import-export-packages.skill.md`
- **Frontend implementation guidance added** for Form↔Model Mapping, API Route Architecture, Frontend JS Architecture, i18n System, NaN/Infinity Sanitization, Chart Integration, Config & Error Handling patterns, and extended Required Output Artifacts.
- **4 new implementation templates**:
  - `form_mapping_spec.md` — bidirectional form↔BookInput mapping contract
  - `i18n_pattern.md` — `data-i18n` + API endpoint internationalization strategy
  - `chart_integration.md` — bilingual matplotlib SVG chart generation pattern
  - `api_route_skeleton.md` — Flask/FastAPI thin-route API architecture
- **12 new webapp skeleton files** under `project_template/engineering_calc_project/webapp/`:
  - `config.py` — application configuration with DEFAULTS dict
  - `routes.py` — Flask Blueprint API routes (calculate, report, import/export, i18n)
  - `form_utils.py` — form↔BookInput bidirectional mapping + NaN sanitization + result→UI
  - `i18n.py` — bilingual translation dictionary with `get_translations()` / `t()` helpers
  - `static/js/main.js` — core orchestration (calculate, report preview, import/export)
  - `static/js/results.js` — result rendering, status badges, utilization bars
  - `static/js/forms.js` — form data collection, population, reset-to-defaults
  - `static/js/i18n.js` — language switching, bilingual chart CSS toggle
  - `templates/base.html` — Bootstrap 5 + KaTeX layout skeleton with report modal
  - `templates/index.html` — left input panel (col-lg-4) + right result panel (col-lg-8)
  - `static/css/style.css` — unified layout styles (navbar, scroll panel, status colors)
- **New core utility**: `src/pkg/core/sanitize.py` — standalone `sanitize_for_json()` for recursive NaN/Infinity cleaning

### Changed

- Updated `ui_layout_spec.md` with Frontend Stack Decision table and Related Templates cross-references.
- Updated `frontend_fields.csv` with example data rows demonstrating field_path/label/unit/group/editable/source columns.

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
