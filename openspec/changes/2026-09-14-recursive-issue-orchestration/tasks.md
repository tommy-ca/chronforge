# Tasks

## 1. Intent contract

- [x] 1.1 Define ownership and recursive issue state machine.
- [x] 1.2 Define canonical machine issue-record shape.
- [x] 1.3 Define swarm, arena, interrogate and lever semantics without copying upstream skills.
- [x] 1.4 Record ADR review.
- [x] 1.5 Refine the contract with self-contained issue execution packets and staged `start_after` / `verify_after` dependencies.

## 2. Execution graph implementation

- [x] 2.1 Add `docs/roadmap/ISSUE-ORCHESTRATION.json` covering #1, #2-#8, #11-#29 through phase fragments.
- [x] 2.2 Update `docs/roadmap/EXECUTION-GRAPH.md` with recursive node protocol and state machine.
- [x] 2.3 Update all covered runtime issues with execution-record references / concrete orchestration protocol.
- [x] 2.4 Bind D0 current frontier to runnable swarm/lever plan without bypassing #14.
- [x] 2.5 Define D1-D3 OpenSpec phase-change names/task bindings and keep implementation blocked until predecessor join + intent gate.
- [x] 2.6 Keep D4-D6 capability-selection gates explicit.
- [x] 2.7 Upgrade orchestration metadata to staged dependencies and correct D0 partial concurrency; restore #2 as the open D0 phase coordinator.
- [x] 2.8 Add deterministic issue-packet renderer and idempotent synchronizer.
- [x] 2.9 Synchronize #1, #2-#8 and #11-#29 issue bodies from their authoritative machine records; record `docs/roadmap/ISSUE-SYNC-RECEIPT.json`.

## 3. Verification tooling

- [x] 3.1 Add a project-owned orchestration-matrix validator.
- [x] 3.2 Extend `verify-chronforge control-plane` to validate matrix schema/coverage and issue-map consistency that repository-local metadata can prove.
- [x] 3.3 Keep future D1-D6 profiles BLOCKED while target-specific runtime levers are unavailable.
- [x] 3.4 Run stable/negative fixtures for the matrix validator (PR #52 final-head CI `34896508871` passed with the negative fixture rejecting an intentionally incomplete required-issue set).
- [x] 3.5 Validate `start_after ⊆ verify_after`, known dependency references, join child receipt completeness, and dependency acyclicity.
- [x] 3.6 Add stable/negative staged-dependency fixtures plus deterministic packet-render and packet-sync self-tests; PR #56 control-plane CI passed before issue synchronization.

## 4. Lifecycle

- [x] 4.1 Merge H2 intent/spec PR before normal implementation apply (PR #51 -> `c1f486379d97054046a0d0c9290cfa88bf522e0c`).
- [x] 4.2 Implement #49 and merge with CI green (PR #52 -> `8392e5f1e267860301e365c8157aff66c5c04b9c`, final-head CI `34896508871` SUCCESS).
- [x] 4.2a Confirm upstream pstack interrogate supports explicit multi-model reviewer configuration; define the H2 run/receipt contract in `docs/roadmap/H2-INTERROGATE-RUNBOOK.md` (PR #53 -> `945c13a895122b0b35f1c1fcff961efffe1836b3`).
- [x] 4.2b Complete #54 execution-packet hardening: intent PR #55 -> `8c05d1e29c9c4284985ab43a131204f6bcab6962`; matrix/tool implementation PR #56 -> `9d1169b96f1b7fbdeca54a5b93ca73f988ab8714`; synchronize all 27 issue bodies and reopen #2.
- [ ] 4.3 Run required interrogate review on the entire cross-cutting H2 implementation through the H2.4 reconciliation merge, with at least two independent reviewer model families; resolve all `Act on` findings.
- [ ] 4.4 Archive the OpenSpec change only after 4.3 PASS.
- [ ] 4.5 Read back the living `chronforge-recursive-issue-orchestration` spec from `main`.
- [ ] 4.6 Record interrogate/archive/CI receipts in #47-#50/#54 and close H2.
