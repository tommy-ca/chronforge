#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "docs/architecture/runtime-recomposition/D0-seam-inventory.json"
PIN_RECEIPT = ROOT / "docs/architecture/runtime-recomposition/D0-pin-receipt.json"
EXPECTED_HBT = "058cfefd9740b6857bb875bad4d5e6547a88379a"
LEGAL_DECISIONS = {"adopt", "adapt", "compose", "defer"}
REQUIRED_SLICES = {62, 63, 64, 65, 66, 67}
REQUIRED_PRESERVATION = {
    "exchange/local timestamp distinction",
    "L2 and L3 depth semantics",
    "local vs exchange processor separation",
    "order-bus latency ordering",
    "queue model behavior",
    "partial vs no-partial fill behavior",
    "fee model behavior including BinaryFeeModel",
    "incremental execution facts needed by D2 projections",
    "Polymarket overlay remains additive",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate D0 hftbacktest seam inventory.")
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT)
    parser.add_argument(
        "--structure-only",
        action="store_true",
        help="validate read-only inventory without requiring accepted #11 D0PinReceipt",
    )
    args = parser.parse_args()

    inventory = json.loads(args.path.read_text())
    issues: list[str] = []
    blocked: list[str] = []

    if inventory.get("schema") != "chronforge.D0SeamInventory/v1":
        issues.append("unexpected seam inventory schema")
    if inventory.get("issue") != 12 or inventory.get("internal_join_issue") != 69:
        issues.append("inventory must bind to #12 and internal join #69")
    if inventory.get("evidence_class") != "Static/Metadata":
        issues.append("seam inventory must remain Static/Metadata")

    pin = inventory.get("pin", {})
    if pin.get("repository") != "tommy-ca/hftbacktest" or pin.get("revision") != EXPECTED_HBT:
        issues.append("inventory hftbacktest pin drifted")
    if pin.get("required_parent_issue") != 11:
        issues.append("inventory must verify after #11")

    swarm = inventory.get("swarm", {})
    if set(swarm.get("children", [])) != REQUIRED_SLICES or swarm.get("join") != 69:
        issues.append("seam swarm/join binding is incomplete")

    attachment = inventory.get("adapter_attachment", {})
    for key in ("market_input", "command_input", "execution_output", "kernel_authorities", "chronforge_authorities", "reverse_dependency"):
        if not attachment.get(key):
            issues.append(f"adapter_attachment missing {key}")
    if attachment.get("reverse_dependency") != "forbidden":
        issues.append("reverse dependency must be forbidden")

    seams = inventory.get("seams", [])
    if not isinstance(seams, list) or len(seams) < 18:
        issues.append("expected a decomposed seam catalog with at least 18 entries")
    ids: list[str] = []
    seen_slices: set[int] = set()
    for index, seam in enumerate(seams):
        sid = seam.get("id")
        if not isinstance(sid, str) or not sid:
            issues.append(f"seam[{index}] missing id")
            continue
        ids.append(sid)
        for key in ("slice", "path", "symbols", "responsibility", "state_owner", "inputs", "outputs", "determinism", "decision", "target_phase"):
            if key not in seam or seam.get(key) in (None, "", []):
                issues.append(f"{sid}: missing/empty {key}")
        slice_id = seam.get("slice")
        if isinstance(slice_id, int):
            seen_slices.add(slice_id)
        if seam.get("decision") not in LEGAL_DECISIONS:
            issues.append(f"{sid}: illegal decision {seam.get('decision')}")

    if len(ids) != len(set(ids)):
        issues.append("duplicate seam ids")
    if seen_slices != REQUIRED_SLICES:
        issues.append(f"catalog does not cover every swarm slice: {sorted(REQUIRED_SLICES - seen_slices)}")

    preservation = set(inventory.get("required_preservation", []))
    missing_preservation = REQUIRED_PRESERVATION - preservation
    if missing_preservation:
        issues.append(f"missing preservation laws: {sorted(missing_preservation)}")

    must_not = "\n".join(inventory.get("must_not", [])).lower()
    for phrase in ("second matching engine", "optional live", "silently replace"):
        if phrase not in must_not:
            issues.append(f"must_not contract missing concept: {phrase}")

    if not args.structure_only:
        if not PIN_RECEIPT.is_file():
            blocked.append("accepted #11 D0PinReceipt is not present in this checkout")
        else:
            parent = json.loads(PIN_RECEIPT.read_text())
            parent_sha = parent.get("pins", {}).get("hftbacktest", {}).get("revision")
            if parent.get("schema") != "chronforge.D0PinReceipt/v1":
                issues.append("parent D0PinReceipt schema is invalid")
            if parent_sha != EXPECTED_HBT or parent_sha != pin.get("revision"):
                issues.append("seam inventory pin does not match D0PinReceipt")

    if issues:
        verdict = "ISSUES"
        rc = 1
    elif blocked:
        verdict = "BLOCKED"
        rc = 2
    else:
        verdict = "PASS"
        rc = 0

    result = {
        "schema": "chronforge.verification.d0-seams/v1",
        "verdict": verdict,
        "evidence_class": "Static/Metadata",
        "structure_only": args.structure_only,
        "seams": len(seams),
        "issues": issues,
        "blocked": blocked,
        "limitations": [
            "This verifies the seam inventory contract, not hftbacktest Runtime behavior.",
            "Final #12 handoff requires accepted #11 D0PinReceipt and does not accept D0.J."
        ],
    }
    print(json.dumps(result, sort_keys=True))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
