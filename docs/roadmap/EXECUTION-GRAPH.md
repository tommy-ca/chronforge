# ChronForge execution graph

This is the canonical development graph tying OpenSpec intent, qstack quant-development composition, pstack execution mechanics, ChronForge issues/PRs, and qorch research handoff together.

## Control flow

```text
USER / PROJECT INTENT
        |
        v
OpenSpec active change
proposal -> specs -> design -> ADR -> tasks
        |
        | intent/spec merge to main
        v
qstack ChronForge ProjectProfile
+ QD CapabilityProfile
+ VerificationProfile
        |
        v
upstream pstack BasePlaybook / orch mechanics
        |
        v
ChronForge leaf issue(s) / PR(s)
        |
        v
phase join gate + evidence receipt
        |
        | implementation merge
        v
OpenSpec strict verify + archive
        |
        v
living spec + SoftwareArtifactRef / RunReceipt / DeterminismReceipt
        |
        +---------------------------> qorch ResearchProgram when research is requested
```

## Harness bootstrap H0

```text
#33 H0 intent-driven development harness
  |
  +-> #34 H0.1 intent/spec boundary ---------------- COMPLETE
  |     PR #37 -> 07a0eb52b6af5b440a9816e42b984576e87a3610
  |
  +-> #35 H0.2 repo-local harness ------------------ ACTIVE
  |     AGENTS / OpenSpec config / docs / CI
  |
  +-> #36 H0.3 strict verify + archive ------------- BLOCKED on H0.2
  |
  `-> H0 closes only after living-spec read-back
```

H0 configures development control-plane behaviour only. It does not establish Runtime/PAPER/LIVE evidence for the trading engine.

## Runtime program — actual current state

PR #32 landed substantial D0 characterization and archived the D0 OpenSpec change, but the recursive child/join graph predates that PR and was not reconciled. The parent #2 auto-closed while #11-#14 remain open. Therefore **D1 is not yet graph-ready**.

```text
#1 ChronForge runtime implementation program
  |
  +-> O0 qstack binding -------------------------------- COMPLETE
  |     #10 / PR #31 / e74dd7ea0dec315b84331fbc0bb941f3a2f9390f
  |
  +-> D0 characterization apply ------------------------ LANDED, JOIN PENDING
  |     #2 parent auto-closed by PR #32
  |     PR #32 / 500e58899ed16d3c2c866c580a8f80e38276373b
  |     archived OpenSpec: 2026-09-14-chronforge-d0-baseline
  |     |
  |     +-> #11 pin/dependency/provenance -------------- OPEN
  |     +-> #12 seam inventory ------------------------- OPEN
  |     +-> #13 executable baseline/goldens ------------ OPEN
  |     `-> #14 D0.J join ------------------------------ OPEN / REQUIRED
  |             |
  |             `-> accepted D0 join receipt unlocks D1
  |
  +-> D1 deterministic engine contracts ---------------- BLOCKED on #14
  |     #3
  |       #15 IDs / units / model identities -----------+
  |       #16 EventPhase / EventKey --------------------+--> #19 D1.J
  |       #17 commands / reports / OrderState ----------+
  |       #18 account / result / receipts --------------+
  |                                                      |
  |                       accepted D1 join receipt ------+
  |                                      |
  +--------------------------------------v
  +-> D2 hftbacktest integration adapters -------------- BLOCKED
  |     #4
  |       #20 dependency + market normalization --------+
  |       #21 command -> kernel processors -------------+--> #24 D2.J
  |       #22 outcomes -> canonical facts --------------+
  |       #23 100-run determinism ----------------------+
  |                                      |
  +--------------------------------------v
  +-> D3 deterministic native strategy runtime --------- BLOCKED
  |     #5
  |       #25 RuntimeEvent / RuntimeEventSource --------+
  |       #26 Strategy / StrategyContext ---------------+--> #29 D3.J
  |       #27 runtime loop / callback serialization ----+
  |       #28 artifact / qorch handoff -----------------+
  |                                      |
  |                                      +--> mandatory MVP complete
  |
  +-> D4 FFI/Python host ------------------------------- OPTIONAL / explicit selection
  |     #6
  |
  +-> D5 bounded live core ----------------------------- OPTIONAL / explicit selection
  |     #7
  |       |
  |       `-> D6 OMS/EMS/EventLedger/recovery ---------- OPTIONAL / capability selected
  |             #8
  |
  `-> verified artifact handoff -> qorch research
```

## Current runtime frontier

After H0 harness setup, finish the D0 recursive contract before starting D1 implementation:

```text
#11 complete pin/dependency/provenance receipt -------+
#12 complete machine-readable seam inventory ---------+--> #14 D0.J
#13 complete baseline-test/golden artifact -----------+
                                                       |
                                                       v
                                               D1 becomes READY
```

PR #32 already provides strong input evidence for all three leaves. Reuse that evidence; do not redo the characterization from scratch. Close each leaf only when its own acceptance criteria are explicitly satisfied, then accept #14 as the single phase gate.

## Intent rule for every D-phase

D0 historical work already used OpenSpec. D1 onward MUST bind material implementation to an OpenSpec change before normal apply.

Recommended granularity:

| Work shape | OpenSpec granularity |
|---|---|
| one coherent phase with tightly coupled leaves | one phase change, leaf tasks map to issues |
| independent capability that can ship/revert alone | separate change |
| read-only investigation | no product change until implementation is selected |
| emergency mitigation | explicit exception + retrospective reconciliation |

Do not create one OpenSpec change per trivial line-level task. OpenSpec captures durable intent/behaviour; issues capture execution state.

## D1 intent graph — prepared but blocked

Once #14 is accepted, create/land a D1 change such as:

```text
OpenSpec: chronforge-d1-engine-contracts
  proposal
  specs:
    deterministic-ordering
    execution-domain
    account-result-receipts
  design
  ADR review
  tasks
    -> #15
    -> #16
    -> #17
    -> #18
    -> #19 join verification
```

Qstack composition:

```text
QD-06 backtest-engine
+ formal-state-model
+ replay-parity
+ deterministic-runtime-audit
```

Pstack execution:

```text
/poteto-mode
  -> feature / multi-phase-plan / orchestrate as appropriate
  -> leaf worktrees/PRs
  -> review/verification
  -> join acceptance
```

## Evidence gates

```text
Intent/spec gate
  accepted OpenSpec artifacts on main

Leaf gate
  issue-specific tests/evidence

Join gate
  cross-leaf invariants + receipt

Merge gate
  implementation PR/stack verified

Archive gate
  strict OpenSpec validation after implementation merge

Research gate
  immutable SoftwareArtifactRef / RunReceipt / DeterminismReceipt available
```

Evidence classes remain distinct: Static, Metadata, formal/property, Runtime, PAPER, LIVE.

## Project-state rule

Only ChronForge owns implementation issue/PR state. OpenSpec tasks and qstack/pstack orchestration reference that state; they do not duplicate it. Qorch does not receive development branches, worktrees, PR status, or worker assignment.
