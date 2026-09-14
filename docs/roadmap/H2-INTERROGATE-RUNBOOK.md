# H2 multi-model interrogate runbook

This runbook closes the remaining H2.3 review gate for recursive issue orchestration.

## Scope

Review the H2 implementation that landed through PR #52.

```text
base intent merge: c1f486379d97054046a0d0c9290cfa88bf522e0c
implementation merge: 8392e5f1e267860301e365c8157aff66c5c04b9c
review scope: c1f486379d97054046a0d0c9290cfa88bf522e0c..8392e5f1e267860301e365c8157aff66c5c04b9c
```

The intent is to verify that ChronForge's recursive issue-orchestration control plane correctly composes OpenSpec intent, qstack quant-development profiles, pstack engineering mechanics, purposeful swarm/arena/interrogate usage, project-owned verification levers, and typed child/join evidence without introducing runtime dependencies or false Runtime/PAPER/LIVE claims.

## Required harness

Run inside a Cursor/pstack session that exposes the `Task` subagent primitive used by upstream `pstack/skills/interrogate`.

Upstream interrogate supports an explicit model panel through:

```text
~/.cursor/rules/pstack-models.mdc
```

Before execution, run `/setup-pstack` or otherwise validate the actual Task model slugs available in that session. Never claim a real model slug is usable until the harness accepts it.

## Preferred reviewer panel

Use four independent model families when the harness exposes compatible slugs:

```text
interrogate reviewers:
  claude-fable-5-1-thinking-max,
  gpt-5.6-sol-max,
  grok-4.6-fast-xhigh,
  claude-opus-5-thinking-xhigh
```

These are the upstream pstack defaults at the pinned pstack revision. If a slug is unavailable, use the closest valid high-reasoning variant from the same family as instructed by upstream pstack. `inherit-parent` or `auto` is legal but reduces model-family diversity and SHOULD be used only when the session cannot expose enough distinct real slugs.

The run is valid when at least two independent reviewer model families execute successfully. Four distinct families are preferred. If fewer than two independent families are available, record the gate as `BLOCKED:model-diversity` rather than silently converting interrogate into a single-model review.

## Invocation

From a checkout containing the merged H2 implementation:

```text
/interrogate review the H2 recursive orchestration changes between
c1f486379d97054046a0d0c9290cfa88bf522e0c and
8392e5f1e267860301e365c8157aff66c5c04b9c.

Intent: verify ownership boundaries, issue graph correctness, OpenSpec intent gates,
qstack/pstack separation, swarm/arena/interrogate semantics, lever falsifiability,
join evidence requirements, control-plane/runtime dependency isolation, and evidence honesty.
Do not modify files. Treat missing Runtime/PAPER/LIVE evidence as a correctness issue only
if the implementation claims that evidence exists.
```

Interrogate is readonly. Reviewer findings MUST NOT be auto-applied.

## Required synthesis

The lead synthesis must contain:

- reviewer label and resolved model slug for every reviewer;
- each reviewer's finding count;
- `Act on`, `Consider`, `Noted`, and `Dismissed` sections;
- an agreement map identifying consensus and disagreement;
- explicit statement of reviewer model-family count;
- explicit statement that no changes were auto-applied.

Every `Act on` item blocks H2 archive until addressed and reverified. `Consider`, `Noted`, and `Dismissed` items are recorded but do not independently block archive.

## Receipt

Post the synthesized verdict to ChronForge issue #50 and record this compact receipt:

```yaml
InterrogateReceipt:
  scope_base: c1f486379d97054046a0d0c9290cfa88bf522e0c
  scope_head: 8392e5f1e267860301e365c8157aff66c5c04b9c
  pstack_revision: be432a96ed36e48d05f44bf375864355f62263f9
  reviewers:
    - label: Reviewer A
      model: <resolved Task slug>
      family: <family>
    - label: Reviewer B
      model: <resolved Task slug>
      family: <family>
  independent_model_families: <N>
  act_on: <count>
  consider: <count>
  noted: <count>
  dismissed: <count>
  auto_applied: false
  verdict: PASS | ISSUES | BLOCKED
```

`PASS` requires:

1. at least two independent reviewer model families;
2. zero unresolved `Act on` findings;
3. the final merged H2 implementation remains green through `bash tools/verify/verify.sh control-plane`;
4. no new false Runtime/PAPER/LIVE claim;
5. no qstack/pstack/OpenSpec control-plane dependency in synchronous runtime crates.

## Runtime limitation policy

The ChatGPT/GitHub connector environment used to construct H2 cannot itself spawn pstack `Task` reviewers. This is an execution-environment limitation, not an interrogate design limitation. Because upstream pstack supports explicit reviewer models, this limitation is **not** a reason to waive the gate.

If a compatible Cursor/pstack harness is unavailable, #50 remains `READY-external` / `BLOCKED-runtime` with this runbook as the exact resumption contract. Do not fabricate reviewer identities or model outputs.

## After PASS

After posting a valid PASS receipt:

1. mark OpenSpec task 4.3 complete;
2. archive `2026-09-14-recursive-issue-orchestration`;
3. run strict OpenSpec validation and `bash tools/verify/verify.sh control-plane` on the archive PR;
4. merge archive PR;
5. read back the living `chronforge-recursive-issue-orchestration` capability from `main`;
6. close #50 and then #47;
7. resume the runtime frontier at #11/#12/#13 -> #14.
