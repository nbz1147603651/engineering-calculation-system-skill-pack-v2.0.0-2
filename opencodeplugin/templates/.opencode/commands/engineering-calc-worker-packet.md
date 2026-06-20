---
description: Draft a worker result packet for delegated engineering calculation work
agent: build
---

Prepare an Engineering Calculation System worker result packet for:

```text
$ARGUMENTS
```

If available, call `engineering_calc_orchestration` with strict JSON object arguments `{"artifact":"agent_result_packet","phase":"implementation"}`.

The worker packet must record changed paths, artifacts created, IDs touched, assumptions, open questions, validation results, merge notes, requested shared-file changes, conflicts, and supervisor actions needed.

Workers must only edit declared `owned_paths` and must not make gate, source authority, ID allocation, public API contract, production/release, or final acceptance decisions.
