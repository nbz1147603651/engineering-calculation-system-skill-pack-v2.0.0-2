---
name: book-runner-and-governing-summary
description: Build the official engineering calculation book runner, orchestration sequence, shared state preparation, module calls, warnings/errors aggregation, BookResult, governing summary, result paths, chart specs, and integration tests.
---

# Book Runner and Governing Summary

## When to use

After core models (skill 09) and reusable modules (skill 10) exist or are designed. Create exactly
one official calculation path for the book.

## Steps

1. Implement the official runner `src/<pkg>/books/<book_name>/book_runner.py`:
   `def run_book(book_input: BookInput) -> BookResult: ...`. The runner must: validate book-level
   input; prepare shared state; apply design options and assumptions; call reusable calculation
   modules; collect module results; preserve warnings and errors; summarize governing checks;
   actively evaluate chartable outputs from the book's own result-path registry and create chart
   specs from already-computed result values when they improve review; create run metadata; return
   a structured BookResult. It must NOT
   render reports, read raw CSV, manage UI state, write batch summaries, or contain report-template
   logic.
2. Implement the governing summary
   (`src/<pkg>/books/<book_name>/governing.py`, spec `templates/implementation/governing_summary_spec.md`)
   exposing: overall_status, governing_check_id, governing_check_name,
   governing_utilization_or_margin, governing_limit, critical_load_case/combination, controlling
   location/member/foundation if applicable, warnings_count, errors_count.
3. Build chart specs (`src/<pkg>/books/<book_name>/charts.py`) from the book-specific result-path
   registry, review needs, and available `BookResult` fields. Do not hardcode a universal chart
   set or copy example chart IDs into unrelated books. Chart specs package already-computed values
   with source result paths and recommended UI/report locations; they never calculate.
   Record the decision basis in
   `implementation/03_book_runner/chart_candidate_inventory.csv`
   (`templates/implementation/chart_candidate_inventory.csv`): each candidate result group,
   trigger condition, `emit`/`not_applicable`/`defer` decision, reason, source result paths, and
   test IDs. If no useful chartable data exists, add a not-applicable row instead of emitting an
   empty chart list without explanation.
4. Define the runner sequence
   (`implementation/03_book_runner/runner_sequence.md`, `templates/implementation/runner_sequence.md`)
   and the result-path registry
   (`implementation/03_book_runner/result_path_registry.csv`,
   `templates/implementation/result_path_registry.csv`).
5. Define the runner closure map
   (`implementation/03_book_runner/runner_closure_map.csv`,
   `templates/implementation/runner_closure_map.csv`). Every production method/check/formula/
   lookup/branch listed in analysis closure artifacts must map to a runner step, called module,
   public function, result path, warning path, and test ID. Do not count unused modules as
   implemented checks.
6. Add an integration test `tests/integration/test_<book_name>_runner.py`.

## Artifacts

```text
implementation/03_book_runner/runner_sequence.md         (templates/implementation/runner_sequence.md)
implementation/03_book_runner/governing_summary_spec.md  (templates/implementation/governing_summary_spec.md)
implementation/03_book_runner/result_path_registry.csv   (templates/implementation/result_path_registry.csv)
implementation/03_book_runner/chart_candidate_inventory.csv (templates/implementation/chart_candidate_inventory.csv)
implementation/03_book_runner/runner_closure_map.csv     (templates/implementation/runner_closure_map.csv)
src/<pkg>/books/<book_name>/book_runner.py
src/<pkg>/books/<book_name>/governing.py
src/<pkg>/books/<book_name>/charts.py  (when chartable result paths exist)
tests/integration/test_<book_name>_runner.py
```

## Exit gate

Non-empty checks for real input; governing status is traceable; runner closure map is closed for
production nodes; chart applicability is recorded from the book-specific result paths, with
`ChartSpec` entries emitted only when useful. See `shared/lifecycle.md` row 11. Next path: 12 to
select interface subskills.
