# Engineering Calculation System Skill Pack v2.4.3

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

v2.4 adds optional multi-agent orchestration for platforms that support
subagents, custom agents, or parallel work. The supervisor keeps routing,
source authority, ID allocation, handoff freeze, `run_book()` public contracts,
and final gate decisions serial while workers handle bounded, disjoint slices.
Use `shared/multi-agent-orchestration.md` and `templates/orchestration/` only
when parallel work is explicitly requested.

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

All entrypoints share `shared/lifecycle.md` as the single source of truth.
Before implementation, declare one delivery mode: `core-only`, `report-only`,
`prototype-web`, or `web-complete`. Default to `web-complete`; its default path
is `08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14`.

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

## Release Layout

Build release profiles from the source checkout:

```bash
python tools/build_release.py
```

Running the command with no arguments builds every release profile and creates ten publish-ready platform zips in `dist/release/`. Use `--profile <name>` when you only need one layer during development.

Default installation target:

```text
dist/core/engineering-calculation-system/
```

Optional overlays:

```text
dist/adapters-light/   AGENTS.md, .agents, .opencode, .trae, and adapter guidance
dist/qoder-addon/      Qoder/Qoder CN-specific files
dist/singlefile/       generated all-in-one fallback
dist/source-dev/       development/reference source bundle
dist/release/          CODEX, MiniMaxCode, ZCode, QODER Skill, QODER project, QoderCN, QoderCN project, TRAE, OpenCode, and AGENTS Generic release zips
```

For publishing or manual installation, use the package for the target tool:

```text
dist/release/engineering-calculation-system-CODEX-v2.4.3.zip
dist/release/engineering-calculation-system-MiniMaxCode-v2.4.3.zip
dist/release/engineering-calculation-system-ZCode-v2.4.3.zip
dist/release/engineering-calculation-system-QODER-v2.4.3.zip
dist/release/engineering-calculation-system-QODER-Project-v2.4.3.zip
dist/release/engineering-calculation-system-QoderCN-v2.4.3.zip
dist/release/engineering-calculation-system-QoderCN-Project-v2.4.3.zip
dist/release/engineering-calculation-system-TRAE-v2.4.3.zip
dist/release/engineering-calculation-system-OpenCode-v2.4.3.zip
dist/release/engineering-calculation-system-AGENTS-Generic-v2.4.3.zip
```

Each package contains one install folder plus `INSTALL.md`, except MiniMaxCode which is packaged as a MiniMax skills repository root:

```text
CODEX:         engineering-calculation-system/
MiniMaxCode:   skills/engineering-calculation-system/ for Github import, or copy that folder to %USERPROFILE%/.mavis/skills/engineering-calculation-system/ for local install
ZCode:         engineering-calculation-system/ for ~/.zcode/skills/engineering-calculation-system/ and $engineering-calculation-system invocation
QODER:         SKILL.md at zip root for direct QODER Skill upload (lightweight skill/resource entrypoint)
QODER Project: copy-to-project-root/ with Qoder Smart Agent supervisor and skill/resource layer
QoderCN:       copy-to-user-home/ with user-level ~/.lingma agents, skills, and references
QoderCN Project: copy-to-project-root/ with project-level .lingma supervisor and skill/resource layer
TRAE:          copy-to-project-root/
OpenCode:      copy-to-project-root/
AGENTS Generic: copy-to-project-root/
```

