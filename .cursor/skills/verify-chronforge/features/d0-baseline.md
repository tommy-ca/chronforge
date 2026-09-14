# D0 baseline receipt

## Sub-features

- characterized hftbacktest pin;
- Titan evidence-only pin;
- evidence-class honesty;
- content-hash shape;
- explicit `live_pass: false` fence.

## How to get to it (user POV)

D0 evidence lives under `docs/architecture/runtime-recomposition/`. This feature verifies the landed receipt contract, not the external hftbacktest runtime itself.

## Driving it with ChronForge verification tools

```bash
bash tools/verify/verify.sh d0
```

Observable proof is exit code 0 plus `chronforge.verification.d0-receipt/v1` and final profile JSON with `PASS` / `Metadata`.

## Gotchas

- This does not close #11/#12/#13 or accept #14 D0.J by itself.
- It does not rerun external hftbacktest tests.
- A metadata receipt cannot earn LIVE/PAPER Runtime status.
- Pin drift must go through the D0 drift/recharacterization path.
