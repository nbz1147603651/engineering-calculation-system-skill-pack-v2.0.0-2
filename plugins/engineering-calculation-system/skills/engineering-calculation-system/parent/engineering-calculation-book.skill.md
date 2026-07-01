---
name: engineering-calculation-book
description: Parent/orchestrator skill for building, refactoring, extending, reviewing, testing, packaging, or deploying reusable engineering calculation book software from a validated Implementation Handoff Contract. Use for typed inputs/results, decoupled reusable formula modules, module asset accumulation, official book runners, report contexts, unified production frontends, Marimo module review apps, import/export packages, batch workflows, traceability, regression tests, local runnable web clients, and Linux cloud deployment.
---

# Engineering Calculation Book - Parent Orchestrator

Use this parent after a valid implementation handoff exists, or when the user explicitly requests a
prototype with clearly recorded assumptions. It builds calculation books as reusable, auditable
software systems, not disposable scripts. `web-complete` means dual closure: a readable, traceable
calculation book AND a complete web calculation system.

## Entry condition

`handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow implementation
(`production_allowed`, or `prototype_allowed` for an explicit prototype). If the handoff is
missing, incomplete, not source-backed, or missing `semantic_closure_contract`, route upstream
through 01-07 first. For any implementation, release, or validation task, read
`shared/lifecycle.md`; it defines the required 08-14 sequence, exit gates, and the web-complete
bar. Also read `shared/execution-discipline.md` and `shared/completion-evidence.md` before acting
on or declaring implementation status.

## Child skills (run in order; default `web-complete` path)

```text
08-calculation-book-architecture
09-core-and-data-models
10-reusable-calculation-modules
11-book-runner-and-governing-summary
12-report-review-batch-interfaces            (router; selects 12a/12b/12c as needed)
12a-report-context-and-rendering             when reports or previews are needed
12b-frontend-and-review-interfaces           when production UI, API, charts, i18n, or Marimo review is needed
12c-batch-import-export-packages             when import/export, upload packages, or batch runs are needed
13-verification-regression-traceability
14-cloud-web-release-deployment              when a runnable local or Linux-cloud web calculator is the goal
```

## Dependency direction (non-negotiable)

```text
presentation / report / review / batch / API  ->  books  ->  libraries  ->  core
```

Reverse dependencies are forbidden (core may not import libraries/books/UI/report; libraries may
not import books/UI/report/batch; books may not import UI pages or report templates; reports and
batch runners may not recalculate). See `shared/lifecycle.md` for the single home of the
`run_book(BookInput) -> BookResult` contract and the formula-placement rule.

## Phase exit gate

Delivery is complete only when `shared/lifecycle.md` and `shared/completion-evidence.md` support
the claimed category. Do not route around 12a, 12b, 12c, 13, or 14 for `web-complete`. If evidence
is missing, label the result draft/prototype/incomplete and route the next remediation step. See
`shared/lifecycle.md` rows 08-14 for the per-step entry/exit gates.

## Cross-cutting rules (loaded on demand, not restated here)

- Multi-agent / parallel implementation: `shared/multi-agent-orchestration.md` (only if the user
  explicitly requests parallel work). Serial items - dependency-direction decisions, `run_book()`
  public contract, governing-summary semantics, production/release readiness - stay with the
  supervisor/integrator.
