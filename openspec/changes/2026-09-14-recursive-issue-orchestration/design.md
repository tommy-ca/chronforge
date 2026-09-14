# Design: recursive issue orchestration

## Ownership

The design composes existing owners and adds no second workflow engine.

```text
OpenSpec
  durable product/software intent
        |
        v
qstack development composition
  QuantDomainOverlay + QD CapabilityProfile
  + VerificationProfile + ChronForge ProjectProfile
        |
        v
pstack /poteto-mode + pstack orch
  generic playbook/dependency/worktree/PR/review/shipping mechanics
        |
        +--> swarm       independent coverage/fan-out
        +--> arena       competing candidates + synthesis
        `--> interrogate adversarial readonly review
        |
        v
ChronForge issue / branch / PR
        |
        v
verify-chronforge project lever(s)
        |
        v
EvidenceReceipt -> parent join
```

Qstack remains the project-facing quant-development composition layer. Pstack remains the generic engineering workflow/orchestration substrate. ChronForge owns project issue/PR state and executable evidence. Qorch begins only after immutable software/runtime artifact handoff.

## Canonical issue record

`docs/roadmap/ISSUE-ORCHESTRATION.json` is a derived project execution map. H2.4 upgrades it to schema v2. Each entry has:

```text
issue
phase
kind = program | phase | leaf | join | optional
status
dependencies {
  start_after[]
  verify_after[]
}
openspec { change, task }
qstack { intent, capability_profiles[], operation_skills[], verification_profile, project_profile }
pstack { base_playbook, orch_role }
swarm { mode, slices[], done }
arena { policy, trigger }
interrogate { required, scope, gate }
verification { profile, levers[], evidence_class, falsifier, current_status }
handoff { produces, consumed_by }
```

`start_after` is the evidence required before material work may begin. `verify_after` is the evidence required before the issue may enter VERIFY/HANDOFF. `start_after` MUST be a subset of `verify_after` unless the verifier has a documented reason otherwise. Joins normally use the same complete child set for both.

This staged dependency model is required for D0: #12 may start its read-only source inventory concurrently with #11, but its final pin-resolved receipt cannot verify until #11 completes; #13 executable goldens cannot start before #11 establishes the final external revisions.

The matrix is orchestration metadata only. It does not become a runtime input.

## Self-contained issue execution packet

Every covered GitHub issue body contains one generated/synchronized `Execution packet` section with the fields needed to execute that issue directly:

```text
matrix record + schema version
state / staged dependencies
OpenSpec binding
qstack development composition
pstack playbook + orch role
swarm mode/slices/done predicate
arena policy/trigger
interrogate scope/gate
verification profile/levers/evidence/falsifier
handoff receipt/consumer
```

The machine row remains authoritative. The issue body is an execution view. A renderer/validator should make drift detectable; hand-edited divergence is an `ISSUES` result, not a second policy source.

## State machine

```text
BLOCKED
  | start_after evidence accepted
  v
INTENT_READY
  | material work has accepted OpenSpec intent/tasks on main
  v
READY
  | qstack composition + pstack base playbook resolved
  v
ACTIVE
  | isolated worker/branch execution
  | verify_after may still be pending for staged investigation
  v
SYNTHESIS
  | arena only when its trigger fired
  v
REVIEW
  | interrogate when required
  v
VERIFY
  | all verify_after evidence present + repo-owned levers run
  +-- ISSUES --> ACTIVE
  +-- BLOCKED -> BLOCKED
  `-- PASS ----> HANDOFF
                    |
                    v
                  DONE
```

For a join node, `READY` normally requires all child handoff receipts because its `start_after` equals its full child set. `DONE` requires an independent join lever; child closure alone cannot satisfy it.

## OpenSpec granularity

A coherent D-phase SHOULD use one OpenSpec change with leaf tasks mapped to issue numbers. A capability that can ship/revert independently MAY use its own change. Read-only investigation does not require product intent until an implementation is selected. Archive happens only after implementation merges and verification passes.

## Qstack composition

Every runtime node is classified as `development`. Qstack selects only the relevant QD profiles and operation skills. It never restates generic worker spawning, worktrees, PR lifecycle, review or shipping mechanics.

## Pstack mechanics

The matrix names a pstack base playbook, but does not copy its body. `Feature` is the default for new runtime behavior, `Investigation` for read-only characterization, `Refactoring` for behavior-preserving migration, and `figure-it-out` for unusually cross-cutting work. A standing project-scale program remains represented by this GitHub execution graph and pstack orch state. Upstream `/orchestrate` remains explicitly user-invoked and is not a ChronForge dependency.

### Swarm

Use `swarm` for parallel coverage where slices are independent or for a declared race. Every slice has a standalone brief, its own writable state, a done predicate, and `PASS | ISSUES | BLOCKED` evidence. No shared-file sibling writes.

### Arena

Arena is conditional, not ceremonial. Trigger it when two or more plausible public API/data-model/adapter/runtime-loop shapes would be expensive to reverse after implementation. Candidates receive the same contract, are cross-judged, one base is selected, useful ideas are grafted manually, and the synthesized artifact is verified. If the design is already constrained by an accepted contract and one obvious implementation exists, record `skip: no competing shape earns a bakeoff`.

### Interrogate

Interrogate is mandatory for join PRs and for leaf PRs that change a public contract, deterministic ordering, state authority, command/fact semantics, callback ownership, recovery policy, or dependency boundary. It is readonly and never auto-applies findings. `Act on` findings block merge until resolved/re-reviewed; `Consider`, `Noted`, and `Dismissed` remain recorded with rationale.

## Lever verification

The smallest rerunnable project command that can falsify the acceptance claim is the lever. Project-wide control-plane checks use `tools/verify/verify.sh`. Phase-specific levers SHALL be added to `verify-chronforge` as executable runtime surfaces land. Until then the profile stays `BLOCKED` rather than promoting Static/Metadata evidence.

A leaf handoff minimally records source SHA, PR, OpenSpec task/change, qstack profile, pstack playbook, swarm/arena/interrogate result, lever command/result, evidence class, acceptance IDs, and unresolved limitations.

## Failure handling

- Start dependency missing: `BLOCKED`; do not fan out material implementation workers.
- Verify dependency missing: read-only/allowed ACTIVE work may continue, but issue cannot enter VERIFY/HANDOFF.
- Intent missing: produce/read OpenSpec artifacts before material apply.
- Swarm disagreement: aggregate evidence; use arena only if disagreement is about competing shapes rather than missing facts.
- Arena divergence: reframe; do not average incompatible designs.
- Interrogate `Act on`: return to implementation.
- Lever failure: issue remains open; minimize a falsifier/counterexample.
- Lever unavailable: `BLOCKED`, never narrative PASS.
- Issue body/matrix drift: regenerate the issue execution packet from the matrix row.

## Current frontier

After H2 archive, the runnable frontier remains #11 plus read-only portions of #12; #13 waits for #11. Final D0 handoff remains #11/#12/#13 -> #14. H2 changes execution discipline only and grants no D0-D3 correctness evidence.
