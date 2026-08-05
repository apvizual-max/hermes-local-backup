# Journal Chunking for RAG — Workflow & Pitfalls

## When to use
SENTINEL_JOURNAL.md (or its separated `- TO SEPARATE.md` exports) grow past
~1GB and become unreadable / unqueryable in one piece. Shard into ≤N-entry
files so each can be opened, grepped, and RAG-indexed independently.

## Workflow (proven on 2 × ~9.7GB files → 3,455 shards, 34.5M entries)
1. Keep the two big source files UNTOUCHED until verification passes.
2. Run `scripts/split_journal_to_chunks.py` per source file with its disjoint
   (--start, --end) range. Outdir is the shared RAG folder.
3. Run `scripts/verify_split_integrity.py` against the chunk dir + both sources.
4. Only after `Difference: 0` (or an explained -N) may sources be deleted.

## Pitfalls (encode these)
- **Naming off-by-one**: a shard holding entries 1..10000 must be named
  `SENTINEL_JOURNAL - 1 - 10000.md`. The END label is the LAST entry
  number (first + N - 1), NOT the next shard's start (first + N).
  The first session run mislabeled as `...-1-10001.md`; content was correct,
  only the filename was off. Verify by `head`/`tail` of the shard.
- **Stray duplicate meta-entries**: a source file may contain a duplicate
  header line (e.g. `AMINTIRE-001` appeared at line 19 of the SECOND
  14M-range file, a copy of entry #1 from the first file). The splitter
  SKIPS entries outside [start,end] via `if num<start or num>end: continue`,
  so the duplicate is intentionally excluded → produces a -1 difference that
  is NOT data loss. Always explain, never "fix" by re-including dupes.
- **search_files on >5GB single files is unreliable**: ripgrep-backed
  search_files timed out / returned 0 even for patterns that MUST exist
  (the 14,634,775 boundary entry). For very large files, use a streaming
  Python script via `terminal` instead (see find_stray pattern).
- **Model rate-limit ≠ background job death**: when you see "limit rate hit
  and stopped you", the background `proc_...` Python job is usually STILL
  RUNNING. Check `process(action='list')` before restarting. Restarting
  spawns a duplicate and wastes hours.
- **Long jobs need background + polling loops**: splitting 9GB took ~2.3h,
  verification longer. Launch with `terminal(background=true,
  notify_on_complete=true)`, then `process(action='wait')` in a loop (each
  wait is clamped to ~60s; loop many times). Don't block on a single huge wait.

## Session result (2026-07-12)
- Sources: `...-1-14634775-TO SEPARATE.md` (16,059,995 entries) +
  `...-14634775-33119251-TO SEPARATE.md` (18,484,477 entries, incl. 1 stray)
- Chunks: 3,455 files in `E:\CLAUDE\SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN\`
- Chunk total 34,544,471 vs source total 34,544,472 → diff -1 = the stray
  duplicate header, confirmed zero real data loss.
