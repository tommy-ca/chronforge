# Design: ChronForge verification harness

## Context

ChronForge already has:

- an intent-driven OpenSpec lifecycle;
- qstack phase/capability/verification profiles;
- pstack generic verification-skill generation and maintenance patterns;
- repo CI for strict OpenSpec validation, Rust workspace compilation, and dependency-boundary checks;
- D0 baseline artifacts and future D1-D3 runtime work.

The missing layer is a single repo-owned verification interface that agents and CI can both use.

## Goals

- One project-local verification skill.
- One executable verification entrypoint.
- Machine-readable phase/profile mapping.
- Typed evidence and honest `PASS | ISSUES | BLOCKED` results.
- D0 executable checks now; D1-D6 extensible later.
- CI and agent runs use the same underlying tools.

## Non-Goals

- Copy pstack verification skills.
- Copy qstack audit/replay/formal-model skills.
- Build a generic test framework.
- Claim runtime/live proof for unimplemented capabilities.
- Put verification dependencies on runtime hot paths.

## Decisions

### D1. Project-local skill is an adapter, not a fork

Create `.cursor/skills/verify-chronforge/` using pstack's documented project verification shape. The skill contains ChronForge-specific commands and feature maps only.

### D2. Repo-owned tools are the executable source

Use `tools/verify/verify.sh <profile>` as the stable entrypoint. Supporting scripts implement concrete checks. CI calls this same entrypoint.

### D3. Profiles bind qstack semantics by identifier

`tools/verify/profiles.json` records per-phase qstack capability/verification names plus local levers. It does not embed qstack skill text.

### D4. Current profiles

- `control-plane`: strict OpenSpec + workspace compile + dependency guard.
- `d0`: control-plane + D0 baseline receipt validation.
- `d1`, `d2`, `d3`: return BLOCKED until corresponding executable runtime levers exist; metadata names expected qstack profiles.
- `d4`-`d6`: BLOCKED unless capability selected and executable levers exist.

### D5. Deterministic repeat helper is intentionally narrow

`repeat_hash.py` runs a command N times, requires identical exit code/stdout bytes, hashes each stdout, and emits JSON. It does not normalize timing/log noise; callers must supply canonical-output commands. This keeps the tool simple and falsifiable.

### D6. Evidence artifact shape

Each profile run prints/optionally writes JSON containing:

- profile;
- verdict;
- evidence_class;
- qstack references;
- local lever results;
- revision when available;
- limitations/blockers.

Individual helpers may emit narrower JSON consumed by the shell entrypoint.

## Risks / Trade-offs

- Shell/Python portability -> depend only on bash, Python 3, Cargo, Node/npm already used by CI.
- Future runtime needs richer canonicalization -> add a new runtime-specific lever rather than expanding `repeat_hash.py` prematurely.
- Skill/feature map drift -> maintain using upstream pstack `maintain-verification-skill`; local CI verifies scripts, not prose completeness.
- CI duplication -> workflow invokes `verify.sh control-plane`; child commands live in repo tools.

## Migration Plan

1. Merge this intent/spec change.
2. Add the project-local skill, feature map, tools and CI refactor.
3. Run doctor/control-plane/D0 and repeat-helper self-tests.
4. Merge implementation.
5. Archive this change and promote living spec.

## Open Questions

None blocking. D1-D6 runtime-specific verification commands will be added by those implementation changes when executable surfaces exist.
