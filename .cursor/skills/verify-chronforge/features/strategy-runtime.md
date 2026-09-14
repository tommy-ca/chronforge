# Strategy runtime

## Sub-features

- `RuntimeEvent` / `RuntimeEventSource` progression;
- `Strategy` / `StrategyContext` boundary;
- serialized callback lifecycle;
- scoped borrowed views;
- immutable software/run/determinism receipts;
- optional native/FFI parity when selected.

## How to get to it (user POV)

This surface is implemented in D3, with optional D4 FFI work after D3.J.

## Driving it with ChronForge verification tools

Current behavior is intentionally blocking:

```bash
bash tools/verify/verify.sh d3
```

When D3 lands, replace the blocker with executable lifecycle/callback/artifact levers. D4 remains separately capability-gated.

## Gotchas

- A strategy callback must not own the event loop or advance the runtime clock.
- Callback serialization/lifetime claims require executable Runtime evidence.
- Native/FFI layout equivalence is not required until FFI is selected.
- Qstack `strategy-runtime-contract` and `replay-parity` remain semantic authorities; local tooling supplies evidence only.
