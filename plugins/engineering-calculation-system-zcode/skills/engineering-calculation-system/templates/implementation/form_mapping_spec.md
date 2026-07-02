# Form ↔ Model Bidirectional Mapping Specification

Use this template to document the conversion layer between web forms and typed calculation models.

## Mapping Functions

| Function | Direction | Input | Output | Module |
| --- | --- | --- | --- | --- |
| `build_case_input_from_form` | form → model | web form JSON dict | `BookInput` | `webapp/form_utils.py` |
| `case_input_to_form` | model → form | `BookInput` | web form JSON dict | `webapp/form_utils.py` |
| `case_result_to_ui` | result → UI | `BookResult` | UI display dict | `webapp/form_utils.py` |

## Form → Model Field Mapping

| Form field path | Model field | Type | Required | Default | Validation |
| --- | --- | --- | --- | --- | --- |
| `project.project_id` | `BookInput.project.project_id` | str | yes | `"UNKNOWN"` | non-empty |
| `foundation.B_m` | `BookInput.foundation.B_m` | float | yes | `1.0` | > 0 |
| `loads.Fz_kN` | `BookInput.load_case.Fz_kN` | float | yes | `0.0` | any |
| `soil_layers[i].thickness_m` | `SoilProfile.layers[i].thickness_m` | float | yes | `1.0` | > 0 |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Model → Form Reverse Mapping

| Model field | Form field path | Notes |
| --- | --- | --- |
| `BookInput.project` | `project` | Direct dict conversion via dataclass fields |
| `BookInput.foundation` | `foundation` | Preserve all geometry fields |
| to_be_defined | to_be_defined | to_be_defined |

## Result → UI Display Mapping

| BookResult path | UI key | Display format | Unit | Status badge |
| --- | --- | --- | --- | --- |
| `governing.governing_check` | `governing.check` | string | — | — |
| `governing.utilization` | `governing.utilization` | `round(x, 4)` | — | color-coded |
| `bearing.check.status` | `bearing.status` | enum → string | — | PASS/FAIL badge |
| `settlement.total_mm` | `settlement.total_mm` | `round(x, 3)` | mm | OK/NG |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Sanitization Rules

| Condition | Action | Warning message |
| --- | --- | --- |
| `float('inf')` | replace with `null` | "Infinity (division by zero or overflow)" |
| `float('-inf')` | replace with `null` | "Infinity (overflow)" |
| `float('nan')` | replace with `null` | "NaN (not a number)" |

## Dynamic List Handling

| List | Add button | Delete button | Min items | Max items |
| --- | --- | --- | --- | --- |
| `soil_layers` | "Add Layer" | per-row delete | 1 | unlimited |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Validation Strategy

```text
required fields: reject with field-level error before runner call
numeric range: reject negative thickness, zero width, etc.
enum values: validate against allowed literals (e.g. "compression" | "tension")
cross-field: validate Fz sign matches limit_state (positive for compression)
```

## Notes

- Keep this mapping in sync with `BookInput` / `BookResult` model definitions.
- When adding a new model field, update this spec, the form template, and the JS rendering.
