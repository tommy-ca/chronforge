# Tasks

## 1. Intent contract

- [x] 1.1 Define ownership and recursive issue state machine.
- [x] 1.2 Define canonical machine issue-record shape.
- [x] 1.3 Define swarm, arena, interrogate and lever semantics without copying upstream skills.
- [x] 1.4 Record ADR review.

## 2. Execution graph implementation

- [ ] 2.1 Add `docs/roadmap/ISSUE-ORCHESTRATION.json` covering #1, #6-#8, #11-#29.
- [ ] 2.2 Update `docs/roadmap/EXECUTION-GRAPH.md` with recursive node protocol and state machine.
- [ ] 2.3 Update #1 and all covered runtime issues with execution-record references / concrete orchestration protocol.
- [ ] 2.4 Bind D0 current frontier to runnable swarm/lever plan without bypassing #14.
- [ ] 2.5 Define D1-D3 OpenSpec phase-change names/task bindings and keep implementation blocked until predecessor join + intent gate.
- [ ] 2.6 Keep D4-D6 capability-selection gates explicit.

## 3. Verification tooling

- [ ] 3.1 Add a project-owned orchestration-matrix validator.
- [ ] 3.2 Extend `verify-chronforge control-plane` to validate matrix schema/coverage and issue-map consistency where repository-local validation can prove it.
- [ ] 3.3 Prove future D1-D6 profiles remain BLOCKED while target-specific runtime levers are unavailable.
- [ ] 3.4 Run stable/negative fixtures for the matrix validator.

## 4. Lifecycle

- [ ] 4.1 Merge H2 intent/spec PR before normal implementation apply.
- [ ] 4.2 Implement #49 and merge with CI green.
- [ ] 4.3 Run required interrogate review on the cross-cutting orchestration implementation; resolve all `Act on` findings.
- [ ] 4.4 Archive the OpenSpec change only after implementation merge.
- [ ] 4.5 Read back the living `chronforge-recursive-issue-orchestration` spec from `main`.
- [ ] 4.6 Record PR/merge/CI receipts in #47-#50.
