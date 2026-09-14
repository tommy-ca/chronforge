## ADDED Requirements

### Requirement: Every Runtime Issue Has One Execution Record

ChronForge SHALL maintain a machine-readable orchestration record for program #1, optional issues #6-#8, and runtime leaf/join issues #11-#29.

Each record SHALL identify staged dependencies, OpenSpec binding, qstack composition, pstack base playbook/orch role, swarm shape, arena policy, interrogate gate, project verification levers/evidence class/falsifier, and produced/consumed handoff.

#### Scenario: Agent resolves an issue before implementation

- **GIVEN** a ChronForge runtime issue is selected
- **WHEN** its orchestration record is resolved
- **THEN** the agent can determine whether the issue is BLOCKED or READY
- **AND** can identify its exact intent, quant profile, generic engineering workflow, review gates and executable proof without reconstructing them from unrelated documents

### Requirement: Issue Bodies Mirror The Authoritative Execution Record

Every covered GitHub issue body SHALL contain a clearly delimited `Execution packet` section synchronized from its authoritative machine orchestration record.

The execution packet SHALL include the matrix schema/record reference, staged dependencies, OpenSpec binding, qstack development composition, pstack playbook/orch role, swarm contract, arena policy, interrogate gate, verification levers/evidence/falsifier, and handoff receipt/consumer.

The machine record SHALL remain authoritative. Divergence between the issue-body packet and its machine row SHALL be treated as orchestration `ISSUES` and corrected by regeneration rather than by creating two policy sources.

#### Scenario: Agent opens a leaf issue directly

- **GIVEN** a developer or agent opens #17 without first reading roadmap documents
- **WHEN** the issue body is read
- **THEN** the `Execution packet` identifies the D1 OpenSpec task, qstack QD-06/formal verification semantics, pstack Feature role, swarm slices, required arena/interrogate gates, executable proof surface, falsifier, and #19 handoff
- **AND** the agent can then resolve the authoritative matrix row for machine validation

### Requirement: Dependencies Distinguish Start Readiness From Verification Readiness

Each orchestration record SHALL declare `dependencies.start_after[]` and `dependencies.verify_after[]`.

`start_after` SHALL identify the evidence that must exist before material work may begin. `verify_after` SHALL identify the evidence that must exist before the issue may enter VERIFY/HANDOFF. `start_after` SHALL be a subset of `verify_after` unless a documented verifier rule justifies otherwise.

A read-only investigation MAY begin before all `verify_after` dependencies exist when its `start_after` set is satisfied, but it SHALL NOT produce a final handoff until all `verify_after` evidence is present.

#### Scenario: D0 seam inventory overlaps pin finalization

- **GIVEN** #11 pin/provenance is still ACTIVE
- **AND** #12 has no `start_after` blocker for read-only source inventory
- **WHEN** #12 begins seam discovery
- **THEN** its read-only swarm MAY run concurrently with #11
- **BUT** #12 cannot VERIFY/HANDOFF its pin-resolved seam receipt until #11's `D0PinReceipt` is available
- **AND** #14 remains blocked until #11, #12 and #13 receipts all exist

### Requirement: Material Apply Requires Accepted OpenSpec Intent

A material runtime leaf or phase SHALL NOT enter normal implementation apply until its governing OpenSpec proposal/spec/design/ADR-review/tasks are accepted on `main`.

A coherent phase MAY use one OpenSpec change whose tasks map to multiple leaf issues.

#### Scenario: D1 remains blocked before its intent gate

- **GIVEN** D0.J is accepted
- **AND** the D1 OpenSpec intent/tasks are not yet accepted on `main`
- **WHEN** #15-#18 are considered for implementation
- **THEN** their state is INTENT_READY rather than ACTIVE
- **AND** implementation workers are not fanned out yet

### Requirement: Qstack Composes Quant Semantics Without Owning Generic Development Mechanics

Every runtime node SHALL classify as qstack `development` and select only relevant QD CapabilityProfile, operation skills, VerificationProfile and ChronForge ProjectProfile semantics.

Generic planning, worker delegation, worktrees/branches/PRs, review, shipping and software-development dependency state SHALL remain upstream pstack responsibilities.

#### Scenario: Quant engine issue uses layered composition

