# Engineering Calculation Lifecycle

This is the single source of truth for the 01-14 lifecycle gates, the delivery-mode bar, and the
quality checks behind each gate. Every adapter and release target uses the same rules.
`web-complete` means dual closure: a reviewable calculation book AND a complete web calculation
system. Scope follows the user's requested deliverable: `core-only` and `report-only` may be
complete within their declared scope after production verification; they are not a web-complete
or deployable web system. `prototype-web` remains explicitly non-production. Marimo is an
optional review adapter, not a numerical correctness requirement.

## Delivery Mode

Before implementation work starts, declare one mode in the working notes or handoff:

```text
core-only | report-only | prototype-web | web-complete
```

Select the mode from the deliverable, without requiring users to know these enum names:

| Explicit requested output | Mode | Applicable implementation path |
| --- | --- | --- |
| Reusable module/library, CLI, or batch computation | `core-only` | 08-11, 12c when batch/import-export is requested, 13 |
| Calculation book or report/export without a web app | `report-only` | 08-11, 12a, 12c when batch is requested, 13 |
| Mockup or prototype web experience | `prototype-web` | Relevant 08-12 stages, 13; no production/deployment claim |
| Operational website, online calculator, or deployable web system | `web-complete` | 08-11, 12a-12c, 13-14 |

An explicit user-selected mode wins. A mixed report+batch request remains `report-only` with
12c included. If a new system's deliverable is unspecified, retain `web-complete` as the
conservative default. Record the selected mode and requested outputs in the handoff. Use
`scripts/delivery_policy.py --deliverable batch` (repeat `--deliverable` for mixed scope) for a
machine-readable selection; the selector does not pass an engineering gate.

Also record `review_adapter: none | marimo` (default `none`, meaning no notebook runtime).
Select Marimo only when notebook review is requested. Traceable saved inputs/results, formula
sources, units, stable result paths, reproducible runner output and executable golden cases
remain required. A web-complete delivery additionally keeps its dependency-free JSON review
session bridge and decision log; no notebook package is required to inspect this evidence.

These scope and adapter rules are authoritative over legacy host-adapter wording that defaults
all tasks to a full website or mandatory Marimo. Host adapters translate installation/tool
mechanics; they do not expand the user's requested output or override engineering gates.

For a requested `web-complete` system, existing code does not lower the delivery bar. If a project contains calculation scripts, a CLI,
generated report HTML, or a static page but lacks `run_book`, `webapp/`, traceable review evidence,
report renderers, import/export, deployment files, or smoke tests,
classify it as `static_report_or_cli_only` and label it incomplete/not-deployable until the missing
web-complete layers are added.

The default calculation-book deliverable is print-ready A4 HTML: browser-viewable pages, `@page
size: A4`, print-safe margins, and chart data tables that survive printing when charts are emitted.
LaTeX/Overleaf/PDF are explicit exports or client-specific additions, not the default replacement
for the A4 HTML book.

Meaningful user choices that affect scope, assumptions, source selection, report language,
template style, review workflow, or output format must be recorded in
`analysis/06_user_interaction/user_interaction_decisions.csv`. Non-blocking unanswered questions
may proceed with an explicit default, but blocking decisions must be resolved before final or
production status is claimed.

## Incremental Work on a Verified Baseline

The 01-14 matrix describes dependencies and acceptance gates, not a mandatory restart wizard.
For a change to an existing system, first record the baseline revision, its validation evidence,
the changed layers, affected contracts, and the evidence that other layers remain valid. Reuse
existing source libraries, handoffs and passing artifacts when their inputs have not changed.
An unknown, stale or unverified baseline requires the full applicable route.

| Changed layer | Minimum owning stages; extend when a dependent contract changes |
| --- | --- |
| Source authority / applicability | 01-14 dependency review; invalidate downstream evidence |
| Formula / unit / branch | 05-07, 10-11, 13; review affected inputs, reports and interfaces |
| Models / public result shape | 09-11, 13 plus every affected consumer |
| Runner | 10-11, 13 plus affected consumer contracts |
| Report only | 12a, 13; validate the rendered report against real BookResult |
| UI / interaction only | 12b, 13; run the changed interaction and API boundary checks |
| Batch only | 12c, 13; prove per-case runner reuse and input/result integrity |
| Packaging / deployment only | 13-14; validate package content and runtime smoke |

