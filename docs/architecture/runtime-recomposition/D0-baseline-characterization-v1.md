# D0 baseline — hftbacktest Soft≠green characterization

**Feature:** `chronforge-d0-baseline` (R-D0-02)  
**Pin:** [`tommy-ca/hftbacktest`](https://github.com/tommy-ca/hftbacktest) @ `058cfefd9740b6857bb875bad4d5e6547a88379a` Soft≠green  
**Upstream:** fork of [`nkaz001/hftbacktest`](https://github.com/nkaz001/hftbacktest) (default branch `master`) — see pin `UPSTREAM.md`  
**ChronForge tip base (this apply branch parent):** `e74dd7ea0dec315b84331fbc0bb941f3a2f9390f`  
**Propose tip floor:** `d8cb90b735086f126a4ca2262de3371f7508c1bc` (#30 MERGED Soft≠green)  
**Receipt:** [D0-baseline-receipt.json](./D0-baseline-receipt.json)  
**Evidence class:** Static / Metadata — `live_pass: false` Soft≠green  

Soft≠green. Timeout≠PASS. No invent LIVE_PASS. Titan evidence-only. Do **not** wire `hbt-engine` → `hftbacktest` in this change.

## Soft≠green honesty

| Claim | Status Soft≠green |
|---|---|
| Pin SHA frozen | Metadata PASS (receipt cites full SHA) |
| Ownership map with concrete paths | Static PASS (this document) |
| A-UP-001 independent build/test at pin | Runtime Soft≠green — `cargo check`/`cargo test --lib` with `--no-default-features --features backtest` exit 0; **default `live`/iceoryx not exercised**; not LIVE_PASS |
| A-UP-002 Polymarket overlay goldens | Metadata Soft≠green — inventory + content hashes at pin; **no migration**; Python `test_polymarket` not run as Runtime PASS here (needs `maturin develop`) |
| A-UP-003 no Titan / embedded hftbacktest tree in chronforge | Static Soft≠green — tree find empty; Cargo has comment-only fence, no hard dep |
| LIVE_PASS / PAPER_PASS | **Not invented** |
| Matching-engine replacement | **Must-not** — kernel remains external |
| qstack/qorch/pstack in kernel | **Must-not** |

Characterization used `gh api` + shallow clone at pin under `/workspace/verify/hftbacktest-d0-pin` Soft≠green. **Not vendored** into chronforge.

## Titan evidence-only Soft≠green

| Ref | SHA | Role |
|---|---|---|
| `dominolu/titan` | `3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024` | Reference evidence for scheduler / execution / runtime / live services Soft≠green |

**MUST NOT** import Titan trees into chronforge. Scaffold cites Titan as evidence only (see root `README.md`).

---

## Kernel vs Polymarket overlay ownership map Soft≠green

### Kernel (upstream-inherited Soft≠green)

| Concern | Classification | Concrete source paths @ pin |
|---|---|---|
| Event / order / bot types | Kernel | `hftbacktest/src/types.rs` — `Event`, `Order`, `Side`, `Status`, `OrdType`, `TimeInForce`, `Bot`, `Recorder`, `StateValues`, `LiveEvent`, `LiveRequest`, `OrderId` |
| Depth traits | Kernel | `hftbacktest/src/depth/mod.rs` — `MarketDepth`, `L2MarketDepth`, `L3MarketDepth`, `ApplySnapshot` |
| L2 depth impls | Kernel | `hftbacktest/src/depth/hashmapmarketdepth.rs`, `btreemarketdepth.rs`, `roivectormarketdepth.rs`, `fuse.rs` (`FusedHashMapMarketDepth`) |
| L3 depth methods | Kernel | L3 add/modify/delete on hashmap / btree / ROIVector implementations (unit tests in same files Soft≠green) |
| L2 local processor | Kernel | `hftbacktest/src/backtest/proc/local.rs` (`Local`) |
| L2 exchange processors | Kernel | `hftbacktest/src/backtest/proc/nopartialfillexchange.rs`, `partialfillexchange.rs` |
| L3 local processor | Kernel | `hftbacktest/src/backtest/proc/l3_local.rs` (`L3Local`) |
| L3 exchange processor | Kernel | `hftbacktest/src/backtest/proc/l3_nopartialfillexchange.rs` (`L3NoPartialFillExchange`) |
| Queue / fill models | Kernel | `hftbacktest/src/backtest/models/queue.rs` — `QueueModel`, `ProbQueueModel`, `RiskAdverseQueueModel`, `L3FIFOQueueModel`, `L3QueueModel`, … |
| Latency models | Kernel | `hftbacktest/src/backtest/models/latency.rs` — `ConstantLatency`, `IntpOrderLatency`, `LatencyModel`, `OrderLatencyRow` |
| Fee models (CEX-style) | Kernel | `hftbacktest/src/backtest/models/fee.rs` — `FeeModel`, `CommonFees`, `TradingValueFeeModel`, `TradingQtyFeeModel`, `FlatPerTradeFeeModel`, `DirectionalFees` |
| Fill simulation | Kernel | Exchange processors above + queue models Soft≠green |
| Backtest recorder | Kernel | `hftbacktest/src/backtest/recorder.rs` (`BacktestRecorder`) |
| Live bot + recorder | Kernel | `hftbacktest/src/live/bot.rs`, `hftbacktest/src/live/recorder.rs` (`LoggingRecorder`) |
| Live IPC | Kernel | `hftbacktest/src/live/ipc/{mod,config,iceoryx}.rs` Soft≠green |
| Collector | Kernel | `collector/` Soft≠green |
| CEX connector | Kernel | `connector/` (Binance / Bybit / Hyperliquid paths Soft≠green) |

### Polymarket overlay (additive Soft≠green — not kernel)

Provenance: reapplies product deltas from `mileswangs/pm-hftbacktest` as additive overlay Soft≠green (`UPSTREAM.md`). **Not** a full-tree replace.

| Concern | Classification | Concrete source paths @ pin |
|---|---|---|
| Binary fee model | Overlay | `hftbacktest/src/backtest/models/fee.rs` (`BinaryFeeModel`) + export in `models/mod.rs` |
| Converter | Overlay | `py-hftbacktest/hftbacktest/data/utils/polymarket.py` |
| Py surface | Overlay | `py-hftbacktest/hftbacktest/__init__.py` — `BacktestAssetPoly`, `init_orderbook`, `polymarket_to_hbt` |
| Stats helpers | Overlay | `py-hftbacktest/hftbacktest/stats/stats.py` — `PolyAssetRecord`, `fix_record_prices`, `earn` |
| PyO3 binding | Overlay | `py-hftbacktest/src/lib.rs` (`binary_fee_model`) |
| Examples | Overlay | `examples/polymarket/` (`smoke_converter.py`, notebooks Soft≠green) |
| Overlay tests | Overlay | `py-hftbacktest/tests/test_polymarket.py` (10 tests Soft≠green); Rust `binary_fee_*` in `fee.rs` |
| Docs | Overlay | `PRODUCT.md`, `UPSTREAM.md`, `DEVELOPMENT.md`, `NOTICE`, README overlay section |

**Skipped from pm Soft≠green (intentional):** PyPI rename, dropping py `s3` feature, replacing root README / deleting upstream examples, CEX collector/connector diffs, agent noise.

---

## Golden inventory Soft≠green (R-D0-03)

### Named lever commands @ pin

```text
cargo check -p hftbacktest --no-default-features --features backtest
cargo test  -p hftbacktest --no-default-features --features backtest --lib
cargo test  -p hftbacktest --no-default-features --features backtest --lib binary_fee
# Overlay (requires maturin develop Soft≠green — not claimed Runtime PASS here):
PYTHONPATH=py-hftbacktest:py-hftbacktest/tests \
  python -m unittest py-hftbacktest.tests.test_polymarket
```

### Fixture / artifact identities Soft≠green

| Path | sha256 Soft≠green |
|---|---|
| `py-hftbacktest/tests/test_polymarket.py` | `7ebbbd6baa407f1fad84da5a37ff246246689723db9414c6408281acbfe18b37` |
| `py-hftbacktest/hftbacktest/data/utils/polymarket.py` | `b5cc1fac9a9be40d1c39a444d9d8fd975387f6ae003c917fb457f4213b0d3e3e` |
| `hftbacktest/src/backtest/models/fee.rs` | `c6311a0c9f432e8f922702746d7481c6da0418a7c2c96ce929b58206b62a7177` |
| `examples/polymarket/smoke_converter.py` | `32a57155e776c3ece89f81c20d78a203650f2e2200abab7f3b77476aead841e8` |

Additional Soft≠green identities: `examples/polymarket/{endline,reverse}.ipynb`; 26 Rust `--lib` unit tests at pin Soft≠green.

### Prove results Soft≠green (VERIFY)

| Lever | Command | Exit | Verdict Soft≠green |
|---|---|---:|---|
| A-UP-001 check | `cargo check -p hftbacktest --no-default-features --features backtest` | 0 | Soft≠green Runtime subset PASS (backtest features only; not default/live) |
| A-UP-001 test binary_fee | `cargo test … --lib binary_fee` | 0 | 4 passed Soft≠green |
| A-UP-001 test --lib | `cargo test … --lib` | 0 | 26 passed Soft≠green; Timeout not observed |
| A-UP-002 overlay inventory | path+sha256 inventory; AST parse `test_polymarket.py` | 0 | Soft≠green Metadata — goldens unchanged; no migration; Python unittest not Runtime PASS |
| A-UP-003 no Titan tree | `find` for `titan`/`hftbacktest` dirs + Cargo dep grep | 0 | Soft≠green Static — empty dirs; comment-only fence in `hbt-engine` |

Soft/Timeout NEVER reported as PASS. Full default-feature suite (incl. live/iceoryx) **not** claimed Soft≠green.

---

## Unlock D1 Soft≠green

This receipt (when MERGED) unlocks characterization gate for D1 (#3) Soft≠green: D1 may consume the pin + ownership map. **D1 remains graph-BLOCKED on accepted #14 join** per roadmap Soft≠green — receipt Soft≠green is necessary but #14 is the sole D0 completion gate. Authors MUST NOT wire `hbt-engine` → `hftbacktest` until after receipt Soft≠green (this Apply lands the receipt; hard Cargo dep is still deferred Soft≠green).

## Must-nots honored Soft≠green

- No Titan import / tree copy  
- No matching-engine replacement  
- No qstack/qorch/pstack runtime in kernel  
- No invent LIVE_PASS  
- No hard wire `hbt-engine` → `hftbacktest` in this PR Soft≠green  
