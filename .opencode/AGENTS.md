<!-- engineering-calc-opencode-managed -->
# Engineering Calculation System OpenCode Rules

Use these rules for Engineering Calculation System work in OpenCode.

## Agent Selection

- Use `engineering-calc-supervisor` for lifecycle routing, gate decisions, source authority, ID allocation, handoff freeze, merge review, validation, and final acceptance.
- Use `engineering-calc-reference-acquirer` for bounded source discovery and acquisition tasks.
- Use `engineering-calc-source-intake` for source cards, authority notes, applicability limits, and conflict candidates.
- Use `engineering-calc-logic-extractor` for source-backed formulas, lookups, branches, units, and logic inventories.
- Use `engineering-calc-module-worker` for one bounded reusable calculation module after coding gates are satisfied.
- Use `engineering-calc-interface-worker` for frontend, report, review, import/export, and batch slices that consume trusted results.
- Use `engineering-calc-verification-worker` for regression, traceability, interface smoke, package, deployment, and release checks.

## Parallel Work

- Split only work with disjoint `owned_paths`.
- Workers edit only declared `owned_paths`.
- Workers return an agent result packet before their output is accepted.
- The supervisor merges through `merge_review.md`.

## Supervisor-Only Decisions

Do not delegate evidence gates, coding gates, source authority, ID allocation, handoff freeze, `run_book(BookInput) -> BookResult` public contract changes, production labels, release acceptance, or final acceptance.

## Engineering Gates

- Do not invent formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Keep formulas out of UI, report templates, frontend JavaScript, notebooks, batch scripts, and CSV/XLSX input files.
- Route official calculations through `run_book(BookInput) -> BookResult`.
- Validate with `scripts/validate_artifacts.py` before calling the work complete.