- **GIVEN** a D2 integration issue
- **WHEN** its execution record is resolved
- **THEN** qstack contributes QD-05/QD-06 and relevant deterministic verification semantics
- **AND** pstack contributes the generic Feature/Refactoring/Investigation mechanics
- **AND** no qorch development unit is required

### Requirement: Swarm Is Used For Independent Parallel Coverage

An issue orchestration record SHALL declare `swarm.mode` as `partition`, `race`, `mixed`, or `none` and SHALL name a done predicate.

Parallel workers SHALL receive standalone briefs and isolated writable state. Sibling workers SHALL NOT rely on shared mutable files/branches.

#### Scenario: Source inventory fans out by independent seam

- **GIVEN** a read-only inventory issue has independent module families
- **WHEN** swarm is selected
- **THEN** the record partitions those module families into independent slices
- **AND** each slice reports `PASS | ISSUES | BLOCKED` with evidence
- **AND** the parent aggregates coverage before the issue can verify

### Requirement: Arena Is Conditional And Produces One Synthesized Artifact

Arena SHALL be required only when two or more plausible artifact/API/data-model/adapter shapes justify a reversible bakeoff before locking the design.

An arena run SHALL use one shared contract and rubric, isolated candidates, cross-judgment, explicit base selection, manual graft/rejection decisions, and verification of the synthesized artifact.

If the trigger is false the orchestration record SHALL state a skip rationale.

#### Scenario: Provenance receipt skips arena

- **GIVEN** an issue only extracts pinned provenance into an already specified schema
- **WHEN** its orchestration record is evaluated
- **THEN** arena MAY be `skip`
- **AND** the record explains that no competing shape earns a bakeoff

### Requirement: Interrogate Is A Readonly Merge And Join Gate

Interrogate SHALL be mandatory for every join PR and for leaf PRs that alter public contracts, deterministic ordering, state authority, command/fact semantics, callback ownership, recovery policy, or dependency boundaries.

Interrogate findings SHALL be categorized as `Act on`, `Consider`, `Noted`, or `Dismissed`. Interrogate SHALL NOT auto-apply changes.

#### Scenario: Act-on finding blocks merge

- **GIVEN** a required interrogate run reports an unresolved `Act on` finding
- **WHEN** the PR is evaluated for merge
- **THEN** the issue remains ACTIVE/REVIEW
- **AND** the implementation must be changed or the finding reclassified with evidence before merge

### Requirement: Every Completion Claim Has A Project Lever

Every leaf/join completion SHALL name the smallest rerunnable ChronForge-owned command that can falsify its acceptance claim, plus the evidence class earned.

If no executable lever exists for a required claim, the issue SHALL be `BLOCKED`; documentation, compilation, review consensus, or qstack routing metadata SHALL NOT be promoted to Runtime/PAPER/LIVE PASS.

#### Scenario: Future D2 runtime proof is unavailable

- **GIVEN** the D2 profile requires integrated deterministic replay
- **AND** the runtime adapter/receipt lever is not implemented
- **WHEN** D2 verification runs
- **THEN** `verify-chronforge d2` returns `BLOCKED`
- **AND** no Static/Metadata check substitutes for Runtime evidence

### Requirement: Join Nodes Consume Child Receipts And Reverify Cross-Child Invariants

A join SHALL require all declared child handoff receipts and SHALL run independent cross-child verification before producing its join receipt.

Closing child issues or merging child PRs SHALL NOT by itself satisfy the join.

#### Scenario: D1 child PRs are all closed but cross-contract verification fails

- **GIVEN** #15-#18 have child handoffs
- **WHEN** #19 runs the D1 cross-module lever
- **AND** duplicate vocabulary or a formal invariant fails
- **THEN** #19 returns `ISSUES`
- **AND** D2 remains blocked

### Requirement: Orchestration Metadata Stays Out Of Runtime Dependencies

OpenSpec, qstack, pstack, swarm/arena/interrogate metadata, issue orchestration records and verification scripts SHALL remain development-time control surfaces and SHALL NOT become dependencies of ChronForge runtime crates.

#### Scenario: Runtime dependency guard runs after H2

- **GIVEN** the orchestration matrix and issue protocol are installed
- **WHEN** the project control-plane dependency guard scans runtime manifests
- **THEN** qstack, qorch, pstack and OpenSpec remain absent from runtime dependencies
