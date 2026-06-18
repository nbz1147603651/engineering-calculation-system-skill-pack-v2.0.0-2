# Coding Go / No-Go

## Gate status

```yaml
status: prototype_allowed # no_go | prototype_allowed | production_allowed
```

## Allowed work

- 

## Blocked work

- 

## Blocking issues

| Issue ID | Issue | Affected module | Required resolution |
| --- | --- | --- | --- |

## Semantic production gate checklist

- [ ] Acquisition handoff status is `analysis_allowed`.
- [ ] Critical/high source coverage rows that block coding are `covered`.
- [ ] Critical/high coverage rows have stable `current_source_id` values.
- [ ] Formula rows have actionable `source_reference` and `test_requirement` values.
- [ ] Lookup rows define interpolation, out-of-range behavior, source reference, and tests.
- [ ] Branch rows define source reference, true/false paths, and required tests.
- [ ] No open question has `blocks_coding=true`.
- [ ] No source conflict has `blocks_coding=true`.
- [ ] No assumption has `blocks_production=true`.

## Notes

Do not implement production formulas when source basis, units, branch rules, or safety factors are unresolved.