Unchanged upstream gates are inherited only with valid evidence. A UI-only change cannot
invalidate a source-backed calculation or silently bypass an explicit `no_go`. A source or
formula change must revisit the owning upstream gate. Every completion claim still requires
fresh checks of the changed behavior; route planning itself is not validation evidence.
Preserve the declared delivery mode and final exit bar: a scoped repair of an existing
`web-complete` system does not require regenerating its unchanged runtime.

Present progress to users as five workstreams (evidence, blueprint/handoff, calculation,
delivery, verification/release), with 01-14 available as detailed traceability. Store one
route/gate/artifact/evidence record in the progress ledger and update it in place; do not
repeat the same four cards in every conversational update. Keep distinct reviewed artifacts
when they carry distinct engineering meaning.

## Hard Handoff Paths

```text
references/acquisition/acquisition_handoff.yaml   connects acquisition -> analysis
handoff/implementation_handoff.yaml                connects analysis -> implementation
```

## Non-Negotiable Rules (single home - reference, do not restate)

- Engineering formulas, lookup rules, branch decisions, and load-combination logic live ONLY in
  reusable calculation modules (skill 10) and the official book runner (skill 11). They never live
  in UI, frontend JS, review notebooks, report templates, batch scripts, CSV/XLSX inputs, or
  presentation-only code.
- The one official calculation path is `run_book(book_input: BookInput) -> BookResult`. Every
  interface (API, UI, batch, report) calls it; none reimplement it.
- Production calculation correctness is gated by calculation semantic closure:
  `calculation_intent_contract.md`, `method_selection_matrix.csv`, `input_semantics_ledger.csv`,
  `calculation_nodes.csv`, `blueprint_validation_matrix.csv`, `computation_graph_coverage.csv`,
  `runner_closure_map.csv`, and `golden_case_registry.csv` must agree before
  `production_allowed`.
- Visualization is a review artifact over computed results. Chart candidates and not-applicable
  decisions are recorded in `implementation/03_book_runner/chart_candidate_inventory.csv`; emitted
  charts are built from `BookResult`/`ChartSpec` values and never calculate.
- Do not invent formulas, coefficients, units, lookup rules, or branch logic when the source basis
  is missing.
- Do not describe a delivery as complete / production-ready / deployable / web-complete if it is
  only a CLI runner, `outputs/book_result.json`, a single static `.html` file, exported report
  HTML, a UI mockup, or a notebook demo. Those are valid prototypes, not a deployable web system.
- Do not start production implementation unless `handoff/implementation_handoff.yaml` and
  `handoff/coding_go_no_go.md` allow it.

## Gate Statuses

```text
Evidence gate (before analysis): evidence_no_go | search_required | partial_analysis_allowed | analysis_allowed
Coding gate    (before implementation): no_go | prototype_allowed | production_allowed
```

## Step / Gate Matrix

