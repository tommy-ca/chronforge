# D0.2 kernel/seam map

**Issue:** #12  
**Pin source:** #11 `D0PinReceipt`  
**Read-only investigation may run before #11; VERIFY/HANDOFF may not.**  
**Machine inventory:** [`D0-seam-inventory.json`](./D0-seam-inventory.json)

This document decomposes the pinned external hftbacktest kernel into seams that ChronForge can adopt, adapt, compose, or defer. It does **not** redefine hftbacktest semantics and does not make the external kernel a D0 hard dependency.

## Ownership law

```text
hftbacktest owns
  feed Event representation at the external boundary
  + depth state/mutation
  + local/exchange processor behavior
  + queue/matching/fill semantics
  + latency transport semantics
  + fee calculation

ChronForge will own
  canonical IDs / checked units
  + EventKey / EventPhase ordering
  + canonical ExecutionCommand / ExecutionReport
  + deterministic runtime/result/receipt schemas

D2 adapter owns translation only.
```

The boundary rule is therefore:

> **Adapt kernel facts and commands; do not duplicate kernel authorities.**

## Canonical data flow discovered at the pin

```text
DataSource / Reader
        |
        v
Event { ev, exch_ts, local_ts, px, qty, order_id, ... }
        |
        +-------------------------------+
        |                               |
        v                               v
Exchange Processor                  Local Processor
sees EXCH_EVENT/exch_ts             sees LOCAL_EVENT/local_ts
        |                               |
        | depth / queue / matching      | local depth/trades/views
        |                               |
        +------ OrderBus + LatencyModel-+
                    |
                    v
               Order responses
                    |
                    v
                State / fees
```

`Processor::event_seen_timestamp` is the explicit semantic seam that preserves exchange-vs-local visibility. ChronForge must not collapse `exch_ts` and `local_ts` during normalization.

## D2 adapter attachment

ChronForge should attach at four narrow places:

1. **Market input adapter** — `Event` / `DataSource` -> D1 canonical market-event contract, preserving exchange/local timestamp and original venue/instrument identity supplied by the adapter context.
2. **Command adapter** — D1 `ExecutionCommand` -> `LocalProcessor::{submit_order,modify,cancel}` with checked tick/lot/unit conversion.
3. **Execution projection adapter** — processed kernel `Order`/state changes -> D1 canonical execution facts and deterministic account/result projections.
4. **Model identity adapter** — selected depth/queue/latency/fee/asset model identities + configuration -> `RunReceipt`/`DeterminismReceipt` metadata.

No reverse dependency from hftbacktest to ChronForge is permitted.

## Seam catalog

| Seam | Pinned source | Authority / responsibility | ChronForge decision |
|---|---|---|---|
| Feed event | `hftbacktest/src/types.rs::Event` | Immutable feed fact carrying both exchange/local timestamps and optional L3 order id | **adapt** at D2 boundary |
| Depth interfaces | `hftbacktest/src/depth/mod.rs` | Authoritative L1/L2/L3 depth mutation/query and snapshots | **adopt** |
| Depth implementations | `depth/{hashmap,btree,roivector,fuse}*` | Concrete book storage/best-level maintenance | **adopt**, keep container out of canonical API |
| Processor contract | `backtest/proc/mod.rs` | Timestamp visibility, market processing, order-receipt progression | **adapt** |
| L2 local | `backtest/proc/local.rs` | Local orders/depth/trades/account projection and outbound requests | **compose** |
| L2 no-partial exchange | `backtest/proc/nopartialfillexchange.rs` | Queue-aware exchange matching with full-fill semantics | **adopt** |
| L2 partial exchange | `backtest/proc/partialfillexchange.rs` | Queue-aware partial-fill semantics | **adopt** |
| L3 processors | `backtest/proc/{l3_local,l3_nopartialfillexchange}.rs` | MBO/L3 local/exchange order processing | **adopt** |
| Order bus | `backtest/order.rs` | Timestamp-ordered local<->exchange request/response transport | **adopt** |
| Queue models | `backtest/models/queue.rs` | Queue-position state and fill eligibility | **adopt** |
| Latency models | `backtest/models/latency.rs` | Entry/response latency; historical interpolation | **adopt** |
| Fee models | `backtest/models/fee.rs` | Maker/taker/directional/quantity/value fee calculation | **adopt** |
| State | `backtest/state.rs` | Position/balance/fee/trade-counter projection from fills | **adapt** into canonical result facts |
| Reader/cache | `backtest/data/{mod,reader}.rs` | Load/cache POD data for processors | **compose** |
| Backtest recorder | `backtest/recorder.rs` | Derived performance recording; not execution authority | **defer** to result/export layer |
| Live bot/IPC/connectors | `live/`, `collector/`, `connector/` | External live transport/connectivity | **defer** to optional D5 |
| Python/PyO3 | `py-hftbacktest/` | Host/binding surface over native semantics | **defer** to parity/optional D4 |
| Binary fee overlay | `backtest/models/fee.rs::BinaryFeeModel` | Polymarket binary-contract fee formula | **adopt** |
| Polymarket converter | `py-hftbacktest/hftbacktest/data/utils/polymarket.py` | Source-data -> hftbacktest event conversion | **compose** |
| Polymarket tests/examples | `py-hftbacktest/tests/test_polymarket.py`, `examples/polymarket/` | Overlay preservation evidence | **compose** into D0 goldens |

