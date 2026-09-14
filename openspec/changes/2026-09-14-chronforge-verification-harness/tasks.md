# Tasks

## 1. Project-local verification skill

- [ ] 1.1 Add `.cursor/skills/verify-chronforge/SKILL.md` with Launch/Doctor/Drive/Evidence/Cleanup/Helpers sections.
- [ ] 1.2 Add feature-map index and control-plane, D0, deterministic-engine, and strategy-runtime feature files.
- [ ] 1.3 Reference pstack create/maintain-verification-skill and qstack verification profiles without copying their skill bodies.

## 2. Repo-owned verification tools

- [ ] 2.1 Add `tools/verify/doctor.sh`.
- [ ] 2.2 Add `tools/verify/profiles.json` mapping ChronForge phases to qstack semantics and local levers.
- [ ] 2.3 Add `tools/verify/control_plane_guard.py`.
- [ ] 2.4 Add `tools/verify/verify_d0_receipt.py`.
- [ ] 2.5 Add `tools/verify/repeat_hash.py` with machine-readable PASS/ISSUES output.
- [ ] 2.6 Add `tools/verify/verify.sh` as the canonical profile entrypoint.

## 3. CI and documentation

- [ ] 3.1 Refactor `.github/workflows/verify.yml` to call `tools/verify/verify.sh control-plane`.
- [ ] 3.2 Add verification harness documentation/receipt shape and link it from README/AGENTS or orchestration docs.
- [ ] 3.3 Ensure unimplemented D1-D6 profiles report BLOCKED rather than PASS.

## 4. Verification and archive

- [ ] 4.1 Run strict OpenSpec validation.
- [ ] 4.2 Run `tools/verify/doctor.sh`.
- [ ] 4.3 Run `tools/verify/verify.sh control-plane`.
- [ ] 4.4 Run `tools/verify/verify.sh d0`.
- [ ] 4.5 Self-test `repeat_hash.py` with one stable and one intentionally divergent command.
- [ ] 4.6 Merge implementation before archive.
- [ ] 4.7 Archive change and read back living `chronforge-verification-harness` spec.
