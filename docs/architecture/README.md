# Architecture Soft≠green

ChronForge architecture docs **cite** qstack composition contracts Soft≠green. They do not invent new EventKey / EventPhase / acceptance contracts.

## Contents

- [boundaries.md](./boundaries.md) — allowed / forbidden dependency directions; EventKey / EventPhase cite
- [runtime-recomposition/D0-baseline.md](./runtime-recomposition/D0-baseline.md) — D0 kernel vs overlay map Soft≠green (R-D0-02)
- [runtime-recomposition/D0-baseline-receipt.json](./runtime-recomposition/D0-baseline-receipt.json) — machine-readable pin + content hash Soft≠green (R-D0-01, R-D0-04); `live_pass: false`

## Layers (summary)

1. **Kernel** — external `hftbacktest` (authoritative microstructure). Remains independently buildable Soft≠green (A-UP-001).
2. **Engine** — `hbt-engine` deterministic domain (scheduler, execution, account, funding, risk, result, adapters).
3. **Runtime** — `hbt-runtime` strategy loop; optional `abi` feature empty Soft≠green.
4. **Live** — optional `hbt-live` deferred until D5 Soft≠green.

## Soft≠green honesty

Scaffold stubs ≠ Runtime PASS. Static/Metadata ≠ LIVE_PASS. Timeout ≠ PASS.
D0 receipt Soft≠green unlocks D1 consumption of pin/map; D1 graph remains BLOCKED on accepted #14 Soft≠green. Do not invent LIVE_PASS. Do not wire `hbt-engine` → `hftbacktest` until after receipt Soft≠green (hard Cargo dep still deferred Soft≠green).
