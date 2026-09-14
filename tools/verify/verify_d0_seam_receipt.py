#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "docs/architecture/runtime-recomposition/D0-seam-receipt.json"
INVENTORY = ROOT / "docs/architecture/runtime-recomposition/D0-seam-inventory.json"
EXPECTED_HBT = "058cfefd9740b6857bb875bad4d5e6547a88379a"
EXPECTED_INVENTORY_BLOB = "fb1bd95e8bfb914a15cee25587598da5a4d44313"


def main() -> int:
    receipt = json.loads(RECEIPT.read_text())
    inventory = json.loads(INVENTORY.read_text())
    issues: list[str] = []

    if receipt.get("schema") != "chronforge.D0SeamInventoryReceipt/v1":
        issues.append("unexpected seam receipt schema")
    if receipt.get("issue") != 12 or receipt.get("internal_join_issue") != 69:
        issues.append("seam receipt must bind to #12/#69")
    pin = receipt.get("pin_receipt", {})
    if pin.get("hftbacktest_revision") != EXPECTED_HBT:
        issues.append("seam receipt pin drifted")
    inv = receipt.get("inventory", {})
    if inv.get("git_blob_sha") != EXPECTED_INVENTORY_BLOB:
        issues.append("inventory blob identity drifted")
    if inv.get("seam_count") != len(inventory.get("seams", [])) or inv.get("seam_count") != 20:
        issues.append("seam count mismatch")
    if sorted(inv.get("swarm_children", [])) != [62, 63, 64, 65, 66, 67]:
        issues.append("swarm child set mismatch")
    adapter = receipt.get("adapter_contract", {})
    if adapter.get("kernel_authorities_preserved") is not True:
        issues.append("kernel authority preservation missing")
    if adapter.get("second_matching_engine") is not False:
        issues.append("second matching engine must remain false")
    if adapter.get("reverse_dependency") is not False:
        issues.append("reverse dependency must remain false")

    verification = receipt.get("verification", {})
    if verification.get("status") != "ACCEPTED_CI":
        issues.append("seam receipt is not stamped ACCEPTED_CI")
    run = verification.get("workflow_run")
    head = verification.get("workflow_head_sha")
    if not isinstance(run, int) or run <= 0:
        issues.append("workflow_run missing")
    if not isinstance(head, str) or len(head) != 40:
        issues.append("workflow_head_sha missing/invalid")
    if verification.get("evidence_class") != "Static/Metadata":
        issues.append("seam receipt must remain Static/Metadata")
    if receipt.get("handoff", {}).get("consumer") != 14:
        issues.append("handoff consumer must be #14")
    if receipt.get("handoff", {}).get("does_not_accept_d0_join") is not True:
        issues.append("receipt must not claim D0 join acceptance")

    result = {
        "schema": "chronforge.verification.d0-seam-receipt/v1",
        "verdict": "ISSUES" if issues else "PASS",
        "evidence_class": "Static/Metadata",
        "issues": issues,
        "limitations": [
            "This validates the stamped #12 handoff receipt; it does not execute Runtime adapter behavior or accept D0.J."
        ],
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
