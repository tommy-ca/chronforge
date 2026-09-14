# ChronForge execution graph

This is the canonical development graph tying OpenSpec intent, qstack quant-development composition, pstack execution mechanics, ChronForge issues/PRs, project verification levers, and qorch research handoff together.

Machine orchestration index: [`ISSUE-ORCHESTRATION.json`](ISSUE-ORCHESTRATION.json). Schema v2 covers program #1, phase coordinators #2-#5, optional capabilities #6-#8, and runtime leaves/joins #11-#29.

## Layered ownership

```text
OpenSpec
  durable intent: proposal -> specs -> design -> ADR review -> tasks
        |
        v
qstack-mode / development
  QuantDomainOverlay
  + QD CapabilityProfile
  + operation skills
  + VerificationProfile
  + ChronForge ProjectProfile
        |
        v
pstack /poteto-mode + pstack orch
  generic planning / dependency state / workers / worktrees / PRs / review / shipping
        |
        +--> swarm       independent coverage/fan-out
        +--> arena       competing candidate bakeoff + synthesis
        `--> interrogate readonly adversarial review
        |
        v
ChronForge issue / branch / PR
        |
        v
verify-chronforge project lever(s)
        |
        v
EvidenceReceipt -> parent join
        |
        v
implementation merge -> OpenSpec strict verify/archive -> living spec
        |
        `--> immutable SoftwareArtifactRef / RunReceipt / DeterminismReceipt -> qorch research when requested
```

Qstack is the project-facing quant-development composition layer; it does not clone pstack's generic engineering workflow. Pstack owns generic software-development mechanics. ChronForge owns implementation state and executable evidence. Qorch owns quant-research orchestration only after immutable artifact handoff.

Upstream `/orchestrate` remains an explicitly invoked Cursor workflow; ChronForge does not make it a build/runtime dependency. The issue graph and pstack orch state are sufficient durable project control.

## Recursive issue state machine

Schema v2 distinguishes work-start readiness from proof/handoff readiness:

```text
BLOCKED
  | dependencies.start_after satisfied
  v
INTENT_READY
  | governing OpenSpec intent/tasks accepted on main
  v
READY
  | qstack composition + pstack base playbook resolved
  v
ACTIVE
  | isolated issue/worker execution
  | dependencies.verify_after may still be pending for staged investigation
  v
SYNTHESIS          only when arena trigger fires
  v
REVIEW             interrogate when required
  | unresolved Act on -> ACTIVE
  v
VERIFY             requires all verify_after evidence
  | ISSUES  -> ACTIVE
  | BLOCKED -> BLOCKED
  ` PASS    -> HANDOFF
               |
               v
              DONE
