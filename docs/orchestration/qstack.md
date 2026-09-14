# Qstack quant-development orchestration for ChronForge

ChronForge is the **implementation/runtime repository**. Qstack is the **quant-development orchestration authority** for ChronForge. Qstack composes quant-domain constraints and verification profiles over upstream pstack engineering workflow/orchestration primitives rather than duplicating them.

## Ownership

```text
ChronForge
  owns source code / tests / runtime receipts / issues / PRs

qstack
  owns quant-development composition:
    intent routing
    QuantDomainOverlay
    QD CapabilityProfile
    VerificationProfile
    ChronForge ProjectProfile

upstream pstack
  remains the generic engineering-workflow substrate used by qstack:
    feature/refactor/investigation/review/shipping mechanics
    development orch bookkeeping
    worktree/branch/PR execution conventions

qorch
  owns quant-research orchestration only after a verified software artifact exists

hftbacktest
  external authoritative microstructure kernel/reference

Titan
  pinned reference evidence only
```

No qstack/qorch/pstack code or state is permitted on the ChronForge synchronous runtime hot path.

## Pinned semantic baseline

ChronForge binds its initial deterministic-runtime development contract to:

- qstack merged runtime recomposition: `tommy-ca/qstack#141`
- qstack merge commit: `6d124b93b6008851c1fc48aaef5ef6a20d6535b6`
- Titan evidence: `dominolu/titan@3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024`
- hftbacktest evidence/kernel baseline: `tommy-ca/hftbacktest@058cfefd9740b6857bb875bad4d5e6547a88379a`

A newer qstack revision may replace the baseline only after compatibility review; the issue/PR evidence must name the revision actually used.

## Composition rule

For every ChronForge development unit:

```text
BasePlaybook (upstream pstack)
  + QuantDomainOverlay (qstack)
  + CapabilityProfile (qstack QD-xx)
  + VerificationProfile (qstack)
  + ChronForge ProjectProfile
  -> ChronForge implementation PR + evidence receipt
```

ChronForge issues describe **what quant-system contract must hold**. They do not restate generic worker spawning, branch/worktree mechanics, review loops, or shipping procedure already owned by pstack/qstack composition.

## D0-D6 qstack mapping

| Phase | Qstack development composition |
|---|---|
| O0 | qstack orchestration binding / ProjectProfile |
| D0 | QD-15 migration-refactor + `deterministic-runtime-audit` |
| D1 | QD-06 backtest-engine + `formal-state-model` + `replay-parity` |
| D2 | QD-05 replay-engine + QD-06 + `deterministic-runtime-audit` + `replay-parity` |
| D3 | QD-16 strategy-runtime + `strategy-runtime-contract` + `replay-parity` |
| D4 optional | QD-16 with FFI capability explicitly selected |
| D5 optional | QD-01 market-data-adapter + QD-10 execution-adapter + `bounded-hot-paths` |
| D6 optional | QD-08 OMS / QD-09 EMS / QD-13 deployment only for explicitly selected capabilities |

## Recursive execution graph

```text
#10 O0 qstack binding
  -> #2 D0
      #11 pin/evidence -------+
      #12 kernel inventory ---+--> #14 D0.J
      #13 baseline goldens ---+
            |
            v
      #3 D1
      #15 ids/units ----------+
      #16 phase/order --------+
      #17 execution state ----+--> #19 D1.J
      #18 result/receipts ----+
            |
            v
      #4 D2
      #20 dependency/market --+
      #21 command bridge -----+
      #22 execution projection+--> #24 D2.J
      #23 100-run determinism +
            |
            v
      #5 D3
      #25 RuntimeEvent -------+
      #26 Strategy/Context ---+
      #27 runtime loop -------+--> #29 D3.J
      #28 artifact/qorch -----+
            |
            +--> #6 D4 optional
            +--> #7 D5 optional --> #8 D6 optional
```

Only accepted join receipts advance the next phase.

## Evidence envelope

Every merged implementation unit should provide, directly or through its PR/receipt:

```text
ChronForge issue/PR reference
ChronForge source revision
qstack semantic/profile revision
qstack capability/verification profiles applied
parent receipt digest(s)
acceptance IDs claimed
verification commands + results
fixture/corpus/config/model identities where relevant
artifact/result digest(s)
known limitations / unavailable evidence / discrepancies
```

Static/Metadata/CI evidence must not be described as Runtime/PAPER/LIVE evidence.

## Development -> research boundary

After D3.J (or selected optional phases), ChronForge emits immutable artifacts:

```text
SoftwareArtifactRef
RunReceipt
DeterminismReceipt
```

Qorch may reference those artifacts from a `ResearchProgram`, `Study`, `ResearchDagUnit`, `ExperimentRun`, validation record, or promotion decision.

Qorch MUST NOT mirror ChronForge development state such as worktrees, branches, PR status, or worker assignment.

```text
qstack-governed ChronForge development
  -> verified SoftwareArtifactRef
  -> qorch artifact dependency
  -> qorch program-ready
  -> research agent/SearchRunner
  -> ChronForge RunReceipt
  -> qorch evidence/candidate/promotion state
```

If research reveals a missing runtime capability, the change returns to ChronForge through qstack quant-development orchestration and later re-enters qorch as a new immutable artifact revision.

## Current frontier

- O0: issue #10 — documentation/profile binding.
- D0: issue #2.
- Leaf work currently available for read-only characterization: #11 and #12.
- D0 implementation claims must be joined by #14 before D1 becomes READY.
- D1-D3 remain blocked by their preceding join gates.
- D4-D6 are not part of the mandatory MVP and require explicit selection.
