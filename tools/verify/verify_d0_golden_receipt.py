#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "docs/architecture/runtime-recomposition/D0-golden-receipt.json"
PIN = "058cfefd9740b6857bb875bad4d5e6547a88379a"
CHILDREN = [76, 77, 78, 79, 80]
EXPECTED_HASHES = {
    "py-hftbacktest/tests/test_polymarket.py": "7ebbbd6baa407f1fad84da5a37ff246246689723db9414c6408281acbfe18b37",
    "py-hftbacktest/hftbacktest/data/utils/polymarket.py": "b5cc1fac9a9be40d1c39a444d9d8fd975387f6ae003c917fb457f4213b0d3e3e",
    "hftbacktest/src/backtest/models/fee.rs": "c6311a0c9f432e8f922702746d7481c6da0418a7c2c96ce929b58206b62a7177",
    "examples/polymarket/smoke_converter.py": "32a57155e776c3ece89f81c20d78a203650f2e2200abab7f3b77476aead841e8",
}
EXPECTED_COMMANDS = [
    "cargo check -p hftbacktest --no-default-features --features backtest",
    "cargo test -p hftbacktest --no-default-features --features backtest --lib",
    "cargo test -p hftbacktest --no-default-features --features backtest --lib binary_fee",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate D0GoldenReceipt structure and CI evidence binding.")
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT)
    parser.add_argument("--allow-pending", action="store_true")
    args = parser.parse_args()

    r = json.loads(args.path.read_text())
    issues: list[str] = []
    blocked: list[str] = []

    if r.get("schema") != "chronforge.D0GoldenReceipt/v1": issues.append("unexpected schema")
    if r.get("issue") != 13 or r.get("internal_join_issue") != 81 or r.get("implementation_issue") != 82: issues.append("issue/join/implementation binding drifted")
    hbt = r.get("hftbacktest", {})
    if hbt.get("repository") != "tommy-ca/hftbacktest" or hbt.get("revision") != PIN: issues.append("hftbacktest pin drifted")
    if hbt.get("features") != "backtest (no-default)": issues.append("feature scope drifted")

    swarm = r.get("swarm", {})
    if swarm.get("children") != CHILDREN or swarm.get("join") != 81: issues.append("golden swarm binding drifted")

    goldens = r.get("goldens", {})
    if goldens.get("commands") != EXPECTED_COMMANDS: issues.append("golden command list drifted")
    if goldens.get("fixture_sha256") != EXPECTED_HASHES: issues.append("golden fixture hashes drifted")

    coverage = r.get("coverage", {})
    for key in ("76_l2_l3_kernel", "77_queue_latency_fee", "78_order_lifecycle", "79_partial_no_partial", "80_polymarket_overlay"):
        if key not in coverage: issues.append(f"missing coverage slice {key}")
    if coverage.get("80_polymarket_overlay", {}).get("python_unittest_runtime_pass") is not False:
        issues.append("Python runtime must not be promoted to PASS without a real lever")

    verification = r.get("verification", {})
    if verification.get("lever") != "bash tools/verify/d0_goldens.sh": issues.append("wrong golden lever")
    status = verification.get("status")
    if status == "PENDING_CI":
        if not args.allow_pending: blocked.append("external golden CI evidence has not been stamped into the receipt")
    elif status == "PASS":
        run = verification.get("workflow_run")
        head = verification.get("workflow_head_sha")
        if not isinstance(run, int) or run <= 0: issues.append("PASS receipt lacks workflow_run")
        if not isinstance(head, str) or len(head) != 40: issues.append("PASS receipt lacks full workflow_head_sha")
    else:
        issues.append(f"illegal verification status {status!r}")

    limitations = "\n".join(r.get("limitations", [])).lower()
    for phrase in ("live/iceoryx", "python", "paper/live", "does not by itself accept"):
        if phrase not in limitations: issues.append(f"missing evidence-honesty limitation: {phrase}")

    if issues:
        verdict, rc = "ISSUES", 1
    elif blocked:
        verdict, rc = "BLOCKED", 2
    else:
        verdict, rc = "PASS", 0
    print(json.dumps({
        "schema": "chronforge.verification.d0-golden-receipt/v1",
        "verdict": verdict,
        "evidence_class": "Runtime-subset + Metadata only when stamped PASS",
        "issues": issues,
        "blocked": blocked,
        "allow_pending": args.allow_pending,
        "limitations": ["Receipt validation does not itself rerun hftbacktest; d0_goldens.sh is the Runtime-subset lever.", "D0.J remains a separate join gate."]
    }, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
