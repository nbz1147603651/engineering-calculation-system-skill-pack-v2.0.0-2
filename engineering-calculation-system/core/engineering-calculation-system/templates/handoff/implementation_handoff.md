# Implementation Handoff

## Handoff Status

Summarize `handoff/implementation_handoff.yaml` and the current coding gate.

## Source Basis

List governing, example, background, and assumption sources by stable source ID.

## Calculation Scope

State included checks, excluded checks, applicability limits, and major assumptions.

## Runtime Stack

Record the primary implementation stack. The default is Python 3.9+, Python calculation modules, Flask/FastAPI backend routes, a `webapp/` browser frontend, and optional Marimo review. If a non-Python calculation runtime is used, record the wrapper, CLI, or API adapter required for Python-based review and deployment.

## Model Groups

Summarize input model groups, result model groups, validation rules, and result paths.

## Module And Runner Plan

Summarize module candidates, formula references, lookup references, branch references, and runner sequence.

## Semantic Closure Contract

Summarize the calculation intent contract, method selection matrix, input semantics ledger,
computation graph coverage, runner closure map, and golden case registry. Explicitly state whether
the production path is closed from calculation purpose to BookInput fields, source-backed rules,
modules, `run_book()`, BookResult result paths, report visibility, and tests.

## Calculation Module Contract

List the reusable calculation module paths, public functions, typed input/result models, source trace requirements, tests, and forbidden dependencies.

## Backend API Contract

List the application factory, health endpoint, calculate endpoint, route files, form/model mapping functions, and the rule that API routes call `run_book()` instead of calculating.

## Frontend Contract

List required templates/static assets, expected BookInput form behavior, result display behavior, trace/review behavior, and the rule that frontend JavaScript and templates do not calculate engineering results. The default frontend format is a browser web app under `webapp/` using Jinja2 templates, Bootstrap 5, and vanilla JavaScript modules.

## Report Localization And Template Contract

Summarize supported report language modes (`en`, `zh`, `bilingual`), the selected/default language,
the user interaction decision IDs, default HTML/LaTeX template IDs, and the rule that template
replacement never changes calculation modules or `run_book()`.

## Visualization Contract

Summarize `implementation/03_book_runner/chart_candidate_inventory.csv`, which candidates are
emitted or not applicable, the `ChartSpec` builder path, and the rule that charts consume
already-computed BookResult values with source result paths.

## Operator Workflow Contract

Record the decisions that make the tool convenient and reliable for repeated engineering use: field defaults, validation, import/export, governing summaries, warnings/errors, traces, report preview, batch comparison, and any justified frontend stack upgrade.

## Release Contract

State whether final delivery is expected. If it is, record local run commands, Linux/cloud deployment files, smoke tests, and explicitly confirm that a static `.html` file or exported report HTML is not the application deliverable.

## Verification Requirements

Summarize required unit, lookup, branch, regression, integration, smoke, and traceability tests.

## Blockers

List unresolved items that block prototype or production work.
