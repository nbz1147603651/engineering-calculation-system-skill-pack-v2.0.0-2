# Result Path Convention

Use stable result paths for reports, tests, and regression checks.

Examples:

```text
bearing.status
bearing.utilization
bearing.capacity_kN
settlement.maximum_settlement_mm
governing.overall_status
governing.governing_check_id
warnings.count
errors.count
```

Report templates should reference result paths; they should not recalculate results.
