# Proposal: Intent-driven development harness

## Why

ChronForge already has an intent-driven OpenSpec schema, qstack project profile, and recursive implementation issues, but those surfaces are not yet bound into one mandatory development lifecycle. Without one control flow, future work can drift between issue-first, spec-first, and ad-hoc implementation paths.

This change makes intent, quant-domain orchestration, generic engineering orchestration, project implementation state, verification, and later research handoff explicit and non-overlapping.

## What Changes

- Establish one repository development flow: `intent -> OpenSpec -> qstack -> pstack/orch -> ChronForge implementation -> verification -> merge -> OpenSpec archive`.
- Add repo-local instructions that point to upstream pstack/qstack rather than vendoring their skills, principles, playbooks, or orchestration code.
- Bind ChronForge D0-D6 phases and leaf/join issues to OpenSpec changes and verification gates.
- Require proposal/spec/design/ADR/tasks to land before apply for material behaviour/architecture work.
- Require implementation to merge before OpenSpec archive.
- Define immutable artifact handoff to qorch after verified software exists.
- Add an explicit emergency-fix exception that still requires retrospective intent/spec reconciliation before archive/release.

## Capabilities

### New Capabilities

- `chronforge-development-flow` — intent-driven software-development lifecycle and ownership contract for ChronForge.

### Modified Capabilities

None.

## Impact

Affected surfaces:

- `AGENTS.md`
- `openspec/config.yaml`
- `docs/orchestration/`
- `docs/roadmap/`
- repository-level `adr/`
- ChronForge issue/PR conventions

External systems remain referenced rather than vendored:

- `intent-driven-dev/intent-driven-template@5673ba9799bc3c768ed499496de476f1f88666c5`
- `cursor/plugins@be432a96ed36e48d05f44bf375864355f62263f9` (`pstack/` subtree)
- `tommy-ca/qstack@cf4e62f4ef98fe378393fa3adff8449ff9457024`

No runtime crate dependency on OpenSpec, qstack, pstack, or qorch is introduced.
