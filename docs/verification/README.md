# ChronForge verification harness

ChronForge verification composes three layers:

```text
pstack
  generic project-verification discipline
      +
qstack
  deterministic-quant invariants / verification profiles
      +
ChronForge
  executable repo levers / fixtures / receipts
```

## Entry points

```bash
bash tools/verify/doctor.sh
bash tools/verify/verify.sh control-plane
bash tools/verify/verify.sh d0
python3 tools/verify/repeat_hash.py -n 3 -- <canonical-output-command>
```

Project skill: `.cursor/skills/verify-chronforge/SKILL.md`.

## Verdicts

- `PASS` — the invoked lever ran and met its declared contract.
- `ISSUES` — the lever ran and falsified at least one required condition.
- `BLOCKED` — the required executable surface/environment/capability does not exist or is not selected.

`BLOCKED`, timeout, skipped, unavailable and unsupported are never PASS.

## Evidence classes

Use the strongest class actually earned, never the strongest class desired:

```text
Static
Metadata
formal/property
Runtime
PAPER
LIVE
```

A profile may require several classes. `Static/Metadata/CI` success does not imply deterministic Runtime/PAPER/LIVE success.

## Profile map

`tools/verify/profiles.json` binds ChronForge phases to qstack semantic identifiers and local executable levers. Qstack skill bodies are not copied into this repository.

Current executable profiles:

| Profile | Local proof | Evidence earned by local profile |
|---|---|---|
| `control-plane` | OpenSpec strict + Cargo check + dependency guard | Static/Metadata/CI |
| `d0` | landed D0 receipt structure/honesty | Metadata |
| `d1` | not implemented | BLOCKED |
| `d2` | not implemented | BLOCKED |
| `d3` | not implemented | BLOCKED |
| `d4`-`d6` | optional capabilities not selected/implemented | BLOCKED |

## Verification receipt envelope

A phase/join or PR verification record should contain at minimum:

```json
{
  "schema": "chronforge.verification.receipt/v1",
  "profile": "d2",
  "verdict": "PASS",
  "evidence_class": ["Runtime"],
  "source_revision": "<git sha>",
  "qstack_revision": "cf4e62f4ef98fe378393fa3adff8449ff9457024",
  "qstack_profiles": ["QD-05", "QD-06", "replay-parity"],
  "acceptance_ids": ["<ids>"],
  "lever_results": [],
  "artifact_digests": {},
  "limitations": []
}
```

The exact phase receipt may add domain fields, but must not weaken verdict/evidence semantics.

## Deterministic repeat helper

`repeat_hash.py` intentionally compares byte-identical stdout and exit status. It sets `CHRONFORGE_VERIFY_RUN_INDEX` for each run so tests can deliberately prove the negative path. It does not normalize timestamps, PIDs or floating logs; runtime work should expose a canonical machine-readable output instead.

## Maintenance

Use upstream pstack `/maintain-verification-skill` to audit the project-local feature map against the repository. If qstack semantics change, update only identifiers/profile bindings and local levers that actually changed; do not vendor qstack skill text.
