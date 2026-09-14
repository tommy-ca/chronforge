# hbt-engine

ChronForge deterministic domain engine — **scaffold Soft≠green**.

## Module skeleton (qstack catalog §4.1)

| Module | Role |
|---|---|
| `domain` | canonical ids, DecimalUnit, capability identities |
| `scheduler` | EventPhase, EventKey, deterministic scheduler |
| `execution` | ExecutionCommand, ExecutionReport, OrderState |
| `account` | deterministic account/position/balance projections |
| `funding` | optional funding attribution |
| `risk` | narrow extension seams (AllowAll / basic limits) |
| `result` | RunReceipt / RunResult / reproducibility metadata |
| `adapters::hftbacktest` | bridge existing local/exchange processors to canonical facts |

## Dependency law

```text
hbt-engine ──(later, after D0 pin)──> hftbacktest
```

- **Allowed later:** `hbt-engine` may depend on `hftbacktest` once D0 (#2) freezes the baseline SHA Soft≠green.
- **Forbidden:** reverse dependency (`hftbacktest` → `hbt-engine` / runtime / live).
- **This scaffold:** no hard `hftbacktest` Cargo dep yet Soft≠green (D0 freezes baseline first).

## Soft≠green honesty

- Compile stubs only — not product logic.
- `cargo check` ≠ Runtime PASS; Static/Metadata ≠ LIVE_PASS.
- Do not vendor Titan. Do not clone Titan/hftbacktest trees into this repo.

## SoT

Contracts: qstack catalog `titan-hftbacktest-recomposition-project.md` + `profile.json` (evidence pins in root README).
