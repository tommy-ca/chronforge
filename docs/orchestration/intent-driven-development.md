# Intent-driven ChronForge development

ChronForge uses one development lifecycle that composes OpenSpec intent artifacts, qstack quant-domain orchestration, upstream pstack engineering mechanics, and ChronForge project state.

## Ownership

```text
OpenSpec
  proposal / specs / design / ADR review / tasks

qstack
  ChronForge ProjectProfile
  QD capability profiles
  quant-specific verification profiles

upstream pstack
  generic engineering workflow + orch mechanics

ChronForge
  issues / branches / PRs / code / tests / receipts

qorch
  quant-research orchestration after immutable artifact handoff
```

No control-plane system is a ChronForge runtime dependency.

## Tooling setup

### Pstack

Pstack is an upstream Cursor plugin. Install it in the agent environment and use its canonical entry:

```text
/add-plugin pstack
/setup-pstack
/poteto-mode <task>
```

The repository does not vendor pstack.

### Qstack

Qstack is the quant overlay on pstack. Ensure the `tommy-ca/qstack` plugin is available to the development agent and use the ChronForge ProjectProfile from qstack. Qstack does not replace `/poteto-mode`; it adds deterministic-quant capability and verification profiles to the upstream pstack workflow.

Pinned project-profile baseline for this harness:

```text
tommy-ca/qstack@cf4e62f4ef98fe378393fa3adff8449ff9457024
```

When using a newer qstack revision, record that revision in the OpenSpec proposal/PR and run compatibility checks before treating it as equivalent.

### OpenSpec

ChronForge bundles the `intent-driven` schema from `intent-driven-dev/intent-driven-template` and selects it in `openspec/config.yaml`.

Reference template pin:

```text
intent-driven-dev/intent-driven-template@5673ba9799bc3c768ed499496de476f1f88666c5
```

CI uses:

```bash
npx --yes @fission-ai/openspec@1.13.0 validate --all --strict
```

The repository does not copy the template's OpenCode/Superpowers collaboration stack because pstack already owns generic engineering workflow.

## Normal material-change flow

Use this flow for changes to behaviour, architecture, dependencies, state models, execution semantics, strategy runtime, live transport, recovery, safety, or other material contracts.

```text
1. Intent
   |
   v
2. OpenSpec active change
   proposal
      -> specs
      -> design
      -> ADR review / durable ADR if needed
      -> tasks
   |
   | merge intent/spec PR to main
   v
3. Qstack composition
   ChronForge ProjectProfile
   + QD capability profiles
   + verification profiles
   |
   v
4. Pstack execution
   choose upstream base playbook
   use pstack orch/multi-phase/worktree/PR mechanics
   |
   v
5. ChronForge project work
   leaf issue(s)
   -> branch/worktree
   -> implementation PR(s)
   -> verification evidence
   -> phase join receipt
   |
   | merge implementation to main
   v
6. OpenSpec verify/archive
   strict validate
   archive change
   read back living spec
   |
   v
7. Artifact handoff
   SoftwareArtifactRef / RunReceipt / DeterminismReceipt
   |
   +--> qorch only when quant research is requested
```

## Three merge boundaries

Material changes use three logical boundaries:

1. **Intent/spec merge** — proposal/specs/design/ADR/tasks are accepted on `main` before normal apply.
2. **Implementation merge(s)** — code/tests/evidence land through ChronForge PRs; large changes may use a pstack multi-phase stack.
3. **Archive merge** — OpenSpec archive occurs only after implementation is merged and verification is complete.

Do not collapse these boundaries merely to reduce PR count when doing so makes intent mutable during implementation or archives unimplemented behaviour.

## OpenSpec -> GitHub mapping

OpenSpec and GitHub issues are complementary, not competing stores.

| Concern | OpenSpec | ChronForge GitHub |
|---|---|---|
| Why change exists | proposal | issue context/link |
| Observable behaviour | specs | acceptance checklist references |
| How/architecture | design + ADR | implementation discussion/PR |
| Accepted work | tasks | leaf issues/work items |
| Execution dependency | task order | issue graph / join gates |
| Implementation state | not authoritative | issue/branch/PR |
| Verification evidence | requirements/tasks reference | CI/test/receipt evidence |
| Living contract | archived living specs | source/tests/docs implement it |

Every material implementation PR should reference:

- active OpenSpec change;
- ChronForge issue/leaf;
- qstack ProjectProfile revision and selected QD/verification profiles;
- relevant parent/join receipt;
- acceptance IDs;
- verification commands/results and evidence classes.

## Qstack phase mapping

| Phase | Qstack composition |
|---|---|
| D0 | QD-15 + `deterministic-runtime-audit` |
| D1 | QD-06 + `formal-state-model` + `replay-parity` |
| D2 | QD-05 + QD-06 + `deterministic-runtime-audit` + `replay-parity` |
| D3 | QD-16 + `strategy-runtime-contract` + `replay-parity` |
| D4 | QD-16 with FFI explicitly selected |
| D5 | QD-01 + QD-10 + `bounded-hot-paths` |
| D6 | QD-08/QD-09/QD-13 only for selected governance/recovery capabilities |

Generic feature/refactor/investigation/review/shipping/orchestration procedure stays upstream pstack.

## Read-only path

Pure investigation, inventory, explanation, or evidence collection can use qstack/pstack investigation workflows without a new product OpenSpec change.

If the investigation produces a material implementation recommendation, create or bind an OpenSpec change before apply.

## Emergency path

For a production/safety emergency where waiting would materially increase risk:

```text
incident
  -> declare emergency exception in issue/PR
  -> smallest safe fix
  -> qstack/pstack verification
  -> merge mitigation
  -> mandatory retrospective OpenSpec reconciliation
  -> normal archive/release closure only after reconciliation
```

Emergency is not a convenience path.

## Evidence classes

Always label evidence honestly:

```text
Static
Metadata
formal/property
Runtime
PAPER
LIVE
```

Examples:

- OpenSpec strict validation: Static/Metadata.
- Rust unit/property tests: Runtime at the tested scope, not PAPER/LIVE.
- 100-run replay determinism receipt: Runtime deterministic evidence.
- Paper trading: PAPER only when the real paper environment is exercised.
- Live venue execution: LIVE only when the live system is actually exercised and verified.

Timeout, skipped, unavailable, soft, or blocked is not PASS.

## Recursive phase rule

Each material D-phase uses:

```text
accepted OpenSpec intent
       |
       v
parallel/serial leaf issues
       |
       v
single join issue
       |
       v
phase receipt
       |
       v
next phase becomes READY
```

See `docs/roadmap/EXECUTION-GRAPH.md` for the current graph.
