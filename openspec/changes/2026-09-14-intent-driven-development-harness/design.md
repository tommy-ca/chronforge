# Design: Intent-driven qstack/pstack development harness

## Context

ChronForge has four relevant control surfaces:

1. OpenSpec intent artifacts already using the bundled `intent-driven` schema.
2. qstack's ChronForge ProjectProfile and quant-domain development contracts.
3. upstream pstack generic engineering playbooks/orchestration mechanics.
4. ChronForge GitHub issues/PRs and project-owned Runtime evidence.

The repository also hands verified artifacts to qorch for later quant research. The defect is not missing capability; it is missing precedence and lifecycle glue between these surfaces.

Reference pins for this design:

- intent template: `intent-driven-dev/intent-driven-template@5673ba9799bc3c768ed499496de476f1f88666c5`
- pstack host repo: `cursor/plugins@be432a96ed36e48d05f44bf375864355f62263f9`, subtree `pstack/`
- qstack project profile: `tommy-ca/qstack@cf4e62f4ef98fe378393fa3adff8449ff9457024`
- ChronForge qstack binding: `e74dd7ea0dec315b84331fbc0bb941f3a2f9390f`

## Goals

- Make one intent-to-implementation lifecycle obvious from the repository itself.
- Preserve qstack/pstack separation rather than creating another generic workflow.
- Keep project work state in ChronForge and research state in qorch.
- Bind D0-D6 recursive issue graphs to OpenSpec intent and join receipts.
- Make evidence classes and merge/archive order explicit.
- Remain agent/harness portable: repo-local instructions should work with Cursor/pstack and other agents that can read `AGENTS.md` and OpenSpec artifacts.

## Non-Goals

- Vendor pstack or qstack.
- Vendor intent-template OpenCode/Superpowers/TDD collaboration layers.
- Replace GitHub issues/PRs with OpenSpec tasks.
- Put qstack, pstack, qorch, OpenSpec, LLM, MCP, or database calls in ChronForge runtime code.
- Make every read-only investigation create a product specification.
- Treat specification validation as runtime proof.

## Decisions

### D1. OpenSpec is the durable intent source

Material behaviour/architecture/dependency/state-contract changes begin with the existing intent-driven artifact chain:

```text
proposal -> specs -> design -> adr -> tasks
```

The change remains active through implementation and is archived after implementation merges and verification is complete.

**Why:** OpenSpec already exists in ChronForge and expresses durable behavioural intent better than issue prose alone.

**Alternative rejected:** issue-only development. Issues are excellent project execution state but weak as durable behavioural/specification source.

### D2. Qstack composes quant development; pstack supplies generic engineering mechanics

Execution resolves as:

```text
OpenSpec accepted intent
  -> qstack ChronForge ProjectProfile
  -> relevant QD capability + verification profiles
  -> upstream pstack base playbook/orch mechanics
  -> ChronForge issue/branch/PR/evidence
```

**Why:** qstack already encodes deterministic-quant invariants and deliberately reuses pstack rather than forking it.

**Alternative rejected:** copy pstack/qstack skills into ChronForge. This creates semantic drift and duplicate ownership.

### D3. ChronForge GitHub state is the project execution source

OpenSpec `tasks.md` describes accepted implementation work. ChronForge issues/child issues are the executable project graph. A task MAY map one-to-one or many-to-one to issues, but every applied task must have an explicit project work reference.

Phase issues aggregate acceptance; leaf issues perform work; join issues own phase readiness transitions.

### D4. Three-step git discipline for material changes

Normal changes use three merge boundaries:

```text
A. intent/spec PR
   proposal/specs/design/ADR/tasks -> main

B. implementation PR(s)
   apply accepted tasks -> verify -> main

C. archive PR
   archive OpenSpec change -> update living spec
```

Small implementation may use one implementation PR; large work may use pstack multi-phase/orchestrate and multiple stacked PRs, but archive remains last.

### D5. Repo-local instructions, not vendored collaboration stacks

Add `AGENTS.md`, a tailored `openspec/config.yaml`, and project docs. Do not copy `.opencode/`, `.agents/`, Superpowers, or duplicate pstack skills solely because the template provides them.

**Why:** pstack already covers generic engineering, review, planning, TDD, swarm, and shipping concerns. Local copies would violate DRY/YAGNI.

### D6. Evidence classes are first-class

The harness records whether evidence is Static, Metadata, formal/property, Runtime, PAPER, or LIVE. Join gates may require specific evidence classes. Lower classes never imply higher classes.

### D7. Emergency fix path is explicit but reconciled

Urgent safety fixes may temporarily bypass the full artifact chain, but the PR must declare the exception and a reconciliation OpenSpec task must be created before normal release/archive closure.

## Execution Architecture

```text
Intent
  |
  v
OpenSpec active change
proposal -> specs -> design -> ADR -> tasks
  |
  | accepted on main
  v
qstack ChronForge ProjectProfile
  +-- QD capability profiles
  +-- verification profiles
  |
  v
pstack base playbook / orch mechanics
  |
  v
ChronForge leaf issues -> PRs -> join gate
  |
  +-- static/formal/runtime verification as required
  |
  v
merge implementation
  |
  v
OpenSpec verify + archive
  |
  v
living specs + immutable software/runtime receipts
  |
  +--> qorch research program when research is requested
```

## D0-D6 Mapping

| Phase | OpenSpec concern | qstack overlay | pstack execution shape | ChronForge gate |
|---|---|---|---|---|
| D0 | baseline/characterization intent | QD-15 + deterministic-runtime-audit | investigation/refactor/multi-phase as needed | D0 join receipt |
| D1 | engine contract behaviour | QD-06 + formal-state-model + replay-parity | feature + multi-phase | D1 contract join |
| D2 | kernel integration behaviour | QD-05/QD-06 + runtime audit | feature/refactor + multi-phase | D2 Runtime join |
| D3 | strategy runtime behaviour | QD-16 + strategy-runtime-contract | feature + multi-phase | D3 native MVP join |
| D4 | optional ABI capability | QD-16, FFI selected | feature | D4 acceptance |
| D5 | optional live capability | QD-01/QD-10 + bounded-hot-paths | multi-phase/runtime-forensics/perf as needed | D5 live acceptance |
| D6 | selected governance/recovery | QD-08/QD-09/QD-13 | multi-phase + formal/runtime verification | D6 selected capability acceptance |

## Risks / Trade-offs

- **Process overhead for tiny changes** -> read-only/docs/mechanical changes may use a no-new-product-intent path; materiality is defined in AGENTS/docs.
- **OpenSpec tasks and GitHub issues drift** -> every active implementation PR names both; join gate checks mapping.
- **Upstream pstack/qstack changes** -> pin references for each material change and review compatibility rather than vendoring.
- **Emergency path becomes normal path** -> require explicit emergency label/statement plus retrospective OpenSpec reconciliation.
- **Spec green mistaken for runtime green** -> evidence class is mandatory in status and join receipts.

## Migration Plan

1. Merge this intent/spec PR.
2. Apply H0.2: add AGENTS, config rules, orchestration docs, execution graph, README pointers, and repository ADR.
3. Verify the implementation against this spec.
4. Merge H0.2 implementation.
5. Archive this change in H0.3 and read back the living spec.
6. Update program #1 so future D1+ work uses the flow. D0 historical evidence remains valid.

## Open Questions

None blocking. Runtime-specific design questions remain owned by D1-D6 changes, not this harness.
