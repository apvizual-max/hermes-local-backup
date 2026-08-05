#!/usr/bin/env python3
"""
recover_chunks.py — REBUILD a damaged chunk file from the READ-ONLY backup big-files by AMINTIRE index range.
NEVER writes to the backups; read-only source. Use ONLY to restore a chunk the cleaner damaged.

Usage: python recover_chunks.py <lo> <hi> <out_chunk.md>
  <lo> - lowest AMINTIRE number to include (inclusive)
  <hi> - highest AMINTIRE number to include (inclusive)
  <out_chunk.md> - output chunk file path
"""
import os
import re
import sys

BACKUP_DIR = r"E:\CLAUDE\SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN\RAG_ROOT FILES"
BACKUP_FILES = [
    os.path.join(BACKUP_DIR, "SENTINEL_JOURNAL - Amintire - 1 - 14634775 - TO SEPARATE.md"),
    os.path.join(BACKUP_DIR, "SENTINEL_JOURNAL - Amintire - 14634775 - 33119251 - TO SEPARATE.md"),
]
AMINTIRE_HDR = re.compile(r'^AMINTIRE-(\d+)\s')

def num_of(line):
    m = AMINTIRE_HDR.match(line)
    return int(m.group(1)) if m else None

def recover(lo, hi, out):
    blocks = []
    cur = []
    cur_num = None
    found = 0
    for bfp in BACKUP_FILES:
        with open(bfp, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                n = num_of(line)
                if n is not None:
                    if cur and cur_num is not None and lo <= cur_num <= hi:
                        blocks.append(''.join(cur))
                        found += 1
                    cur = [line]
                    cur_num = n
                else:
                    cur.append(line)
        # flush tail of this file
        if cur and cur_num is not None and lo <= cur_num <= hi:
            blocks.append(''.join(cur))
            found += 1
        cur = []
        cur_num = None
    with open(out, 'w', encoding='utf-8') as f:
        f.writelines(blocks)
    print(f"Recovered {found} blocks for [{lo},{hi}] -> {out}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python recover_chunks.py <lo> <hi> <out_chunk.md>")
        sys.exit(1)
    lo = int(sys.argv[1])
    hi = int(sys.argv[2])
    out = sys.argv[3]
    recover(lo, hi, out)