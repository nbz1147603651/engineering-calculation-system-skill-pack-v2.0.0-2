---
name: engineering-calculation-router
description: Route engineering calculation tasks to the correct reference acquisition, reference analysis, handoff, implementation, reporting, batch, verification, reusable-module, or cloud-web release skill. Use whenever the user request spans multiple stages, lacks source materials, has unclear source sufficiency, or when it is unclear whether to find references, analyze references, write code, refactor, generate reports, test, package, or deploy a runnable online calculator.
---

# Engineering Calculation Router

Use this skill to decide which engineering calculation skill path should handle the task. The gate
status vocabulary, the 01-14 step matrix, and the end-of-step rule live in `shared/lifecycle.md`.
For non-trivial tasks, also read `shared/execution-discipline.md` and output a route card before
implementation action.
For multi-step implementation plans, review feedback, or release/platform work, also read the
matching discipline file: `shared/planning-discipline.md`,
`shared/review-feedback-discipline.md`, or `shared/version-control-discipline.md`.

## Routing principle

Do not jump into analysis or coding when the source basis is missing or insufficient. Do not jump
into coding when raw references exist but no implementation handoff exists. Do not re-analyze
references when a valid source-backed `implementation_handoff.yaml` already exists and the user
asks for implementation. Do not put formulas in report, UI, frontend, batch, or CSV/Excel work.

If the user explicitly asks for multi-agent / subagent / delegated / parallel work, read
`shared/multi-agent-orchestration.md` after this router. Use task briefs, owned paths, result
packets, review packages, and the progress ledger. Parallel work must never bypass evidence gates,
coding gates, source-authority review, ID allocation, handoff freeze, the `run_book()` contract,
or final release acceptance.

For bug fixes, read `shared/systematic-debugging.md`. Identify the lowest correct repair layer in
the chain `source/evidence -> formula_inventory/lookup_inventory/branch_inventory -> module ->
run_book() -> API/batch -> report/UI`. If the root cause is source, unit, formula, lookup, branch,
or semantic closure, route back to 04-07 or 10-11 instead of patching symptoms in 12a/12b.

For review feedback, read `shared/review-feedback-discipline.md` before editing. If the feedback
changes sources, units, formulas, lookups, branches, semantic closure, gate status, or public API
shape, route to the owning lifecycle phase instead of applying it as a local patch.

## Step 1 - classify the material state

| State | Meaning | Route |
| --- | --- | --- |
| `no_materials` | desired calculator, no references | 01 -> 02 -> 03 |
| `insufficient_materials` | formulas/units/coefficients/examples/branches missing | 01 -> 02 -> 03 |
| `materials_available_untrusted` | authority/version/conflicts unclear | 04, maybe 01 -> 02 -> 03 |
| `local_evidence_library_available` | source registry + cards + raw/extracted + acquisition handoff exist | 04 -> 05 -> 06 -> 07 |
| `analysis_handoff_available` | implementation handoff + coding gate exist | 08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14 (default `web-complete`; narrower only if explicitly requested) |
| `static_report_or_cli_only` | existing scripts, CLI output, notebook, static HTML, or exported calculation book but no complete runtime web scaffold | 08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14 if `web-complete` is expected; label incomplete until validator passes |
| `codebase_available` | existing implementation | classify bug/feature by layer, then route to 08-14 |

## Step 2 - classify the task intent

| User intent | Route |
| --- | --- |
| Find sources / search references / gather standards/manuals/examples | 01 -> 02 -> 03 |
| Decide if sources are sufficient | 01 |
| Persist gathered references locally | 03 |
| Analyze standards, PDFs, Excel, reports, scripts, soil reports, manual calcs | 04 -> 05 -> 06 -> 07 |
| Create Calculation Logic Blueprint | 05 (with 04 first) |
| Extract formulas, lookups, branches, units, assumptions | 06 |
| Prepare downstream coding guidance | 07 |
| Build/refactor engineering calculation software | 08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14 by default; reduce scope only on explicit `core-only` / `report-only` / `prototype-web` |
| Build reusable / asset-ready calculation modules | 08 -> 10 -> 13 |
| Build typed models only | 09 |
| Build official calculation-book runner | 11 (plus 13) |
| Build report / review UI / CLI / API / batch flow | 12, then 12a/12b/12c as needed (plus 13) |
| Add tests / regression / traceability / hash / quality gates | 13 |
| Package / release / run locally / deploy cloud/Linux/Docker/systemd/nginx / online web calculator | 14, after 12b and 13 when web UI/API exists |
| Fix bug | read `shared/systematic-debugging.md`, identify the lowest correct layer, then route to 04-07, 10-11, 12, 13, or 14 as evidence requires |

## Step 3 - check parallel suitability

Parallel work is useful only after the lifecycle phase is known and write ownership can be
separated (use `templates/orchestration/parallel_work_plan.yaml`). Good slices: search different
gaps/jurisdictions/source families (01-03); intake separate documents/tables (04); extract
formulas/lookups/branches/units/examples/inventories (05-06); implement disjoint
core/model/module/interface/report/batch paths (08-12); prepare unit/regression/smoke/deployment
checks (13-14). Serial: routing decision, evidence gate, source authority & conflicts, ID
namespace allocation, handoff freeze, coding gate, the `run_book(BookInput) -> BookResult`
contract, production/release readiness.

## Step 4 - output the route card

```text
task_type:
material_state:
required_skill_path:
delivery_mode:
plan_required: yes | no
review_feedback_mode: none | accept | reject | escalate | route_upstream
workspace_isolation: not_needed | check_existing | recommended
required_input_artifacts:
expected_output_artifacts:
gate_status:
immediate_next_action:
parallel_suitability: none | optional | recommended
completion_evidence_category:
```

For `web-complete`, do not route around 12a, 12b, 12c, 13, or 14. The final delivery must close
both the readable calculation-book track and the complete web-system track. Do not begin
implementation until this route card and the execution-discipline gate card agree.
