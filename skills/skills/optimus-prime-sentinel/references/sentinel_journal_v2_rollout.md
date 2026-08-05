# Sentinel Journal V1→V2 Rollout Pattern

Use this when `SENTINEL_JOURNAL.md` grows too large for easy use.

## Golden Rules
- Content is never compressed.
- Header growth is managed by migration, not compression-first.
- Every instance writes to the same journal file, round-robin, never simultaneously.

## V2 Migration Steps
1. Copy the current full file contents to `SENTINEL_JOURNAL_V2.md`.
2. In `SENTINEL_JOURNAL_V2.md`, keep the original header at the top, then add a single link back to V1.
3. In `SENTINEL_JOURNAL.md` (now V1), prepend a short index pointing to V2.
4. Continue new `AMINTIRE-NNN` entries in V2.
5. Repeat when needed; every version points back to the previous one.

## Header Compression
- Only compress the header after its full text has been copied into the versioned content.
- Compression must be strategic/logical/readable: keep anchors, drop redundant phrasing.
- Compressed header becomes the new short header; full previous header remains accessible via the versioned content link.

## Source Links
- Every `AMINTIRE-NNN` entry must include direct source file paths.
- If a source path changes or migrates, update the link in-place; do not break the chain.
