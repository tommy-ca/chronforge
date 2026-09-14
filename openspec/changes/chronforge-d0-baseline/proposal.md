## Why

ChronForge D0 (#2) is the sole READY frontier after scaffold #9 @ `1c8ee86c`. The workspace has `hbt-engine`/`hbt-runtime` **stubs**. Kernel behavior in `tommy-ca/hftbacktest` is still an implicit assumption. D1 is BLOCKED until a frozen, hash-verifiable baseline receipt exists.

Soft≠green. Timeout≠PASS. No invent LIVE_PASS. Titan evidence-only. No matching-engine replacement.

Cite: [OpenSpec intent flow](sand-workflow:openspec-intent-flow) + [Planner worker split](sand-workflow:planner-worker-split). Thermos apply/merge only.

## What Changes

- Bootstrap OpenSpec `intent-driven` schema in ChronForge (this PR).
- Mint NEW capability `chronforge-d0-baseline`: pin `tommy-ca/hftbacktest` SHA `058cfefd…`; characterize kernel vs Polymarket overlay; golden inventory; machine-readable receipt; D0-baseline.md.
- MUST NOT wire `hbt-engine` → `hftbacktest` until receipt lands (Apply).
- MUST NOT import Titan; MUST NOT add qstack/qorch/pstack runtime deps to kernel.

## Capabilities

### New Capabilities

- `chronforge-d0-baseline`: Freeze hftbacktest kernel baseline + overlay map + golden inventory + content-addressable receipt; D1 blocked until receipt Soft≠green; no Titan copy; Soft≠green honesty.

### Modified Capabilities

- None.

## Impact

Propose artefacts + OpenSpec schema bootstrap. Apply HOLD until eng-lead GO: land `docs/architecture/runtime-recomposition/D0-baseline.md` + receipt JSON + golden inventory; prove A-UP-001..003 via named levers (`cargo test` / overlay goldens at pin). Horizon leaf.

## Probe Evidence Record

- Evidence label: `Static`
  - Query: Scaffold tip / D0 issue / hftbacktest pin
  - Path: chronforge `1c8ee86c`; issue #2; hftbacktest `058cfefd` (= master tip dig)
  - Result summary: Stubs only; pin matches master; Titan evidence SHA cited
  - Conclusion: Propose D0 freeze contract; Apply produces receipt.

- Evidence label: `Unavailable`
  - Query: LIVE_PASS / Titan import
  - Path: BRIEF parks
  - Result summary: Parks held
  - Conclusion: MUST NOT invent.

## Non-Goals

- D1–D6 implementation; Titan copy; matching-engine replacement; qorch in kernel; invent LIVE_PASS
