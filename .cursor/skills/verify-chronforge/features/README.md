# ChronForge verification feature map

| Feature | Current lever | Current status |
|---|---|---|
| [Development control plane](development-control-plane.md) | `bash tools/verify/verify.sh control-plane` | executable |
| [D0 baseline receipt](d0-baseline.md) | `bash tools/verify/verify.sh d0` | executable Metadata validation |
| [Deterministic engine](deterministic-engine.md) | D1/D2 profiles | BLOCKED until D1/D2 levers exist |
| [Strategy runtime](strategy-runtime.md) | D3 profile | BLOCKED until D3 levers exist |

Use the smallest profile that can falsify the claim. A feature map entry is not a PASS receipt.
