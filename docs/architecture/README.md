# Architecture Soft≠green

ChronForge architecture docs **cite** qstack composition contracts Soft≠green. They do not invent new EventKey / EventPhase / acceptance contracts.

## Contents

- [boundaries.md](./boundaries.md) — allowed / forbidden dependency directions; EventKey / EventPhase cite

## Layers (summary)

1. **Kernel** — external `hftbacktest` (authoritative microstructure). Remains independently buildable Soft≠green (A-UP-001).
2. **Engine** — `hbt-engine` deterministic domain (scheduler, execution, account, funding, risk, result, adapters).
3. **Runtime** — `hbt-runtime` strategy loop; optional `abi` feature empty Soft≠green.
4. **Live** — optional `hbt-live` deferred until D5 Soft≠green.

## Soft≠green honesty

Scaffold stubs ≠ Runtime PASS. Static/Metadata ≠ LIVE_PASS. Timeout ≠ PASS.
