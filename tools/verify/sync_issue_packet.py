#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import re
import sys

from render_issue_packet import END, START, load_entries, render

PACKET_RE = re.compile(
    r"\n?<!-- chronforge-execution-packet:v2 issue=\d+ -->.*?<!-- /chronforge-execution-packet -->\n?",
    re.DOTALL,
)


def sync(body: str, packet: str) -> str:
    base = PACKET_RE.sub("\n", body).rstrip()
    return f"{base}\n\n{packet}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize a GitHub issue body with its canonical ChronForge execution packet.")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--body-file", type=pathlib.Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        entries = load_entries()
        issue = min(entries)
        entry, rel = entries[issue]
        packet = render(entry, rel)
        first = sync("# Example\n\nBody.\n", packet)
        second = sync(first, packet)
        ok = first == second and first.count(START) == 1 and first.count(END) == 1
        print("PASS" if ok else "ISSUES")
        return 0 if ok else 1

    if args.issue is None or args.body_file is None:
        parser.error("--issue and --body-file are required unless --self-test is used")

    entries = load_entries()
    if args.issue not in entries:
        print(f"unknown issue #{args.issue}", file=sys.stderr)
        return 2
    entry, rel = entries[args.issue]
    packet = render(entry, rel)
    original = args.body_file.read_text()
    expected = sync(original, packet)

    if args.check:
        if original != expected:
            print("ISSUES")
            return 1
        print("PASS")
        return 0

    sys.stdout.write(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