The full catalog includes concrete IO and determinism assumptions in `D0-seam-inventory.json`.

## Important state authorities

### Market book

The selected `MarketDepth` implementation owns book state. ChronForge may expose canonical read-only projections, but must not maintain a second independently mutating book for D2.

### Orders and fills

The exchange processor owns simulated matching/fill outcomes. The local processor owns the locally delivered order view. Those two views can differ in time because `OrderBus` + `LatencyModel` delays requests/responses.

ChronForge D2 must therefore represent:

```text
exchange-final state != necessarily local-delivered-final state at the same timestamp
```

without declaring two competing authorities.

### Account state

`State::apply_fill` updates position, balance, fees, trade count, volume and value from executed `Order` fields. ChronForge should project canonical result/account facts from the same execution outcomes rather than create an unrelated fill ledger.

### Queue state

`QueueModel` mutates queue-estimation data associated with the kernel order and consumes market-depth/trade changes. Queue state is a simulation-model implementation detail; its **identity/configuration** belongs in reproducibility receipts, but its concrete internal type does not belong in ChronForge's public canonical schema.

## Determinism assumptions to preserve

The following are inputs to deterministic semantics, not incidental implementation details:

- exact ordered `Event` stream;
- `exch_ts` and `local_ts` preserved independently;
- tick/lot sizes and checked boundary conversions;
- selected depth implementation semantics;
- selected queue model + configuration;
- selected latency model + data/configuration;
- selected fee/asset models + configuration;
- order type / TIF behavior;
- initial local/exchange/account state;
- Polymarket overlay version when selected.

Parallel file loading or concrete map/container choice must not be promoted into the semantic contract unless it changes observable canonical results.

## Polymarket overlay boundary

The fork overlay remains additive:

```text
upstream kernel
  + BinaryFeeModel
  + converter / Python exposure
  + stats helpers
  + tests/examples/docs
```

It is not evidence for replacing upstream queue/depth/matching architecture. D0/D2 should preserve overlay behavior without copying the product overlay into ChronForge's canonical domain model.

## Optional surfaces

The repository includes live bot, IPC, collectors/connectors and Python bindings. Their presence does **not** make them mandatory ChronForge D0-D3 capabilities.

- native deterministic engine/runtime: D0-D3 mandatory;
- foreign strategy host/parity: optional D4;
- live transport/services: optional D5;
- OMS/EMS/ledger/reconciliation: optional D6 and not implied by hftbacktest.

## Must preserve into D2

1. exchange/local timestamp distinction;
2. L2/L3 book semantics;
3. local vs exchange processor separation;
4. timestamp-ordered order bus + latency semantics;
5. queue model behavior;
6. partial vs no-partial fill semantics;
7. maker/taker/fee semantics, including `BinaryFeeModel` when Polymarket is selected;
8. order lifecycle facts required to reconstruct canonical execution/account projections;
9. additive Polymarket provenance.

## Must not infer

- `f64` in the kernel becomes ChronForge's canonical unit representation;
- kernel `Order` becomes the canonical public order schema;
- a concrete depth container becomes part of the canonical contract;
- `BacktestRecorder` is an authoritative event ledger;
- hftbacktest live IPC/connectors are required by the deterministic MVP;
- Python bindings own runtime progression;
- ChronForge needs a second matching engine, queue model, or fee engine.

## Verification state

This document is currently **read-only evidence**. `verify_d0_seams.py` may validate catalog structure on the draft branch, but final `D0SeamInventoryReceipt` handoff is blocked until #11's accepted `D0PinReceipt` proves that this exact hftbacktest revision is still the selected source.
