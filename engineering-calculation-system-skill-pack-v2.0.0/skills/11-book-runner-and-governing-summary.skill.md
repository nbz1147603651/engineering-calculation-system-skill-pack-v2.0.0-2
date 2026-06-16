---
name: book-runner-and-governing-summary
description: Build the official engineering calculation book runner, orchestration sequence, shared state preparation, module calls, warnings/errors aggregation, BookResult, governing summary, result paths, and integration tests.
---

# Book Runner and Governing Summary

Use this skill after core models and reusable modules exist or have been designed.

## Goal

Create exactly one official calculation path for a formal engineering calculation book.

## Official Runner

Every calculation book must define:

```python
def run_book(book_input: BookInput) -> BookResult:
    ...
```

The runner must:

```text
validate book-level input
prepare shared state
apply design options and assumptions
call reusable calculation modules
collect module results
preserve warnings and errors
summarize governing checks
create run metadata
return structured BookResult
```

The runner must not:

```text
render reports
read raw CSV files
manage UI state
write batch summaries
contain report-template logic
```

## Governing Summary

Expose:

```text
overall_status
governing_check_id
governing_check_name
governing_utilization_or_margin
governing_limit
critical_load_case or combination
controlling location/member/foundation if applicable
warnings_count
errors_count
```

## Required Output Artifacts

```text
implementation/03_book_runner/runner_sequence.md
implementation/03_book_runner/governing_summary_spec.md
implementation/03_book_runner/result_path_registry.csv
src/<pkg>/books/<book_name>/book_runner.py
src/<pkg>/books/<book_name>/governing.py
tests/integration/test_<book_name>_runner.py
```

## Required Final Response

Provide:

```text
runner sequence
module call order
shared state plan
BookResult structure
governing summary logic
warnings/errors behavior
integration test
```
