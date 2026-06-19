# Status Semantics

| Status | Meaning | Typical Handling |
| --- | --- | --- |
| PASS | check satisfies the stated criterion | report normally |
| FAIL | check does not satisfy the criterion | expose as governing or blocking |
| WARNING | result exists but requires attention | preserve and report |
| ERROR | required calculation could not complete | block dependent result |
| NOT_APPLICABLE | check does not apply | omit from governing failure selection |
| NEEDS_CONFIRMATION | source or assumption must be confirmed | prototype only unless resolved |
| NOT_EVALUATED | calculation was not run | expose reason |

