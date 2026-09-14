#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "docs/architecture/runtime-recomposition/D0-baseline-characterization-receipt-v1.json"
EXPECTED_HBT = "058cfefd9740b6857bb875bad4d5e6547a88379a"
EXPECTED_TITAN = "3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate preserved historical D0 characterization receipt v1.")
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT)
    args = parser.parse_args()
    receipt = json.loads(args.path.read_text())
    issues: list[str] = []
    if receipt.get("schema") != "chronforge.D0BaselineReceipt/v1":
        issues.append("unexpected historical receipt schema")
    if receipt.get("feature") != "chronforge-d0-baseline":
        issues.append("unexpected historical feature id")
    if receipt.get("evidence_class") != "Static/Metadata" or receipt.get("live_pass") is not False:
        issues.append("historical evidence honesty changed")
    if receipt.get("soft_ne_green") is not True or receipt.get("timeout_ne_pass") is not True:
        issues.append("historical Soft/timeout honesty flags changed")
    if receipt.get("hftbacktest", {}).get("sha") != EXPECTED_HBT:
        issues.append("historical hftbacktest pin drifted")
    titan = receipt.get("titan_evidence_only", {})
    if titan.get("sha") != EXPECTED_TITAN or titan.get("imported") is not False:
        issues.append("historical Titan evidence-only contract drifted")
    print(json.dumps({
        "schema":"chronforge.verification.d0-characterization-v1",
        "verdict":"ISSUES" if issues else "PASS",
        "evidence_class":"Static/Metadata",
        "issues":issues,
        "limitations":["Historical characterization is preserved evidence and never authorizes D1 by itself."]
    }, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
