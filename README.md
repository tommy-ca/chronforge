# ChronForge

**ChronForge** is a deterministic event-time trading runtime built from proven microstructure primitives.

It recomposes selected Titan scheduling / execution-domain / strategy-runtime contracts around the authoritative external `hftbacktest` microstructure kernel — without vendoring Titan, without moving qstack/qorch into the runtime, and without building a second matching engine.

> **Evidence honesty:** this repository is early-stage. Static/Metadata/`cargo check` evidence is not Runtime/PAPER/LIVE PASS. Timeout/skipped/unavailable checks are not PASS.

## Development control plane

ChronForge uses an intent-driven, qstack-governed development flow:

```text
intent
  -> OpenSpec proposal/specs/design/ADR/tasks
  -> qstack ChronForge ProjectProfile + QD/verification profiles
  -> upstream pstack BasePlaybook/orch mechanics
  -> ChronForge issues / branches / PRs / evidence
  -> phase join receipt
  -> implementation merge
  -> OpenSpec strict verify/archive
  -> immutable software/runtime artifacts
  -> qorch only when quant research begins
```

See:

- [AGENTS.md](AGENTS.md)
- [Intent-driven development](docs/orchestration/intent-driven-development.md)
- [Qstack orchestration](docs/orchestration/qstack.md)
- [Canonical execution graph](docs/roadmap/EXECUTION-GRAPH.md)

## Project ownership

| Surface | Owner | Role |
|---|---|---|
| Durable intent | OpenSpec in ChronForge | proposal/specs/design/ADR/tasks; living behaviour specs |
| Product implementation | `tommy-ca/chronforge` | engine/runtime/live code, tests, issues, PRs, receipts |
| Quant-development orchestration | `tommy-ca/qstack` | quant intent/domain composition, QD capability profiles, verification profiles, ChronForge ProjectProfile |
| Generic engineering mechanics | upstream pstack via qstack | base playbooks, orch/worktree/PR mechanics, review/shipping conventions |
| Quant-research orchestration | qstack `qorch` | ResearchProgram/Study/ResearchDagUnit readiness/evidence after immutable artifact handoff |
| Microstructure kernel | `tommy-ca/hftbacktest` (external) | depth, processors, queue/latency/fee/fill behaviour |
| Reference evidence | `dominolu/titan` | deterministic phase/execution/runtime/live-service semantics to selectively recompose |

ChronForge runtime code has **no dependency on OpenSpec, qstack, qorch, pstack, LLMs, MCP, or research orchestration**.

## Tooling setup

- Install/use upstream pstack in Cursor: `/add-plugin pstack`, then `/setup-pstack`; canonical engineering entry is `/poteto-mode`.
- Ensure the `tommy-ca/qstack` plugin/skills are available to the development agent; qstack overlays quant-domain constraints on pstack rather than replacing `/poteto-mode`.
- ChronForge already bundles the `intent-driven` OpenSpec schema. CI runs `npx --yes @fission-ai/openspec@1.13.0 validate --all --strict`.

The repository deliberately does **not** vendor pstack/qstack skills or the intent-driven template's OpenCode/Superpowers collaboration stack.

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
ChronForge runtime -> OpenSpec/qstack/qorch/pstack
runtime hot path -> LLM/MCP/database/research orchestration
```

## Recursive implementation roadmap

Program tracker: [#1](https://github.com/tommy-ca/chronforge/issues/1)

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

Each phase is recursively decomposed into leaf issues plus a single join gate. Full graph: [docs/roadmap/EXECUTION-GRAPH.md](docs/roadmap/EXECUTION-GRAPH.md).

### Current runtime frontier

PR #32 landed substantial D0 characterization and an archived D0 OpenSpec change, but the recursive D0 child/join graph is not yet complete:

- #11 — pin/dependency/provenance receipt: OPEN
- #12 — seam inventory: OPEN
- #13 — executable baseline/golden artifact: OPEN
- #14 — D0 join: OPEN and required
- D1 #3 remains BLOCKED until #14 is accepted

Reuse PR #32 evidence to finish those leaves; do not redo characterization unnecessarily.

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
OpenSpec + qstack-governed ChronForge development
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
| intent-driven template | `5673ba9799bc3c768ed499496de476f1f88666c5` | OpenSpec intent lifecycle reference |
| pstack host repo | `be432a96ed36e48d05f44bf375864355f62263f9` | generic engineering substrate (`pstack/`) |
| qstack runtime spec | `6d124b93b6008851c1fc48aaef5ef6a20d6535b6` | deterministic runtime recomposition baseline |
| qstack ChronForge profile | `cf4e62f4ef98fe378393fa3adff8449ff9457024` | project-specific development composition |
| Titan | `3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024` | reference evidence for scheduler/execution/runtime/live services |
| hftbacktest | `058cfefd9740b6857bb875bad4d5e6547a88379a` | external authoritative microstructure kernel baseline |

These are evidence/dependency pins, not an allowlist of future compatible revisions.

## Docs

- [Intent-driven development](docs/orchestration/intent-driven-development.md)
- [Qstack orchestration](docs/orchestration/qstack.md)
- [Canonical execution graph](docs/roadmap/EXECUTION-GRAPH.md)
- [D0-D6 roadmap](docs/roadmap/D0-D6.md)
- [Architecture boundaries](docs/architecture/boundaries.md)

## License

Apache-2.0 — see [LICENSE](LICENSE).
