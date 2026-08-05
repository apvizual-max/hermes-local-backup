#!/usr/bin/env python3
"""
Streaming split of large SENTINEL_JOURNAL .md files into chunks of CHUNK_SIZE
AMINTIRE entries each. NEVER loads a whole file into memory.

USAGE: python split_journal.py
Edit SOURCES / TARGET / RANGES below for your run.
"""
import os, re

TARGET_DIR = r"E:\CLAUDE\SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN"
CHUNK_SIZE = 10000
AMINTIRE_PATTERN = re.compile(r'^AMINTIRE-(\d+)\s*[—-]')

# (source_path, start_amintire, end_amintire)
SOURCES = [
    (r"E:\CLAUDE\SENTINEL_JOURNAL - Amintire - 1 - 14634775 - TO SEPARATE.md", 1, 14634775),
    (r"E:\CLAUDE\SENTINEL_JOURNAL - Amintire - 14634775 - 33119251 - TO SEPARATE.md", 14634776, 33119251),
]

def write_chunk(lines, start_num, end_num):
    fn = f"SENTINEL_JOURNAL - {start_num} - {end_num}.md"
    with open(os.path.join(TARGET_DIR, fn), 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"  Written: {fn} ({len(lines)} lines, AMINTIRE {start_num}-{end_num})")

def process_file(path, start_amintire, end_amintire):
    print(f"\nProcessing {os.path.basename(path)} range {start_amintire}-{end_amintire}")
    cur, cur_start, cur_end, count, files = [], None, None, 0, 0
    last = None
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = AMINTIRE_PATTERN.match(line)
            if m:
                n = int(m.group(1))
                if n < start_amintire:
                    continue
                if n > end_amintire:
                    break
                if n != last:
                    count += 1
                    last = n
                    if cur_start is None:
                        cur_start = n
                    if count > CHUNK_SIZE:
                        write_chunk(cur, cur_start, cur_end)
                        files += 1
                        cur, cur_start, cur_end, count = [line], n, n, 1
                    else:
                        cur.append(line); cur_end = n
                else:
                    cur.append(line); cur_end = n
            else:
                if cur:
                    cur.append(line)
    if cur:
        write_chunk(cur, cur_start, cur_end); files += 1
    print(f"  Done: {files} files")

if __name__ == "__main__":
    os.makedirs(TARGET_DIR, exist_ok=True)
    for p, s, e in SOURCES:
        if not os.path.exists(p):
            print(f"MISSING: {p}"); continue
        process_file(p, s, e)
    print("\nALL SPLIT COMPLETE")
