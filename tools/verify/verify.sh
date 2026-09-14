#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROFILE="${1:-}"

emit_issue() {
  local profile="$1" lever="$2" rc="$3" evidence="$4"
  python3 - "$profile" "$lever" "$rc" "$evidence" <<'PY'
import json, sys
print(json.dumps({
    "schema": "chronforge.verification.profile-run/v1",
    "profile": sys.argv[1],
    "verdict": "ISSUES",
    "evidence_class": sys.argv[4],
    "failed_lever": sys.argv[2],
    "exit_code": int(sys.argv[3]),
}, sort_keys=True))
PY
}

run_required() {
  local profile="$1" lever="$2" evidence="$3"
  shift 3
  "$@"
  local rc=$?
  if [[ $rc -ne 0 ]]; then
    emit_issue "$profile" "$lever" "$rc" "$evidence"
    exit "$rc"
  fi
}

case "$PROFILE" in
  control-plane)
    run_required control-plane openspec-strict Static/Metadata/CI \
      npx --yes @fission-ai/openspec@1.13.0 validate --all --strict
    run_required control-plane cargo-check-workspace Static/Metadata/CI \
      cargo check --workspace
    run_required control-plane control-plane-guard Static/Metadata/CI \
      python3 "$ROOT/tools/verify/control_plane_guard.py"
    run_required control-plane issue-orchestration-matrix Static/Metadata/CI \
      python3 "$ROOT/tools/verify/validate_issue_orchestration.py"
    printf '%s\n' '{"schema":"chronforge.verification.profile-run/v1","profile":"control-plane","verdict":"PASS","evidence_class":"Static/Metadata/CI"}'
    ;;
  d0)
    run_required d0 d0-receipt-validation Metadata \
      python3 "$ROOT/tools/verify/verify_d0_receipt.py"
    printf '%s\n' '{"schema":"chronforge.verification.profile-run/v1","profile":"d0","verdict":"PASS","evidence_class":"Metadata","limitations":["Receipt validation does not rerun external hftbacktest Runtime evidence and does not accept D0.J."]}'
    ;;
  d1|d2|d3|d4|d5|d6)
    python3 - "$ROOT/tools/verify/profiles.json" "$PROFILE" <<'PY'
import json, pathlib, sys
profiles = json.loads(pathlib.Path(sys.argv[1]).read_text())["profiles"]
name = sys.argv[2]
p = profiles[name]
print(json.dumps({
    "schema": "chronforge.verification.profile-run/v1",
    "profile": name,
    "verdict": "BLOCKED",
    "evidence_class": p["evidence_class"],
    "qstack": p["qstack"],
    "expected_levers": p["levers"],
    "blocker": p.get("blocker", "profile not executable"),
}, sort_keys=True))
PY
    exit 2
    ;;
  *)
    echo "usage: bash tools/verify/verify.sh {control-plane|d0|d1|d2|d3|d4|d5|d6}" >&2
    exit 64
    ;;
esac
