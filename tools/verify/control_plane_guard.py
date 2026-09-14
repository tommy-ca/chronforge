#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[2]
BANNED = ("qstack", "qorch", "pstack", "openspec")


def contains_banned(value: object) -> list[str]:
    text = json.dumps(value, sort_keys=True).lower()
    return [name for name in BANNED if name in text]


def main() -> int:
    problems: list[dict[str, object]] = []
    manifests = sorted((ROOT / "crates").glob("*/Cargo.toml"))
    for manifest in manifests:
        data = tomllib.loads(manifest.read_text())
        for section in ("dependencies", "dev-dependencies", "build-dependencies"):
            deps = data.get(section, {})
            for name, value in deps.items():
                hits = contains_banned({name: value})
                if hits:
                    problems.append({
                        "manifest": str(manifest.relative_to(ROOT)),
                        "section": section,
                        "dependency": name,
                        "forbidden": hits,
                    })
    result = {
        "schema": "chronforge.verification.control-plane-guard/v1",
        "verdict": "ISSUES" if problems else "PASS",
        "evidence_class": "Static",
        "manifests_checked": [str(p.relative_to(ROOT)) for p in manifests],
        "issues": problems,
    }
    print(json.dumps(result, sort_keys=True))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
