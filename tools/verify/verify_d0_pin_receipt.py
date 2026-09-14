#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "docs/architecture/runtime-recomposition/D0-pin-receipt.json"
EXPECTED = {
    "hftbacktest": "058cfefd9740b6857bb875bad4d5e6547a88379a",
    "titan": "3c56818f6e412f21bc8b305ff3dc0f6dc1aa7024",
    "qstack_runtime_recomposition": "6d124b93b6008851c1fc48aaef5ef6a20d6535b6",
    "qstack_chronforge_profile": "cf4e62f4ef98fe378393fa3adff8449ff9457024",
    "pstack": "be432a96ed36e48d05f44bf375864355f62263f9",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the D0 provenance/dependency pin receipt.")
    parser.add_argument("path", nargs="?", type=pathlib.Path, default=DEFAULT)
    args = parser.parse_args()
    receipt = json.loads(args.path.read_text())
    issues: list[str] = []

    if receipt.get("schema") != "chronforge.D0PinReceipt/v1": issues.append("unexpected receipt schema")
    if receipt.get("issue") != 11 or receipt.get("internal_join_issue") != 68: issues.append("receipt must bind to #11 and internal join #68")
    if receipt.get("evidence_class") != "Metadata/Static": issues.append("D0PinReceipt must remain Metadata/Static")

    pins = receipt.get("pins", {})
    for name, expected_sha in EXPECTED.items():
        pin = pins.get(name, {})
        if pin.get("revision") != expected_sha: issues.append(f"{name} pin drifted")
        revision = str(pin.get("revision", ""))
        if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision.lower()): issues.append(f"{name} revision is not a full commit SHA")

    hbt = pins.get("hftbacktest", {})
    if hbt.get("upstream") != "nkaz001/hftbacktest": issues.append("hftbacktest upstream relationship missing/drifted")
    if hbt.get("license") != "MIT" or hbt.get("copied_into_chronforge") is not False: issues.append("hftbacktest license/copy provenance is invalid")

    titan = pins.get("titan", {})
    if titan.get("role") != "reference-evidence-only" or titan.get("runtime_dependency") is not False or titan.get("imported") is not False: issues.append("Titan must remain evidence-only and unimported")
    for name in ("qstack_runtime_recomposition", "qstack_chronforge_profile", "pstack"):
        if pins.get(name, {}).get("runtime_dependency") is not False: issues.append(f"{name} must not be a runtime dependency")

    mode = receipt.get("dependency_mode", {})
    if mode.get("d0_d1") != "detached-checkout-at-exact-revision": issues.append("D0/D1 dependency mode must use exact detached checkout")
    if mode.get("d2_selected_mode") != "cargo-git-exact-rev": issues.append("D2 selected dependency mode must be exact-rev Cargo git")
    if mode.get("d2_revision") != EXPECTED["hftbacktest"]: issues.append("D2 selected revision must equal the D0 hftbacktest pin")
    if mode.get("floating_branch_or_tag") != "forbidden": issues.append("floating dependency refs must be forbidden")
    if mode.get("d0_hard_dependency_present") is not False: issues.append("D0 must not claim a hard hftbacktest dependency")
    if mode.get("dependency_direction") != "chronforge -> hftbacktest only" or mode.get("reverse_dependency") != "forbidden": issues.append("dependency direction contract is invalid")

    drift = receipt.get("drift_policy", {})
    if drift.get("pin_change_invalidates_receipt") is not True or drift.get("requires_explicit_drift_review") is not True: issues.append("pin drift must invalidate the receipt and require review")
    if drift.get("silent_substitution") != "forbidden": issues.append("silent pin substitution must be forbidden")
    swarm = receipt.get("swarm", {})
    if swarm.get("children") != [58, 59, 60, 61] or swarm.get("join") != 68: issues.append("provenance swarm/join binding drifted")

    manifest = tomllib.loads((ROOT / "crates/hbt-engine/Cargo.toml").read_text())
    dependencies = manifest.get("dependencies", {})
    if "hftbacktest" in dependencies: issues.append("hbt-engine is hard-wired to hftbacktest before D2")
    for forbidden in ("qstack", "pstack", "qorch"):
        if forbidden in dependencies: issues.append(f"hbt-engine has forbidden control-plane runtime dependency: {forbidden}")

    verification = receipt.get("verification", {})
    if "python3 tools/verify/verify_d0_pin_receipt.py" not in verification.get("commands", []): issues.append("receipt does not name its smallest falsifying verifier")
    if verification.get("runtime_or_live_claim") is not False: issues.append("D0PinReceipt must not claim Runtime/PAPER/LIVE evidence")

    result = {"schema":"chronforge.verification.d0-pin-receipt/v1","verdict":"ISSUES" if issues else "PASS","evidence_class":"Metadata/Static","receipt":str(args.path.relative_to(ROOT)) if args.path.is_relative_to(ROOT) else str(args.path),"issues":issues,"limitations":["This validates pinned provenance, dependency direction and evidence honesty.","It does not rerun the external hftbacktest kernel or accept D0.J."]}
    print(json.dumps(result, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
