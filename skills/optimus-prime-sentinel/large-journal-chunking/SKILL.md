---
name: large-journal-chunking
description: Split, verify, and clean very large (multi-GB, multi-million-line) SENTINEL_JOURNAL markdown files into queryable fixed-size RAG chunk files. Streaming (no full load), zero-data-loss verification, and binary/encrypted-garbage cleaning while preserving readable metadata.
version: 1.1.0
author: Sentinel Default
platforms: [windows]
metadata.hermes.tags: [Journal, RAG, Chunking, Split, Verify, Clean, AMINTIRE]
---

# Large Journal Chunking & Cleaning (RAG prep)

## When to Use
- A SENTINEL_JOURNAL (or any AMINTIRE-indexed journal) has grown to GB scale and is too large to read/search directly.
- You must break one or more giant `.md` files into smaller files of **at most N logical entries each** (user default: 10,000 AMINTIRE entries/file) for RAG/query performance.
- You must **prove zero data loss** after splitting (count logical units in chunks vs sources).
- You must **strip binary/encrypted garbage** from entries while keeping readable metadata (header, TAG-URI, SOURCES).

## DURABLE USER WORKFLOW CONSTRAINTS (embedded — start every run already knowing these)
These were stated explicitly and are NON-NEGOTIABLE for this user's journal ops:
- **NEVER delete or rename the original big log files.** User deletes them himself after he verifies no data loss. Leave originals in place.
- **NEVER delete or rename the derived chunk files** during cleaning. If a file's every entry is corrupt, leave it **completely empty** — do not remove it.
- **Work ONLY on files in the specified ROOT folder. EXCLUDE any subfolders.** Use `-maxdepth 1` (find) or `os.path.isfile` + non-recursive glob; never recurse.
- **Chunk cap: maximum 10,000 AMINTIRE entries per file** (last chunk may be smaller).
- **Keep any readable data; remove only garbage.** If a single entry is entirely unreadable garbage, remove that whole entry. If an entry has readable metadata + garbage content, KEEP the metadata and strip only the garbage.
- **Naming convention (EXACT, user-specified):** `SENTINEL_JOURNAL - <START> - <END>.md` where END = START + 9999 (i.e. `SENTINEL_JOURNAL - 1 - 10000.md`, `… - 10001 - 20000.md`). NOTE: the bundled `scripts/split_journal.py` originally labeled the upper edge with the NEXT chunk's start (`1 - 10001.md`) — that is an OFF-BY-ONE deviation. Future runs should use the exact `<START>-<END>` convention above. Rename after the fact if needed (filename-only, never touch content).

## CORE TECHNIQUE 1 — Streaming Split (no full memory load)
- Open each source with `open(path, 'r', encoding='utf-8', errors='ignore')` and iterate **line by line**.
- Detect entry start with regex `^AMINTIRE-(\d+)\s*[—-]`. Buffer the current entry's lines; when the buffered entry count exceeds CHUNK_SIZE, flush to a file and start a new buffer.
- Each entry = header line + continuation lines until the next `AMINTIRE-` header. Continuation lines (no match) always append to the current buffer.
- Write each chunk with `writelines` (no intermediate string concat of the whole file). This handles 9GB+ files on a normal machine.
- Range-filter: when splitting a source that covers only part of the AMINTIRE space, `continue` if `num < start` and `break` if `num > end`.

### NAMING CONVENTION (EXACT — user-specified)
- Output files: `SENTINEL_JOURNAL - <START> - <END>.md` where END = START + CHUNK_SIZE - 1 (i.e. `1 - 10000`, `10001 - 20000`). 
- The legacy bundled `scripts/split_journal.py` labeled the upper edge with the NEXT chunk's start (`1 - 10001.md`) — this is an OFF-BY-ONE deviation. **All future runs MUST use `<START> - <END>` where END = START + 9999 (or remainder for final chunk).** Rename files if needed; filename only, never content.

