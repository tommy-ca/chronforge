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


def main() -> int:
    positive = run(INDEX)
    if positive.returncode != 0 or '"verdict": "PASS"' not in positive.stdout:
        print("positive orchestration fixture failed", file=sys.stderr)
        print(positive.stdout, file=sys.stderr)
        print(positive.stderr, file=sys.stderr)
        return 1

    data = json.loads(INDEX.read_text())
    data["required_issues"] = data["required_issues"][:-1]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(data, handle)
        bad_path = pathlib.Path(handle.name)

    try:
        negative = run(bad_path)
    finally:
        bad_path.unlink(missing_ok=True)

    if negative.returncode == 0 or '"verdict": "ISSUES"' not in negative.stdout:
        print("negative orchestration fixture was not rejected", file=sys.stderr)
        print(negative.stdout, file=sys.stderr)
        print(negative.stderr, file=sys.stderr)
        return 1

    print(json.dumps({
        "schema": "chronforge.verification.issue-orchestration-self-test/v1",
        "verdict": "PASS",
        "evidence_class": "Static/Metadata",
        "positive_fixture": "PASS",
        "negative_fixture": "REJECTED_AS_EXPECTED",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
