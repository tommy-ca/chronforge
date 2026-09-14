#!/usr/bin/env bash
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
missing=()
for cmd in python3 cargo rustc node npx; do
  command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
done

for path in \
  "$ROOT/tools/verify/profiles.json" \
  "$ROOT/.cursor/skills/verify-chronforge/SKILL.md" \
  "$ROOT/openspec/config.yaml" \
  "$ROOT/Cargo.toml"; do
  [[ -f "$path" ]] || missing+=("${path#$ROOT/}")
done

if ((${#missing[@]})); then
  python3 - "${missing[@]}" <<'PY'
import json, sys
print(json.dumps({
    "schema": "chronforge.verification.doctor/v1",
    "verdict": "BLOCKED",
    "evidence_class": "Static",
    "missing": sys.argv[1:],
}, sort_keys=True))
PY
  exit 2
fi

python3 - "$ROOT/tools/verify/profiles.json" <<'PY'
import json, pathlib, sys
path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text())
assert data["schema_version"] == 1
assert "control-plane" in data["profiles"]
print(json.dumps({
    "schema": "chronforge.verification.doctor/v1",
    "verdict": "PASS",
    "evidence_class": "Static",
    "profiles": sorted(data["profiles"]),
}, sort_keys=True))
PY
