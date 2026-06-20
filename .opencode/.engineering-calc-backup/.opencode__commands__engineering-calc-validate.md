<!-- engineering-calc-opencode-managed -->
---
description: Run Engineering Calculation System validation diagnostics
agent: build
---

Call `engineering_calc_doctor` with strict JSON object arguments `{"mode":"verbose","validate":true}`.

Treat failed skill-root, schema-version, required-files, orchestration-template, Python validation, or project-template validation checks as blockers unless the user explicitly asks for a draft.