```

`start_after` MUST be a subset of `verify_after`. A read-only issue may start before its final evidence dependencies arrive, but it cannot VERIFY or HANDOFF until `verify_after` is satisfied. For join nodes, `start_after == verify_after == all required child receipts`; closing child issues or merging their PRs is not sufficient evidence.

## Per-issue execution packet

Every covered issue has one authoritative machine row and one synchronized `Execution packet` view in its GitHub issue body. The packet contains:

1. **Staged dependencies** — `start_after[]` and `verify_after[]`.
2. **Intent gate** — OpenSpec change and task binding.
3. **Qstack composition** — `development` intent, exact QD profiles, operation skills, VerificationProfile and ChronForge ProjectProfile.
4. **Pstack execution** — BasePlaybook and pstack orch role; generic workflow bodies are upstream-owned.
5. **Swarm** — `none | partition | race | mixed`, independent slices and done predicate.
6. **Arena** — `skip | conditional | required | required-if-selected`, trigger and synthesis policy.
7. **Interrogate** — whether readonly adversarial review is required, its scope, and the `Act on` merge gate.
8. **Lever verification** — exact project command(s), evidence class, current proof status and smallest falsifier.
9. **Handoff** — typed evidence receipt and the node that consumes it.

The machine row is the source of truth. Generate a synchronized view with:

```bash
python3 tools/verify/render_issue_packet.py --issue 17
python3 tools/verify/render_issue_packet.py --check
```

### Swarm rule

Use swarm for independent coverage or an explicit race. Each slice receives a standalone brief, isolated writable state and a done predicate, then returns `PASS | ISSUES | BLOCKED` with evidence. Siblings do not coordinate through shared mutable files.

### Arena rule

Arena is conditional, not ceremonial. Use it when two or more plausible public API/data-model/adapter/runtime-loop shapes have meaningful lock-in cost. Candidates use the same contract/rubric, are cross-judged, one base is selected, useful ideas are grafted deliberately, and the synthesized artifact is verified. Proof/inventory tasks usually skip arena.

Planned arena-heavy nodes:

- #17 execution command/report/order-state design;
- #20 hftbacktest adapter boundary;
- #25 `RuntimeEventSource` ownership/lifetime API;
- #26 `Strategy` / `StrategyContext` public API;
- optional #6-#8 when selected and competing shapes remain.

### Interrogate rule

Interrogate is mandatory for every join and for leaves changing public contracts, deterministic ordering, state authority, command/fact semantics, callback ownership, recovery policy or dependency boundaries. It is readonly. Findings are classified `Act on | Consider | Noted | Dismissed`; unresolved `Act on` findings block merge. Interrogate never auto-applies changes.

### Lever rule

A completion claim needs the smallest rerunnable ChronForge-owned command capable of falsifying it. Narrative review, OpenSpec validation or compilation cannot substitute for Runtime/PAPER/LIVE evidence. Missing executable proof means verification remains `BLOCKED`, even when investigation work itself is READY/ACTIVE.

Current project verifier:

```bash
bash tools/verify/doctor.sh
bash tools/verify/verify.sh control-plane
bash tools/verify/verify.sh d0
bash tools/verify/verify.sh d1   # currently BLOCKED
bash tools/verify/verify.sh d2   # currently BLOCKED
bash tools/verify/verify.sh d3   # currently BLOCKED
```

`d4`-`d6` also remain BLOCKED until optional capability selection plus implementation.

## Runtime program

```text
#1 ChronForge runtime program
  |
  +-> O0 qstack binding -------------------------------- COMPLETE
  |
  +-> #2 D0 phase coordinator -------------------------- ACTIVE / REOPENED
  |     #11 pin/provenance ------------------------------ READY
  |     #12 seam inventory ------------------------------ READY for read-only work
  |     |     verify_after: #11
  |     #13 executable goldens -------------------------- BLOCKED; start_after #11
  |     `-> #14 D0.J ------------------------------------ BLOCKED on #11/#12/#13 receipts
  |             |
  |             `-> D0BaselineReceipt closes #2 and unlocks D1 intent/apply
  |
  +-> #3 D1 engine contracts --------------------------- BLOCKED
  |     OpenSpec: chronforge-d1-engine-contracts
  |     #15 IDs/units/model identities -----------------+
  |     #16 EventPhase/EventKey ------------------------+
  |     #17 commands/reports/OrderState ----------------+--> #19 D1.J
  |     #18 account/result/receipts --------------------+
  |                                                     |
  |                               D1EngineContractReceipt
  +-----------------------------------------------------v
  +-> #4 D2 hftbacktest integration -------------------- BLOCKED
  |     OpenSpec: chronforge-d2-hftbacktest-integration
  |     #20 dependency/market normalization ------------+
  |     #21 command -> kernel processors ---------------+
  |     #22 outcomes -> canonical facts ----------------+--> #24 D2.J
  |     #23 100-run determinism ------------------------+
  |                                                     |
  |                                  D2IntegrationReceipt
  +-----------------------------------------------------v
  +-> #5 D3 native strategy runtime -------------------- BLOCKED
  |     OpenSpec: chronforge-d3-native-runtime
  |     #25 RuntimeEvent/Source ------------------------+
  |     #26 Strategy/Context ---------------------------+
  |     #27 runtime loop/callback serialization --------+--> #29 D3.J
  |     #28 artifact/qorch handoff ---------------------+
  |                                                     |
  |                                           D3MvpReceipt
  |                                                     |
  |                                      mandatory MVP complete
  |
  +-> #6 D4 FFI host ----------------------------------- OPTIONAL / selected only
  +-> #7 D5 live core ---------------------------------- OPTIONAL / selected only
  `-> #8 D6 governance/recovery ------------------------ OPTIONAL / selected capability only
```

