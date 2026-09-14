# ChronForge

**ChronForge** is a deterministic event-time trading runtime built from proven microstructure primitives.

It recomposes selected Titan scheduling / execution-domain / strategy-runtime contracts around the authoritative external `hftbacktest` microstructure kernel — without vendoring Titan, without moving qstack/qorch into the runtime, and without building a second matching engine.

> **Soft≠green honesty:** this repository is still early-stage. Static/Metadata/`cargo check` evidence is not Runtime/PAPER/LIVE PASS.

## Project ownership

| Surface | Owner | Role |
|---|---|---|
| Product implementation | `tommy-ca/chronforge` | engine/runtime/live code, tests, issues, PRs, receipts |
| Quant-development orchestration | `tommy-ca/qstack` | quant intent, QD capability profiles, verification profiles, ChronForge ProjectProfile |
| Generic engineering mechanics | upstream pstack via qstack | base playbooks, development orch/workflow mechanics, review/shipping conventions |
| Quant-research orchestration | qstack `qorch` | ResearchProgram/Study/ResearchDagUnit readiness/evidence after artifact handoff |
| Microstructure kernel | `tommy-ca/hftbacktest` (external) | depth, processors, queue/latency/fee/fill behavior |
| Reference evidence | `dominolu/titan` | deterministic phase/execution/runtime/live-service semantics to selectively recompose |

ChronForge runtime code has **no dependency on qstack, qorch, pstack, LLMs, MCP, or research orchestration**.

## Quant-development orchestration

ChronForge enters development through qstack:

```text
ChronForge issue / development intent
  -> qstack intent/domain dispatch
  -> QuantDomainOverlay
  -> QD CapabilityProfile + VerificationProfile
  -> ChronForge ProjectProfile
  -> upstream pstack BasePlaybook/orch mechanics
  -> ChronForge branch / PR / evidence receipt
```

See [docs/orchestration/qstack.md](docs/orchestration/qstack.md).

The initial qstack semantic baseline is the merged runtime recomposition specification:

- `tommy-ca/qstack#141`
- merge `6d124b93b6008851c1fc48aaef5ef6a20d6535b6`

## Architecture boundaries

```text
external hftbacktest kernel
        |
        v
crates/hbt-engine
  deterministic domain / scheduler / execution / account / result
        |
        v
crates/hbt-runtime
  RuntimeEventSource / native strategy runtime / receipts
        |
        +----> optional FFI host
        |
        +----> optional crates/hbt-live
                    |
                    +----> optional OMS/EMS/EventLedger/reconciliation
```

Dependency law:

```text
hbt-live (optional)
   |-> hbt-runtime
   `-> hbt-engine

hbt-runtime -> hbt-engine
hbt-engine  -> pinned external hftbacktest dependency
```

Forbidden:

```text
hftbacktest -> ChronForge
ChronForge runtime -> qstack/qorch/pstack
runtime hot path -> LLM/MCP/database/research orchestration
```

## Recursive implementation roadmap

Program tracker: [#1](https://github.com/tommy-ca/chronforge/issues/1)  
Qstack orchestration binding: [#10](https://github.com/tommy-ca/chronforge/issues/10)

```text
O0 qstack binding
  -> D0 characterize/freeze hftbacktest
      -> D1 deterministic engine contracts
          -> D2 hftbacktest integration adapter
              -> D3 native strategy runtime
                  +-> D4 optional FFI
                  +-> D5 optional live
                        -> D6 optional governance/recovery
```

Mandatory MVP = **O0 -> D0 -> D1 -> D2 -> D3**.

Each mandatory phase is recursively decomposed into leaf issues plus a join gate:

| Phase | Parent | Leaf work | Join |
|---|---:|---|---:|
| O0 qstack binding | #10 | orchestration/profile contract | #10 |
| D0 baseline | #2 | #11, #12, #13 | #14 |
| D1 engine contracts | #3 | #15, #16, #17, #18 | #19 |
| D2 kernel integration | #4 | #20, #21, #22, #23 | #24 |
| D3 native runtime | #5 | #25, #26, #27, #28 | #29 |
| D4 FFI | #6 | optional after D3.J | conditional |
| D5 live | #7 | optional after D3.J | conditional |
| D6 governance | #8 | optional after D5 | conditional |

Full graph: [docs/roadmap/D0-D6.md](docs/roadmap/D0-D6.md).

### Current frontier

- #10 O0 is READY.
- #2 D0 is READY for read-only characterization.
- #11 and #12 can start immediately; #13 follows the pin receipt.
- #14 is the D0 join gate.
- D1-D3 remain blocked by preceding join receipts.
- D4-D6 are not selected by default.

## Qstack profile map

| Phase | Qstack composition |
|---|---|
| D0 | QD-15 migration/refactor + `deterministic-runtime-audit` |
| D1 | QD-06 backtest-engine + `formal-state-model` + `replay-parity` |
| D2 | QD-05 replay-engine + QD-06 + `deterministic-runtime-audit` + `replay-parity` |
| D3 | QD-16 strategy-runtime + `strategy-runtime-contract` + `replay-parity` |
| D4 | QD-16 with FFI selected |
| D5 | QD-01 + QD-10 + `bounded-hot-paths` |
| D6 | QD-08/QD-09/QD-13 only when governance/recovery is explicitly selected |

## Development -> research handoff

A verified ChronForge build emits:

```text
SoftwareArtifactRef
RunReceipt
DeterminismReceipt
```

Those immutable artifacts may then become qorch research dependencies:

```text
qstack-governed ChronForge development
  -> verified artifact
  -> qorch ResearchProgram / Study
  -> qorch program-ready
  -> research agent / SearchRunner
  -> ChronForge RunReceipt
  -> qorch validation / candidate / promotion evidence
```

Qorch does not mirror ChronForge worktrees, branches, PR state, or developer-agent assignments.

## Evidence pins

| Source | Revision | Role |
|---|---|---|
| qstack | `6d124b93b6008851c1fc48aaef5ef6a20d6535b6` | initial quant-development semantic baseline |
| Titan | `3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024` | reference evidence for scheduler/execution/runtime/live services |
| hftbacktest | `058cfefd9740b6857bb875bad4d5e6547a88379a` | external authoritative microstructure kernel baseline |

These are evidence/dependency pins, not an allowlist of future compatible revisions.

## Docs

- [Qstack orchestration](docs/orchestration/qstack.md)
- [Recursive roadmap](docs/roadmap/D0-D6.md)
- [Architecture boundaries](docs/architecture/boundaries.md)

## License

Apache-2.0 — see [LICENSE](LICENSE).
