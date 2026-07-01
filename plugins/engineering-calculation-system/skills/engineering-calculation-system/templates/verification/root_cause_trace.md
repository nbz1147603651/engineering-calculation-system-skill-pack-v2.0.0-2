# Root Cause Trace

observed_failure:
reproduction:
first_bad_layer: source/evidence | formula_inventory | lookup_inventory | branch_inventory | module | run_book | api_batch | report_ui | deployment
source_or_handoff_impact:
root_cause:
fix_layer:
files_changed:
validation_commands:
completion_evidence_category: bug fixed

## Notes

- Fix formula, unit, lookup, branch, and source issues at their lowest correct layer.
- Do not hide calculation defects in presentation, report, batch, or imported data layers.
