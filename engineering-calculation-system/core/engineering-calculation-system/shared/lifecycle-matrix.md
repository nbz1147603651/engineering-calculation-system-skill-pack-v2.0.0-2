# Engineering Calculation Lifecycle Matrix

This matrix is the shared control surface for every adapter and release target.
`web-complete` means dual closure: a reviewable calculation book and a complete
web calculation system. Reduced modes (`core-only`, `report-only`,
`prototype-web`) are valid only when the user explicitly narrows scope and must
not be described as production complete.

| Step | Entry condition | Required actions | Required artifacts | Exit gate | Cannot skip |
| --- | --- | --- | --- | --- | --- |
| 01 Reference adequacy | User asks for engineering calculation and source basis is unclear | Classify missing formulas, units, branches, examples, jurisdiction, authority, and copyright/access limits | Gap assessment, open reference questions | Evidence status is set | Source sufficiency decision |
| 02 Discovery and acquisition | 01 finds gaps or current/jurisdiction-specific sources are needed | Search, select candidates, record retrieval decisions, avoid unauthorized source copying | Search log, candidate sources, retrieval decisions, coverage matrix draft | Critical gaps have source candidates or blockers | Search log for missing/stale sources |
| 03 Local evidence library | Sources are available or selected | Persist allowed metadata/extracts, source cards, hashes, coverage status, and access limits | Source registry, evidence manifest, source cards, acquisition handoff | `analysis_allowed` or explicit blocker | Source IDs and access notes |
| 04 Source intake | Evidence library is present | Rank authority, extract applicability limits, identify conflicts, normalize source IDs | Source inventory, authority table, conflicts | Sources are trusted or conflicts block work | Authority ranking |
| 05 Logic blueprint | Trusted source set exists | Map calculation concepts, inputs, outputs, nodes, assumptions, risks, and visibility | Calculation logic blueprint, concept map, inventories | Logic is traceable enough for extraction | Input/output/node traceability |
| 06 Formula/lookup/branch extraction | Logic blueprint exists | Extract formulas, lookup tables, branch conditions, units, sign conventions, and test requirements | Formula, lookup, branch, unit/sign, assumption inventories | Every production rule has source and test requirement | Source-backed formula inventory |
| 07 Implementation handoff | Analysis artifacts are complete enough | Freeze public scope, runtime stack, module candidates, API/UI/report/batch/release contracts, and coding gate | `handoff/implementation_handoff.yaml`, `handoff/coding_go_no_go.md`, artifact index | `production_allowed` for production completion; otherwise prototype/no-go | Coding gate and official `run_book` contract |
| 08 Architecture | Coding gate allows implementation or explicit prototype is requested | Define project structure, dependency direction, feature layers, and package layout | Project structure, dependency rules, package layout, feature classification | Architecture prevents formulas in UI/report/batch | Dependency direction |
| 09 Core/data models | Architecture is fixed | Implement typed inputs/results, statuses, hashes, serialization, errors, units, and result paths | Core package, book models, status semantics, unit system | Models support `BookInput` and `BookResult` | Stable public models |
| 10 Reusable modules | Models and source-backed formulas exist | Build decoupled modules with typed interfaces, formula traces, unit tests, and asset registry entries | Library modules, module specs, asset registry, unit tests | Modules are independently testable and traceable | Formula trace and module tests |
| 11 Book runner | Reusable modules or source-backed checks exist | Implement official orchestration, validation, governing summary, warnings/errors, charts, and result hashes | `run_book(BookInput) -> BookResult`, integration tests, chart specs | Non-empty checks for real input and governing status is traceable | Official runner path |
| 12 Interface routing | Runner exists | Select report, frontend/review, batch/import/export subskills according to delivery mode | Interface decision record | Required subskills are selected | Thin interface over `run_book` |
| 12a Report context/rendering | Calculation book or preview is in scope | Build report context and HTML A4/LaTeX renderers; preserve warnings/errors/traces; no template calculations | Report context, HTML/LaTeX templates, final report route | Readable A4/LaTeX book with required sections | Formula Logic Trace and Template Boundary Statement |
| 12b Frontend/review/API | Web or review UI is in scope | Build backend API, UI kit, i18n, charts, formula/source trace display, capability detection, and optional review app | `webapp/`, API routes, JS/CSS/templates, i18n, UI smoke tests | API/UI calculate through `run_book` and render real results | Web API/UI framework |
| 12c Batch/import/export | Repeated use or packages are in scope | Build JSON import/export, batch runner/API, package manifests, hashes, and output registries | Import/export routes, batch route, package/output folders, smoke tests | Batch uses `run_book` once per case | Batch and reproducible inputs |
| 13 Verification/traceability | Core/report/web/batch pieces exist | Run unit, regression, smoke, i18n, report, batch, traceability, and artifact validation | Test matrix, pytest results, validation output, traceability records | Hard blockers are fixed or delivery is downgraded | Validator before completion claim |
| 14 Release/deployment | Web-complete delivery is requested and tests pass | Package local/cloud run path, Docker or systemd/nginx, env examples, release checklist, and deployment smoke commands | Deploy files, release checklist, runbook, packaged release | Runnable local and Linux-cloud path exists | Deployment artifacts for production completion |

## Web-Complete Exit Gate

Before claiming `web-complete`, all of these must be true:

- `coding_gate.status=production_allowed`.
- Real project input exists and is not empty.
- `BookResult.checks` is non-empty and at least one check is evaluated.
- Reports include Formula Logic Trace, Template Boundary Statement, input
  summary, governing result, detailed checks, charts, sources, and assumptions.
- Web API/UI, import/export, batch, report generation, deployment files, and
  smoke tests exist.
- `scripts/validate_artifacts.py --delivery web-complete` passes.

If any item fails, return a remediation list and label the delivery as draft,
prototype, incomplete, or not deployable.