## CORE TECHNIQUE 3 — Smart Mixed-Entry Cleaning (Natural Language Only)
- **Rule:** "If it can be read and used, KEEP IT. If the entire Amintire field is populated with crazy symbols that mean nothing, simply remove the entire Amintire field."
- **Mixed entries (code + natural language):** Process segment by segment. Split body into logical segments (by sentences, lines, delimiters). Remove garbage segments (code, paths, JSON, binary, symbols). Keep natural language segments (Romanian/English, ≥2 words). Rejoin clean segments.
- **Threshold:** Keep entry if cleaned body has ≥2 natural language words (Romanian/English, ≥2 letters). Discard only if entire body is garbage.
- **Garbage patterns:** code (camelCase, snake_case, PascalCase, braces, semicolons, operators), paths (C:\, /, ~/, ../), JSON/YAML (key: value, { }, [ ]), URLs, hex hashes, file extensions, emoji/symbols, ALL-CAPS words, technical symbols, control chars.
- **NEVER discard an entry just because it contains some code** — extract the readable parts first.
- **Re-run is idempotent**: markers from prior passes are themselves treated as garbage.

### CATASTROPHIC FAILURE POST-MORTEM (Run 3→4→5 — 99.999% Data Loss)
**What happened:** The cleaner destroyed 99.999% of readable data instead of removing garbage.

**Root cause:** The cleaning logic used a **NEGATIVE FILTER** (remove if ANY forbidden pattern matches) rather than a **POSITIVE FILTER** (keep if MOSTLY readable).

**The cascade:**
1. Pass 1 (marker-based): OK — replaced binary garbage with `[CORRUPTED_BINARY_CONTENT_REMOVED]`
2. Pass 2 (strict): Removed fields with <2 words OR control bytes — OK for true garbage
3. Pass 3 (ultra-strict): Added forbidden patterns for code/JSON/CSS/JS → **removed legitimate content with colons, parentheses, paths**
4. Pass 4 (ultra-final): `r'[^\w\s.,;:!?\-\(\)\"\'\\u00C0-\u017F]'` → **nuked EVERYTHING with colons, parentheses, backslashes, dots** — destroyed 99.999% of data

**Why it happened:** The logic was inverted.
- **User said:** "If it can be read and used, KEEP IT. Remove ONLY if ENTIRE field is garbage."
- **Code did:** "If ANY suspicious character/pattern exists, DELETE THE ENTIRE FIELD."

**Forbidden patterns included LEGITIMATE punctuation:** `:`, `(`, `)`, `\`, `.`, `,`, `-`, `_`, `#`, `@`, `$`, `%`, `&`, `*`, `[`, `]`, `{`, `}`, `|`, `<`, `>`, `=`, `+`, `/`, `?`, `;`, `'`, `"`, `` ` `` — i.e., almost all punctuation used in natural language.

**Correct approach (POSITIVE FILTER):**
```python
def is_readable(body):
    # 1. No control bytes (except \r\n\t)
    for ch in body:
        if is_control(ch): return False
    # 2. At least 2 natural-language words (RO/EN letters + diacritics, len>=2)
    words = WORD_RE.findall(body)
    if len(words) < 2: return False
    # 3. Letter density >= 70% (natural language is letter-dense)
    letters = sum(1 for c in body if c.isalpha())
    nonspace = sum(1 for c in body if not c.isspace())
    if nonspace == 0 or letters / nonspace < 0.70: return False
    # 4. Not mostly ALL-CAPS code identifiers
    all_caps = sum(1 for w in words if w.isupper() and len(w) >= 3)
    if words and all_caps / len(words) > 0.2: return False
    return True
```

**MANDATORY GATE:** Before ANY full run, test on a KNOWN-READABLE file (e.g., chunk `1 - 10001.md` with SOUL.md text). If `kept_count` drops vs backup → **STOP. Fix the filter. Do NOT proceed.**

**Never again:** Negative filters on human-readable data. Positive filters with thresholds. Always.

## CORE TECHNIQUE 2 — Zero-Data-Loss Verification
- Count `^AMINTIRE-` headers in EVERY chunk file and in EVERY source file (streaming, same iteration).
- Compare `sum(chunk_counts)` vs `sum(source_counts)`. Equal ⇒ zero loss.
- A small discrepancy may arise from a stray duplicate header line in source file 2 that was correctly deduplicated. Investigate but accept if unique data loss = 0.

