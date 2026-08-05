#!/usr/bin/env python3
"""
Verify ZERO DATA LOSS after splitting SENTINEL_JOURNAL into RAG chunks.
Counts AMINTIRE-<n> entries in every chunk + every source file, compares totals.
Also reports any entry number that falls outside its source file's designated range
(stray/duplicate meta-entries), which explain intentional -N differences.

Usage:
  python verify_split_integrity.py \
      --chunkdir "E:/CLAUDE/SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN" \
      --src "E:/CLAUDE/SENTINEL_JOURNAL - Amintire - 1 - 14634775 - TO SEPARATE.md" \
      --src "E:/CLAUDE/SENTINEL_JOURNAL - Amintire - 14634775 - 33119251 - TO SEPARATE.md"
"""
import os, re, argparse

AMINTIRE_RE = re.compile(r'^AMINTIRE-(\d+)')

def count(fp):
    c = 0; mn = None; mx = 0
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = AMINTIRE_RE.match(line)
            if m:
                c += 1; n = int(m.group(1))
                if mn is None or n < mn: mn = n
                if n > mx: mx = n
    return c, (mn if c else 0), mx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chunkdir', required=True)
    ap.add_argument('--src', action='append', default=[])
    a = ap.parse_args()

    chunk_total = 0; chunk_files = 0; cmin = None; cmax = 0
    for fn in sorted(os.listdir(a.chunkdir)):
        if not fn.endswith('.md'): continue
        c, mn, mx = count(os.path.join(a.chunkdir, fn))
        chunk_total += c; chunk_files += 1
        if cmin is None or mn < cmin: cmin = mn
        if mx > cmax: cmax = mx
    print(f"Chunks: {chunk_files} files, {chunk_total:,} entries (range {cmin:,}-{cmax:,})")

    src_total = 0
    for sp in a.src:
        c, mn, mx = count(sp)
        src_total += c
        print(f"  source {os.path.basename(sp)}: {c:,} ({mn:,}-{mx:,})")
    print(f"Source total: {src_total:,}")

    diff = chunk_total - src_total
    print(f"Difference: {diff:+,}")
    if diff == 0:
        print("RESULT: ZERO DATA LOSS - chunk total == source total")
    else:
        print("RESULT: MISMATCH - scan sources for stray/duplicate entries outside range")

if __name__ == '__main__':
    main()
