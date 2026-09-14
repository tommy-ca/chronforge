# Proposal: recursive ChronForge issue orchestration

## Why

ChronForge has a correct D0-D3 dependency graph, qstack phase profiles, and a project verification harness, but individual GitHub issues do not yet encode one repeatable execution protocol. This leaves OpenSpec intent, qstack profile composition, pstack execution mechanics, parallel-agent techniques, adversarial review, and project lever verification as separate conventions that an agent must reconstruct each time.

The missing capability is a project-local orchestration contract that composes those existing owners without copying them.

## What changes

Add `chronforge-recursive-issue-orchestration` as the durable control-plane capability for runtime issue execution.

Every runtime issue SHALL map to a machine-readable orchestration record defining:

- dependency/readiness gate;
- OpenSpec change/task binding;
- qstack development/QD/operation/verification composition;
- pstack BasePlaybook and generic orchestration ownership;
- swarm shape and done predicate;
- arena trigger or explicit skip rationale;
- interrogate scope and merge/join gate;
- exact ChronForge verification lever/profile and evidence class;
- child/parent handoff receipt.

Join issues SHALL require verified child handoffs plus independent cross-child verification. Closing child issues is not sufficient evidence.

## Non-goals

- no local clone of pstack `/poteto-mode`, `swarm`, `arena`, `interrogate`, `orch`, or `/orchestrate`;
- no local clone of qstack QD profiles or runtime operation skills;
- no qorch development units;
- no automatic Runtime/PAPER/LIVE claims from orchestration metadata;
- no runtime dependency on OpenSpec/qstack/pstack.

## Program

- #48 specifies this contract.
- #49 applies it to the execution graph and issues.
- #50 verifies, archives, and reads back the living capability.
