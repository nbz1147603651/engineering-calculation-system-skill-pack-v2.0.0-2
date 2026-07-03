---
name: engineering-calculation-router
description: Use when an engineering calculation request spans multiple stages or needs routing across references, logic extraction, implementation, reporting, verification, or deployment.
---

# Engineering Calculation Router

Use this ZCode entrypoint for lifecycle skill 00 of the Engineering Calculation
System plugin.

1. Read `../engineering-calculation-system/SKILL.md` for the canonical package
   contract and ZCode adapter.
2. Read `../engineering-calculation-system/skills/00-engineering-calculation-router.skill.md`.
3. Follow the router output and load only the parent and child files it selects.
4. Keep project artifacts, evidence, reports, and generated code in the active
   ZCode workspace, not in the plugin package.
