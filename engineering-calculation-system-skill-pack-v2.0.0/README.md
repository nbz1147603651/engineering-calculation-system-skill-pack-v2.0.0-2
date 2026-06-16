# Engineering Calculation System Skill Pack v2.1.1

This package organizes engineering calculation software development into a full three-stage lifecycle:

```text
reference acquisition and local persistence
-> reference analysis and calculation logic blueprint
-> implementation, reporting, batch execution, verification, and traceability
```

The implementation stage now includes a unified interface pattern:

```text
polished frontend with left-side inputs and right-side review results
Marimo review pages for module-level inspection and draft edits
managed data/report import and uploadable calculation packages
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
12 report review batch interfaces, unified UI, Marimo review, and data packages
13 verification regression traceability
```

## Parent skills

```text
parent/engineering-calculation-reference-acquisition.skill.md
parent/engineering-calculation-logic-architecture.skill.md
parent/engineering-calculation-book.skill.md
```

## Agent entrypoints

Use `SKILL.md` as the root skill entrypoint for Codex-compatible environments. For other agents, see:

```text
adapters/agent-entrypoints.md
```

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
