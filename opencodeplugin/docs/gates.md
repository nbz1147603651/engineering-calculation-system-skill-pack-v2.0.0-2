# Engineering Gate Diagnostics

The "non-negotiable" rules of the Engineering Calculation System live in
the shared skill pack, especially `shared/lifecycle.md`,
`shared/multi-agent-orchestration.md`, and the lifecycle router. The
legacy gate files redirect readers to `shared/lifecycle.md`; the OpenCode
plugin exposes a diagnostic view of those rules, not a second governance
kernel.

## What is hard

The installer refuses targets inside:

- `plugins/engineering-calculation-system/`
- `engineering-calculation-system/core/`

Those paths belong to the Codex plugin and the shared core skill pack.
Install OpenCode assets at a project root instead.

## What is advisory

The gate diagnostics check for:

| Diagnostic | Meaning |
| --- | --- |
| `handoff-freeze` | `coding_go_no_go.md` indicates the handoff is frozen, so handoff files should not be edited casually. |
| `owned-paths` | An active parallel work plan exists and the target path is outside declared `owned_paths`. |
| `protected-registries` | The path looks like a supervisor-owned source/formula/lookup/branch/module registry. |
| `formula-in-presentation` | Presentation, UI, notebook, batch, or input content appears to contain formula logic. |
| `cross-platform-boundary` | The path is inside the Codex plugin or shared core skill pack. |

Use these diagnostics in `engineering_calc_gate_status`,
`engineering_calc_status`, doctor output, supervisor merge reviews, and
OpenCode permissions.

## Configuration

Plugin-specific config uses strict JSON:

```json
{
  "gates": {
    "enabled": true,
    "enforcement": "warn",
    "runtimeHook": false,
    "disable": []
  }
}
```

- `enforcement: "warn"` is the default advisory mode.
- `enforcement: "strict"` only matters when the experimental runtime hook
  is enabled.
- `runtimeHook: true` wires diagnostics into OpenCode's
  `tool.execute.before` hook. This is experimental and disabled by
  default.
- `disable` can opt out of named diagnostics for status and route output.

## Preferred enforcement path

Use OpenCode-native permissions for platform guardrails. The
`opencode-json` command emits a recommended `opencode.json` snippet with
conservative `edit`, `bash`, `external_directory`, `task`, and `skill`
permissions. Keep engineering authority decisions in the supervisor
workflow and verify work through the core skill templates and validation
scripts.
