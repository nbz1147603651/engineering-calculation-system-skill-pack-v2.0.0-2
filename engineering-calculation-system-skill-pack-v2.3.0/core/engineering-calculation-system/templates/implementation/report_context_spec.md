# Report Context Specification

Use this template to define how a report, review page, export, or batch artifact consumes already-computed results. Keep it domain-neutral. Do not prescribe a fixed report layout unless the user, source basis, client requirement, or implementation handoff requires one.

## Report Production Decision Record

| Decision item | Selected value | Reason | Source or artifact |
| --- | --- | --- | --- |
| Report purpose | to_be_defined | to_be_defined | user request / handoff |
| Intended audience | to_be_defined | to_be_defined | user request / handoff |
| Review depth | draft / review / final / prototype | to_be_defined | coding gate |
| Report status | draft / review / final / superseded / prototype / not_for_construction | to_be_defined | coding gate |
| Output format | html / pdf / docx / xlsx / json / other | to_be_defined | user request |
| Renderer or export path | to_be_defined | to_be_defined | environment |
| Saved input source | final_input.json / other | to_be_defined | output registry |
| Saved result source | BookResult JSON / trusted BookResult | to_be_defined | output registry |
| Verification method | smoke / regression / visual / manual review | to_be_defined | verification plan |

## Production Eligibility

| Requirement | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Coding gate allows production | to_be_defined | handoff/coding_go_no_go.md |  |
| Source basis is sufficient | to_be_defined | references/source_registry.yaml |  |
| Report uses saved final input or trusted BookResult | to_be_defined | output path |  |
| Templates do not calculate | to_be_defined | review or test |  |
| Warnings and errors are preserved | to_be_defined | smoke test |  |
| Traceability metadata is preserved | to_be_defined | result/report metadata |  |
| Renderer smoke test exists | to_be_defined | tests/smoke |  |

If any production requirement is not satisfied, the report status must not be `final`.

## Inputs

List external or saved inputs displayed in the report. These are presentation fields only; official calculations must already be represented in `BookInput` and `BookResult`.

| Report field | BookInput or BookResult path | Unit | Display rule | Source | Notes |
| --- | --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Report Sections

Derive sections from the user request, calculation scope, result paths, review needs, and source-backed reporting requirements.

| Section ID | Section title | Purpose | Required data paths | Visibility rule | Notes |
| --- | --- | --- | --- | --- | --- |
| R001 | to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Module summaries

| Module or check | Result paths | Values to display | Formula trace visibility | Notes |
| --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | summary / detailed / appendix / hidden | to_be_defined |

## Governing summary

| Field | BookResult path | Display rule | Notes |
| --- | --- | --- | --- |
| overall_status | governing.overall_status | to_be_defined |  |
| governing_check_id | governing.governing_check_id | to_be_defined |  |
| governing_utilization_or_margin | governing.governing_utilization_or_margin | to_be_defined |  |
| warnings_count | governing.warnings_count | to_be_defined |  |
| errors_count | governing.errors_count | to_be_defined |  |

## Warnings/errors

| Source path | Severity | Display location | Must appear in final report | Notes |
| --- | --- | --- | --- | --- |
| warnings | warning | to_be_defined | true |  |
| errors | error | to_be_defined | true |  |

## Assumptions And Limitations

| Item ID | Text or reference | Source | Blocks final report | Display rule |
| --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Traceability

| Metadata item | Source path | Required for production | Notes |
| --- | --- | --- | --- |
| report_status | ReportContext metadata | true |  |
| input_hash | BookResult metadata or saved input | true |  |
| result_hash | BookResult metadata or saved result | true |  |
| source_references | BookResult / traces | true |  |
| runner_version | BookResult metadata | true |  |
| report_template_version | renderer metadata | true when templated |  |
| data_package_id | package manifest | true when packages exist |  |
| imported_report_ids | import records | true when imported reports are used |  |

## Imported Reports and Packages

| Item | Source | Display rule | Final report impact |
| --- | --- | --- | --- |
| imported reports | data/imported/reports or package manifest | label as comparison/reference/client/prior version | never override official result |
| package manifest | data_package_manifest.yaml | show package id, status, hashes, and validation | required when package export is used |
| input/result diff | saved final input/result or imported report context | show changed paths and review note | blocks final only when unresolved |

## Template Boundaries

Allowed in templates:

```text
value references
loops
conditionals
section visibility logic
formatting filters
unit display formatting
cross-references
```

Forbidden in templates:

```text
engineering formulas
capacity/demand/status recalculation
lookup table selection
load-combination generation
optimization logic
official unit conversion
warning/error suppression
```
