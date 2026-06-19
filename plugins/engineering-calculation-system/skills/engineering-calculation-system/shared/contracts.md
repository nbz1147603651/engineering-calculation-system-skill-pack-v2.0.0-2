# Shared Lifecycle Contracts

## Full lifecycle

```text
user request
-> material state classification
-> reference adequacy assessment
-> reference discovery and acquisition
-> local evidence library
-> source intake and authority
-> calculation logic blueprint
-> formula / lookup / branch extraction
-> implementation handoff contract
-> calculation book architecture
-> core and data models
-> reusable calculation modules
-> book runner and governing summary
-> report / review / batch interfaces
-> verification / regression / traceability
```

## Hard handoffs

```text
references/acquisition/acquisition_handoff.yaml
```

connects acquisition to analysis.

```text
handoff/implementation_handoff.yaml
```

connects analysis to implementation.

## Source principle

A calculation rule is not implementation-ready until its source, applicability, units, branch behavior, and test requirement are explicit or its uncertainty is recorded.

## Software principle

Engineering formulas belong in reusable calculation modules and official book runners only. Interfaces and reports consume results; they do not calculate.
