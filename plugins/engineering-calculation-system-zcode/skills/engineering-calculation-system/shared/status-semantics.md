# Status Semantics

Recommended statuses:

```text
PASS
FAIL
WARNING
ERROR
NOT_APPLICABLE
NEEDS_CONFIRMATION
NOT_EVALUATED
```

Suggested comparison rule:

```text
PASS: utilization <= limit + tolerance
FAIL: utilization > limit + tolerance
NOT_APPLICABLE: check does not apply to this case
ERROR: required calculation could not be completed
WARNING: result exists but inputs or assumptions require attention
NEEDS_CONFIRMATION: source or assumption must be confirmed before production use
```
