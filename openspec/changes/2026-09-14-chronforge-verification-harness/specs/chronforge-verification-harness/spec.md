## ADDED Requirements

### Requirement: One Canonical Project Verification Skill

ChronForge SHALL provide exactly one project-local verification skill named `verify-chronforge` for repository-specific proof workflows.

The skill SHALL follow the pstack project-verification shape (`Launch`, `Doctor`, `Drive`, `Evidence`, `Cleanup`, `Helpers`) while containing only ChronForge-specific commands, feature maps, evidence rules and tool references.

#### Scenario: Agent starts verification from the project skill

- **GIVEN** an agent must prove a ChronForge change
- **WHEN** it invokes or reads `verify-chronforge`
- **THEN** the skill directs it to the repo-owned verification entrypoint and relevant feature map
- **AND** it does not duplicate pstack's create/maintain-verification-skill implementation
- **AND** it references qstack quant verification semantics rather than copying their bodies

### Requirement: Verification Profiles Compose Qstack Semantics

ChronForge SHALL maintain a machine-readable profile map from project phase/surface to applicable qstack capability and verification profiles plus repo-owned executable levers.

#### Scenario: D-phase profile resolves quant semantics and local levers

- **GIVEN** a D0-D6 verification request
- **WHEN** the profile map is read
- **THEN** it names the applicable qstack profile/skills by identifier
- **AND** it names only ChronForge-owned executable levers
- **AND** unselected optional capabilities are not treated as required

### Requirement: Verification Results Are Typed And Honest

Every repo-owned verification command SHALL classify its result as `PASS`, `ISSUES`, or `BLOCKED` and SHALL state the evidence class actually earned.

Static, Metadata, formal/property, Runtime, PAPER and LIVE evidence SHALL remain distinct. Timeout, skipped, unsupported and unavailable checks SHALL NOT be reported as PASS.

#### Scenario: Missing runtime lever is blocked

- **GIVEN** D1-D6 executable runtime functionality required by a profile does not yet exist
- **WHEN** that profile is requested
- **THEN** verification returns `BLOCKED` with the missing lever named
- **AND** it does not infer Runtime/PAPER/LIVE success from OpenSpec, compilation, or documentation checks

### Requirement: Control Plane Verification Uses One Repo Entry Point

ChronForge SHALL expose a repo-owned control-plane verification command that runs strict OpenSpec validation, Rust workspace compilation, and the control-plane dependency boundary check.

CI SHALL call the same entrypoint rather than reimplementing those commands independently.

#### Scenario: CI and agent verification share the same control-plane lever

- **GIVEN** a pull request or local agent run
- **WHEN** control-plane verification executes
- **THEN** both use `tools/verify/verify.sh control-plane`
- **AND** a failure in any required child lever fails the profile

### Requirement: D0 Receipt Verification Is Executable

ChronForge SHALL provide an executable validator for the current D0 baseline receipt.

The validator SHALL check required identity/evidence fields, pinned repository revisions, evidence-class honesty, and `live_pass: false` unless later Runtime/LIVE evidence explicitly changes the receipt contract.

#### Scenario: Overstated D0 receipt is rejected

- **GIVEN** a D0 receipt claims LIVE pass without corresponding selected/live verification evidence
- **WHEN** the D0 validator runs
- **THEN** it returns `ISSUES`
- **AND** identifies the stronger-than-earned claim

### Requirement: Deterministic Repetition Tool Compares Canonical Output

ChronForge SHALL provide a small command-runner that executes a supplied canonical-output command N times and compares byte-identical stdout plus exit status.

The tool SHALL emit machine-readable hashes/results and SHALL return failure on divergence.

#### Scenario: Stable command proves repeated equality

- **GIVEN** a deterministic command with canonical stdout
- **WHEN** it is executed N times by the repeat tool
- **THEN** all exit codes and output hashes match
- **AND** the tool emits `PASS` with repeat count and canonical hash

#### Scenario: Divergent command is detected

- **GIVEN** a command that changes canonical stdout between runs
- **WHEN** it is executed by the repeat tool
- **THEN** the tool emits `ISSUES`
- **AND** returns nonzero

### Requirement: Verification Feature Map Is Maintained

The `verify-chronforge` skill SHALL include a feature map covering at minimum the development control plane, D0 baseline, deterministic engine, and strategy runtime surfaces.

Each feature SHALL state how to reach it, which repo-owned lever drives it, what observable evidence proves it, and what currently blocks verification if the feature is not yet implemented.

#### Scenario: Future runtime feature remains visible without false proof

- **GIVEN** deterministic engine or strategy runtime functionality is not yet implemented
- **WHEN** an agent reads its feature map
- **THEN** the map states the expected future lever and current blocker
- **AND** does not claim the feature is verified

### Requirement: Verification Tools Stay Outside Runtime Dependencies

Verification scripts, skills, OpenSpec, pstack and qstack SHALL remain development-time surfaces and SHALL NOT become dependencies of ChronForge runtime crates.

#### Scenario: Runtime manifests stay control-plane free

- **GIVEN** the verification harness is installed
- **WHEN** runtime crate manifests are scanned
- **THEN** they contain no qstack, qorch, pstack or OpenSpec dependency