| Step | Entry condition | Required actions | Exit gate | Cannot skip |
| --- | --- | --- | --- | --- |
| 01 Reference adequacy | Source basis unclear | Classify missing formulas, units, branches, examples, jurisdiction, authority, copyright/access | Evidence status set | Source sufficiency decision |
| 02 Discovery & acquisition | 01 finds gaps | Search, select candidates, record retrieval decisions, no unauthorized copying | Critical gaps have candidates or blockers | Search log for missing/stale sources |
| 03 Local evidence library | Sources available/selected | Persist allowed metadata/extracts, source cards, hashes; write acquisition handoff | `analysis_allowed` or explicit blocker | Source IDs and access notes |
| 04 Source intake | Evidence library present | Rank authority, extract applicability limits, identify conflicts, normalize IDs | Sources trusted or conflicts block work | Authority ranking |
| 05 Logic blueprint | Trusted source set | Map concepts, inputs, outputs, nodes, assumptions, risks, visibility; freeze calculation intent, method selection, input semantics, typed calculation nodes, blueprint validation matrix, user interaction decisions, and early visualization candidates | Logic traceable enough for extraction and no blueprint validation blockers | Input/output/node traceability, user decisions, source-backed blueprint validation, and semantic closure seeds |
| 06 Formula/lookup/branch | Blueprint exists and validation matrix does not block extraction | Extract formulas, lookups, branches, units, sign conventions, test requirements; update blueprint validation rows and link each rule to method/input semantics and graph coverage | Every production rule has source + validation row + test requirement + closure target | Source-backed formula inventory |
| 07 Implementation handoff | Analysis artifacts complete | Freeze public scope, runtime stack, module candidates, semantic closure contract, API/UI/report/batch/release contracts, report language/template decisions, visualization contract, coding gate | `production_allowed` for production only if blueprint validation and semantic closure pass; else prototype/no-go | Coding gate + `run_book` contract + semantic closure |
| 08 Architecture | Coding gate allows work | Define project structure, dependency direction, feature layers, package layout | Architecture prevents formulas in UI/report/batch | Dependency direction |
| 09 Core/data models | Architecture fixed | Typed inputs/results, statuses, hashes, serialization, errors, units, result paths | Models support `BookInput`/`BookResult` | Stable public models |
| 10 Reusable modules | Models + source-backed formulas exist | Decoupled modules, typed interfaces, formula traces, explicit default/assumption warnings, unit tests, asset registry | Modules independently testable + traceable | Formula trace + module tests |
| 11 Book runner | Modules or source-backed checks exist | Official orchestration, validation, governing summary, warnings/errors, chart candidate inventory, emitted chart specs, result hashes; close every production graph node through `runner_closure_map.csv` | Non-empty checks for real input; governing status traceable | Official runner path |
| 12 Interface routing | Runner exists | Select report / frontend-review / batch subskills per delivery mode | Required subskills selected | Thin interface over `run_book` |
| 12a Report context/rendering | Calc-book or preview in scope | Report context + print-ready A4 HTML by default, optional LaTeX/PDF exports; preserve warnings/errors/traces; no template calculations; honor recorded language and template decisions | Readable A4 HTML/exports with required sections | Formula Logic Trace + Template Boundary Statement |
| 12b Frontend/review/API | Web or review UI in scope | Backend API, UI kit, i18n, charts, trace display, capability detection, recorded report language mode, JSON review evidence for `web-complete`; optional Marimo adapter when requested | API/UI calculate through `run_book` and render real results | Web API/UI framework |
| 12c Batch/import/export | Repeated use or packages in scope | JSON import/export, batch runner/API, package manifests, hashes, output registries | Batch uses `run_book` once per case | Batch + reproducible inputs |
| 13 Verification/traceability | Core/report/web/batch pieces exist | Unit, regression, golden-case, branch, smoke, i18n, report, chart inventory, user-decision, batch, traceability, artifact validation | Hard blockers fixed or delivery downgraded | Validator before completion claim |
| 14 Release/deployment | Web-complete requested, tests pass | Local/cloud run path, Docker or systemd/nginx, env examples, release checklist, deploy smoke | Runnable local + Linux-cloud path exists | Deployment artifacts for production |

## End-of-Step Rule (every step)

Each step's final response states:

```text
artifacts created or updated (paths)
gate status reached
completion evidence category from shared/completion-evidence.md
next skill path (or "blocked: <reason>")
```

## Web-Complete Exit Gate

Before claiming `web-complete`, ALL of these must hold:

- `coding_gate.status = production_allowed`
- Real, non-empty project input exists
- Calculation semantic closure artifacts exist and have no production blockers
- Blueprint validation matrix is verified and contains no `blocks_coding=true` rows
- Executable golden-case verification passes for production-blocking rows
- `BookResult.checks` non-empty with at least one evaluated check
- Reports include Formula Logic Trace, Template Boundary Statement, input summary, governing
  result, detailed checks, emitted charts, sources, assumptions
- The final calculation book defaults to print-ready A4 HTML with `@page size: A4` and chart data
  tables/source paths when charts are emitted; requested LaTeX/PDF exports remain optional
- User interaction decisions contain no unresolved `blocks_progress=true` rows; report language
  and template defaults or selections are recorded
- Chart candidate inventory records every useful chart candidate as `emit` or records why charting
  is not applicable; emitted charts preserve source result paths and printable data tables
- Web API/UI, import/export, batch, report generation, deployment files, and smoke tests all exist
- Dependency-free review evidence is wired: `/api/review/session`,
  `/api/review/state/<session_id>`, and `src/<pkg>/review/bridge.py` persist the exact input,
  result, report context, review state and append-only decisions. Formula/source/unit traces
  remain available in reports and saved results, and repeated runs plus golden-case replay pass
- Only when `review_adapter: marimo` is selected: add the notebook review/admin scaffold,
  password-gated `/admin/`, proxied `/admin/review/` and `/admin/formulas/`, review apps,
  `ADMIN_REVIEW_PASSWORD` and `ADMIN_REVIEW_TOKEN`. Missing optional Marimo never blocks the
  main calculator; a requested notebook feature remains incomplete until its own smoke passes
- `scripts/validate_artifacts.py --delivery web-complete` passes

If any fails, return a remediation list and label the delivery draft / prototype / incomplete /
not-deployable.
