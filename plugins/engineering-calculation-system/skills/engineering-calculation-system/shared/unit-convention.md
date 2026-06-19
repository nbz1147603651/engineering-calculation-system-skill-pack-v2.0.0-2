# Unit Convention

Default internal units:

```text
length: m
area: m2
volume: m3
force: kN
stress/pressure: kPa
unit_weight: kN/m3
moment: kNm
settlement/displacement: mm
angle_input: degree
angle_internal: radian
```

Rules:

```text
convert units at input boundaries
use internal units inside calculation modules
format units only at presentation boundaries
store unit metadata in public input/result models
reject ambiguous dimensional values
avoid mixing degree and radian fields
```
