## ADDED Requirements

### Requirement: Intent Artifacts Precede Material Implementation

ChronForge SHALL use the bundled OpenSpec `intent-driven` lifecycle as the durable intent source for material behavioural, architectural, dependency, state-model, or runtime-contract changes.

The normal artifact order SHALL be `proposal -> specs -> design -> adr -> tasks`. Accepted tasks SHALL exist on `main` before implementation apply begins.

#### Scenario: Material deterministic-runtime change starts from accepted intent

- **GIVEN** a change modifies deterministic ordering, execution semantics, state ownership, strategy runtime, live transport, recovery, or another material project contract
- **WHEN** implementation work is about to begin
- **THEN** a named OpenSpec change exists with proposal, applicable specs, design, ADR review, and tasks
- **AND** those intent artifacts have landed on `main`
- **AND** the implementation PR references the OpenSpec change and ChronForge issue graph

#### Scenario: Read-only investigation does not create fake product intent

- **GIVEN** a task is purely investigative and changes no product behaviour or architecture
- **WHEN** qstack/pstack routes the work
- **THEN** the task MAY proceed without a new product OpenSpec change
- **AND** any later implementation discovered by the investigation SHALL create or bind to an OpenSpec change before apply

### Requirement: Quant Development Composes Qstack Over Pstack

ChronForge SHALL treat qstack as the project-facing quant-development orchestration/composition authority and upstream pstack as the generic engineering workflow/orchestration substrate underneath qstack.

ChronForge SHALL NOT vendor or fork generic pstack workflow, and SHALL NOT copy qstack quant-domain skills/principles/playbooks into the repository.

#### Scenario: D-phase implementation selects quant profile and generic playbook

- **GIVEN** a ChronForge D0-D6 implementation unit becomes ready
- **WHEN** development execution is planned
- **THEN** the applicable qstack ChronForge ProjectProfile and QD capability/verification profiles are selected
- **AND** generic engineering execution is delegated to an upstream pstack base playbook/orch mechanism
- **AND** project issue, branch, PR, and Runtime evidence remain in `tommy-ca/chronforge`

#### Scenario: Generic engineering behaviour is not duplicated

- **GIVEN** pstack already provides investigation, feature, refactoring, multi-phase, review, shipping, or orchestration mechanics
- **WHEN** ChronForge documents its development harness
- **THEN** ChronForge references those upstream mechanics
- **AND** does not create a local clone of those playbooks or principles

### Requirement: ChronForge Owns Project Implementation State

ChronForge SHALL be the authoritative repository for its implementation issues, branches, pull requests, code, tests, verification evidence, and software artifacts.

OpenSpec, qstack, and pstack SHALL describe or orchestrate work without becoming runtime dependencies or duplicate project-state stores.

#### Scenario: Implementation task maps to one project work item

- **GIVEN** an accepted OpenSpec task is ready for apply
- **WHEN** the task is executed
- **THEN** it maps to a ChronForge issue or explicit child work item
- **AND** its implementation lands through a ChronForge branch/PR
- **AND** completion evidence references the issue, PR/head SHA, acceptance IDs, and verification results

### Requirement: Recursive Execution Uses Leaf Work And Join Gates

The ChronForge execution graph SHALL decompose each material phase into independently verifiable leaf units followed by a single join gate that owns phase acceptance.

A downstream phase SHALL remain blocked until the upstream join receipt is accepted.

#### Scenario: D1 cannot bypass D0 join

- **GIVEN** D0 leaf work is partially complete
- **WHEN** D1 readiness is evaluated
- **THEN** D1 remains blocked until the D0 join receipt is accepted
- **AND** D1 references the accepted D0 receipt instead of rediscovering baseline facts

#### Scenario: Parallel leaves do not weaken phase acceptance

- **GIVEN** two leaf tasks within a phase can execute independently
- **WHEN** pstack/orch parallelizes them
- **THEN** each leaf produces its own verification evidence
- **AND** the phase is not complete until the join gate verifies their combined invariants

### Requirement: Verification Evidence Is Typed And Honest

Every change SHALL distinguish Static, Metadata, formal/property, Runtime, PAPER, and LIVE evidence as applicable. A weaker evidence class SHALL NOT be reported as a stronger one.

Timeout, skipped, unavailable, or soft checks SHALL NOT be treated as PASS.

#### Scenario: Static OpenSpec validation does not imply runtime correctness

- **GIVEN** an OpenSpec change validates strictly and documentation checks pass
- **WHEN** status is reported
- **THEN** the result is reported as specification/configuration evidence
- **AND** no Runtime, PAPER, or LIVE pass is inferred without corresponding executable evidence

### Requirement: Implementation Merges Before OpenSpec Archive

The intent-driven git discipline SHALL require accepted proposal/spec/design/ADR/tasks to land before apply and require implementation to merge before the corresponding OpenSpec change is archived.

#### Scenario: Archive waits for implementation merge

- **GIVEN** an OpenSpec change has accepted tasks and implementation is in progress
- **WHEN** archive readiness is evaluated
- **THEN** the change remains active until the implementation PR is merged and verification is complete
- **AND** archive updates the living specification only after that merge

### Requirement: Emergency Fixes Reconcile Intent Before Release Closure

A production-critical or safety-critical emergency fix MAY begin before a full proposal/spec/design/ADR/tasks chain when delay would materially increase risk, but the exception SHALL be explicit and temporary.

Before the fix is considered fully closed for release governance, the project SHALL reconcile the change into OpenSpec and applicable ADR/spec surfaces.

#### Scenario: Emergency safety fix uses retrospective reconciliation

- **GIVEN** an urgent defect requires immediate mitigation
- **WHEN** the maintainer declares an emergency-fix exception
- **THEN** the smallest safe implementation MAY proceed under pstack/qstack verification
- **AND** the PR records the exception and evidence
- **AND** a follow-up OpenSpec reconciliation task is created before normal release/archive closure

### Requirement: Research Handoff Uses Immutable Runtime Artifacts

After verified ChronForge software exists, qorch SHALL own durable quant-research orchestration. Qorch SHALL consume immutable software/run/determinism references and SHALL NOT mirror ChronForge development state.

#### Scenario: Verified runtime becomes a qorch research dependency

- **GIVEN** ChronForge emits a verified `SoftwareArtifactRef`, `RunReceipt`, or `DeterminismReceipt`
- **WHEN** a research program depends on that runtime
- **THEN** qorch records the immutable reference/digest
- **AND** does not copy branch, worktree, PR, or development-worker state
- **AND** ChronForge runtime execution does not require qorch access
