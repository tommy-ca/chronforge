# ChronForge agent instructions

ChronForge is a deterministic event-time trading runtime. Treat this repository as a safety-sensitive quant-system implementation project.

## Control-plane ownership

Use these owners without duplicating them locally:

```text
OpenSpec
  durable intent: proposal / specs / design / ADR review / tasks

qstack
  project-facing quant-development composition:
  ChronForge ProjectProfile + QD capability profiles + verification profiles

upstream pstack
  generic engineering workflow/orchestration mechanics underneath qstack

ChronForge
  implementation state: issues / branches / PRs / code / tests / project evidence

qorch
  quant-research orchestration only after immutable software/runtime artifact handoff
```

Runtime crates MUST NOT depend on OpenSpec, qstack, pstack, qorch, LLM, MCP, or research orchestration.

## Canonical development flow

For a material behaviour, architecture, dependency, state-model, execution, runtime, live, recovery, or safety change:

```text
intent
  -> OpenSpec change
     proposal -> specs -> design -> adr -> tasks
  -> merge accepted intent artifacts to main
  -> resolve qstack ChronForge ProjectProfile + QD/verification profiles
  -> use upstream pstack base playbook/orch mechanics
  -> execute ChronForge issue leaf work / PRs
  -> satisfy join-gate evidence
  -> merge implementation
  -> verify OpenSpec change strictly
  -> archive OpenSpec change
  -> publish/reference immutable artifact receipts
  -> qorch only if quant research follows
```

Do not start normal implementation apply for a material change until accepted OpenSpec tasks are on `main`.

Do not archive an OpenSpec change until its implementation is merged and verified.

## Upstream reuse

- pstack canonical entry: `/poteto-mode`.
- qstack is a thin quant overlay on pstack; do not create a second generic engineering workflow.
- Do not vendor/copy pstack or qstack skills, principles, playbooks, or orchestration scripts into ChronForge.
- Do not vendor the intent-driven template's OpenCode/Superpowers collaboration layers merely because they exist; pstack already owns generic engineering mechanics.

Use repo-local OpenSpec configuration and docs to bind those external capabilities to ChronForge.

## Current external pins

Review compatibility before changing these pins:

- intent-driven template: `intent-driven-dev/intent-driven-template@5673ba9799bc3c768ed499496de476f1f88666c5`
- pstack host repository: `cursor/plugins@be432a96ed36e48d05f44bf375864355f62263f9`, subtree `pstack/`
- qstack ChronForge profile baseline: `tommy-ca/qstack@cf4e62f4ef98fe378393fa3adff8449ff9457024`
- hftbacktest kernel baseline: `tommy-ca/hftbacktest@058cfefd9740b6857bb875bad4d5e6547a88379a`
- Titan reference evidence: `dominolu/titan@3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024`

## Recursive execution

Phase parents aggregate acceptance. Leaf issues do work. Join issues decide readiness for the next phase.

Never bypass an upstream join receipt because individual leaves look green.

See:

- `docs/roadmap/EXECUTION-GRAPH.md`
- `docs/roadmap/D0-D6.md`
- `docs/orchestration/intent-driven-development.md`
- `docs/orchestration/qstack.md`

## Evidence honesty

Always name the evidence class:

- Static
- Metadata
- formal/property
- Runtime
- PAPER
- LIVE

A lower evidence class never implies a higher one. Timeout, skipped, unavailable, soft, or blocked checks are not PASS.

`cargo check` is not Runtime PASS. OpenSpec validation is not Runtime PASS. Runtime PASS is not PAPER/LIVE PASS.

## Project verification

Use the project-local `.cursor/skills/verify-chronforge/` adapter and repo-owned tools for executable proof. Generic verification-skill creation/maintenance remains upstream pstack-owned; quant semantics remain qstack-owned.

Start every non-trivial verification with:

```bash
bash tools/verify/doctor.sh
```

Then run the smallest applicable profile:

```bash
bash tools/verify/verify.sh control-plane
bash tools/verify/verify.sh d0
```

D1-D6 profiles MUST remain `BLOCKED` until their executable levers exist. Do not turn compilation/specification success into synthetic Runtime proof.

For repeated canonical-output equality use:

```bash
python3 tools/verify/repeat_hash.py -n <N> -- <canonical-output-command>
```

See `docs/verification/README.md` and `.cursor/skills/verify-chronforge/features/`.

## Read-only work

Pure investigation, explanation, inventory, or evidence gathering may proceed without creating a new product OpenSpec change. If that work leads to material implementation, create/bind the OpenSpec change before apply.

## Emergency fixes

A production-critical or safety-critical fix may use an explicit emergency exception when waiting for the full artifact chain would materially increase risk. Keep the implementation minimal, record the exception/evidence in the PR, and create retrospective OpenSpec reconciliation before normal release/archive closure.

## Change checklist

Before coding:

1. Identify the ChronForge parent/leaf issue and current join gate.
2. Identify or create the OpenSpec change.
3. Confirm accepted intent artifacts are on `main` for normal material changes.
4. Select qstack ProjectProfile/QD/verification profiles.
5. Select the upstream pstack playbook/orch execution shape.

Before merge:

1. Run `bash tools/verify/doctor.sh` and the applicable `verify-chronforge` profile(s).
2. Run phase-specific project tests/checks required by the issue.
3. Run strict OpenSpec validation for the active change when applicable (the control-plane profile includes it).
4. Record acceptance IDs and evidence classes honestly.
5. Confirm no reverse/runtime dependency on control-plane tooling.

After implementation merge:

1. Archive the OpenSpec change.
2. Read back the living specification.
3. Update the join receipt/frontier.
4. Hand immutable artifacts to qorch only when research is requested.
