---
name: verify-chronforge
description: "Verify ChronForge repository behavior and deterministic-trading development contracts using repo-owned tools, qstack quant profiles, and pstack verification discipline. Use before review/merge, at D-phase join gates, or when evidence claims need to be proven."
disable-model-invocation: true
---

# Verify ChronForge

This is the project-local verification adapter generated from pstack's verification-skill pattern. Generic verification methodology remains upstream pstack-owned; quant semantics remain qstack-owned. This skill contains only ChronForge-specific commands, evidence rules, and feature maps.

## Launch

ChronForge is currently a Rust workspace/library, not a long-running app. There is no daemon to launch.

Start by establishing the verification environment:

```bash
bash tools/verify/doctor.sh
```

Then select the smallest applicable profile:

```bash
bash tools/verify/verify.sh control-plane
bash tools/verify/verify.sh d0
```

D1-D6 profiles intentionally return `BLOCKED` until their executable surfaces exist.

## Doctor

Always run:

```bash
bash tools/verify/doctor.sh
```

A valid doctor result is JSON with `"verdict":"PASS"`. `BLOCKED` means the checkout/toolchain is not worth driving yet; fix the environment rather than weakening proof.

## Drive

Use the feature map under `features/` to choose the relevant surface.

Primary profiles:

- `control-plane` — strict OpenSpec validation, workspace compilation, and runtime dependency boundary.
- `d0` — validates the landed D0 baseline receipt and evidence honesty; it does not rerun external hftbacktest Runtime evidence.
- `d1`..`d6` — read the qstack profile mapping and return `BLOCKED` until phase-specific executable levers are implemented.

For a canonical-output determinism probe:

```bash
python3 tools/verify/repeat_hash.py -n 3 -- <canonical-output-command> [args...]
```

`repeat_hash.py` is byte-exact. Do not feed it logs containing timestamps, PIDs, random IDs, or progress noise and then normalize the mismatch away. Build a canonical-output lever instead.

## Evidence

Capture the full command transcript plus the final JSON result under a task-specific directory, for example:

```bash
mkdir -p .artifacts/verification/issue-42
bash tools/verify/verify.sh control-plane \
  | tee .artifacts/verification/issue-42/control-plane.log
```

Proof rules:

- exercise the real repo command path, not an invented mock verifier;
- capture command, exit code, revision, profile and final JSON verdict;
- preserve evidence class: `Static`, `Metadata`, `formal/property`, `Runtime`, `PAPER`, `LIVE`;
- `Static/Metadata/CI PASS` never implies Runtime/PAPER/LIVE PASS;
- `BLOCKED`, timeout, skipped and unavailable are not PASS;
- qstack skill names/profile ids are semantic references, not evidence by themselves;
- D-phase join evidence must cite the issue/PR/head SHA and applicable acceptance IDs.

The machine-readable profile map is `tools/verify/profiles.json`.

## Cleanup

Verification starts no persistent service. Individual commands may create Cargo/OpenSpec caches; leave normal build caches alone unless the task explicitly owns them.

Do not delete `.artifacts/verification/` proof during cleanup. Remove only scratch files/processes created by a task-specific future runtime lever, and only by exact path/PID that lever recorded.

## Helpers

Repo-owned helpers:

```text
tools/verify/doctor.sh
tools/verify/verify.sh
tools/verify/profiles.json
tools/verify/control_plane_guard.py
tools/verify/verify_d0_receipt.py
tools/verify/repeat_hash.py
```

Invoke shell helpers with `bash` so checkout mode bits do not become a portability assumption.

For generic skill maintenance use upstream pstack `/maintain-verification-skill`; do not fork that maintenance logic here. For quant-domain audits compose the applicable qstack skills (for example `deterministic-runtime-audit`, `replay-parity`, `formal-state-model`, `strategy-runtime-contract`) with this repo's executable levers.
