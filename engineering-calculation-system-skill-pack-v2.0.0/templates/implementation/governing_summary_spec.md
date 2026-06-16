# Governing Summary Specification

## Required Fields

| Field | Meaning |
| --- | --- |
| overall_status | aggregate PASS/FAIL/WARNING/ERROR state |
| governing_check_id | controlling check ID |
| governing_check_name | controlling check name |
| governing_utilization_or_margin | utilization, margin, or equivalent measure |
| governing_limit | criterion used for governing selection |
| critical_load_case_or_combination | controlling load case if applicable |
| warnings_count | number of preserved warnings |
| errors_count | number of preserved errors |

## Selection Rule

Document how governing checks are ranked when multiple checks are near or beyond limits.

