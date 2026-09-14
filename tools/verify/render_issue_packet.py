#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
INDEX = ROOT / "docs/roadmap/ISSUE-ORCHESTRATION.json"
START = "<!-- chronforge-execution-packet:v2"
END = "<!-- /chronforge-execution-packet -->"


def load_entries() -> dict[int, tuple[dict[str, object], str]]:
    index = json.loads(INDEX.read_text())
    out: dict[int, tuple[dict[str, object], str]] = {}
    for rel in index["includes"]:
        fragment = json.loads((ROOT / rel).read_text())
        for entry in fragment["entries"]:
            out[int(entry["issue"])] = (entry, rel)
    return out


def fmt(values: object) -> str:
    if not values:
        return "none"
    if isinstance(values, list):
        return ", ".join(f"`#{x}`" if isinstance(x, int) else f"`{x}`" for x in values)
    return f"`{values}`"


def render(entry: dict[str, object], rel: str) -> str:
    issue = int(entry["issue"])
    deps = entry["dependencies"]
    qstack = entry["qstack"]
    pstack = entry["pstack"]
    swarm = entry["swarm"]
    arena = entry["arena"]
    interrogate = entry["interrogate"]
    verification = entry["verification"]
    handoff = entry["handoff"]
    openspec = entry["openspec"]

    selection = ""
    if "selection" in entry:
        sel = entry["selection"]
        selection = (
            f"\n- **Selection:** `{sel['predicate']}`; otherwise `{sel['otherwise']}`."
        )

    return f"""{START} issue={issue} -->
## Execution packet

Authoritative machine record: `{rel}` → `issue: {issue}` (`chronforge.issue-orchestration-fragment/v2`).

- **State:** `{entry['status']}`; phase `{entry['phase']}`; kind `{entry['kind']}`.
- **Dependencies:** start after {fmt(deps['start_after'])}; verify/handoff after {fmt(deps['verify_after'])}.
- **OpenSpec:** `{openspec['change']}` / task `{openspec['task']}`.
- **Qstack-mode:** intent `development`; CapabilityProfile {fmt(qstack['capability_profiles'])}; skills {fmt(qstack['operation_skills'])}; VerificationProfile `{qstack['verification_profile']}`; ProjectProfile `{qstack['project_profile']}`.
- **Pstack:** BasePlaybook `{pstack['base_playbook']}`; orch role `{pstack['orch_role']}`.
- **Swarm:** `{swarm['mode']}` over {fmt(swarm.get('slices', []))}. Done when: {swarm['done']}.
- **Arena:** `{arena['policy']}`. Trigger: {arena['trigger']}.
- **Interrogate:** `{'required' if interrogate['required'] else 'conditional/not-required'}`. Scope: {interrogate['scope']}. Gate: {interrogate['gate']}.
- **Lever verification:** profile `{verification['profile']}`; commands {fmt(verification['levers'])}; evidence `{verification['evidence_class']}`; current proof `{verification['current_status']}`.
- **Falsifier:** {verification['falsifier']}.
- **Handoff:** produce `{handoff['produces']}` → `{handoff['consumed_by']}`.{selection}

The machine row is authoritative. This packet is a synchronized execution view; issue closure alone never substitutes for its declared lever/handoff evidence.
{END}"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render ChronForge issue execution packets from the canonical matrix.")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    entries = load_entries()
    if args.check:
        problems: list[str] = []
        for issue, (entry, rel) in sorted(entries.items()):
            first = render(entry, rel)
            second = render(entry, rel)
            if first != second:
                problems.append(f"#{issue}: nondeterministic render")
            if f"issue={issue}" not in first or END not in first:
                problems.append(f"#{issue}: packet markers missing")
            if "None" in first or "<missing>" in first:
                problems.append(f"#{issue}: unresolved packet field")
        print(json.dumps({
            "schema": "chronforge.verification.issue-packets/v1",
            "verdict": "ISSUES" if problems else "PASS",
            "evidence_class": "Static/Metadata",
            "records": len(entries),
            "issues": problems,
            "limitation": "This checks deterministic packet rendering, not remote GitHub issue-body synchronization or runtime correctness.",
        }, sort_keys=True))
        return 1 if problems else 0

    if args.issue is not None:
        if args.issue not in entries:
            print(f"unknown issue #{args.issue}", file=sys.stderr)
            return 2
        entry, rel = entries[args.issue]
        print(render(entry, rel))
        return 0

    if args.all:
        for issue, (entry, rel) in sorted(entries.items()):
            print(render(entry, rel))
            print()
        return 0

    parser.error("one of --issue, --all, or --check is required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
