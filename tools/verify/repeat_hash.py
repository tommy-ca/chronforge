#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class RunResult:
    index: int
    returncode: int
    stdout_sha256: str
    stderr_sha256: str


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a canonical-output command repeatedly and compare byte-identical stdout/exit status.")
    parser.add_argument("-n", "--repeat", type=int, default=2)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if args.repeat < 2:
        parser.error("--repeat must be >= 2")
    if not command:
        parser.error("command required after --")

    results: list[RunResult] = []
    first_stdout: bytes | None = None
    first_code: int | None = None
    issues: list[str] = []

    for index in range(args.repeat):
        env = os.environ.copy()
        env["CHRONFORGE_VERIFY_RUN_INDEX"] = str(index)
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)
        results.append(RunResult(index, proc.returncode, digest(proc.stdout), digest(proc.stderr)))
        if first_stdout is None:
            first_stdout = proc.stdout
            first_code = proc.returncode
        else:
            if proc.stdout != first_stdout:
                issues.append(f"stdout diverged at run {index}")
            if proc.returncode != first_code:
                issues.append(f"exit status diverged at run {index}: {proc.returncode} != {first_code}")
        if proc.returncode != 0:
            issues.append(f"run {index} exited nonzero: {proc.returncode}")

    result = {
        "schema": "chronforge.verification.repeat-hash/v1",
        "verdict": "ISSUES" if issues else "PASS",
        "evidence_class": "Runtime",
        "repeat_count": args.repeat,
        "command": command,
        "canonical_stdout_sha256": results[0].stdout_sha256,
        "runs": [r.__dict__ for r in results],
        "issues": sorted(set(issues)),
        "limitations": [
            "Comparison is byte-exact stdout plus exit status.",
            "Callers must supply canonical-output commands; timing/log normalization is intentionally out of scope."
        ],
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
