#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "tools/verify/validate_issue_orchestration.py"
INDEX = ROOT / "docs/roadmap/ISSUE-ORCHESTRATION.json"


def run(path: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def expect_rejected(path: pathlib.Path, label: str) -> bool:
    result = run(path)
    if result.returncode == 0 or '"verdict": "ISSUES"' not in result.stdout:
        print(f"negative fixture {label} was not rejected", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False
    return True


def write_temp_index(data: dict[str, object]) -> pathlib.Path:
    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    with handle:
        json.dump(data, handle)
    return pathlib.Path(handle.name)


def main() -> int:
    positive = run(INDEX)
    if positive.returncode != 0 or '"verdict": "PASS"' not in positive.stdout:
        print("positive orchestration fixture failed", file=sys.stderr)
        print(positive.stdout, file=sys.stderr)
        print(positive.stderr, file=sys.stderr)
        return 1

    index = json.loads(INDEX.read_text())

    coverage = json.loads(INDEX.read_text())
    coverage["required_issues"] = coverage["required_issues"][:-1]
    coverage_path = write_temp_index(coverage)
    try:
        if not expect_rejected(coverage_path, "coverage"):
            return 1
    finally:
        coverage_path.unlink(missing_ok=True)

    d0_rel = "docs/roadmap/issue-orchestration/d0.json"
    d0 = json.loads((ROOT / d0_rel).read_text())

    bad_subset = json.loads(json.dumps(d0))
    row12 = next(row for row in bad_subset["entries"] if row["issue"] == 12)
    row12["dependencies"]["start_after"] = [11, 14]
    subset_rel = "tools/verify/.tmp-issue-orchestration-bad-subset.json"
    subset_path = ROOT / subset_rel
    subset_path.write_text(json.dumps(bad_subset))
    subset_index = json.loads(INDEX.read_text())
    subset_index["includes"] = [subset_rel if rel == d0_rel else rel for rel in subset_index["includes"]]
    subset_index_path = write_temp_index(subset_index)
    try:
        if not expect_rejected(subset_index_path, "start-after-subset"):
            return 1
    finally:
        subset_path.unlink(missing_ok=True)
        subset_index_path.unlink(missing_ok=True)

    bad_cycle = json.loads(json.dumps(d0))
    row11 = next(row for row in bad_cycle["entries"] if row["issue"] == 11)
    row11["dependencies"] = {"start_after": [12], "verify_after": [12]}
    cycle_rel = "tools/verify/.tmp-issue-orchestration-cycle.json"
    cycle_path = ROOT / cycle_rel
    cycle_path.write_text(json.dumps(bad_cycle))
    cycle_index = json.loads(INDEX.read_text())
    cycle_index["includes"] = [cycle_rel if rel == d0_rel else rel for rel in cycle_index["includes"]]
    cycle_index_path = write_temp_index(cycle_index)
    try:
        if not expect_rejected(cycle_index_path, "dependency-cycle"):
            return 1
    finally:
        cycle_path.unlink(missing_ok=True)
        cycle_index_path.unlink(missing_ok=True)

    print(json.dumps({
        "schema": "chronforge.verification.issue-orchestration-self-test/v2",
        "verdict": "PASS",
        "evidence_class": "Static/Metadata",
        "positive_fixture": "PASS",
        "negative_fixtures": [
            "coverage:REJECTED_AS_EXPECTED",
            "start-after-subset:REJECTED_AS_EXPECTED",
            "dependency-cycle:REJECTED_AS_EXPECTED",
        ],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