Mandatory MVP remains `O0 -> D0 -> D1 -> D2 -> D3`.

## D0 staged execution plan

D0 material characterization already landed in PR #32 and its OpenSpec change was archived. H2 does not invent a second D0 intent cycle. It reconciles that evidence into the recursive graph:

```text
                 +--> #12 read-only seam swarm ---------+
#11 pin swarm ---+                                        |
                 +--> #13 executable golden swarm -------+--> #14 interrogate + D0 join lever
                     #12 VERIFY also waits on #11 -------+
```

Operationally:

- #11 and the read-only discovery slices of #12 may execute in parallel.
- #12 cannot verify or emit `D0SeamInventoryReceipt` until #11 fixes the final revisions.
- #13 cannot start the executable baseline/golden run until #11 emits `D0PinReceipt`.
- #14 cannot start until all three child receipts exist, and then independently reruns cross-child ownership/pin/evidence invariants plus interrogate.
- #2 is the phase coordinator and remains open until #14 is accepted. Historical PR auto-close is not a phase-completion signal.

Reuse PR #32 evidence and only add missing issue-specific receipts/levers.

## D1-D3 intent gates

After each predecessor join is accepted, the next phase first lands one coherent OpenSpec change before leaf apply:

```text
#14 PASS
 -> close #2 / mark #3 INTENT_READY
 -> OpenSpec chronforge-d1-engine-contracts intent/spec/design/tasks
 -> #15/#16/#17/#18 workers under their staged dependencies
 -> #19 interrogate + cross-child formal/property lever

#19 PASS
 -> close #3 / mark #4 INTENT_READY
 -> OpenSpec chronforge-d2-hftbacktest-integration
 -> #20/#21/#22/#23 workers
 -> #24 interrogate + integrated Runtime lever

#24 PASS
 -> close #4 / mark #5 INTENT_READY
 -> OpenSpec chronforge-d3-native-runtime
 -> #25/#26/#27/#28 workers
 -> #29 interrogate + integrated 100-run Runtime lever
```

Phase-level OpenSpec changes map leaf tasks to GitHub issues; do not create one change per trivial implementation edit.

## Evidence gates

```text
Start gate    = dependencies.start_after satisfied
Intent gate   = accepted OpenSpec artifacts on main
Verify gate   = dependencies.verify_after satisfied + issue-specific lever
Arena gate    = synthesized candidate verified when trigger fired
Review gate   = interrogate required findings triaged; Act on resolved
Handoff gate  = typed receipt emitted at earned evidence class
Join gate     = all child receipts + independent cross-child lever
Merge gate    = project CI / verify-chronforge green at earned evidence class
Archive gate  = implementation merged, strict OpenSpec validation, living spec read-back
Research gate = immutable software/runtime artifact reference available
```

Evidence classes stay distinct: `Static`, `Metadata`, `formal/property`, `Runtime`, `PAPER`, `LIVE`.

## Project-state rule

Only ChronForge owns implementation issue/PR state. Pstack orch may track generic work-unit dependencies, but OpenSpec/qstack/pstack metadata does not become runtime state. Qorch does not mirror worktrees, branches, PR status or developer-agent assignments.
