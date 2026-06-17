# Engineering Calculation System Skill Pack v2.2.0

This package organizes engineering calculation software development into a full delivery lifecycle:

```text
reference acquisition and local persistence
-> reference analysis and calculation logic blueprint
-> implementation, reporting, batch execution, verification, traceability, release, and Linux cloud deployment
```

The implementation stage now includes a unified interface pattern:

```text
polished frontend with left-side inputs and right-side review results
Marimo review pages for module-level inspection and draft edits
managed data/report import and uploadable calculation packages
runnable local web client and Linux-cloud deployable web service
embedded Marimo admin review for declaration-based formula publishing
```

A final web calculation system uses a Python-first stack by default:

```text
primary runtime: Python 3.9+
calculation modules: src/<pkg>/libraries/
official runner: run_book(BookInput) -> BookResult
backend/API: Flask or FastAPI
frontend format: browser web app served from webapp/
default UI files: Jinja2 templates, Bootstrap 5 CSS, vanilla JavaScript modules
review/admin: Marimo when Python-native review is needed
```

The goal is operational quality and convenience, not minimalism for its own sake. The default stack stays simple so projects remain maintainable, but features such as validation, trace review, report preview, import/export, charts, i18n, and Marimo review should be included when they make engineering work safer or faster.

A final web calculation system is not complete when the deliverable is only a static `.html` file, exported report HTML, or UI mockup. Production delivery must include reusable calculation modules, the official runner, backend API/application entrypoint, frontend assets, tests, local run commands, and a Linux/cloud deployment path unless the user explicitly requests a static prototype.

v2.2.0 splits the interface layer into a lightweight router plus three focused subskills:

```text
12  report/review/batch interface router
12a report context and rendering
12b frontend and review interfaces
12c batch, import/export, and upload packages
14  cloud web release and Linux deployment
```

## Why v2.0 exists

The earlier architecture handled two mature stages:

```text
analyze available references
-> create an implementation-ready handoff
-> build reusable engineering calculation book software
```

v2.0 adds the missing upstream layer for cases where the user has no references, incomplete references, or references that are not authoritative enough:

```text
assess reference gaps
-> discover candidate sources
-> actively use available internet search / browser / retrieval tools
-> screen authority and relevance
-> persist a local evidence library
-> hand off to source intake and analysis
```

## Core lifecycle

```text
00 router
01 reference adequacy and gap assessment
02 reference discovery and acquisition
03 reference persistence and local library
04 source intake and authority
05 engineering logic blueprint
06 formula lookup branch extraction
07 implementation handoff contract
08 calculation book architecture
09 core and data models
10 reusable calculation modules
11 book runner and governing summary
12 report review batch interface router
12a report context and rendering
12b frontend and review interfaces
12c batch import/export packages
13 verification regression traceability
14 cloud web release deployment
```

## Parent skills

```text
parent/engineering-calculation-reference-acquisition.skill.md
parent/engineering-calculation-logic-architecture.skill.md
parent/engineering-calculation-book.skill.md
```

## Agent entrypoints

Use `SKILL.md` as the root skill entrypoint for Codex-compatible environments. Qoder-compatible files are included under `.qoder/`. OpenCode and AGENTS.md-compatible entries are included in `AGENTS.md`, `.opencode/`, and `.agents/`. Trae-compatible project rules are included under `.trae/`. For other agents, see:

```text
adapters/agent-entrypoints.md
```

Optional MCP guidance is included in:

```text
adapters/mcp-recommendations.md
```

MCP servers are optional accelerators. Enable only task-scoped MCPs for search/fetch, documentation lookup, public code search, diagnostics, authorized document extraction, or browser testing. Do not make MCPs mandatory for correctness or use them to bypass access controls.

If the target environment cannot coordinate multiple files, load:

```text
engineering-calculation-system.all-in-one.md
```

## Key handoff artifacts

```text
references/acquisition/acquisition_handoff.yaml
references/source_registry.yaml
analysis/02_logic_blueprint/calculation_blueprint.md
handoff/implementation_handoff.yaml
handoff/artifact_index.yaml
handoff/coding_go_no_go.md
implementation/02_modules/module_asset_registry.csv
handoff calculation/backend/frontend/release contracts
deploy/
release/release_checklist.md
```

## Copyright and access rule

Do not bypass paywalls, login walls, licensing restrictions, or access controls. Persist full raw documents only when user-provided, explicitly authorized, or openly downloadable with acceptable use. For copyrighted standards, codes, manuals, papers, and textbooks, prefer source cards, citations, clause identifiers, short compliant excerpts, and paraphrased notes.

## Validation

Validate the package itself:

```bash
python3 scripts/validate_artifacts.py --package-root .
```

Validate the included scaffold:

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
```

Run the scaffold smoke test:

```bash
cd project_template/engineering_calc_project
python3 -m pytest -q
```
