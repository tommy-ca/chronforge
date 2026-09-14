# ADR-0001: Intent-driven development control plane

- Status: accepted
- Date: 2026-09-14
- Supersedes: none

## Context

ChronForge uses OpenSpec intent artifacts, qstack quant-development profiles, upstream pstack engineering/orchestration mechanics, GitHub issues/PRs, and qorch for downstream quant research. Without an explicit ownership decision, those systems can become overlapping sources of workflow truth.

The repository must preserve deterministic quant-domain semantics without copying generic engineering workflow into the project or allowing research/runtime state to leak into development orchestration.

## Decision

ChronForge adopts the following control-plane ownership:

```text
OpenSpec
  owns durable intent/spec/design/ADR/task artifacts

qstack
  owns project-facing quant-development composition,
  deterministic-quant capability profiles, and verification profiles

upstream pstack
  owns generic engineering workflow/orchestration mechanics underneath qstack

ChronForge
  owns project implementation state: issues, branches, PRs, code, tests,
  project verification evidence, and software/runtime artifacts

qorch
  owns durable quant-research orchestration only after immutable artifact handoff
```

Material behaviour/architecture changes follow `proposal -> specs -> design -> adr -> tasks` before normal implementation apply. Implementation merges before OpenSpec archive. Project runtime code has no dependency on OpenSpec, qstack, pstack, or qorch.

ChronForge references upstream pstack/qstack capabilities rather than vendoring their skills, principles, playbooks, or orchestration implementations.

## Consequences

Positive:

- one durable intent source and one project implementation-state source;
- qstack can add quant-specific gates without forking generic engineering workflow;
- pstack upgrades remain upstream rather than copied into ChronForge;
- qorch research lineage stays separate from software development state;
- OpenSpec changes remain auditable across implementation and archive.

Costs:

- material changes require intent/spec artifacts before normal apply;
- agents must resolve both OpenSpec intent and ChronForge issue state before coding;
- upstream pstack/qstack compatibility must be reviewed when pins change.

Emergency production/safety fixes may use an explicit temporary exception, but must reconcile durable intent/spec/ADR surfaces before normal release/archive closure.
