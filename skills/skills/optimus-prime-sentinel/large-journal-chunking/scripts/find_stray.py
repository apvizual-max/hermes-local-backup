#!/usr/bin/env python3
"""
Locate stray AMINTIRE entries that fall BELOW the expected start range of a
source file. Used to prove a -1 (or small) verify_split.py difference is a
duplicate meta-entry, NOT real data loss.

In this session: source file 2 (AMINTIRE 14634776-33119251) contained ONE
stray `AMINTIRE-001` header line at line 19 (a duplicate of the entry already
in source file 1). The range filter in split_journal.py correctly excluded it.

USAGE: python find_stray.py <source_file.md> <expected_min_num>
  e.g. python find_stray.py "E:\CLAUDE\SENTINEL_JOURNAL - Amintire - 14634775 - 33119251 - TO SEPARATE.md" 14634776
Prints every AMINTIRE header with number < expected_min (with line number + text).
"""
import os, re, sys

PAT = re.compile(r'^AMINTIRE-(\d+)\s')

def main():
    if len(sys.argv) < 3:
        print("USAGE: python find_stray.py <source_file.md> <expected_min_num>")
        sys.exit(1)
    path = sys.argv[1]
    expected_min = int(sys.argv[2])
    if not os.path.isfile(path):
        print(f"MISSING: {path}")
        sys.exit(1)
    found = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f, 1):
            m = PAT.match(line)
            if m and int(m.group(1)) < expected_min:
                found.append((i, int(m.group(1)), line.rstrip()[:120]))
            if i % 50_000_000 == 0:
                print(f"  scanned {i:,} lines...")
    print(f"\nFound {len(found)} AMINTIRE entries with number < {expected_min}:")
    for ln, n, txt in found[:20]:
        print(f"  line {ln}: AMINTIRE-{n} | {txt}")
    if not found:
        print("  -> No strays. Difference is NOT a duplicate; investigate real loss.")

if __name__ == "__main__":
    main()
