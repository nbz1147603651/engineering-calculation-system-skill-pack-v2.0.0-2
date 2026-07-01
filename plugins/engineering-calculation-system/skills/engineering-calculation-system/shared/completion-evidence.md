# Completion Evidence

Use this matrix before any claim that work is source-backed, verified, production-ready,
web-complete, deployable, or fixed. `shared/lifecycle.md` remains the lifecycle authority; this
file defines the evidence needed to make claims about that lifecycle.

## Evidence Matrix

| Claim | Required evidence | Not sufficient |
| --- | --- | --- |
| `source-backed` | `references/source_registry.yaml`, source cards or evidence manifest, search/retrieval logs, source authority table | memory, generic engineering knowledge, a copied formula without source ID |
| `analysis_allowed` | acquisition handoff plus source intake, authority/conflict records, and no blocking source gaps | a PDF exists, one source was found |
| `production_allowed` | `handoff/implementation_handoff.yaml`, `handoff/coding_go_no_go.md`, calculation intent, method selection, input semantics, graph coverage, runner closure, golden-case targets | UI/report completeness, prototype gate, partial semantic closure |
| `formula verified` | formula/lookup/branch inventory, reusable module tests, formula traces, golden cases or regression references | formula appears in code, manual spot check |
| `report-ready` | A4 HTML report sections, Formula Logic Trace, Template Boundary Statement, sources, assumptions, chart data tables when charts exist | static HTML alone, visual polish |
| `web-complete` | `shared/lifecycle.md` Web-Complete Exit Gate plus a fresh `validate_artifacts.py --delivery web-complete` pass for the project | CLI runner, notebook, static export, old validator output |
| `deployable` | deployment files, env examples, health/smoke route, release checklist, and fresh validation evidence | Dockerfile exists, app opened once |
| `bug fixed` | root cause trace, minimal reproduction, fix at the lowest correct layer, regression or smoke validation | symptom hidden in UI/report layer, agent report says fixed |

## Gate Function

Before making a completion claim:

1. Identify the claim category in the matrix.
2. List the exact artifact paths and commands that prove it.
3. Run the required validation fresh in this work session.
4. Report the claim only if the evidence directly proves it.
5. If evidence is missing or weak, state the blocker and next lifecycle path.

Old output, partial checks, and optimistic worker summaries do not prove completion.
