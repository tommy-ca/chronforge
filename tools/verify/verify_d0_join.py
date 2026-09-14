#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
JOIN = ROOT / "docs/architecture/runtime-recomposition/D0-baseline-receipt.json"
PIN = ROOT / "docs/architecture/runtime-recomposition/D0-pin-receipt.json"
SEAM = ROOT / "docs/architecture/runtime-recomposition/D0-seam-receipt.json"
INVENTORY = ROOT / "docs/architecture/runtime-recomposition/D0-seam-inventory.json"
GOLDEN = ROOT / "docs/architecture/runtime-recomposition/D0-golden-receipt.json"
DISC = ROOT / "docs/architecture/runtime-recomposition/D0-discrepancy-register.json"
INTERROGATE = ROOT / "docs/architecture/runtime-recomposition/D0-join-interrogate-receipt.json"
EXPECTED_HBT = "058cfefd9740b6857bb875bad4d5e6547a88379a"
EXPECTED_BLOBS = {
    "pin": "e6c54a4b34fd0aad6e86d750dd5281ac7e96bcf4",
    "seams": "09edcda3d3c87ccb9b40465cd1d619f688c766d8",
    "inventory": "fb1bd95e8bfb914a15cee25587598da5a4d44313",
    "goldens": "1ef4cb20f5f42c6dc07370f64b775f1025823364",
}
EXPECTED_DISCREPANCIES = {"D0-DISC-001", "D0-DISC-002", "D0-DISC-003", "D0-DISC-004"}


def load(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())


