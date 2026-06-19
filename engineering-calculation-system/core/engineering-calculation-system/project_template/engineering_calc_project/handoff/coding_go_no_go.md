# Coding Go / No-Go

## Gate status

```yaml
status: production_allowed # no_go | prototype_allowed | production_allowed
```

## Allowed work

- run the template demonstration calculation
- replace the example module with source-backed engineering modules for real projects

## Blocked work

- none for the template demonstration

## Blocking issues

| Issue ID | Issue | Affected module | Required resolution |
| --- | --- | --- | --- |

## Semantic production gate checklist

- [x] Acquisition handoff status is `analysis_allowed`.
- [x] Critical/high source coverage rows that block coding are `covered`.
- [x] Critical/high coverage rows have stable `current_source_id` values.
- [x] Formula rows have actionable `source_reference` and `test_requirement` values.
- [x] Lookup rows define interpolation, out-of-range behavior, source reference, and tests.
- [x] Branch rows define source reference, true/false paths, and required tests.
- [x] No open question has `blocks_coding=true`.
- [x] No source conflict has `blocks_coding=true`.
- [x] No assumption has `blocks_production=true`.

## Notes

This template is production-allowed only for the included demonstration check.
Replace the demonstration source and module with project-specific engineering
sources before using it for real design decisions.
