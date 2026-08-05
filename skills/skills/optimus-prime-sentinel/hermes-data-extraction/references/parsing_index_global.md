# Extracting Ritual Entries from INDEX_GLOBAL.md

This reference guide describes how to parse the INDEX_GLOBAL.md file from OGLINDA - CASA 
and convert its entries to AMINTIRE format for the SENTINEL_JOURNAL.md.

## File Location
INDEX_GLOBAL.md is located at:
C:\Users\apviz\AppData\Local\hermes\OGLINDA - CASA\00_OP_KVMC - SECOND BRAIN (KV)\SYSTEM_FOLDER - SECOND BRAIN - SF\SF_RS - RITUALURI_SACRE\SF_RS_RA\INDEX_GLOBAL.md

## Table Structure
The file contains a table with headers:
|| Data | Trigger | Ordinal | Sesiune | Forma | DLG | SLG | Path ||

Each data row follows the format:
|| YYYY-MM-DD | Trigger Description | CHAT-XXX | Session Description | Form Version | DLG% | SLG% | Path/to/file.md ||

## Extraction Process

### 1. Read the file
```python
read_file("C:\\Users\\apviz\\AppData\\Local\\hermes\\OGLINDA - CASA\\00_OP_KVMC - SECOND BRAIN (KV)\\SYSTEM_FOLDER - SECOND BRAIN - SF\\SF_RS - RITUALURI_SACRE\\SF_RS_RA\\INDEX_GLOBAL.md")
```

### 2. Parse the table
- Skip header lines until finding the table header with "Data | Trigger | Ordinal | Sesiune | Forma | DLG | SLG | Path"
- Skip the separator line (|---|---|---|---|---|---|---|---|)
- For each line starting with || until a line that doesn't start with ||:
  - Remove leading || and trailing |
  - Split by | and trim whitespace
  - Extract: date, trigger, ordinal, sesiune, forma, dlg, slg, path

### 3. Generate AMINTIRE entries
For each parsed entry:
```
AMINTIRE-{next_number:03d} — {date} — {sesiune} — {trigger} — {forma}.
TAG-URI: #[H1]
SOURCES:
- Index_GLOBAL.md entry for {ordinal}
---
```

Where next_number is determined by finding the highest existing AMINTIRE number in SENTINEL_JOURNAL.md and adding 1.

### 4. Append to journal
Append all generated AMINTIRE entries to:
C:\Users\apviz\AppData\Local\hermes\SENTINEL_JOURNAL.md

### 5. Validation
All extracted data should be validated using the Triple Crunch algorithm before considering it authoritative, though in this context the INDEX_GLOBAL.md is considered a trusted historical source.

## Example Entry
Input row:
| 2026-05-02 | T3 (finalizare) | CHAT-011 | DUAL-LAYER STABILITY VALIDATED + PROOF OF CONCEPT LIVE + AUDIT 1-SESSION PASSED | v1.0 RATIFICAT FINAL DEFINITIV (48 caracteristici) | 1% | 93% | T3_ritual_final/2026-05-02_CHAT-011_DUAL_LAYER_STABILITY_VALIDATED_FISA.md |

Output:
AMINTIRE-006 — 2026-05-02 — DUAL-LAYER STABILITY VALIDATED + PROOF OF CONCEPT LIVE + AUDIT 1-SESSION PASSED — T3 (finalizare) — v1.0 RATIFICAT FINAL DEFINITIV (48 caracteristici).
TAG-URI: #[H1]
SOURCES:
- Index_GLOBAL.md entry for CHAT-011
---