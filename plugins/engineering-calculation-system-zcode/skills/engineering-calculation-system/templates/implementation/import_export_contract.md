# Import, Report Import, and Export Contract

Use this template for data import, prior report import, upload packages, and repeatable exports.

## Managed Data Directories

```text
data/input/
data/imported/reports/
data/imported/references/
data/staging/
data/normalized/cases/
data/packages/
outputs/results_json/
outputs/reports_html/
outputs/reports_pdf/
outputs/reports_docx/
outputs/upload_packages/
outputs/logs/
```

## Accepted Imports

| Import type | Formats | Destination | Normalization target | Allowed use |
| --- | --- | --- | --- | --- |
| case input | JSON / YAML / CSV / XLSX | data/input or data/staging | BookInput JSON | official calculation after validation |
| batch control | CSV / XLSX / YAML | data/input | batch_control.csv | batch orchestration |
| prior report | HTML / PDF / DOCX / XLSX / context.json | data/imported/reports | report_import record | review/comparison only |
| reference file | PDF / image / document / spreadsheet | data/imported/references | source card or registry entry | source-backed review only |
| upload package | ZIP / folder | data/packages | manifest + normalized inputs | repeatable import/export |

## Upload Package Flow

```text
receive package
-> store in data/staging/
-> compute file hashes
-> read data_package_manifest.yaml if present
-> classify files by role
-> validate schema and allowed extensions
-> preview case list and imported report list
-> normalize accepted case inputs
-> run selected case or batch through run_book()
-> write BookResult JSON, reports, and package manifest
```

## Report Import Rules

- Imported reports are evidence or comparison artifacts, not official calculation truth.
- Imported report metadata must include original filename, hash, import date, role, and trust level.
- If an imported report is used as a regression reference, record the expected result paths and tolerances in verification artifacts.
- If an imported report contains values that must become official inputs, convert them into BookInput fields with provenance and reviewer confirmation.

## Export Package Contents

| Path | Required | Notes |
| --- | --- | --- |
| data_package_manifest.yaml | true | Package inventory and hashes. |
| inputs/final_input.json | true for final | Exact normalized BookInput. |
| inputs/draft_input.json | optional | Exploratory or review input. |
| results/book_result.json | true when calculated | Exact BookResult. |
| reports/ | optional | HTML/PDF/DOCX/XLSX outputs. |
| traces/ | optional | Formula/source trace exports. |
| logs/ | optional | Run logs and validation summaries. |

## Validation Summary

| Check | Status | Evidence | Notes |
| --- | --- | --- | --- |
| manifest present or generated | to_be_defined | data_package_manifest.yaml |  |
| file hashes recorded | to_be_defined | manifest |  |
| inputs normalized to BookInput | to_be_defined | normalized cases |  |
| imported reports classified | to_be_defined | report import records |  |
| no formulas in imported UI/report files | to_be_defined | review |  |

