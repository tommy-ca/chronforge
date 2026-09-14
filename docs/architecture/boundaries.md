# Dependency boundaries Soft≠green

Cited from qstack catalog §5 / `profile.json` `target.dependency_direction` Soft≠green. Do not invent new contracts.

## Allowed

```text
hbt-live (optional)
   ├──> hbt-runtime
   └──> hbt-engine

hbt-runtime
   └──> hbt-engine

hbt-engine
   └──> hftbacktest
```

Notes Soft≠green:

- MVP scaffold wires `hbt-runtime` → `hbt-engine` (path).
- `hbt-engine` → `hftbacktest` is **deferred** until D0 (#2) freezes the baseline pin Soft≠green.
- `hbt-live` is **omitted** from the workspace until D5 Soft≠green.

## Forbidden

```text
hftbacktest -> hbt-engine / hbt-runtime / hbt-live
hftbacktest -> qstack / qorch / pstack
hbt-engine  -> qorch research schemas
runtime hot path -> LLM / MCP / database / research orchestration
```

## EventKey / EventPhase Soft≠green (cite)

From `profile.json` `ordering` (phase_contract_version = 2):

**EventKey fields** (lexicographic order authoritative):

1. `timestamp`
2. `phase`
3. `source_priority`
4. `venue_no`
5. `asset_no`
6. `sequence`

**Phases:**

| Code | Name |
|---:|---|
| 10 | OldResponseDelivery |
| 20 | ExchangeState |
| 30 | MarketDelivery |
| 40 | StrategyCallback |
| 50 | CommandArrival |
| 60 | Matching |
| 65 | PostMatchingSettlement |
| 70 | ZeroLatencyResponse |
| 80 | Timer |
| 90 | PostTradeRisk |

Invariant Soft≠green (cite §6):

```text
same initial state + same canonical event set + same config/models/seed
=> same ordered transitions + same canonical terminal state
```

Typed Rust definitions land in **D1 (#3)** Soft≠green — not in this scaffold PR.
