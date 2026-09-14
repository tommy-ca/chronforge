# Design — chronforge-d0-baseline

## Context

Scaffold stubs at `1c8ee86c`. Kernel lives in external `tommy-ca/hftbacktest` @ `058cfefd`. D1 blocked.

## Goals

- Frozen pin + ownership map + golden inventory + hash receipt
- Additive plan; Titan evidence-only

## Non-Goals

D1–D6 code; Titan import; matching engine; qorch in kernel; LIVE_PASS invent

## Decisions

### D1 Arena SKIP
Characterization uncontested.

### D2 Pin
Issue-cited SHA `058cfefd` (master tip at dig).

### D3 Propose vs Apply
This PR: OpenSpec + schema. Apply: docs/receipt/levers.

## Risks

| Risk | Mitigation |
|---|---|
| Pin drift | Receipt hash; refresh only via new Act-on |
| Overlay mistaken for kernel | Ownership map |

## Migration

Propose VALID → merge → APPLY GO → receipt → unlock D1.
