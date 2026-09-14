# D0.3 executable baseline and golden corpus

**Issue:** #13  
**Pin:** `tommy-ca/hftbacktest@058cfefd9740b6857bb875bad4d5e6547a88379a`  
**Receipt:** [`D0-golden-receipt.json`](./D0-golden-receipt.json)  
**Runtime-subset lever:** `bash tools/verify/d0_goldens.sh`

## Purpose

D0.3 converts the previously characterized hftbacktest baseline into a small rerunnable proof surface. It protects D1-D3 from silently redefining external-kernel behavior while keeping evidence classes honest.

The proof harness does not copy hftbacktest into ChronForge. It creates a temporary checkout of the exact commit, verifies `HEAD`, executes the pinned commands, checks overlay artifact hashes, and deletes the checkout.

## Golden execution

```bash
cargo check -p hftbacktest --no-default-features --features backtest
cargo test -p hftbacktest --no-default-features --features backtest --lib
cargo test -p hftbacktest --no-default-features --features backtest --lib binary_fee
```

The first command proves the pinned core backtest feature builds independently. The second is the compact broad Rust library regression surface. The third is a narrow explicit Polymarket binary-fee regression.

## Artifact identities

The lever also requires these exact SHA-256 values before executing tests:

```text
7ebbbd6baa407f1fad84da5a37ff246246689723db9414c6408281acbfe18b37  py-hftbacktest/tests/test_polymarket.py
b5cc1fac9a9be40d1c39a444d9d8fd975387f6ae003c917fb457f4213b0d3e3e  py-hftbacktest/hftbacktest/data/utils/polymarket.py
c6311a0c9f432e8f922702746d7481c6da0418a7c2c96ce929b58206b62a7177  hftbacktest/src/backtest/models/fee.rs
32a57155e776c3ece89f81c20d78a203650f2e2200abab7f3b77476aead841e8  examples/polymarket/smoke_converter.py
```

A hash mismatch is a failure. The expected hashes must never be rewritten merely to make CI green; a legitimate source-pin/overlay change requires a D0 drift review.

## Swarm coverage

### #76 L2/L3 baseline

The full pinned `--lib` suite is the executable baseline. If the exact pin does not expose separately stable addressable L2/L3 test names, D0 records that limitation instead of inventing a narrower PASS. D2 still must add adapter-specific L2/L3 fixtures.

### #77 queue / latency / fee models

The full pinned library suite guards model implementations. The targeted `binary_fee` filter proves the additive binary-contract fee tests execute independently. Model identity/configuration remains a future receipt input; D0 does not declare every configuration exhaustively tested.

### #78 order lifecycle

Submit/modify/cancel and accept/reject/fill/expire semantics are protected to the extent the pinned library suite exercises them. Missing explicit lifecycle fixtures remain D2 acceptance obligations and are not inferred from a successful build.

### #79 partial vs no-partial fill

The source-characterized semantic distinction between `PartialFillExchange` and `NoPartialFillExchange` is preserved by the pinned full suite. D0 does not normalize one model into the other. Any missing direct fixture is carried as a D2 gap.

### #80 Polymarket overlay

The lever executes the native `BinaryFeeModel` tests and verifies converter/test/example source identities. Python unittest/PyO3 runtime is **not** promoted to PASS unless a separate reproducible Python lever is added and executed.

## Evidence classes

```text
exact checkout + cargo check/test      -> Runtime-subset
source / fixture SHA-256 identity      -> Metadata/Static
Python unittest not executed           -> unavailable, not PASS
default live/iceoryx not executed      -> unavailable, not PASS
PAPER/LIVE                             -> not earned
```

The phrase `Runtime-subset` means actual code at the exact pinned external revision executed successfully in the declared `backtest` feature configuration. It does not imply live connectors, Python host parity, ChronForge D2 adapter correctness, PAPER, or LIVE readiness.

## Failure semantics

The lever is fail-fast and returns non-zero for:

- checkout SHA mismatch;
- overlay hash mismatch;
- Rust build failure;
- any Rust library test failure;
- targeted binary-fee test failure.

A failure must be minimized into a discrepancy/regression record. Retrying until green is not a verification policy.

## Relationship to D0 join

`D0GoldenReceipt` is one child receipt. #14 still requires:

```text
D0PinReceipt
+ D0SeamInventoryReceipt
+ D0GoldenReceipt
+ mandatory interrogate
+ independent D0 join lever
=> D0BaselineReceipt
```

Therefore #13 PASS cannot unlock D1 directly.
