# Development control plane

## Sub-features

- strict OpenSpec validation;
- Rust workspace compilation;
- runtime-manifest control-plane dependency boundary.

## How to get to it (user POV)

From repository root, use the same control-plane verification entrypoint used by CI.

## Driving it with ChronForge verification tools

```bash
bash tools/verify/doctor.sh
bash tools/verify/verify.sh control-plane
```

Observable proof is exit code 0 plus the final profile JSON with `"verdict":"PASS"`. CI should invoke the same command.

## Gotchas

- This earns Static/Metadata/CI evidence only.
- `cargo check` is not deterministic Runtime/PAPER/LIVE proof.
- OpenSpec validation proves specification consistency, not engine behavior.