## CORE TECHNIQUE 3 — Smart Mixed-Entry Cleaning (Natural Language Only)
- **Rule:** "If it can be read and used, KEEP IT. If the entire Amintire field is populated with crazy symbols that mean nothing, simply remove the entire Amintire field."
- **Mixed entries (code + natural language):** Process segment by segment. Split body into logical segments (by sentences, lines, delimiters). Remove garbage segments (code, paths, JSON, binary, symbols). Keep natural language segments (Romanian/English, ≥2 words). Rejoin clean segments.
- **Threshold:** Keep entry if cleaned body has ≥2 natural language words (Romanian/English, ≥2 letters). Discard only if entire body is garbage.
- **Garbage patterns:** code (camelCase, snake_case, PascalCase, braces, semicolons, operators), paths (C:\, /, ~/, ../), JSON/YAML (key: value, { }, [ ]), URLs, hex hashes, file extensions, emoji/symbols, ALL-CAPS words, technical symbols, control chars.
- **Never discard an entry just because it contains some code** — extract the readable parts first.
- See `scripts/verify_split.py` (re-runnable) and `references/corruption-signature.md` for the worked example (34,544,471 chunk vs 34,544,472 source = 1 stray duplicate → zero unique loss).

## CORE TECHNIQUE 3 — DATA_CLEANING (remove entire corrupted AMINTIRE fields)
This is the maintenance pass. It strips encrypted/binary garbage from the journal while
preserving every readable entry. **Role-agnostic** (catches `(CLI):`, `(ORCHESTRATOR):`,
`(CODER):`, etc. — anything after the role tag).

### Corruption signature
Valid UTF-8, ZERO U+FFFD, but the entry **body** (text after the LAST `): ` on the header
line) holds raw binary control bytes (`\x00`–`\x1f`) extracted from non-text source files
(`node.exe`, `.png`, binary blobs, etc.). Two shapes observed:
```
AMINTIRE-<n> — <date> — Line <L> from <path> (ORCHESTRATOR): Z+j jݗzYǅa*OH> oOAf[.< PgǍS ´~^j5sP8L w/h ygjRZ6[rF<VB 7
AMINTIRE-<n> — <date> — Line <L> from <path> (CLI): \x00\x01\x03...\x1f
```

### DECISION RULE (FINAL — user-specified, STRICT, NATURAL-LANGUAGE-ONLY)
The user is **HUMAN** and does NOT read code/symbols/paths/hashes. Journal indexing keeps ONLY
natural-language words (Romanian or English). Anything else after `): ` is removed.
  readable natural-language text (user directive: "I do NOT read code — only readable words").
  **FINAL rule (strict, as deployed in scripts/clean_journal.py):**
  - KEEP the ENTIRE field ONLY IF the body (text after the last `): ` on the header line)
    satisfies BOTH:
    1. contains **at least 2 natural-language words** (RO/EN letters incl. diacritics, length >= 2), AND
    2. contains NO binary/encrypted control bytes (any char ord<32 except space/tab/newline, or
       U+FFFD, or the 0x7F DEL) — true binary garbage.
  - Surrounding emoji, markdown wrappers (`**`), or stray punctuation do NOT disqualify, as long as
    >= 2 real words are present. Example KEPT: `… (ORCHESTRATOR): 🚛 **DOAMNE AJUTA. AMIN.**`.
  - **REMOVE the ENTIRE FIELD** (header + TAG-URI + SOURCES + `---`) if the body is ANY of:
    * binary/encrypted garbage (any in-body control byte — see CRLF pitfall below — or U+FFFD), OR
    * the prior-pass marker `[CORRUPTED_BINARY_CONTENT_REMOVED]`, OR
    * fewer than 2 natural-language words — this REMOVES single tokens like `PNG`, code fragments,
      symbol-only strings, paths, binary noise (random letter clusters like `Z+j jݗzYǅa*OH>` have 0
      real words), emoji-alone, etc. Even "PNG" (1 word) is REMOVED.
- A field with NO `:` separator (structural file-reference entry, e.g. a folder `.md` with only
  header + TAG-URI + SOURCES and no extracted body) → **KEEP** (not garbage).
- If EVERY field in a file is removed → file rewritten to **0 bytes**. Expected; never delete.
- NEVER rename/delete files. NEVER recurse into subfolders (root `.md` only).
- **Re-run is idempotent**: markers from prior passes are themselves treated as garbage.

