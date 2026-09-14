# Proposal: ChronForge verification harness

## Why

ChronForge now has an intent-driven development flow, but verification is still split between CI YAML, issue prose, qstack semantic profiles, and ad-hoc commands. The project needs one repo-owned verification entrypoint and one project-local skill so agents can prove behaviour consistently without copying pstack or qstack.

## What Changes

- Add one project-local `verify-chronforge` skill following pstack's project-verification shape.
- Add repo-owned verification tools for doctor, profile selection, control-plane checks, D0 receipt checks, and deterministic repeated-output comparison.
- Bind verification profiles to qstack phase semantics by reference.
- Make CI invoke the same repo-owned verification entrypoint used by agents.
- Add a maintained feature map for current and future verification surfaces.
- Require unimplemented runtime levers to report `BLOCKED`, never synthetic PASS.

## Capabilities

### New Capabilities

- `chronforge-verification-harness` — project-local verification skill, executable tooling, typed evidence and profile mapping.

### Modified Capabilities

None.

## Impact

Affected surfaces:

- `.cursor/skills/verify-chronforge/`
- `tools/verify/`
- `.github/workflows/verify.yml`
- verification documentation and evidence receipts

External responsibilities remain referenced, not vendored:

- pstack `create-verification-skill` / `maintain-verification-skill` @ `cursor/plugins@be432a96ed36e48d05f44bf375864355f62263f9`
- qstack ChronForge ProjectProfile and verification skills @ `cf4e62f4ef98fe378393fa3adff8449ff9457024`

No runtime dependency on pstack, qstack, OpenSpec, qorch, LLMs, or MCP is introduced.
