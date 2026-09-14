# Deterministic engine

## Sub-features

- canonical IDs/units/model identities;
- versioned `EventPhase` / `EventKey` ordering;
- command/report/order-state contracts;
- account/result projections;
- replay parity and 100-run deterministic equality.

## How to get to it (user POV)

This surface is implemented through D1 and D2. Until their join gates land, there is no executable engine verification claim.

## Driving it with ChronForge verification tools

Current behavior is intentionally blocking:

```bash
bash tools/verify/verify.sh d1
bash tools/verify/verify.sh d2
```

Both must return `BLOCKED` until D1/D2 add the named executable levers. When canonical-output commands exist, use `repeat_hash.py` only on those canonical outputs.

## Gotchas

- Compilation is not deterministic replay proof.
- Aggregate PnL equality is insufficient for semantic replay parity.
- Do not change expected goldens merely to make a refactor pass; record an explicit semantic migration/discrepancy.
- The qstack `formal-state-model`, `deterministic-runtime-audit`, and `replay-parity` skills define quant semantics; this local map does not duplicate them.
