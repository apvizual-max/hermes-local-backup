#!/usr/bin/env python3
"""
Zero-data-loss verifier: count AMINTIRE- headers in every chunk + every source
file (streaming). Reports difference. A -1 difference is usually a stray
duplicate meta-entry in the 2nd source (already present in source 1) — confirm
with find_stray.py, not a real loss.
"""
import os, re

CHUNK_DIR = r"E:\CLAUDE\SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN"
SOURCES = [
    r"E:\CLAUDE\SENTINEL_JOURNAL - Amintire - 1 - 14634775 - TO SEPARATE.md",
    r"E:\CLAUDE\SENTINEL_JOURNAL - Amintire - 14634775 - 33119251 - TO SEPARATE.md",
]
PAT = re.compile(r'^AMINTIRE-(\d+)')

def count(path):
    c = mn = 0; mx = 0
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = PAT.match(line)
            if m:
                c += 1; n = int(m.group(1))
                mn = n if mn == 0 else min(mn, n); mx = max(mx, n)
    return c, mn, mx

print("Counting chunks...")
ct, cf, cmin, cmax = 0, 0, float('inf'), 0
for fn in sorted(os.listdir(CHUNK_DIR)):
    if not fn.endswith('.md'):
        continue
    c, mn, mx = count(os.path.join(CHUNK_DIR, fn))
    ct += c; cf += 1; cmin = min(cmin, mn); cmax = max(cmax, mx)
    if cf % 200 == 0:
        print(f"  {cf} files, running total {ct:,}")

st = 0
for s in SOURCES:
    c, mn, mx = count(s)
    print(f"  Source {os.path.basename(s)}: {c:,} ({mn}-{mx})")
    st += c

print(f"\nChunk total: {ct:,}  range {cmin}-{cmax}")
print(f"Source total: {st:,}")
print(f"Difference: {ct - st:,}")
print("SUCCESS: zero loss" if ct == st else "CHECK: difference (likely stray duplicate)")
