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

`docs/roadmap/ISSUE-ORCHESTRATION.json` is a derived project execution map. Each entry has:

```text
issue
phase
kind = program | phase | leaf | join | optional
status
blocked_by[]
openspec { change, task }
qstack { intent, capability_profiles[], operation_skills[], verification_profile }
pstack { base_playbook, orch_role }
swarm { mode, slices[], done }
arena { policy, trigger, artifact, rubric[] }
interrogate { required, scope, gate }
verification { project_profile, levers[], evidence_class, falsifier }
handoff { produces, consumed_by }
```

The matrix is orchestration metadata only. It does not become a runtime input.

## State machine

```text
BLOCKED
  | dependencies accepted
  v
INTENT_READY
  | material work has accepted OpenSpec intent/tasks on main
  v
READY
  | qstack composition + pstack base playbook resolved
  v
ACTIVE
  | isolated worker/branch execution
  v
SYNTHESIS
  | arena only when its trigger fired
  v
REVIEW
  | interrogate when required
  v
VERIFY
  | repo-owned levers run
  +-- ISSUES --> ACTIVE
  +-- BLOCKED -> BLOCKED
  `-- PASS ----> HANDOFF
                    |
                    v
                  DONE
```

For a join node, `READY` additionally requires all required child handoff receipts. `DONE` requires an independent join lever; child closure alone cannot satisfy it.

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

- Dependency missing: `BLOCKED`; do not fan out implementation workers.
- Intent missing: produce/read OpenSpec artifacts before apply.
- Swarm disagreement: aggregate evidence; use arena only if disagreement is about competing shapes rather than missing facts.
- Arena divergence: reframe; do not average incompatible designs.
- Interrogate `Act on`: return to implementation.
- Lever failure: issue remains open; minimize a falsifier/counterexample.
- Lever unavailable: `BLOCKED`, never narrative PASS.

## Current frontier

After H2 archive, the runnable frontier remains #11/#12/#13 -> #14. H2 changes execution discipline only and grants no D0-D3 correctness evidence.