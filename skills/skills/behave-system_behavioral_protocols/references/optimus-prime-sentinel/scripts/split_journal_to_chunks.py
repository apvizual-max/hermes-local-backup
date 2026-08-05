#!/usr/bin/env python3
"""
Split a large SENTINEL_JOURNAL markdown file into shards of N AMINTIRE entries
for RAG-friendly querying. Streams line-by-line so 9GB+ files never load into RAM.

Usage (two disjoint source files, typical):
  python split_journal_to_chunks.py \
      --src "E:/CLAUDE/SENTINEL_JOURNAL - Amintire - 1 - 14634775 - TO SEPARATE.md" \
      --outdir "E:/CLAUDE/SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN" \
      --start 1 --end 14634775 --chunk 10000

  python split_journal_to_chunks.py \
      --src "E:/CLAUDE/SENTINEL_JOURNAL - Amintire - 14634775 - 33119251 - TO SEPARATE.md" \
      --outdir "E:/CLAUDE/SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN" \
      --start 14634776 --end 33119251 --chunk 10000

Output file naming:  SENTINEL_JOURNAL - <first>-<last>.md
  where <last> = <first> + CHUNK_SIZE - 1   (NOT first + CHUNK_SIZE)
  e.g. entries 1..10000  ->  SENTINEL_JOURNAL - 1 - 10000.md
"""
import os, re, argparse

AMINTIRE_RE = re.compile(r'^AMINTIRE-(\d+)')

def write_chunk(lines, first, last, outdir):
    fn = f"SENTINEL_JOURNAL - {first} - {last}.md"
    with open(os.path.join(outdir, fn), 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return fn

def split(src, outdir, start, end, chunk_size, progress_every=200):
    os.makedirs(outdir, exist_ok=True)
    chunk = []
    chunk_first = None
    chunk_count = 0
    files_written = 0
    total_written = 0
    with open(src, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = AMINTIRE_RE.match(line)
            if m:
                num = int(m.group(1))
                if num < start or num > end:
                    continue  # outside this file's range; skip (drops stray dupes too)
                if chunk_first is None:
                    chunk_first = num
                chunk.append(line)
                chunk_count += 1
                if chunk_count >= chunk_size:
                    last = chunk_first + chunk_count - 1
                    write_chunk(chunk, chunk_first, last, outdir)
                    files_written += 1
                    total_written += chunk_count
                    if files_written % progress_every == 0:
                        print(f"  wrote {files_written} files, {total_written:,} entries", flush=True)
                    chunk = []
                    chunk_first = None
                    chunk_count = 0
            else:
                if chunk:
                    chunk.append(line)
    if chunk:
        last = chunk_first + chunk_count - 1
        write_chunk(chunk, chunk_first, last, outdir)
        files_written += 1
        total_written += chunk_count
    print(f"DONE {os.path.basename(src)}: {files_written} files, {total_written:,} AMINTIRE written", flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='source journal file')
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--start', type=int, required=True)
    ap.add_argument('--end', type=int, required=True)
    ap.add_argument('--chunk', type=int, default=10000)
    a = ap.parse_args()
    split(a.src, a.outdir, a.start, a.end, a.chunk)

if __name__ == '__main__':
    main()
