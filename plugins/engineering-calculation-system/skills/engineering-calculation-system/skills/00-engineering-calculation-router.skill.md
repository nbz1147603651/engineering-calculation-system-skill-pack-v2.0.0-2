---
name: engineering-calculation-router
description: Route engineering calculation tasks to the correct reference acquisition, reference analysis, handoff, implementation, reporting, batch, verification, reusable-module, or cloud-web release skill. Use whenever the user request spans multiple stages, lacks source materials, has unclear source sufficiency, or when it is unclear whether to find references, analyze references, write code, refactor, generate reports, test, package, or deploy a runnable online calculator.
---

# Engineering Calculation Router

Use this skill to decide which engineering calculation skill path should handle the task.

## Routing Principle

Do not jump into analysis or coding when the source basis is missing or insufficient.

Do not jump into coding when raw references exist but no implementation handoff exists.

Do not analyze references again when a valid source-backed `implementation_handoff.yaml` already exists and the user asks for implementation.

Do not put formulas in report, UI, frontend, batch, or CSV/Excel input work.

If the user explicitly asks for multi-agent, subagent, delegated, or parallel
work, read `shared/multi-agent-orchestration.md` after this router. Do not use
parallel work to bypass evidence gates, coding gates, source authority review,
ID allocation, handoff freeze, `run_book()` contract control, or final release
acceptance.

## Source State Classification

Classify the material state first:

| State | Meaning | Route |
| --- | --- | --- |
| `no_materials` | User describes a desired calculator but provides no references | 01 -> 02 -> 03 |
| `insufficient_materials` | Some materials exist but formula, code basis, units, coefficients, examples, or branches are missing | 01 -> 02 -> 03 |
| `materials_available_untrusted` | Materials exist but authority/version/conflicts are unclear | 04, and maybe 01 -> 02 -> 03 |
| `local_evidence_library_available` | Source registry, source cards, raw/extracted references, and acquisition handoff exist | 04 -> 05 -> 06 -> 07 |
| `analysis_handoff_available` | Implementation handoff and coding gate exist | 08 -> 09 -> 10 -> 11 -> 13, plus 12 if interfaces needed, plus 14 for deployable web delivery |
| `codebase_available` | Existing implementation exists | classify bug/feature by layer, then route to 08-14 |

## Task Classification

| User intent | Route |
| --- | --- |
| Find资料, search references, gather standards/manuals/examples | 01 -> 02 -> 03 |
| Decide if provided资料足够 | 01 |
| Persist gathered references locally | 03 |
| Analyze standards, PDFs, Excel, reports, scripts, soil reports, or manual calculations | 04 -> 05 -> 06 -> 07 |
| Create Calculation Logic Blueprint | 05, with 04 first |
| Extract formulas, lookup tables, branch rules, units, assumptions | 06 |
| Prepare downstream coding guidance | 07 |
| Build or refactor engineering calculation software | 08 -> 09 -> 10 -> 11 -> 13, plus 12 if needed, plus 14 when final delivery is expected |
| Build reusable or asset-ready calculation modules | 08 -> 10 -> 13, record module assets |
| Build typed models only | 09 |
| Build reusable formula/calculation module | 10, plus 13 |
| Build official calculation book runner | 11, plus 13 |
| Build report, review UI, CLI, API, or batch flow | 12, then 12a/12b/12c as needed, plus 13 smoke tests |
| Add tests, regression, traceability, hash, quality gates | 13 |
| Package, release, run locally, deploy to cloud/Linux, Docker, systemd, nginx, online web calculator | 14, after 12b and 13 when web UI/API exists |
| Fix bug | Identify lowest correct layer, then route there |

## Parallel Suitability

Parallel work is useful only after the lifecycle phase is known and write
ownership can be separated. Use `templates/orchestration/parallel_work_plan.yaml`
for explicit parallel plans.

Good parallel slices:

```text
01-03: search different gaps, jurisdictions, or source families
04: intake separate documents or tables
05-06: extract formulas, lookups, branches, units, examples, or inventories
08-12: implement disjoint core/model/module/interface/report/batch paths
13-14: prepare unit, regression, smoke, deployment, and release checks
```

Keep these serial:

```text
routing decision
evidence gate
source authority and conflicts
ID namespace allocation
implementation handoff freeze
coding gate
run_book(BookInput) -> BookResult public contract
production and release readiness
```

## Gate Statuses

Use evidence gate statuses before analysis:

```text
evidence_no_go: cannot analyze or code because source basis is absent or unreliable
search_required: references must be found before analysis
partial_analysis_allowed: enough for outline, not enough for implementation handoff
analysis_allowed: enough to produce a traceable blueprint
```

Use coding gate statuses before implementation:

```text
no_go: do not code except scaffolding or non-formula architecture notes
prototype_allowed: code only with explicit assumptions and needs_confirmation markers
production_allowed: implementation can proceed with tests and traceability
```

## Required Checks Before Routing

Ask or infer:

```text
Is this reference acquisition, reference analysis, or implementation?
Are there any user-provided sources?
Is there a local evidence library?
Is there a valid acquisition_handoff.yaml?
Is there a valid implementation_handoff.yaml?
Does the task require current or jurisdiction-specific information?
Does the task involve formulas, lookup rules, branch logic, or units?
Does the task involve only presentation/report/UI/batch?
Does the final output need to be a runnable online web calculation program?
Does deployment target Linux, Docker, systemd, nginx, or another cloud runtime?
Do calculation modules need to become reusable assets for later projects?
Are there source conflicts or missing design-code bases?
Did the user explicitly request multi-agent or parallel work?
Can write ownership be split into disjoint paths?
```

## Output

Provide a short routing decision:

```text
Task type:
Material state:
Required skill path:
Required input artifacts:
Expected output artifacts:
Gate status:
Immediate next action:
Parallel suitability: none | optional | recommended
```
