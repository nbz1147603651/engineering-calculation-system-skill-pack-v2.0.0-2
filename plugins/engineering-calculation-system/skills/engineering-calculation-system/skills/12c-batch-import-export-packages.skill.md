---
name: batch-import-export-packages
description: Design and implement managed import/export, uploaded calculation packages, prior report import, hashes, manifests, CLI/API batch execution, saved normalized inputs, saved BookResult JSON, report exports, and batch summaries for engineering calculation books. Use when building repeatable package, data exchange, or batch workflows over trusted run_book() results.
---

# Batch, Import/Export, and Upload Packages

Use this skill when the task involves data packages, imported reports, export bundles, batch runs, or automated case processing.

## Goal

Make engineering calculation inputs, results, reports, and review artifacts portable and repeatable without moving formulas into data files or batch scripts.

## Managed Data Area

Use a predictable data layout:

```text
data/input/                  user-provided input files
data/imported/reports/       prior reports used for review or comparison
data/imported/references/    allowed project reference files
data/staging/                uploaded but not yet accepted files
data/normalized/cases/       normalized BookInput JSON per case
data/packages/               unpacked upload/export packages
outputs/results_json/        trusted BookResult JSON
outputs/reports_html/        generated HTML reports
outputs/reports_pdf/         generated PDF reports
outputs/reports_docx/        generated DOCX reports
outputs/upload_packages/     ZIP or folder packages ready to share/upload
outputs/logs/                run and validation logs
```

Use `templates/implementation/import_export_contract.md` and `templates/implementation/data_package_manifest.yaml`.

## Upload Package Flow

Required flow:

```text
upload ZIP or files
-> store in data/staging/
-> compute hashes and inspect manifest
-> classify inputs, reports, references, and outputs
-> normalize accepted inputs into BookInput JSON
-> show validation and diff summary
-> run_book only after case selection or batch approval
-> save BookResult JSON
-> render requested reports
-> export package with manifest and hashes
```

Imported reports are review artifacts. They may support comparison or regression evidence, but they must not inject formulas or override official status.

## Batch Flow

Use this sequence:

```text
read batch_control.csv or package manifest
-> load case input
-> validate
-> run_book()
-> save normalized input JSON
-> save BookResult JSON
-> render report if requested
-> write batch summary CSV/HTML
-> export upload package if requested
-> write logs
```

Use `templates/implementation/batch_flow.md`.

## Manifest and Hash Rules

Every package should record:

```text
package id
schema version
created timestamp
project/book name
input files and hashes
result files and hashes
report files and hashes
runner version
template version
source basis references
validation status
known limitations
```

Do not accept a package as trusted if required hashes, runner version, source basis, or validation status are missing.

## CLI/API Rules

Batch CLI and API endpoints may:

```text
load package manifests
validate files and hashes
normalize BookInput JSON
call run_book()
save BookResult JSON
render reports
write summaries
export packages
```

They must not:

```text
implement formulas
recalculate pass/fail status
silently override saved final inputs
hide warnings/errors
treat imported reports as source of truth
```

## Required Final Response

Provide:

```text
managed data paths
package manifest fields
import/export flow
batch sequence
hash and trust rules
created or updated artifacts
proof that batch/import layers do not calculate
smoke test
run command
```