def git_blob(path: pathlib.Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-validate the joined D0 phase receipt.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--candidate", action="store_true", help="allow mandatory interrogate to remain pending")
    mode.add_argument("--prestamp", action="store_true", help="require interrogate PASS but allow final CI stamp to remain pending")
    args = parser.parse_args()

    issues: list[str] = []
    for path in (JOIN, PIN, SEAM, INVENTORY, GOLDEN, DISC):
        if not path.is_file():
            issues.append(f"missing required join artifact: {path.relative_to(ROOT)}")
    if issues:
        print(json.dumps({"schema":"chronforge.verification.d0-join/v1","verdict":"ISSUES","issues":issues}, sort_keys=True))
        return 1

    joined, pin, seam, inventory, golden, disc = map(load, (JOIN, PIN, SEAM, INVENTORY, GOLDEN, DISC))

    if joined.get("schema") != "chronforge.D0BaselineReceipt/v2" or joined.get("issue") != 14:
        issues.append("joined receipt must be chronforge.D0BaselineReceipt/v2 bound to #14")
    if joined.get("phase_issue") != 2 or joined.get("implementation_issue") != 90:
        issues.append("joined receipt phase/implementation issue binding drifted")
    if joined.get("live_pass") is not False or joined.get("paper_pass") is not False:
        issues.append("D0 joined receipt must not claim PAPER/LIVE")
    if "Runtime-subset" not in str(joined.get("evidence_class", "")) or "Static/Metadata" not in str(joined.get("evidence_class", "")):
        issues.append("joined evidence class must remain composite Runtime-subset + Static/Metadata")

    children = joined.get("children", {})
    checks = [
        ("pin", PIN, children.get("pin", {}).get("git_blob_sha")),
        ("seams", SEAM, children.get("seams", {}).get("git_blob_sha")),
        ("inventory", INVENTORY, children.get("seams", {}).get("inventory_git_blob_sha")),
        ("goldens", GOLDEN, children.get("goldens", {}).get("git_blob_sha")),
    ]
    for name, path, declared in checks:
        actual = git_blob(path)
        if actual != EXPECTED_BLOBS[name]:
            issues.append(f"{name} child blob changed from accepted identity: {actual}")
        if declared != actual:
            issues.append(f"{name} declared child blob does not match checkout")

    if pin.get("schema") != "chronforge.D0PinReceipt/v1":
        issues.append("invalid D0PinReceipt schema")
    pin_hbt = pin.get("pins", {}).get("hftbacktest", {}).get("revision")
    seam_hbt = seam.get("pin_receipt", {}).get("hftbacktest_revision")
    inv_hbt = inventory.get("pin", {}).get("revision")
    golden_hbt = golden.get("hftbacktest", {}).get("revision")
    joined_hbt = joined.get("pins", {}).get("hftbacktest")
    if {pin_hbt, seam_hbt, inv_hbt, golden_hbt, joined_hbt} != {EXPECTED_HBT}:
        issues.append("hftbacktest revision is not identical across all D0 child/join artifacts")

    if pin.get("pins", {}).get("titan", {}).get("role") != "reference-evidence-only":
        issues.append("Titan role drifted from evidence-only")
    for name in ("titan", "qstack_runtime_recomposition", "qstack_chronforge_profile", "pstack"):
        if pin.get("pins", {}).get(name, {}).get("runtime_dependency") is not False and name != "qstack_chronforge_profile":
            issues.append(f"{name} must not become a runtime dependency")
    dep = joined.get("dependency_mode", {})
    if dep.get("floating_branch_or_tag") != "forbidden" or dep.get("reverse_dependency") != "forbidden":
        issues.append("joined dependency mode weakened exact/reverse-dependency policy")
    if any(dep.get(k) is not False for k in ("titan_runtime_dependency", "qstack_runtime_dependency", "pstack_runtime_dependency")):
        issues.append("joined receipt introduced a control-plane/reference runtime dependency")

    if seam.get("schema") != "chronforge.D0SeamInventoryReceipt/v1":
        issues.append("invalid seam receipt schema")
    if inventory.get("schema") != "chronforge.D0SeamInventory/v1" or len(inventory.get("seams", [])) != 20:
        issues.append("seam inventory must remain the accepted 20-seam catalog")
    adapter = seam.get("adapter_contract", {})
    if adapter.get("kernel_authorities_preserved") is not True or adapter.get("second_matching_engine") is not False or adapter.get("reverse_dependency") is not False:
        issues.append("seam adapter authority contract is invalid")
    ownership = joined.get("ownership", {})
    if ownership.get("second_matching_engine") is not False or ownership.get("one_authority_per_state") is not True:
        issues.append("joined ownership contract permits duplicate authority")

    if golden.get("schema") != "chronforge.D0GoldenReceipt/v1":
        issues.append("invalid golden receipt schema")
    gv = golden.get("verification", {})
    if gv.get("status") != "PASS" or gv.get("external_golden_step") != "SUCCESS":
        issues.append("golden child lacks accepted external Runtime-subset proof")
    if "Runtime-subset" not in str(gv.get("evidence_class", "")):
        issues.append("golden evidence class lost Runtime-subset qualification")
    limitations = "\n".join(golden.get("limitations", []) + joined.get("accepted_limitations", [])).lower()
    for phrase in ("python", "live", "paper", "d2"):
        if phrase not in limitations:
            issues.append(f"joined limitations lost required scope: {phrase}")

    if disc.get("schema") != "chronforge.D0DiscrepancyRegister/v1" or disc.get("issue") != 14:
        issues.append("invalid D0 discrepancy register")
    if disc.get("unresolved_blocking_count") != 0:
        issues.append("D0 discrepancy register has unresolved blocking contradictions")
    disc_entries = disc.get("discrepancies", [])
    if {d.get("id") for d in disc_entries} != EXPECTED_DISCREPANCIES:
        issues.append("D0 discrepancy register does not explicitly enumerate all four audited metadata discrepancies")
    for d in disc_entries:
        if d.get("severity") != "nonblocking" or d.get("resolution") != "resolved-by-later-acceptance-evidence" or d.get("rewrite_child") is not False:
            issues.append(f"invalid discrepancy disposition: {d.get('id')}")

    acceptance = joined.get("acceptance", {})
    if acceptance.get("A-UP-001", {}).get("status") != "PASS" or acceptance.get("A-UP-001", {}).get("evidence_class") != "Runtime-subset":
        issues.append("A-UP-001 must bind scoped Runtime-subset evidence")
    if acceptance.get("A-UP-002", {}).get("status") != "PASS-scoped":
        issues.append("A-UP-002 must remain scoped rather than imply Python runtime proof")
    if acceptance.get("A-UP-003", {}).get("status") != "PASS" or acceptance.get("A-UP-003", {}).get("evidence_class") != "Static/Metadata":
        issues.append("A-UP-003 must remain Static/Metadata")

    interrogate = joined.get("interrogate", {})
    verification = joined.get("verification", {})
    if args.candidate:
        if interrogate.get("status") not in {"PENDING", "PASS"}:
            issues.append("candidate join has invalid interrogate state")
        if joined.get("d1_unlock") is not False:
            issues.append("candidate join must not unlock D1")
        if verification.get("status") not in {"CANDIDATE_PENDING_INTERROGATE", "READY_FOR_FINAL_STAMP", "ACCEPTED_CI"}:
            issues.append("candidate join has invalid verification state")
    else:
        if not INTERROGATE.is_file():
            issues.append("strict/prestamp join requires D0JoinInterrogateReceipt")
        else:
            ir = load(INTERROGATE)
            if ir.get("schema") != "chronforge.D0JoinInterrogateReceipt/v1" or ir.get("issue") != 91:
                issues.append("invalid D0JoinInterrogateReceipt schema/binding")
            if ir.get("status") != "PASS" or ir.get("unresolved_blocking_findings") != 0:
                issues.append("mandatory interrogate did not pass with zero blockers")
        if interrogate.get("status") != "PASS" or interrogate.get("unresolved_blocking_findings") != 0:
            issues.append("joined receipt does not bind interrogate PASS")
        if args.prestamp:
            if verification.get("status") != "READY_FOR_FINAL_STAMP":
                issues.append("prestamp verification state must be READY_FOR_FINAL_STAMP")
            if joined.get("d1_unlock") is not False:
                issues.append("prestamp receipt must not unlock D1")
        else:
            if verification.get("status") != "ACCEPTED_CI":
                issues.append("strict joined receipt must be stamped ACCEPTED_CI")
            if not isinstance(verification.get("workflow_run"), int) or verification.get("workflow_run") <= 0:
                issues.append("strict joined receipt lacks final workflow_run")
            head = verification.get("workflow_head_sha")
            if not isinstance(head, str) or len(head) != 40:
                issues.append("strict joined receipt lacks final workflow_head_sha")
            if joined.get("d1_unlock") is not True:
                issues.append("strict accepted joined receipt must explicitly unlock D1")

    result = {
        "schema": "chronforge.verification.d0-join/v1",
        "mode": "candidate" if args.candidate else ("prestamp" if args.prestamp else "strict"),
        "verdict": "ISSUES" if issues else "PASS",
        "evidence_class": "Composite: Runtime-subset + Static/Metadata",
        "issues": issues,
        "limitations": ["This verifier composes accepted D0 evidence; only #92 strict stamped-head PASS authorizes D1 activation."],
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
