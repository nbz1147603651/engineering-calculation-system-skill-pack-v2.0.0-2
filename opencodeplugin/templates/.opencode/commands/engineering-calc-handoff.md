---
description: Check engineering calculation handoff readiness before coding
agent: build
---

Use the Engineering Calculation System implementation handoff workflow for:

```text
$ARGUMENTS
```

If available, call `engineering_calc_route` with strict JSON object arguments `{"phase":"implementation-handoff"}`.

Review or create these artifacts before production coding:

```text
handoff/implementation_handoff.yaml
handoff/coding_go_no_go.md
handoff/artifact_index.yaml
```

Treat unresolved reference gaps, missing traceability, incomplete source authority decisions, or a blocked go/no-go state as coding blockers.
