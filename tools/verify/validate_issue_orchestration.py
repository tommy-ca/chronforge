#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "docs/roadmap/ISSUE-ORCHESTRATION.json"
LEGAL_KIND = {"program", "phase", "leaf", "join", "optional"}
LEGAL_STATUS = {"ACTIVE", "READY", "INTENT_READY", "BLOCKED", "DONE"}
LEGAL_SWARM = {"none", "partition", "race", "mixed"}
LEGAL_ARENA = {"skip", "conditional", "required", "required-if-selected"}
RUNTIME_PROFILES = {"d1", "d2", "d3", "d4", "d5", "d6"}
REQUIRED_KEYS = {
    "issue", "phase", "kind", "status", "blocked_by", "openspec", "qstack",
    "pstack", "swarm", "arena", "interrogate", "verification", "handoff",
}


def load(path: pathlib.Path) -> object:
    return json.loads(path.read_text())


def fail(issues: list[str], text: str) -> None:
    issues.append(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ChronForge recursive issue orchestration metadata.")
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT)
    args = parser.parse_args()

    index = load(args.path)
    issues: list[str] = []
    if index.get("schema") != "chronforge.issue-orchestration/v1":
        fail(issues, "unexpected index schema")

    required = index.get("required_issues", [])
    if not isinstance(required, list) or not required or len(required) != len(set(required)):
        fail(issues, "required_issues must be a non-empty unique list")

    entries: list[dict[str, object]] = []
    for rel in index.get("includes", []):
        path = ROOT / rel
        if not path.is_file():
            fail(issues, f"missing include: {rel}")
            continue
        fragment = load(path)
        if fragment.get("schema") != "chronforge.issue-orchestration-fragment/v1":
            fail(issues, f"unexpected fragment schema: {rel}")
            continue
        entries.extend(fragment.get("entries", []))

    ids = [entry.get("issue") for entry in entries]
    if len(ids) != len(set(ids)):
        fail(issues, "duplicate issue records")
    if sorted(ids) != sorted(required):
        fail(issues, f"coverage mismatch required={sorted(required)} actual={sorted(ids)}")
    known = set(ids)

    profiles_path = ROOT / "tools/verify/profiles.json"
    known_profiles = set(load(profiles_path).get("profiles", {})) if profiles_path.is_file() else set()

    for entry in entries:
        issue = entry.get("issue", "?")
        missing = REQUIRED_KEYS - set(entry)
        if missing:
            fail(issues, f"#{issue}: missing keys {sorted(missing)}")
            continue
        if entry["kind"] not in LEGAL_KIND:
            fail(issues, f"#{issue}: illegal kind {entry['kind']}")
        if entry["status"] not in LEGAL_STATUS:
            fail(issues, f"#{issue}: illegal status {entry['status']}")
        blockers = entry["blocked_by"]
        if not isinstance(blockers, list) or any(x not in known for x in blockers):
            fail(issues, f"#{issue}: blocked_by references unknown issue")

        qstack = entry["qstack"]
        if qstack.get("intent") != "development":
            fail(issues, f"#{issue}: qstack intent must be development")
        if qstack.get("project_profile") != "ChronForgeProjectProfile":
            fail(issues, f"#{issue}: wrong project profile")
        if not isinstance(qstack.get("capability_profiles"), list):
            fail(issues, f"#{issue}: capability_profiles must be a list")

        swarm = entry["swarm"]
        if swarm.get("mode") not in LEGAL_SWARM or not swarm.get("done"):
            fail(issues, f"#{issue}: invalid swarm contract")
        if swarm.get("mode") != "none" and not swarm.get("slices"):
            fail(issues, f"#{issue}: swarm slices required")

        arena = entry["arena"]
        if arena.get("policy") not in LEGAL_ARENA or not arena.get("trigger"):
            fail(issues, f"#{issue}: invalid arena contract")

        interrogate = entry["interrogate"]
        if entry["kind"] == "join" and interrogate.get("required") is not True:
            fail(issues, f"#{issue}: join must require interrogate")
        if interrogate.get("required") and not interrogate.get("scope"):
            fail(issues, f"#{issue}: required interrogate scope missing")

        verification = entry["verification"]
        profile = verification.get("profile")
        if profile not in known_profiles:
            fail(issues, f"#{issue}: unknown verification profile {profile}")
        if not verification.get("levers") or not verification.get("evidence_class") or not verification.get("falsifier"):
            fail(issues, f"#{issue}: incomplete lever/evidence/falsifier contract")
        if profile in RUNTIME_PROFILES and verification.get("current_status") != "BLOCKED":
            fail(issues, f"#{issue}: {profile} must remain BLOCKED until executable profile exists")

        if entry["kind"] == "optional" and "selection" not in entry:
            fail(issues, f"#{issue}: optional node missing selection predicate")
        if not entry["openspec"].get("change") or not entry["openspec"].get("task"):
            fail(issues, f"#{issue}: OpenSpec binding incomplete")
        if not entry["pstack"].get("base_playbook") or not entry["pstack"].get("orch_role"):
            fail(issues, f"#{issue}: pstack binding incomplete")
        if not entry["handoff"].get("produces") or not entry["handoff"].get("consumed_by"):
            fail(issues, f"#{issue}: handoff contract incomplete")

    result = {
        "schema": "chronforge.verification.issue-orchestration/v1",
        "verdict": "ISSUES" if issues else "PASS",
        "evidence_class": "Static/Metadata",
        "records": len(entries),
        "required_issues": required,
        "issues": issues,
        "limitations": [
            "This validates orchestration metadata, not runtime correctness.",
            "GitHub issue body references are verified during H2 reconciliation, not inferred as Runtime evidence."
        ],
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
