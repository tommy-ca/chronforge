# Tasks

## 1. Project-local verification skill

- [x] 1.1 Add `.cursor/skills/verify-chronforge/SKILL.md` with Launch/Doctor/Drive/Evidence/Cleanup/Helpers sections.
- [x] 1.2 Add feature-map index and control-plane, D0, deterministic-engine, and strategy-runtime feature files.
- [x] 1.3 Reference pstack create/maintain-verification-skill and qstack verification profiles without copying their skill bodies.

## 2. Repo-owned verification tools

- [x] 2.1 Add `tools/verify/doctor.sh`.
- [x] 2.2 Add `tools/verify/profiles.json` mapping ChronForge phases to qstack semantics and local levers.
- [x] 2.3 Add `tools/verify/control_plane_guard.py`.
- [x] 2.4 Add `tools/verify/verify_d0_receipt.py`.
- [x] 2.5 Add `tools/verify/repeat_hash.py` with machine-readable PASS/ISSUES output.
- [x] 2.6 Add `tools/verify/verify.sh` as the canonical profile entrypoint.

## 3. CI and documentation

- [x] 3.1 Refactor `.github/workflows/verify.yml` to call `tools/verify/verify.sh control-plane`.
- [x] 3.2 Add verification harness documentation/receipt shape and link it from AGENTS instructions.
- [x] 3.3 Ensure unimplemented D1-D6 profiles report BLOCKED rather than PASS.

## 4. Verification and archive

- [x] 4.1 Run strict OpenSpec validation — PR #45 workflow run `34892562672` passed via the control-plane profile.
- [x] 4.2 Run `tools/verify/doctor.sh` — PR #45 workflow run `34892562672` passed.
- [x] 4.3 Run `tools/verify/verify.sh control-plane` — PR #45 workflow run `34892562672` passed.
- [x] 4.4 Run `tools/verify/verify.sh d0` — PR #45 workflow run `34892562672` passed with Metadata evidence only.
- [x] 4.5 Self-test `repeat_hash.py` with one stable and one intentionally divergent command — PR #45 workflow run `34892562672` passed; divergence was correctly rejected.
- [x] 4.6 Merge implementation before archive — PR #45 merged as `cb0e0f0d1e798d1d093fed70223edfb3a8c697db`; final-head workflow run `34892623082` passed.
- [ ] 4.7 Archive change and read back living `chronforge-verification-harness` spec — archive/read-back completion is recorded by issue #43 after the archive PR merges.
