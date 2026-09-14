# Proposal: recursive ChronForge issue orchestration

## Why

ChronForge has a correct D0-D3 dependency graph, qstack phase profiles, and a project verification harness, but individual GitHub issues do not yet encode one repeatable execution protocol. This leaves OpenSpec intent, qstack profile composition, pstack execution mechanics, parallel-agent techniques, adversarial review, and project lever verification as separate conventions that an agent must reconstruct each time.

The missing capability is a project-local orchestration contract that composes those existing owners without copying them.

The first H2 implementation established the canonical machine matrix and issue pointers. A second hardening pass is required so each GitHub issue is itself executable without opening unrelated files, while the matrix remains the source of truth. The same refinement must represent partial-order dependencies honestly: read-only work may sometimes start before a predecessor handoff, while verification and handoff must still wait for the required evidence.

## What changes

Add `chronforge-recursive-issue-orchestration` as the durable control-plane capability for runtime issue execution.

Every runtime issue SHALL map to a machine-readable orchestration record defining:

- staged dependency/readiness gates (`start_after` and `verify_after`);
- OpenSpec change/task binding;
- qstack development/QD/operation/verification composition;
- pstack BasePlaybook and generic orchestration ownership;
- swarm shape and done predicate;
- arena trigger or explicit skip rationale;
- interrogate scope and merge/join gate;
- exact ChronForge verification lever/profile and evidence class;
- child/parent handoff receipt.

Every covered GitHub issue body SHALL mirror the executable fields from its authoritative machine row in a clearly delimited `Execution packet` section. The body is a synchronized execution view, not a second source of truth.

Join issues SHALL require verified child handoffs plus independent cross-child verification. Closing child issues is not sufficient evidence.

## Non-goals

- no local clone of pstack `/poteto-mode`, `swarm`, `arena`, `interrogate`, `orch`, or `/orchestrate`;
- no local clone of qstack QD profiles or runtime operation skills;
- no qorch development units;
- no automatic Runtime/PAPER/LIVE claims from orchestration metadata;
- no runtime dependency on OpenSpec/qstack/pstack;
- no attempt to make GitHub issue text authoritative over the machine matrix.

## Program

- #48 specifies the base recursive orchestration contract.
- #49 applies the base contract to the execution graph and issues.
- #54 hardens staged dependencies and materializes self-contained issue execution packets.
- #50 runs the required multi-model interrogate, then verifies, archives, and reads back the living capability.
