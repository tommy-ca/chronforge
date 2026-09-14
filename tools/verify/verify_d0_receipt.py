#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "docs/architecture/runtime-recomposition/D0-baseline-receipt.json"
EXPECTED_HBT = "058cfefd9740b6857bb875bad4d5e6547a88379a"
EXPECTED_TITAN = "3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT)
    args = parser.parse_args()
    receipt = json.loads(args.path.read_text())

    issues: list[str] = []
    required = ["schema", "feature", "evidence_class", "live_pass", "hftbacktest", "titan_evidence_only", "content_hash", "levers"]
    for key in required:
        if key not in receipt:
            issues.append(f"missing required field: {key}")

    if receipt.get("schema") != "chronforge.D0BaselineReceipt/v1":
        issues.append("unexpected receipt schema")
    if receipt.get("feature") != "chronforge-d0-baseline":
        issues.append("unexpected feature id")
    if receipt.get("evidence_class") != "Static/Metadata":
        issues.append("D0 receipt evidence_class must remain Static/Metadata for this contract version")
    if receipt.get("live_pass") is not False:
        issues.append("D0 receipt must not claim live_pass")
    if receipt.get("soft_ne_green") is not True:
        issues.append("soft_ne_green honesty flag missing/false")
    if receipt.get("timeout_ne_pass") is not True:
        issues.append("timeout_ne_pass honesty flag missing/false")

    hbt = receipt.get("hftbacktest", {})
    if hbt.get("sha") != EXPECTED_HBT:
        issues.append("hftbacktest pin drifted from characterized baseline")
    titan = receipt.get("titan_evidence_only", {})
    if titan.get("sha") != EXPECTED_TITAN:
        issues.append("Titan evidence pin drifted from characterized baseline")
    if titan.get("imported") is not False:
        issues.append("Titan must remain evidence-only")

    hash_value = receipt.get("content_hash", {}).get("value", "")
    if len(hash_value) != 64 or any(c not in "0123456789abcdef" for c in hash_value.lower()):
        issues.append("content_hash.value is not a sha256 hex digest")

    result = {
        "schema": "chronforge.verification.d0-receipt/v1",
        "verdict": "ISSUES" if issues else "PASS",
        "evidence_class": "Metadata",
        "receipt": str(args.path.relative_to(ROOT)) if args.path.is_relative_to(ROOT) else str(args.path),
        "issues": issues,
        "limitations": [
            "This validates receipt structure and evidence honesty only.",
            "It does not rerun external hftbacktest Runtime evidence or promote D0 join readiness."
        ],
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
