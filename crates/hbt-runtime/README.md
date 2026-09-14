# hbt-runtime

ChronForge strategy runtime — **scaffold Soft≠green**.

## Module skeleton (qstack catalog §4.2)

| Module | Role |
|---|---|
| `event` | RuntimeEvent + borrowed payload views |
| `source` | RuntimeEventSource |
| `strategy` | native Strategy contract + StrategyContext |
| `runtime` | runtime-owned loop / callback lifecycle |
| `command` | strategy request → canonical ExecutionCommand |
| `abi` | feature-gated optional foreign ABI (`abi` feature) |

## Dependencies

```text
hbt-runtime ──> hbt-engine
```

Runtime owns clock/event loop; strategies own local state and decisions only Soft≠green.

## Soft≠green honesty

- Compile stubs only — not product logic.
- `cargo check` ≠ Runtime PASS; Static/Metadata ≠ LIVE_PASS.
