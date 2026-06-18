# Module Interface Specification

Use this template for decoupled reusable calculation modules that can become long-lived engineering assets.

## Module identity

| Item | Value |
| --- | --- |
| module_id | to_be_defined |
| domain | to_be_defined |
| category | to_be_defined |
| reuse_status | draft / reviewed / stable / deprecated |

## Public functions

## Input models

## Options models

## Result models

## Formula traces

## Warning/error behavior

## Dependency boundary

```text
no UI dependency
no report dependency
no batch-specific dependency
no deployment dependency
no file I/O unless explicitly classified as a lookup-data loader
```

## Asset registry row

Record this module in `module_asset_registry.csv`.
