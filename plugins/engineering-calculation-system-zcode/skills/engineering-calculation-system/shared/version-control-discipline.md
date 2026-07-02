# Version Control Discipline

Use this file before large skill-package changes, multi-platform release work, plugin sync, or
parallel implementation that can disturb existing user work.

## Workspace Card

Record:

```text
workspace_state:
branch_or_worktree:
dirty_paths:
baseline_validation:
owned_changes:
sync_targets:
finish_options:
```

## Isolation Rules

- Detect the current git state before large edits. If already in an isolated worktree or platform
  workspace, use it; do not create nested worktrees.
- For project-local worktrees, use `.worktrees/` or `worktrees/` only when the directory is ignored.
- Do not overwrite dirty generated or bundled files unless the sync command has a preview and the
  overwrite is intentional.
- Run baseline validation before broad changes when the existing state is expected to pass.

## Sync And Release Closure

For platform packages, keep core as the source of truth. Generated plugin, adapter, Qoder, QoderCN,
OpenCode, TRAE, AGENTS, and singlefile outputs must load the canonical shared docs rather than copy
full gate text.

Before claiming release completion:

- run the core validator and behavior runner
- run plugin/platform validators or type checks
- run release build smoke for all configured platform archives
- inspect the platform acceptance report
- report remaining dirty paths or blockers instead of calling the release complete
