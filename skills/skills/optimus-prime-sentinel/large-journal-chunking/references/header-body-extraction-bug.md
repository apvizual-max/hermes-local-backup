# Header Body Extraction Bug — CRITICAL POST-MORTEM

## The Bug
The `extract_body_from_header()` function was extracting the body from AMINTIRE header lines **incorrectly**, causing 100% false positive garbage detection.

### What It Did (WRONG)
```python
def extract_body_from_header(header_line):
    idx = header_line.rfind('): ')
    if idx != -1:
        return header_line[idx + 3:]  # Returns EVERYTHING after '): '
    return ''
```

This returned **everything after `): `** including:
- TAG-URI: `#[LN9150] #[VAULT:...] #[ROLE:ORCHESTRATOR]`
- SOURCES: lines
- `---` delimiter
- File paths with `C:\Users\...`
- Code snippets from the source file

### What It Should Do (CORRECT)
Extract **only the body text on the header line itself**, stopping at the newline:
```python
def extract_body_from_header(header_line):
    """
    Extract only the body content from an AMINTIRE header line.
    Body = text after '): ' up to end of line.
    Does NOT include TAG-URI, SOURCES, or '---' lines.
    """
    idx = header_line.rfind('): ')
    if idx != -1:
        body = header_line[idx + 3:]  # Get text after '): '
        # Stop at newline - body is ONLY on the header line
        body = body.split('\n')[0]
        return body
    return ''
```

## Impact
- **Before fix:** 100% of entries with TAG-URI/SOURCES/paths were flagged as "garbage" and removed
- **After fix:** Only the actual header body text is evaluated; TAG-URI/SOURCES/paths are metadata, not body content
- **Result:** Natural language entries with paths in SOURCES are now KEPT (e.g., maintenance logs, heartbeat entries)

## Example

### Header Line (actual format):
```
AMINTIRE-20001 — 2026-07-10 — Line 9150 from - ORCHESTRATOR - Sys Folder - Hermes Default\.obsidian\plugins\hermes-tts\main.js (ORCHESTRATOR):   new_byte: Xa,
TAG-URI: #[LN9150] #[VAULT:- ORCHESTRATOR - Sys Folder - Hermes Default] #[ROLE:ORCHESTRATOR]
SOURCES:
- `C:\Users\apviz\AppData\Local\hermes\OGLINDA - CASA\00_KV_SECOND BRAIN\- ORCHESTRATOR - Sys Folder - Hermes Default\.obsidian\plugins\hermes-tts\main.js`
---
```

### Buggy Extraction (INCORRECT - returns everything after `): `):
```
new_byte: Xa,
TAG-URI: #[LN9150] #[VAULT:- ORCHESTRATOR - Sys Folder - Hermes Default] #[ROLE:ORCHESTRATOR]
SOURCES:
- `C:\Users\apviz\AppData\Local\hermes\OGLINDA - CASA\00_KV_SECOND BRAIN\- ORCHESTRATOR - Sys Folder - Hermes Default\.obsidian\plugins\hermes-tts\main.js`
---
```

### Correct Extraction (body ONLY on header line):
```
new_byte: Xa,
```

## Resolution
The `extract_body_from_header()` function in `recover_smart.py` and `clean_journal.py` MUST be fixed to:
1. Find `): ` in header line
2. Take substring after it
3. **Split on `\n` and take only first part** (the header line body)
4. Ignore everything after the first newline (TAG-URI, SOURCES, `---`)

This was the **root cause** of the 99.999% data loss in the ultra-final pass.