# Qstack quant-development orchestration for ChronForge

ChronForge is the implementation/runtime repository. Qstack is the project-facing **quant-development orchestration/composition authority**. Qstack adds quant-domain constraints and verification profiles over upstream pstack engineering workflow/orchestration primitives rather than duplicating them.

OpenSpec is the durable intent layer in front of that composition. See [intent-driven development](intent-driven-development.md).

## Ownership

```text
OpenSpec
  owns proposal / specs / design / ADR review / tasks

ChronForge
  owns source code / tests / runtime receipts / issues / branches / PRs

qstack
  owns quant-development composition:
    intent/domain classification
    QuantDomainOverlay
    QD CapabilityProfile
    VerificationProfile
    ChronForge ProjectProfile

upstream pstack
  owns generic engineering workflow/orchestration mechanics used under qstack:
    investigation/feature/refactor/review/shipping mechanics
    orch / multi-phase / worktree / branch / PR execution conventions

qorch
  owns quant-research orchestration only after a verified immutable artifact exists

hftbacktest
  external authoritative microstructure kernel/reference

Titan
  pinned reference evidence only
```

No OpenSpec/qstack/qorch/pstack code or state is permitted on the ChronForge synchronous runtime hot path.

## Pinned semantic baseline

ChronForge currently references:

- qstack runtime recomposition merge: `tommy-ca/qstack#141` / `6d124b93b6008851c1fc48aaef5ef6a20d6535b6`;
- qstack ChronForge ProjectProfile merge: `tommy-ca/qstack#150` / `cf4e62f4ef98fe378393fa3adff8449ff9457024`;
- upstream pstack host repo: `cursor/plugins@be432a96ed36e48d05f44bf375864355f62263f9`, subtree `pstack/`;
- Titan evidence: `dominolu/titan@3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024`;
- hftbacktest baseline: `tommy-ca/hftbacktest@058cfefd9740b6857bb875bad4d5e6547a88379a`.

A newer revision may replace a baseline only after compatibility review. The active OpenSpec proposal/PR evidence must name the revision actually used.

## Composition rule

For material ChronForge development:

```text
Accepted OpenSpec intent
  + BasePlaybook (upstream pstack)
  + QuantDomainOverlay (qstack)
  + CapabilityProfile (qstack QD-xx)
  + VerificationProfile (qstack)
  + ChronForge ProjectProfile
  -> ChronForge issue/worktree/PR + evidence receipt
  -> join gate
  -> merge
  -> OpenSpec archive
```

ChronForge issues describe project execution and quant-system contracts. They do not restate generic worker spawning, branch/worktree mechanics, review loops, or shipping procedure already owned by pstack/qstack composition.

## D0-D6 qstack mapping

| Phase | Qstack development composition |
|---|---|
| D0 | QD-15 migration-refactor + `deterministic-runtime-audit` |
| D1 | QD-06 backtest-engine + `formal-state-model` + `replay-parity` |
| D2 | QD-05 replay-engine + QD-06 + `deterministic-runtime-audit` + `replay-parity` |
| D3 | QD-16 strategy-runtime + `strategy-runtime-contract` + `replay-parity` |
| D4 optional | QD-16 with FFI capability explicitly selected |
| D5 optional | QD-01 market-data-adapter + QD-10 execution-adapter + `bounded-hot-paths` |
| D6 optional | QD-08 OMS / QD-09 EMS / QD-13 deployment only for explicitly selected capabilities |

## Recursive execution rule

Every material phase uses leaf work plus one acceptance join:

```text
accepted OpenSpec intent
  -> leaf issues / PRs
  -> phase join receipt
  -> next phase READY
```

Canonical graph: [docs/roadmap/EXECUTION-GRAPH.md](../roadmap/EXECUTION-GRAPH.md).

Current runtime state is intentionally conservative:

- O0 qstack binding is complete.
- PR #32 landed a D0 characterization receipt and archived the D0 OpenSpec change.
- #11, #12, #13 and join #14 remain open; PR #32 itself states D1 remains blocked on #14.
- D1 #3 is therefore **BLOCKED**, not READY.
- D2-D3 are blocked by their preceding join gates.
- D4-D6 require explicit capability selection.

## Evidence envelope

Every merged implementation unit should provide, directly or through its PR/receipt:

```text
active/archived OpenSpec change
ChronForge issue/PR reference
ChronForge source revision
qstack semantic/profile revision
qstack capability/verification profiles applied
pstack playbook/orchestration shape used
parent receipt digest(s)
acceptance IDs claimed
verification commands + results
evidence class
fixture/corpus/config/model identities where relevant
artifact/result digest(s)
known limitations / unavailable evidence / discrepancies
```

Static/Metadata/CI evidence must not be described as Runtime/PAPER/LIVE evidence.

## Development -> research boundary

After D3.J or selected optional phases, ChronForge emits immutable artifacts:

```text
SoftwareArtifactRef
RunReceipt
DeterminismReceipt
```

Qorch may reference those artifacts from research program/study/experiment/validation/promotion state. Qorch MUST NOT mirror ChronForge worktrees, branches, PR status, or development-worker assignment.

```text
OpenSpec + qstack-governed ChronForge development
  -> verified SoftwareArtifactRef
  -> qorch artifact dependency
  -> qorch program-ready
  -> research agent/SearchRunner
  -> ChronForge RunReceipt
  -> qorch evidence/candidate/promotion state
```

If research reveals a missing runtime capability, the change returns to ChronForge through a new OpenSpec intent and qstack development composition, then later re-enters qorch as a new immutable artifact revision.
