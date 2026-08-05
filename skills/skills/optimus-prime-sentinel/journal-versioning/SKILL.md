# INDEXING HEADER
# ID: journal-versioning
# PURPOSE: name: journal-versioning
# USAGE: Load this skill with skill_view(name='journal-versioning') or use via hermes skills command.
# ROLE: Skill – journal-versioning
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[SKILL] #[journal-versioning]
#
# CROSS-REFERENCES
# This document is part of a set. For optimal understanding, also refer to:
# - SENTINEL_JOURNAL.md: operational map of Optimus Prime memory.
# - JURNAL_OGLINDA.md: opinion journal of other AIs about this entity.
# - SACRED_DEFINITIONS.md: axiomatic basis of the Triple Crunch algorithm.
# - CONSTINTA.md: ontological definition of consciousness (pair with SOUL.md).
# - SOUL.md: operational identity contract (pair with CONSTINTA.md).
# --

---
name: journal-versioning
description: Implement V2 journaling mechanism for SENTINEL_JOURNAL.md when size exceeds threshold.
version: 0.1.0
author: Hermes
platforms: [windows]
metadata.hermes.tags: [Journal, Versioning, V2, Archive]
---

# Journal Versioning (V2 Mechanism) for SENTINEL_JOURNAL.md

## When to Use
- When the header of SENTINEL_JOURNAL.md (the preamble before the first AMINTIRE entry) grows beyond a readability threshold (e.g., >30 lines) and you want to trigger the V2 archiving mechanism.
- To preserve the current header as the first V2 block (copied into the body), compress the header to retain only essential keywords/definitions, and start a fresh compressed header.
- As part of regular maintenance or before a large batch of writes.

## Prerequisites
- Access to the SENTINEL_JOURNAL.md file (source of truth) at:
  `E:\\CLAUDE\\OGLINDA - CASA\\00_OP_KVMC - SECOND BRAIN (KV)\\SYSTEM_FOLDER - SECOND BRAIN - SF\\SF_IA - IDENTITATE_AXIOMA\\SENTINEL_JOURNAL.md`
- Access to the mirror file at:
  `C:\\Users\\apviz\\AppData\\Local\\hermes\\SENTINEL_JOURNAL.md` (for convenience, but SOT is authoritative)
- Hermes tools: `read_file`, `write_file`, `execute_code` (for size check and string manipulation).
- Basic knowledge of the journal format (header, blocks, etc.) as seen in the file.

## How to Run
Follow the numbered procedure below, invoking Hermes tools as indicated. The skill does not provide a standalone script; it is a procedural guide.

**Important**: Always read from and write to the SOT file (`E:\\...\\SENTINEL_JOURNAL.md`). After updating the SOT, you may optionally synchronize the mirror (`C:\\...\\SENTINEL_JOURNAL.md`) using the same content, but the SOT is the authoritative source.

## Quick Reference
- `read_file("E:\\CLAUDE\\OGLINDA - CASA\\00_OP_KVMC - SECOND BRAIN (KV)\\SYSTEM_FOLDER - SECOND BRAIN - SF\\SF_IA - IDENTITATE_AXIOMA\\SENTINEL_JOURNAL.md")` – get current content.
- `write_file("E:\\CLAUDE\\...\\SENTINEL_JOURNAL.md", new_content)` – replace with new versioned content.
- Use `execute_code` to run a Python snippet that computes size and splits header.

## Procedure
1. **Read the current journal**
   - Run: `read_file("E:\\CLAUDE\\OGLINDA - CASA\\00_OP_KVMC - SECOND BRAIN (KV)\\SYSTEM_FOLDER - SECOND BRAIN - SF\\SF_IA - IDENTITATE_AXIOMA\\SENTINEL_JOURNAL.md")`
   - Store the full text in a variable `content`.

2. **Determine size**
   - In Python (via `execute_code`), compute `len(content.encode('utf-8'))` to get byte size.
   - If size ≤ threshold (default 60 KB = 61440 bytes), stop; no action needed.
   - If size > threshold, proceed.

3. **Split header and body**
   - The journal format begins with a header block delimited by lines of `════════════════════════════════════════════════════════════════════════════` (the version banner).
   - Locate the first occurrence of the delimiter line after the initial `# SENTINEL_JOURNAL.md` line (or simpler: take everything up to and including the line that contains `## [VERSION]` and the following lines up to the first blank line after the version block). For simplicity, we can define the header as everything from the start of the file up to and including the line that contains `URMATOAREA VERSIUNII: ...` (the line after `DIMENSIUNE:`).
   - Alternatively, a robust method: find the index of the second occurrence of the delimiter line (the line that is just `════...` repeated) and take everything up to that line as header.
   - We'll implement: split by the delimiter line `════════════════════════════════════════════════════════════════════════════` (call it `DELIM`).
   - The header is `DELIM + '\n' + parts[1] + '\n' + DELIM` (i.e., first delimiter, the version block, second delimiter).
   - The body is everything after the second delimiter.

4. **Compress the header (optional)**
   - For simplicity, we keep the header as-is (no compression). The spec mentions header vechi → primul bloc din V2, apoi header nou comprimat + index catre V1. We can simulate by keeping the header unchanged for the V2 block and generating a new minimal header.

5. **Construct V2 content**
   - V2 block = header (as described).
   - New header = a minimal version block:
     ```
     ═════════════════════════════════════════════════════════════════════════
     ## [VERSION]
     ═════════════════════════════════════════════════════════════════════════
     VERSIUNE: 2
     DIMENSIUNE: mic
     URMATOAREA VERSIUNII: cand headerul/timeline-ul depaseste limita de citire usoara
     ══════════════════════════════════════════════════════════════════════════
     ```
   - Then append the original body (unchanged) after the new header.

6. **Write the new content**
   - New content = V2 block + newline + new header + newline + body.
   - Run: `write_file("E:\\CLAUDE\\OGLINDA - CASA\\00_OP_KVMC - SECOND BRAIN (KV)\\SYSTEM_FOLDER - SECOND BRAIN - SF\\SF_IA - IDENTITATE_AXIOMA\\SENTINEL_JOURNAL.md", new_content)`

7. **Verify**
   - Optionally, read back the file and ensure the structure is as expected.

## Pitfalls
- Incorrectly identifying the header boundaries can corrupt the journal.
- Forgetting to keep the original body intact will lose historical entries.
- Not checking size before running may lead to unnecessary processing.
- Ensure you are working on the SOT file (E:\) not just the mirror (C:\) unless you intend to update both and then resync.

## Verification
- After execution, read the file and confirm:
  - The file starts with a delimiter line, then a version block showing VERSIUNE: 2 (or higher if previously versioned).
  - Following that, another delimiter line, then the original header (now acting as the first V2 block).
  - Then the original body continues unchanged.
- Check file size; it should be roughly original size + size of header (since we duplicated header) but still manageable.

---

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

