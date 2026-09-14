# Tasks

## 1. Repository control-plane instructions

- [ ] 1.1 Add `AGENTS.md` with the canonical intent -> OpenSpec -> qstack -> pstack -> ChronForge -> archive -> qorch flow.
- [ ] 1.2 Record precedence/ownership rules: OpenSpec=intent, qstack=quant composition, pstack=generic engineering substrate, ChronForge=project implementation state, qorch=research state.
- [ ] 1.3 Document the material-change threshold and explicit emergency-fix reconciliation path.

## 2. OpenSpec configuration

- [ ] 2.1 Tailor `openspec/config.yaml` context for Rust ChronForge, external hftbacktest kernel, qstack project profile, and evidence-class honesty.
- [ ] 2.2 Add proposal/spec/design/ADR/tasks rules that require qstack profile selection and ChronForge issue/acceptance mapping without referencing missing local skills.
- [ ] 2.3 Preserve the bundled `intent-driven` schema unchanged unless a schema-level need is separately proposed.

## 3. Orchestration and execution graph

- [ ] 3.1 Add `docs/orchestration/intent-driven-development.md` with normal, read-only, and emergency flows.
- [ ] 3.2 Add `docs/roadmap/EXECUTION-GRAPH.md` showing H0 and D0-D6 leaf/join gates and OpenSpec change boundaries.
- [ ] 3.3 Update README and existing qstack orchestration docs with pointers to the canonical development-flow docs.
- [ ] 3.4 Update program issue #1 with the intent-driven lifecycle and current D1 frontier after H0 closes.

## 4. Verification and archive

- [ ] 4.1 Verify no pstack/qstack/OpenCode/Superpowers workflow copy was introduced.
- [ ] 4.2 Verify runtime crates contain no OpenSpec/qstack/pstack/qorch dependency.
- [ ] 4.3 Run `openspec validate 2026-09-14-intent-driven-development-harness --type change --strict` before implementation merge/archive.
- [ ] 4.4 Merge implementation before archiving this change.
- [ ] 4.5 Archive the change and read back `openspec/specs/chronforge-development-flow/spec.md`.
- [ ] 4.6 Close #33 only after living-spec read-back and issue/PR/merge SHAs are recorded.
