# Architecture Soft≠green

ChronForge architecture docs **cite** qstack composition contracts Soft≠green. They do not invent new EventKey / EventPhase / acceptance contracts.

## Contents

- [boundaries.md](./boundaries.md) — allowed / forbidden dependency directions; EventKey / EventPhase cite
- [runtime-recomposition/D0-pin-receipt.json](./runtime-recomposition/D0-pin-receipt.json) — #11 machine-readable provenance, exact dependency mode and drift policy; Metadata/Static only
- [runtime-recomposition/D0-baseline.md](./runtime-recomposition/D0-baseline.md) — D0 kernel vs overlay map Soft≠green (R-D0-02)
- [runtime-recomposition/D0-baseline-receipt.json](./runtime-recomposition/D0-baseline-receipt.json) — legacy aggregate D0 characterization receipt; `live_pass: false`; #14 remains the sole phase join

## Layers (summary)

1. **Kernel** — external `hftbacktest` (authoritative microstructure). Remains independently buildable Soft≠green (A-UP-001).
2. **Engine** — `hbt-engine` deterministic domain (scheduler, execution, account, funding, risk, result, adapters).
3. **Runtime** — `hbt-runtime` strategy loop; optional `abi` feature empty Soft≠green.
4. **Live** — optional `hbt-live` deferred until D5 Soft≠green.

## Soft≠green honesty

Scaffold stubs ≠ Runtime PASS. Static/Metadata ≠ LIVE_PASS. Timeout ≠ PASS.

`D0PinReceipt` only satisfies #11 when its dedicated verifier passes. It unblocks #12 verification and #13 start, but it does **not** accept #14. The old aggregate D0 receipt is source evidence for decomposition, not a substitute for the #11/#12/#13 child receipts plus #14 join.

Do not wire `hbt-engine` → `hftbacktest` during D0. The selected D2 dependency mode is an exact Git revision; floating branches/tags are forbidden.
