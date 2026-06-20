# Engineering Calculation Lifecycle

This is the single source of truth for the 01-14 lifecycle gates, the
delivery-mode bar, and the quality checks behind each gate. Every adapter and
release target uses the same rules. `web-complete` means dual closure: a
reviewable calculation book AND a complete web calculation system. Reduced modes
(`core-only`, `report-only`, `prototype-web`) are valid only when the user
explicitly narrows scope and must be labeled not-complete / not-deployable.

## Delivery Mode

Before implementation work starts, declare one mode in the working notes or
handoff:

```text
core-only | report-only | prototype-web | web-complete
```

Default to `web-complete` for any calculation system, calculation-book software,
web app, online calculator, deployable tool, reusable package, batch workflow,
or request that does not explicitly ask for narrower scope. For `web-complete`
the default path is `08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14`.

## Hard Handoffs

```text
references/acquisition/acquisition_handoff.yaml   connects acquisition -> analysis
handoff/implementation_handoff.yaml                connects analysis -> implementation
```

## Non-Negotiable Rules (single home — reference, do not restate)

- Engineering formulas, lookup rules, branch decisions, and load-combination
  logic live ONLY in reusable calculation modules (skill 10) and the official
  book runner (skill 11). They never live in UI, frontend JS, review notebooks,
  report templates, batch scripts, CSV/XLSX inputs, or presentation-only code.
- The one official calculation path is `run_book(book_input: BookInput) -> BookResult`.
  Every interface (API, UI, batch, report) calls it; none reimplement it.
- Do not invent formulas, coefficients, units, lookup rules, or branch logic
  when the source basis is missing.
- Do not describe a delivery as complete / production-ready / deployable /
  web-complete if it is only a CLI runner, `outputs/book_result.json`, a single
  static `.html` file, exported report HTML, a UI mockup, or a notebook demo.
  Those are valid prototypes, not a deployable web system.
- Do not start production implementation unless
  `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.

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
| 05 Logic blueprint | Trusted source set | Map concepts, inputs, outputs, nodes, assumptions, risks, visibility | Logic traceable enough for extraction | Input/output/node traceability |
| 06 Formula/lookup/branch | Blueprint exists | Extract formulas, lookups, branches, units, sign conventions, test requirements | Every production rule has source + test requirement | Source-backed formula inventory |
| 07 Implementation handoff | Analysis artifacts complete | Freeze public scope, runtime stack, module candidates, API/UI/report/batch/release contracts, coding gate | `production_allowed` for production; else prototype/no-go | Coding gate + `run_book` contract |
| 08 Architecture | Coding gate allows work | Define project structure, dependency direction, feature layers, package layout | Architecture prevents formulas in UI/report/batch | Dependency direction |
| 09 Core/data models | Architecture fixed | Typed inputs/results, statuses, hashes, serialization, errors, units, result paths | Models support `BookInput`/`BookResult` | Stable public models |
| 10 Reusable modules | Models + source-backed formulas exist | Decoupled modules, typed interfaces, formula traces, unit tests, asset registry | Modules independently testable + traceable | Formula trace + module tests |
| 11 Book runner | Modules or source-backed checks exist | Official orchestration, validation, governing summary, warnings/errors, charts, result hashes | Non-empty checks for real input; governing status traceable | Official runner path |
| 12 Interface routing | Runner exists | Select report / frontend-review / batch subskills per delivery mode | Required subskills selected | Thin interface over `run_book` |
| 12a Report context/rendering | Calc-book or preview in scope | Report context + HTML A4/LaTeX renderers; preserve warnings/errors/traces; no template calculations | Readable A4/LaTeX book with required sections | Formula Logic Trace + Template Boundary Statement |
| 12b Frontend/review/API | Web or review UI in scope | Backend API, UI kit, i18n, charts, trace display, capability detection, optional review app | API/UI calculate through `run_book` and render real results | Web API/UI framework |
| 12c Batch/import/export | Repeated use or packages in scope | JSON import/export, batch runner/API, package manifests, hashes, output registries | Batch uses `run_book` once per case | Batch + reproducible inputs |
| 13 Verification/traceability | Core/report/web/batch pieces exist | Unit, regression, smoke, i18n, report, batch, traceability, artifact validation | Hard blockers fixed or delivery downgraded | Validator before completion claim |
| 14 Release/deployment | Web-complete requested, tests pass | Local/cloud run path, Docker or systemd/nginx, env examples, release checklist, deploy smoke | Runnable local + Linux-cloud path exists | Deployment artifacts for production |

## End-of-Step Rule (every step)

Each step's final response states three things, nothing more:

```text
artifacts created or updated (paths)
gate status reached
next skill path (or "blocked: <reason>")
```

## Web-Complete Exit Gate

Before claiming `web-complete`, ALL of these must hold:

- `coding_gate.status = production_allowed`
- Real, non-empty project input exists
- `BookResult.checks` non-empty with at least one evaluated check
- Reports include Formula Logic Trace, Template Boundary Statement, input
  summary, governing result, detailed checks, charts, sources, assumptions
- Web API/UI, import/export, batch, report generation, deployment files, and
  smoke tests all exist
- `scripts/validate_artifacts.py --delivery web-complete` passes

If any fails, return a remediation list and label the delivery
draft / prototype / incomplete / not-deployable.
