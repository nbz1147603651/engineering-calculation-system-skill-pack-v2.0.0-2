---
name: batch-import-export-packages
description: Design and implement managed import/export, uploaded calculation packages, prior report import, hashes, manifests, CLI/API batch execution, saved normalized inputs, saved BookResult JSON, report exports, and batch summaries for engineering calculation books. Use when building repeatable package, data exchange, or batch workflows over trusted run_book() results.
---

# Batch, Import/Export, and Upload Packages

## When to use

When the task involves data packages, imported reports, export bundles, batch runs, or automated
case processing. Make inputs/results/reports/review artifacts portable and repeatable without
moving formulas into data files or batch scripts. The `run_book()` contract and static-HTML guard
live in `shared/lifecycle.md`.

## Steps

1. Set up the managed data area (`templates/implementation/import_export_contract.md`):
   `data/{input,imported/reports,imported/references,staging,normalized/cases,packages}`;
   `outputs/{results_json,reports_html,reports_pdf,reports_docx,upload_packages,logs}`.
2. Implement the upload-package flow: upload ZIP/files → store in `data/staging/` → compute hashes
   and inspect manifest → classify inputs/reports/references/outputs → normalize accepted inputs
   into `BookInput` JSON → show validation and diff summary → `run_book` only after case selection
   or batch approval → save `BookResult` JSON → render requested reports → export package with
   manifest and hashes. Imported reports are review artifacts (comparison/regression evidence)
   only — they never inject formulas or override official status.
3. Implement the batch flow (`templates/implementation/batch_flow.md`): read `batch_control.csv`
   or package manifest → load case input → validate → `run_book()` → save normalized input JSON →
   save `BookResult` JSON → render report if requested → write batch summary CSV/HTML → export
   upload package if requested → write logs.
4. Enforce manifest & hash rules (`templates/implementation/data_package_manifest.yaml`): every
   package records package id, schema version, created timestamp, project/book name, input/result/
   report files + hashes, runner version, template version, source-basis references, validation
   status, known limitations. Do not accept a package as trusted if required hashes, runner
   version, source basis, or validation status are missing.
5. Keep CLI/API endpoints thin: they may load manifests, validate files/hashes, normalize
   `BookInput`, call `run_book()`, save `BookResult`, render reports, write summaries, export
   packages. They must NOT implement formulas, recalculate pass/fail, silently override saved
   final inputs, hide warnings/errors, or treat imported reports as source of truth.

## Artifacts

```text
implementation/04_interfaces/import_export_contract.md   (templates/implementation/import_export_contract.md)
implementation/04_interfaces/batch_flow.md               (templates/implementation/batch_flow.md)
data/{input,imported,staging,normalized/cases,packages}/...
outputs/{results_json,reports_*,upload_packages,logs}/...
data_package_manifest.yaml  (templates/implementation/data_package_manifest.yaml)
```

## Exit gate

Batch uses `run_book` once per case; reproducible inputs exist. See `shared/lifecycle.md` row 12c.
Next path: 13 for verification.