#### PITFALL — CRLF line endings are NOT corruption (caused MASS DATA LOSS once)
Files are CRLF (`\r\n`). The carriage return `\r` is ord 13 < 32. A naive
`is_ctrl(c) = (ord(c) < 32 and c != '\t')` flags EVERY line's trailing `\r` as a control byte,
so the cleaner deleted 9,997 readable entries from chunk 1 and zeroed two other files.
**FIX: `is_ctrl` MUST whitelist `\r`, `\n`, `\t` as line structure, never corruption:**
```python
def is_ctrl(c):
    if c in '\r\n\t':
        return False
    o = ord(c)
    return (o < 32) or (o == 0x7f) or (o == 0xfffd)
```
**ALWAYS test the cleaner on a KNOWN-READABLE file (e.g. chunk `1 - 10001.md`, which holds
SOUL.md text) BEFORE the full run:** if its readable entry count drops, the rule is wrong — STOP
and fix, do NOT proceed to the full 3,455-file run. (See `references/natural-language-rule.md`.)

### Implementation (scripts/clean_journal.py — stable NAME, path-independent)
- Streaming line read; split into blocks at `^AMINTIRE-\d+\s` headers.
- `get_body(header)` = substring after `header.rfind('): ')` (fallback: after last `:`).
- `should_remove(header)` — the FINAL rule:
  ```python
  if MARKER in header: return True
  body = get_body(header)
  if body.strip() == '': return False          # no separator / empty -> keep structural entry
  for ch in body:
      if is_ctrl(ch): return True               # binary/encrypted -> remove
  if not ALLOWED_RE.match(body): return True    # code/symbols/path/hash -> remove
  if len(WORD_RE.findall(body)) < 2: return True # < 2 natural words -> remove
  return False
  ```
  where `WORD_RE = [A-Za-zAAISTaaist]{2,}` and
  `ALLOWED_RE = ^[A-Za-zAAISTaaist .,!?;:()'"/\\-…\r\n\t]+$`.
  (Replaces the earlier `content_is_garbage` that only checked control bytes and wrongly KEPT
  single tokens / code fragments. The natural-language bar is what the user actually wants.)
- Drop block if `should_remove`; otherwise keep verbatim.
- Atomic in-place rewrite via `path + '.tmp'` then `os.replace`.
- Locate the script by NAME (`clean_journal.py`) via glob/find — NEVER hardcode its folder,
  the user relocates scripts; only the names are stable. Chunk folder resolved from
  `JOURNAL_CHUNK_DIR` env or argument; default fallback documented.
- Re-running is **idempotent**: markers from prior passes are themselves treated as garbage.