The MiniMaxCode package follows MiniMax's skills repository layout with `skills/engineering-calculation-system/SKILL.md`. For this machine, the local MiniMax Code / Mavis user skill root is `%USERPROFILE%/.mavis/skills/`; for sharing, the same archive can be published as a Github repository root and imported through MiniMax Code. The ZCode package follows ZCode's user skill directory shape: copy `engineering-calculation-system/` to `%USERPROFILE%/.zcode/skills/engineering-calculation-system/`, refresh Settings -> Skills, keep the skill enabled, and invoke it with `$engineering-calculation-system`. Put persistent ZCode project guardrails in the workspace `AGENTS.md`. The QODER package is for direct QODER Skill upload and is intentionally lightweight. For Qoder Smart Agent workflows and QODER web-complete generation, prefer QODER Project because it includes the custom agent supervisor, delegated worker agents, skill/resource layer, core runtime files, templates, schemas, validator, project scaffold, and `.qoder/` overlay. Qoder CN uses the same Qoder supervisor/worker skill resources, remapped to user-level `~/.lingma` or project-root `.lingma/` for Qoder CN IDE custom Skills and Agents. The QODER Project, QoderCN Project, TRAE, OpenCode, and AGENTS Generic packages are already merged with the core runtime files, so users can copy the matching package contents directly. Use the raw core and overlay profiles only when debugging or repackaging.

Release metadata and classified install targets are maintained in:

```text
tools/release_config.json
```

Change that file when updating the version, release date, publish targets, single-file contents, source-dev contents, or target-agent folders.

## Agent entrypoints

Use `dist/core/engineering-calculation-system/SKILL.md` as the root skill entrypoint for Codex-compatible, MiniMax Code standard-skill, and ZCode user-skill environments. Qoder-compatible files are distributed through `dist/qoder-addon/`. In Qoder, `.qoder/agents/engineering-calc-system.md` is the Smart Agent supervisor, `.qoder/agents/engineering-calc-*.md` are delegated worker agents, `.qoder/skills/engineering-calc-system/` is the skill/resource layer, and `.qoder/references/` holds long non-agent references. In Qoder CN IDE packages, the same resources are placed under `~/.lingma/agents|skills|references` for user-level install or project-root `.lingma/` for project-level install. OpenCode, AGENTS.md-compatible, and Trae-compatible entries are distributed through `dist/adapters-light/`.

For Qoder, one `python tools/build_release.py` run packages the direct Skill zip and the multi-agent QODER Project zip. Use the QODER Project zip when you want the supervisor plus worker agents installed together; use the direct QODER zip only for Qoder Skill import. From a source checkout, `python tools/install_qoder_user.py --build` builds the Qoder overlay and syncs the supervisor, worker agents, skill resources, and references into `QODER_HOME` or `~/.qoder`. For Qoder CN, use `python tools/install_qoder_user.py --product qodercn --build` to sync the same resources into `QODER_CN_HOME`, `QODERCN_HOME`, `LINGMA_HOME`, or `~/.lingma`. Use `python tools/install_qoder_user.py --audit` (or add `--product qodercn`) to check for missing or redundant managed files, and `--uninstall` to remove only this package's files.

For adapter details, see:

```text
dist/adapters-light/adapters/agent-entrypoints.md
```

Optional MCP guidance is included in:

```text
dist/adapters-light/adapters/mcp-recommendations.md
```

MCP servers are optional accelerators. Enable only task-scoped MCPs for search/fetch, documentation lookup, public code search, diagnostics, authorized document extraction, or browser testing. Do not make MCPs mandatory for correctness or use them to bypass access controls.

Optional multi-agent orchestration guidance is included in:

```text
dist/core/engineering-calculation-system/shared/multi-agent-orchestration.md
dist/core/engineering-calculation-system/templates/orchestration/
```

Use it only for explicit multi-agent, delegated, or parallel work. Workers must
declare disjoint owned paths and return result packets; the supervisor merges
through `merge_review.md`.

If the target environment cannot coordinate multiple files, load:

```text
dist/singlefile/engineering-calculation-system.all-in-one.md
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
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core
```

Validate the included scaffold:

```bash
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/core/engineering-calculation-system --profile core --project dist/core/engineering-calculation-system/project_template/engineering_calc_project --delivery web-complete
```

Run the scaffold smoke test:

```bash
cd dist/core/engineering-calculation-system/project_template/engineering_calc_project
python -B -m pytest -q -p no:cacheprovider
```
