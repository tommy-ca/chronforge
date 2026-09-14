# D0 baseline — joined characterization candidate

**Phase:** D0 / issue #2  
**Join:** #14 (`D0.J`)  
**Join implementation:** #90  
**OpenSpec:** archived `2026-09-14-chronforge-d0-baseline` / `join-reconciliation`  
**Qstack:** development / `QD-15` / `deterministic-runtime-audit` + `replay-parity` / VerificationProfile `d0` / `ChronForgeProjectProfile`  
**Pstack:** `Babysit` join-verifier  
**Arena:** skipped — the join validates accepted child evidence rather than selecting a new architecture.  
**Interrogate:** **mandatory and pending** at #91.  
**D1:** locked until #91 and #92 pass.

This document is the current synthesis. The original Soft≠green characterization is preserved unchanged at [D0-baseline-characterization-v1.md](./D0-baseline-characterization-v1.md), with its original receipt at [D0-baseline-characterization-receipt-v1.json](./D0-baseline-characterization-receipt-v1.json). Later evidence does not rewrite what those historical artifacts claimed.

## Accepted child evidence

| Child | Role | Accepted evidence |
|---|---|---|
| #11 `D0PinReceipt` | exact evidence/dependency pins and drift policy | PR #73 merge `5d5bfca9c2fe033cdf2cede81f32503bd8a66406`; CI `34900722736`; Metadata/Static |
| #12 `D0SeamInventoryReceipt` | 20-seam source/ownership map and D2 adapter boundary | PR #84 merge `4d266a23a6ceede69f2c4a0c782a1d54430749b4`; first proof `34907915973`; strict stamp validation `34907990818`; Static/Metadata |
| #13 `D0GoldenReceipt` | exact-pin executable kernel/overlay baseline | PR #83 merge `6e4dbe70d04bc81e98bcc41653e1eb61e0ec38bb`; external proof `34902006353`; strict stamp validation `34902178966`; Runtime-subset + Metadata |

The joined machine contract is [D0-baseline-receipt.json](./D0-baseline-receipt.json). Child blobs are content-addressed there and are not rewritten by the join.

## Frozen external identities

- hftbacktest kernel: `tommy-ca/hftbacktest@058cfefd9740b6857bb875bad4d5e6547a88379a`.
- Titan evidence only: `dominolu/titan@3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024`.
- qstack runtime recomposition: `6d124b93b6008851c1fc48aaef5ef6a20d6535b6`.
- qstack ChronForge ProjectProfile: `cf4e62f4ef98fe378393fa3adff8449ff9457024`.
- pstack substrate: `cursor/plugins@be432a96ed36e48d05f44bf375864355f62263f9`, subtree `pstack/`.

D0/D1 use an exact detached hftbacktest checkout. D2 may introduce only an exact-revision Cargo Git dependency. Floating branches/tags and reverse `hftbacktest -> ChronForge` dependencies are forbidden.

## Ownership synthesis

The implementation rule is one authority per state.

**hftbacktest remains authoritative for:** market-depth state, queue semantics/state, exchange matching/fills, simulated latency transport and fee calculation.

**ChronForge owns:** canonical IDs/units, deterministic `EventKey`/`EventPhase` contracts, canonical execution schemas, and runtime/result/determinism receipts.

D2 is an adapter boundary. It may translate canonical commands onto hftbacktest processors and project kernel facts outward; it must not create a second matching engine or competing order/fill/account truth.

## Acceptance evidence

### A-UP-001 — independently executable pinned kernel

**PASS, Runtime-subset.** The exact pin was checked out and the following completed successfully under the accepted #13 workflow:

```text
cargo check -p hftbacktest --no-default-features --features backtest
cargo test -p hftbacktest --no-default-features --features backtest --lib
cargo test -p hftbacktest --no-default-features --features backtest --lib binary_fee
```

This does not prove default live/iceoryx behavior.

### A-UP-002 — Polymarket overlay preservation

**PASS-scoped, Runtime-subset + Metadata.** Targeted Rust `BinaryFeeModel` tests passed and four overlay artifact SHA-256 identities were preserved. Python/PyO3 runtime was not executed and is not promoted to PASS.

### A-UP-003 — additive architecture / no Titan tree

**PASS, Static/Metadata.** Titan remains evidence-only, hftbacktest remains external, and the seam inventory exposes a narrow one-way adapter boundary. No copied Titan tree or second matching engine is accepted.

## Explicit discrepancy register

[D0-discrepancy-register.json](./D0-discrepancy-register.json) contains four nonblocking creation-time metadata discrepancies. Each is resolved by later acceptance evidence while preserving the child blob unchanged:

1. #11 receipt was authored before its CI result was known.
2. #12 inventory was authored while the #11 verify gate was still blocked.
3. #12 receipt records its first proof run; a later strict run validated the stamped receipt.
4. #13 receipt records its first external proof run; a later strict run validated the stamped receipt.

There are currently zero join-blocking contradictions. #91 must independently challenge this conclusion.

## Accepted limitations and downstream obligations

D0 does **not** prove Python/PyO3 runtime, default live/iceoryx, PAPER readiness or LIVE readiness. It also does not prove D2 canonical adapter behavior merely because the underlying kernel goldens pass. Granular L2/L3, order-lifecycle and partial-fill coverage gaps remain explicit D2 acceptance obligations.

D1 must define canonical domain/ordering/execution/result contracts without duplicating kernel truth. D2 must map those contracts onto the pinned seams and preserve the accepted goldens. D3 must prove native strategy runtime/replay semantics over the accepted D1/D2 contracts.

## Candidate gate

The candidate lever is:

```text
python3 tools/verify/verify_d0_join.py --candidate
bash tools/verify/verify.sh d0
```

A green candidate is **not D0 acceptance**. #91 must produce a `D0JoinInterrogateReceipt` with zero unresolved blocking findings. #92 then runs the post-interrogate and strict stamped-head levers. Only the accepted strict `D0BaselineReceipt` may set `d1_unlock=true`.
