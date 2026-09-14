# chronforge-d0-baseline Specification

## Purpose
Freeze tommy-ca/hftbacktest Soft≠green kernel pin, kernel vs Polymarket overlay ownership map, golden inventory, and hash-verifiable D0BaselineReceipt Soft≠green. D1 consumes the receipt Soft≠green; no Titan import; no invent LIVE_PASS; no hbt-engine→hftbacktest hard wire until after receipt Soft≠green.

## Requirements

### Requirement: R-D0-01 Pin Hftbacktest Kernel Baseline

Feature: chronforge-d0-baseline
Rule: D0 SHALL pin tommy-ca/hftbacktest at a content-addressable SHA before D1.

On APPLY GO, authors SHALL record pin SHA `058cfefd9740b6857bb875bad4d5e6547a88379a` (or a later SHA with dig refresh) in a machine-readable baseline receipt. Authors MUST NOT treat pin as LIVE_PASS. Soft≠green; Timeout≠PASS.

#### Scenario: Receipt cites pin SHA

- **GIVEN** D0 Apply completes
- **WHEN** the baseline receipt is read
- **THEN** it contains the hftbacktest SHA and upstream/fork identity
- **AND** no LIVE_PASS is assigned from pin alone
- **Evidence class:** Static / Metadata

### Requirement: R-D0-02 Kernel Versus Overlay Ownership Map

Feature: chronforge-d0-baseline
Rule: Baseline SHALL classify kernel vs additive overlay (e.g. Polymarket) with source paths.

Apply SHALL document event/depth types, L2/L3 processors, local/exchange processors, queue/latency/fee/fill, recorder/live IPC as kernel vs overlay. Authors MUST NOT copy Titan trees.

#### Scenario: Ownership map present

- **GIVEN** D0-baseline.md is landed
- **WHEN** a reader looks up queue/latency/fee/fill
- **THEN** each has a concrete source path under the pinned SHA
- **AND** overlay goldens are classified separately
- **Evidence class:** Static

### Requirement: R-D0-03 Golden Inventory And Independent Build

Feature: chronforge-d0-baseline
Rule: Existing hftbacktest package SHALL remain independently buildable; goldens inventoried.

Apply SHALL list baseline golden commands and fixture identities. A-UP-001: package independently testable at pin. A-UP-002: Polymarket overlay goldens unchanged unless a separate migration Act-on. A-UP-003: no copied Titan embedded hftbacktest tree.

#### Scenario: Inventory names commands

- **GIVEN** D0 Apply
- **WHEN** VERIFY runs named levers
- **THEN** inventory commands are cited and exit-code recorded
- **AND** Soft/Timeout are not PASS
- **Evidence class:** Runtime / Metadata

### Requirement: R-D0-04 Receipt Hash-Verifiable And D1 Gate

Feature: chronforge-d0-baseline
Rule: Receipt SHALL be hash-verifiable; D1 SHALL consume it.

Apply SHALL land a content-addressable receipt (hash of pin+inventory+map). D1 MUST remain BLOCKED until receipt exists. Authors MUST NOT wire `hbt-engine` → `hftbacktest` before receipt Soft≠green.

#### Scenario: D1 blocked without receipt

- **GIVEN** D0 propose merged but receipt not landed
- **WHEN** D1 start is evaluated
- **THEN** D1 remains BLOCKED
- **Evidence class:** Metadata

### Requirement: R-D0-05 Parks Soft Honesty

Feature: chronforge-d0-baseline
Rule: Soft≠green; Timeout≠PASS; no invent LIVE_PASS; no Titan; no qstack runtime in kernel.

Authors SHALL honor issue #2 must-nots. Scaffold `cargo check` MUST NOT be reported as Runtime PASS.

#### Scenario: Honesty parks

- **GIVEN** Apply done bar
- **WHEN** status is reported
- **THEN** Soft≠green and Timeout≠PASS hold
- **AND** LIVE_PASS is not invented
- **Evidence class:** Metadata

### Requirement: R-D0-06 Propose-Only Fence

Feature: chronforge-d0-baseline
Rule: This PR SHALL be OpenSpec artefacts (+ schema bootstrap) until APPLY GO.

Product D0-baseline.md / receipt files MUST wait for Apply unless included as empty stubs labeled Apply-held.

#### Scenario: Propose artefacts only

- **GIVEN** Wave-4 propose PR
- **WHEN** validated --strict
- **THEN** kernel wiring to hftbacktest is absent
- **Evidence class:** Metadata
