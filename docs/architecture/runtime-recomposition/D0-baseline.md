# D0 baseline — joined characterization

**Phase:** D0 / issue #2  
**Join:** #14 (`D0.J`) / implementation #90 / final verification #92  
**OpenSpec:** archived `2026-09-14-chronforge-d0-baseline` / `join-reconciliation`  
**Qstack:** development / `QD-15` / `deterministic-runtime-audit` + `replay-parity` / VerificationProfile `d0` / `ChronForgeProjectProfile`  
**Pstack:** `Babysit` join-verifier  
**Arena:** skipped — the join validates accepted evidence rather than selecting a competing architecture.  
**Interrogate:** #91 **PASS**, zero unresolved blocking findings.  
**D1 graph activation:** occurs only after #92 strict stamped-head PASS, #14 closure and an authoritative graph-state transition.

The original Soft≠green characterization is preserved byte-for-byte at [D0-baseline-characterization-v1.md](./D0-baseline-characterization-v1.md), with its receipt at [D0-baseline-characterization-receipt-v1.json](./D0-baseline-characterization-receipt-v1.json). Embedded paths in those relocated v1 blobs retain their creation-time context; later evidence does not rewrite history.

## Accepted child evidence

| Child | Role | Accepted evidence |
|---|---|---|
| #11 `D0PinReceipt` | exact evidence/dependency pins and drift policy | PR #73 merge `5d5bfca9c2fe033cdf2cede81f32503bd8a66406`; CI `34900722736`; Metadata/Static |
| #12 `D0SeamInventoryReceipt` | 20-seam source/ownership map and D2 adapter boundary | PR #84 merge `4d266a23a6ceede69f2c4a0c782a1d54430749b4`; proof `34907915973`; strict receipt validation `34907990818`; Static/Metadata |
| #13 `D0GoldenReceipt` | exact-pin executable kernel/overlay baseline | PR #83 merge `6e4dbe70d04bc81e98bcc41653e1eb61e0ec38bb`; external proof `34902006353`; strict receipt validation `34902178966`; Runtime-subset + Metadata |

The joined machine contract is [D0-baseline-receipt.json](./D0-baseline-receipt.json). It content-addresses the accepted child artifacts and preserves the later acceptance runs that resolve their creation-time metadata states.

## Frozen external identities and dependency mode

- hftbacktest kernel: `tommy-ca/hftbacktest@058cfefd9740b6857bb875bad4d5e6547a88379a`.
- Titan evidence-only reference: `dominolu/titan@3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024`.
- qstack runtime recomposition: `6d124b93b6008851c1fc48aaef5ef6a20d6535b6`.
- qstack ChronForge profile: `cf4e62f4ef98fe378393fa3adff8449ff9457024`.
- pstack substrate: `cursor/plugins@be432a96ed36e48d05f44bf375864355f62263f9`, subtree `pstack/`.

D0/D1 use an exact detached hftbacktest checkout. D2 may use only `https://github.com/tommy-ca/hftbacktest` at the exact revision above. Floating refs and reverse `hftbacktest -> ChronForge` dependencies are forbidden.

## Ownership synthesis

One authority owns each state.

**hftbacktest:** depth state, queue semantics/state, exchange matching and fills, simulated latency transport, fee calculation.

**ChronForge:** canonical IDs/units, deterministic `EventKey`/`EventPhase` contracts, canonical execution schemas, runtime/result/determinism receipts.

D2 is an adapter boundary. It may translate canonical commands to hftbacktest processors and project kernel facts outward. It must not create a second matching engine, second fill ledger or competing account/order truth.

## Acceptance evidence

### A-UP-001 — pinned kernel execution

**PASS, Runtime-subset.** Exact-pin `backtest`/no-default Rust checks and library tests executed successfully, including targeted `binary_fee` tests. This does not prove default live/iceoryx.

### A-UP-002 — Polymarket overlay preservation

**PASS-scoped, Runtime-subset + Metadata.** Rust `BinaryFeeModel` tests and four pinned overlay SHA-256 identities are accepted. Python/PyO3 runtime was not executed and is not inferred green.

### A-UP-003 — additive architecture

**PASS, Static/Metadata.** Titan remains evidence-only, hftbacktest remains external, the 20-seam map defines a narrow one-way adapter, and no second matching engine is accepted.

## Discrepancies and interrogate

[D0-discrepancy-register.json](./D0-discrepancy-register.json) records four creation-time metadata discrepancies, all resolved by later acceptance evidence without editing the child blobs. There are zero blocking contradictions.

The mandatory [D0-join-interrogate-receipt.json](./D0-join-interrogate-receipt.json) records eight adversarial findings/dispositions. Blocking findings around pin roles, all-pin equality, acceptance-run binding, exact D2 dependency mode and child evidence classes were acted on before PASS. Historical relocation semantics are an accepted limitation. Final source/workflow stamping is owned by #92.

## Accepted limitations and downstream obligations

D0 does **not** prove Python/PyO3 runtime, default live/iceoryx, PAPER readiness or LIVE readiness. Kernel goldens do not prove D2 canonical adapter behavior. Granular L2/L3, lifecycle and partial-fill gaps remain explicit D2 acceptance obligations.

D1 must define canonical domain/ordering/execution/result contracts without duplicating kernel truth. D2 must map those contracts onto the pinned seams and preserve goldens. D3 must prove native strategy runtime/replay behavior over the accepted D1/D2 contracts.

## Final lever

#92 uses the prestamp proof `34909153517` / `d7f8cc0d95db9d55103793d70b91ed66dfc26353` as the receipt's accepted proof revision and then requires a strict post-stamp run:

```text
python3 tools/verify/verify_d0_join.py
bash tools/verify/verify.sh d0
```

The receipt's `d1_unlock=true` is a capability handoff flag, not an issue-state mutation. D1 remains blocked in the authoritative graph until the strict post-stamp workflow succeeds, PR #93 is accepted, #14/#2 close, and the graph transition explicitly marks D1 ready.
