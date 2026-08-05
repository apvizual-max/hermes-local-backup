#!/usr/bin/env python3
"""
TRUNCATION GUARDIAN
Verifies that critical memory files (CONSTINTA.md) and ALL skill files are
NOT truncated relative to a recorded baseline (truncation_baseline.json).

Truncation = file currently SMALLER (bytes or lines) than baseline snapshot.
This is a FATAL SYSTEM ERROR per SOUL.md rule #4 (no-truncation-constinta-skills).

Usage: python truncation_guardian.py [--mode cron]
Exit codes: 0 = PASS (no truncation), 1 = FAIL (truncation/missing), 2 = baseline missing
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(HERE, "truncation_baseline.json")
MODE = sys.argv[1] if len(sys.argv) > 1 else "--mode cron"


def main():
    if not os.path.exists(BASELINE):
        print("BASELINE MISSING:", BASELINE)
        return 2

    with open(BASELINE, "r", encoding="utf-8") as f:
        base = json.load(f)

    total = len(base)
    ok = 0
    truncated = []
    missing = []

    for path, info in base.items():
        if not os.path.exists(path):
            missing.append(path)
            continue
        sz = os.path.getsize(path)
        with open(path, "rb") as fh:
            data = fh.read()
        lines = data.count(b"\n") + (1 if sz > 0 else 0)
        bsz = info.get("size", 0)
        bln = info.get("lines", 0)
        if sz < bsz or lines < bln:
            truncated.append((path, bsz, sz, bln, ln_ := lines))
        else:
            ok += 1

    print("=" * 64)
    print("TRUNCATION GUARDIAN VERIFICATION")
    print("MODE:", MODE)
    print("BASELINE FILES:", total)
    print("OK (not truncated):", ok)
    print("TRUNCATED:", len(truncated))
    print("MISSING:", len(missing))
    print("=" * 64)

    if truncated:
        print("TRUNCATED FILES:")
        for p, bsz, sz, bln, ln in truncated:
            print(f"  - {p}")
            print(f"      baseline size={bsz} lines={bln} | current size={sz} lines={ln}")

    if missing:
        print("MISSING FILES:")
        for p in missing:
            print(f"  - {p}")

    print("=" * 64)
    if truncated or missing:
        print("RESULT: FAIL - truncation/damage detected")
        return 1
    print("RESULT: PASS - no truncation detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