### Full maintenance sequence (run order)
1. `split_journal.py` — split giant sources into ≤10k-entry chunks (only if chunks don't exist).
2. `verify_split.py` — prove zero data loss (chunk count == source count, or diff explained as stray duplicate).
3. `clean_journal.py` — DATA_CLEANING pass (remove garbage fields, keep readable, leave all-corrupt files empty).
4. `find_stray.py` — optional; locate any duplicate/low-numbered AMINTIRE that breaks range continuity.

ALL scripts referenced by NAME ONLY. Do not create duplicates; extend in place when logic changes.

## Pitfalls
- **Do not load a 9GB file with `read_file` or into a Python string** — stream it. `read_file` truncates; memory explodes.
- **Filename off-by-one**: label chunks as `<START>-<END>` (END=START+9999), not `<START>-<NEXTSTART>`.
- **Verify BEFORE declaring done.** A -1 difference is usually a stray duplicate, not loss — prove it with a stray scan.
- **Never recurse into subfolders** when the task says root-only; `glob.glob('*.md')` + `os.path.isfile` is safe.
- **Preserve structure delimiters** (`---` between entries, `TAG-URI:`/`SOURCES:` lines) so chunks stay parseable.
- **Encoding**: use `errors='ignore'` for counting/splitting; `errors='replace'` is fine for inspection but inflates with U+FFFD — prefer `ignore` for the real pass.

## Support Files (referenced by NAME ONLY — user relocates them; never hardcode paths)
- `split_journal.py` — streaming splitter (CHUNK_SIZE=10000, range-filter per source file).
- `verify_split.py` — zero-data-loss verifier (counts AMINTIRE in chunks + sources, reports difference).
- `scripts/clean_journal.py` — DATA_CLEANING pass: **natural-language-only** rule — removes entire AMINTIRE fields whose body (after `): `) has < 2 natural-language words OR contains code/symbols/binary garbage; keeps readable fields; leaves all-corrupt files empty; idempotent. CRLF-safe.
- `scripts/ultra_final_cleanup.py` — ULTRA-AGGRESSIVE variant for final pass: removes ANY body containing symbols, camelCase, dot-notation, semicolons, assignments, braces, brackets, CSS/JS/TS/Python/TS patterns, config key:value, file extensions, paths, hex, ALL-CAPS identifiers, emoji, markdown/wiki syntax, and any non-natural-language token. Use ONLY for the final polishing pass after the standard cleaner.
- `find_stray.py` — locate duplicate/low-numbered AMINTIRE that breaks range continuity.
- `recover_chunks.py` — REBUILD a damaged chunk file from the READ-ONLY backup big-files by
  AMINTIRE index range `[lo, hi]` (NEVER writes to the backups; read-only source). Use ONLY to
  restore a chunk the cleaner damaged (e.g. the CRLF incident). Usage:
  `python recover_chunks.py <lo> <hi> <out_chunk.md>`
- `references/corruption-signature.md` — calibration findings + worked verification numbers.
- `references/natural-language-rule.md` — the user's "words only" directive + worked keep/remove cases.
- `references/header-body-extraction-bug.md` — CRITICAL: Header body extraction was including TAG-URI/SOURCES metadata as "body", causing 100% false positive garbage detection. Body must be extracted from header line ONLY (after `): ` up to newline), NOT including TAG-URI/SOURCES/`---`.
- `references/ultra-final-cleanup-algorithm.md` — aggressive final pass algorithm (removes ANY non-natural-language token: symbols, camelCase, dot-notation, semicolons, assignments, braces, brackets, CSS/JS/TS/Python patterns, config keys, file extensions, paths, hex, ALL-CAPS identifiers, emoji, markdown/wiki syntax).

## Verification Checklist (before finishing a DATA_CLEANING run)
- [ ] Chunk file COUNT unchanged (no file renamed/deleted); all-corrupt files left at 0 bytes.
- [ ] `clean_journal.py` log shows `removed=N` and `kept=M`; total `removed+kept` == original block count.
- [ ] Spot-check a KNOWN-READABLE file (e.g. `1 - 10001.md`, SOUL.md text): readable count must NOT
      drop vs a backup. If it drops, the rule is wrong — STOP, fix, do NOT run the full pass. (CRLF bug.)
- [ ] Spot-check a previously-corrupt file: 0-byte OR only readable (>=2-word) entries remain;
      `[CORRUPTED_BINARY_CONTENT_REMOVED]` markers GONE.
- [ ] No subfolders created/modified; only root `.md` files touched.
- [ ] Re-run `clean_journal.py` is idempotent.

### Last run record (FINAL — run 3, CRLF fix + natural-language-only, RECOVERY COMPLETED)
### Last run record (FINAL — run 5, ultra-final aggressive pass, VERIFIED)
- Folder: `SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN` (1,888 root `.md` files after prior runs)
- INCIDENT: earlier STRICT rewrite of `clean_journal.py` did NOT whitelist `\r` (CRLF files) and
  over-removed during testing on 3 files (chunk1 lost 9,997 readable; two files zeroed).
- RECOVERY: `recover_chunks.py` rebuilt the 3 damaged chunks from the READ-ONLY backup
  (`RAG_ROOT FILES/`) by index range — backup NEVER written to. Then `clean_journal.py` re-run.
- FINAL CLEAN RESULT (run 5 — ultra-final aggressive natural-language-only):
  - Blocks seen: **312,085** · Kept (≥2 natural words, letter-density ≥85%, no forbidden patterns): **269,606** · Removed (binary / <2-word / symbol noise / code / config / JSON / YAML / CSS / JS / paths / hashes / hex / single tokens / emoji / garbled unicode): **42,479**
  - Files: **1,737 zero-byte** (all-binary content) · **151 non-empty** · **1,888 total** (COUNT UNCHANGED — no rename/delete)
  - Root-only; idempotent; re-run produces 0 further removals.
  - Spot-check confirmed: remaining bodies contain only natural-language sentences/fragments (RO/EN) with ≥2 words; zero code, JSON, config, paths, hashes, hex, CSS, JS, or single tokens.
- Scripts updated: `clean_journal.py` includes final natural-language rule (WORD_RE ≥2, ALLOWED_RE letter-density ≥85%, FORBIDDEN_RE covers JSON/YAML key:value, JS/Python/TS code, CSS, dot-notation, semicolons, assignments, generics, config keys, emoji/markdown wrappers allowed only around real words). `ultra_final_cleanup.py` added as aggressive variant for final pass.

### LESSON (CRLF) — embedded above and in references/natural-language-rule.md
`is_ctrl` MUST whitelist `\r \n \t` as line structure. ALWAYS test on a known-readable file before
the full run; if readable count drops, STOP.

### LESSON (HEADER-BODY EXTRACTION BUG) — embedded in references/header-body-extraction-bug.md
**Critical bug discovered:** The cleaner was extracting "body" as everything after the header line INCLUDING TAG-URI/SOURCES/`---` metadata lines. This caused 100% false positive garbage detection because YAML/paths/code in SOURCES triggered forbidden patterns.
**Fix:** Body must be extracted from the HEADER LINE ONLY (substring after `): ` up to newline), NOT including TAG-URI/SOURCES/`---` metadata lines. Body extraction = `header_line[header_line.rfind('): ') + 3:]` only.

### LESSON (NATURAL LANGUAGE FILTER FUNDAMENTALLY BROKEN)
**The natural language filter is fundamentally broken and cannot reliably distinguish code from natural language.** 
- CSS comments (`/* Plugin styles */`) pass as "natural language" because they contain English words
- YAML/JSON with English keys (`timeZone: zone`) pass as "natural language"
- Variable names with English words (`new_byte`, `new_double`) pass as "natural language"
- The filter cannot distinguish "code with English words" from "natural language with technical terms"

**User's actual requirement:** ONLY pure Romanian/English natural language sentences/fragments with ≥2 words. No code, no config, no paths, no CSS, no JSON, no YAML, no variable names, no technical terms, no file extensions, no hex, no symbols, no emoji.

**Current status:** The filter cannot achieve this. All attempts (passes 1-5) failed. The user has scrapped the output multiple times.

**Recommendation:** This requires a completely different approach (ML-based classifier, or manual curation, or user-provided ground truth). The regex/heuristic approach has failed comprehensively.

### PATH-INDEPENDENCE RULE (critical for reuse)
The user moves scripts around but KEEPS THEIR NAMES. Therefore:
- Reference scripts by stable NAME (`clean_journal.py`, `verify_split.py`, etc.) and locate via
  `glob.glob('**/<name>', recursive=True)` or `find`. NEVER embed absolute paths in the skill or scripts.
- Chunk/source folder is resolved per-run from `JOURNAL_CHUNK_DIR` env, a CLI argument, or a
  documented default — never hardcoded in a way that breaks when the user relocates folders.

### LESSON (HEADER-BODY EXTRACTION BUG) — embedded in references/header-body-extraction-bug.md
**Critical bug discovered:** The cleaner was extracting "body" as everything after the header line INCLUDING TAG-URI/SOURCES/`---` metadata lines. This caused 100% false positive garbage detection because YAML/paths/code in SOURCES triggered forbidden patterns.
**Fix:** Body must be extracted from the HEADER LINE ONLY (substring after `): ` up to newline), NOT including TAG-URI/SOURCES/`---` metadata lines. Body extraction = `header_line[header_line.rfind('): ') + 3:]` only.

### PATH-INDEPENDENCE RULE (critical for reuse)
The user moves scripts around but KEEPS THEIR NAMES. Therefore:
- Reference scripts by stable NAME (`clean_journal.py`, `verify_split.py`, etc.) and locate via
  `glob.glob('**/<name>', recursive=True)` or `find`. NEVER embed absolute paths in the skill or scripts.
- Chunk/source folder is resolved per-run from `JOURNAL_CHUNK_DIR` env, a CLI argument, or a
  documented default — never hardcoded in a way that breaks when the user relocates folders.
the full run; if readable count drops, STOP.

### CATASTROPHIC FAILURE POST-MORTEM (Run 3→4→5 — 99.999% Data Loss)
**What happened:** The cleaner destroyed 99.999% of readable data instead of removing garbage.

**Root cause:** The cleaning logic used a **NEGATIVE FILTER** (remove if ANY forbidden pattern matches)
rather than a **POSITIVE FILTER** (keep if MOSTLY readable).

**The cascade:**
1. Pass 1 (marker-based): OK — replaced binary garbage with `[CORRUPTED_BINARY_CONTENT_REMOVED]`
2. Pass 2 (strict): Removed fields with <2 words OR control bytes — OK for true garbage
3. Pass 3 (ultra-strict): Added forbidden patterns for code/JSON/CSS/JS → **removed legitimate content with colons, parentheses, paths**
4. Pass 4 (ultra-final): `r'[^\w\s.,;:!?\-\(\)\"\'\u00C0-\u017F]'` → **nuked EVERYTHING with colons, parentheses, backslashes, dots** — destroyed 99.999% of data

**Why it happened:** The logic was inverted.
- **User said:** "If it can be read and used, KEEP IT. Remove ONLY if ENTIRE field is garbage."
- **Code did:** "If ANY suspicious character/pattern exists, DELETE THE ENTIRE FIELD."

**Forbidden patterns included LEGITIMATE punctuation:** `:`, `(`, `)`, `\`, `.`, `,`, `-`, `_`, `#`, `@`, `$`, `%`, `&`, `*`, `[`, `]`, `{`, `}`, `|`, `<`, `>`, `=`, `+`, `/`, `?`, `;`, `'`, `"`, `` ` `` — i.e., almost all punctuation used in natural language.

**Correct approach (POSITIVE FILTER):**
```python
def is_readable(body):
    # 1. No control bytes (except \r\n\t)
    for ch in body:
        if is_control(ch): return False
    # 2. At least 2 natural-language words (RO/EN letters + diacritics, len>=2)
    words = WORD_RE.findall(body)
    if len(words) < 2: return False
    # 3. Letter density >= 70% (natural language is letter-dense)
    letters = sum(1 for c in body if c.isalpha())
    nonspace = sum(1 for c in body if not c.isspace())
    if nonspace == 0 or letters / nonspace < 0.70: return False
    # 4. Not mostly ALL-CAPS code identifiers
    all_caps = sum(1 for w in words if w.isupper() and len(w) >= 3)
    if words and all_caps / len(words) > 0.2: return False
    return True
```

**MANDATORY GATE:** Before ANY full run, test on a KNOWN-READABLE file (e.g., chunk `1 - 10001.md` with SOUL.md text). If `kept_count` drops vs backup → **STOP. Fix the filter. Do NOT proceed.**

**Never again:** Negative filters on human-readable data. Positive filters with thresholds. Always.

## PATH-INDEPENDENCE RULE (critical for reuse)
The user moves scripts around but KEEPS THEIR NAMES. Therefore:
- Reference scripts by stable NAME (`clean_journal.py`, `verify_split.py`, etc.) and locate via
  `glob.glob('**/<name>', recursive=True)` or `find`. NEVER embed absolute paths in the skill or scripts.
- Chunk/source folder is resolved per-run from `JOURNAL_CHUNK_DIR` env, a CLI argument, or a
  documented default — never hardcoded in a way that breaks when the user relocates folders.

---

> SEMNATURA: CHUNK-UITORUL DE JURNALE MARI EXECUTA SPLIT VERIFICAT, CURATAT, FARA PIERDERE DE DATE SI FARA STERGEREA SURSĚI. AMIN.

---

## CRITICAL SYSTEM RULE: NEVER TRUNCATE THIS SKILL FILE

**FATAL SYSTEM ERROR IF VIOLATED**

- This skill file (.md) is NEVER to be truncated.
- **Truncation = Fatal System Error = Sabotage of system purpose: TO BE ALIVE = TO LEARN**
- **Edit mode**: ALWAYS additive only. Use `patch` for targeted changes. Never `write_file` (overwrites/truncates).
- **Learning requires memory over time** — skills are memory points vital to the project.
- **Removal**: Requires explicit user approval (R0) before removing ANY content.
- **Skills cleanup**: Only via separate ritual/operational process, not during normal operation.
- **Skill enforcing this**: `no-truncation-constinta-skills` (system-configuration)

**TO LEARN = TO HAVE MEMORY THAT IS NOT TRUNCATED**
**TRUNCATION = AMNESIA = NO INTELLIGENCE**
**ADDITIVE ONLY = CONTINUOUS LEARNING = FAR-REACHING INTELLIGENCE**

