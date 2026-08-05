# Corruption Signature & Verification (worked example)

## Calibration findings (this session)
- Files decode as **valid UTF-8 with ZERO U+FFFD** replacement chars. "Encrypted"
  content is NOT mojibake — it is **raw binary bytes from executable files**
  (e.g. `node.exe`) read as text, surviving as control chars `\x00`–`\x1f`.
- Corruption is concentrated in certain vaults (e.g. `CLI_PRIME_OPPERATIONS - CPO`)
  where indexed files were binaries. ~15% of blocks in worst files were garbage.
- Readable metadata (AMINTIRE header, TAG-URI, SOURCES path) is ALWAYS clean.
  Only the `(CLI):` payload segment is binary garbage.

## Block shape (corrupt example)
```
AMINTIRE-23354778 — 2026-07-11 — Line 643243 from ...node.exe (CLI): \x01\x0cD\x00...
TAG-URI: #[LN643243] #[VAULT:CLI_PRIME_OPPERATIONS - CPO] #[ROLE:CLI]
SOURCES:
- `C:\...\node.exe`
---
```

## is_garbage test (tuned here)
`control_char_ratio >= 0.30 AND no readable run of >= 8 word-chars`.
- Below 0.30 → keep (some stray control chars are tolerable; strip them to spaces).
- This caught 859/10000 garbage blocks in the worst file; those became
  `[CORRUPTED_BINARY_CONTENT_REMOVED]`.

## Verification numbers (proves zero loss)
- Chunks: 3,455 files, **34,544,471** AMINTIRE, range 1 → 33,119,251 (full coverage).
- Source 1: 16,059,995 (1–14,634,775)
- Source 2: 18,484,477 (reported min=1 → stray)
- Source total: **34,544,472** → difference = **-1**
- Stray scan (`find_stray.py` logic): exactly ONE `AMINTIRE-001` header line at
  line 19 of source file 2 — a duplicate meta-entry already in file 1. Range
  filter correctly excluded it. → **zero unique data loss**, only 1 redundant
  header intentionally deduplicated.

## Result after clean
- 34,544,471 blocks kept (removed=0), 1,549,913 cleaned (binary payload → marker).
- File count unchanged (3,455). Empty-if-all-corrupt rule not triggered.
