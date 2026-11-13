# Input Mapping Specification

## Flow

```text
CSV / JSON / API / UI input
-> parse external fields
-> validate shape and units
-> enforce input_semantics_ledger.csv
-> build BookInput
-> run_book(BookInput)
```

## Boundary Rules

- Unit conversion is allowed only at parse/model boundaries and must be recorded.
- Sign changes, coordinate transforms, absolute-value handling, clipping, default substitution, and
  empirical parameter estimates must match `input_semantics_ledger.csv`.
- Missing required engineering inputs must raise validation errors unless the ledger defines an
  explicit non-production default policy.
- UI, API, import/export, batch, report, and review layers must not change engineering meaning
  after `BookInput` is built.

## Mapping Table

| External Field | BookInput Path | Input ID | Unit | Required | Default Policy | Validation | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | IN001 | to_be_defined | true | no_default_required | to_be_defined | to_be_defined |
