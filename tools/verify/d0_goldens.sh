#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PIN="058cfefd9740b6857bb875bad4d5e6547a88379a"
REPO="https://github.com/tommy-ca/hftbacktest"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

printf 'D0 external golden corpus\nrepo=%s\npin=%s\n' "$REPO" "$PIN"

git -C "$WORK" init -q
git -C "$WORK" remote add origin "$REPO"
git -C "$WORK" fetch -q --depth 1 origin "$PIN"
git -C "$WORK" checkout -q --detach FETCH_HEAD
ACTUAL="$(git -C "$WORK" rev-parse HEAD)"
if [[ "$ACTUAL" != "$PIN" ]]; then
  echo "pin mismatch: expected $PIN got $ACTUAL" >&2
  exit 10
fi

pushd "$WORK" >/dev/null

cat > /tmp/chronforge-d0-golden.sha256 <<'EOF'
7ebbbd6baa407f1fad84da5a37ff246246689723db9414c6408281acbfe18b37  py-hftbacktest/tests/test_polymarket.py
b5cc1fac9a9be40d1c39a444d9d8fd975387f6ae003c917fb457f4213b0d3e3e  py-hftbacktest/hftbacktest/data/utils/polymarket.py
c6311a0c9f432e8f922702746d7481c6da0418a7c2c96ce929b58206b62a7177  hftbacktest/src/backtest/models/fee.rs
32a57155e776c3ece89f81c20d78a203650f2e2200abab7f3b77476aead841e8  examples/polymarket/smoke_converter.py
EOF
sha256sum -c /tmp/chronforge-d0-golden.sha256
rm -f /tmp/chronforge-d0-golden.sha256

cargo check -p hftbacktest --no-default-features --features backtest
cargo test -p hftbacktest --no-default-features --features backtest --lib
cargo test -p hftbacktest --no-default-features --features backtest --lib binary_fee

popd >/dev/null

python3 - "$PIN" <<'PY'
import json, sys
print(json.dumps({
    "schema": "chronforge.verification.d0-external-goldens/v1",
    "verdict": "PASS",
    "evidence_class": "Runtime-subset + Metadata",
    "hftbacktest_revision": sys.argv[1],
    "features": "backtest (no-default)",
    "commands": [
        "cargo check -p hftbacktest --no-default-features --features backtest",
        "cargo test -p hftbacktest --no-default-features --features backtest --lib",
        "cargo test -p hftbacktest --no-default-features --features backtest --lib binary_fee"
    ],
    "limitations": [
        "Default live/iceoryx features are not exercised.",
        "Python unittest/PyO3 runtime is not exercised by this lever.",
        "PASS is not PAPER or LIVE evidence."
    ]
}, sort_keys=True))
PY
