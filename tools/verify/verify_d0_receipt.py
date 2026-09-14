#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "docs/architecture/runtime-recomposition/D0-baseline-receipt.json"


def main() -> int:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    receipt = json.loads(path.read_text())
    schema = receipt.get("schema")
    if schema == "chronforge.D0BaselineReceipt/v1":
        cmd = [sys.executable, str(ROOT / "tools/verify/verify_d0_characterization_receipt.py"), str(path)]
    elif schema == "chronforge.D0BaselineReceipt/v2":
        status = receipt.get("verification", {}).get("status")
        cmd = [sys.executable, str(ROOT / "tools/verify/verify_d0_join.py")]
        if status == "CANDIDATE_PENDING_INTERROGATE":
            cmd.append("--candidate")
        elif status == "READY_FOR_FINAL_STAMP":
            cmd.append("--prestamp")
    else:
        print(json.dumps({"schema":"chronforge.verification.d0-receipt-router/v1","verdict":"ISSUES","issues":[f"unsupported D0 receipt schema: {schema}"]}, sort_keys=True))
        return 1
    return subprocess.run(cmd, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
