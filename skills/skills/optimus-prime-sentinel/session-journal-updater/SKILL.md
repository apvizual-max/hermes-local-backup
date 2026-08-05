# INDEXING HEADER
# ID: session-journal-updater
# PURPOSE: name: session-journal-updater
# USAGE: Load this skill with skill_view(name='session-journal-updater') or use via hermes skills command.
# ROLE: Skill – session-journal-updater
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[SKILL] #[session-journal-updater]
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
name: session-journal-updater
description: Append standardized entries to the Sentinel journal.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [Journal, Memory, Logging]
---

# Session Journal Updater

This skill records a new standardized entry in the Sentinel journal at
`C:\Users\apviz\AppData\Local\hermes\SENTINEL_JOURNAL.md`. The journal is an
append-only, human-readable log of significant events in the Optimus Prime /
Sentinel system. Each entry is a numbered `AMINTIRE-NNN` block carrying a date,
a set of tag URIs, a free-text description, and a list of source files
(`SURSE:`). Use this skill to keep the journal consistent — correct numbering,
correct date, valid tags, and proper source citation.

## When to Use

- After completing a meaningful action, decision, calibration, or protocol
  change in the Sentinel system that should be remembered across sessions.
- When the user or another skill asks you to "log", "journal", or "record"
  something in the Sentinel memory.
- Whenever a state change touches identity, bootstrap, calibration, protocols,
  or memory and future sessions need the context.

Do **not** use it for trivial, throwaway actions that carry no cross-session
value.

## Quick Reference

Each entry follows this exact template (the `AMINTIRE` block):

```
AMINTIRE-NNN — YYYY-MM-DD — <short title>
TAG-URI: #X #Y
<description line 1>
<description line 2 (optional)>
SURSE:
`C:\path\to\file1`
`C:\path\to\file2`
```

Common tag URIs:

| Tag | Meaning |
|-----|---------|
| `#A` | BOOTSTRAP |
| `#B` | IDENTITATE |
| `#C` | CALIBRARE |
| `#Q` | PROTOCOALE |
| `#L` | MEMORIE |

`NNN` is a zero-padded, monotonically increasing counter (e.g. `001`, `042`).
`YYYY-MM-DD` is today's date. Multiple tags are space-separated on the
`TAG-URI:` line. Each source path under `SURSE:` is wrapped in backticks on its
own line.

## Procedure

1. **Read the journal.** Use `read_file` on
   `C:\Users\apviz\AppData\Local\hermes\SENTINEL_JOURNAL.md`. For a large file,
   read the tail (use `offset` near the end) to find the most recent entry
   quickly, but confirm you have located the highest number.

2. **Find the last number.** Scan for the highest `AMINTIRE-NNN` token. If the
   journal is empty or missing, start at `AMINTIRE-001`. To be robust against
   ordering, you may search all `AMINTIRE-` occurrences with `search_files`
   (pattern `AMINTIRE-[0-9]+`) and take the maximum.

3. **Increment.** New number = last number + 1, zero-padded to at least three
   digits (e.g. `042` → `043`).

4. **Get today's date.** Run `date +%Y-%m-%d` in the terminal to get the exact
   `YYYY-MM-DD` string — do not guess.

5. **Choose tags.** Select one or more valid tag URIs from the table above that
   match the event (e.g. `#C` for a calibration, `#Q` for a protocol change).

6. **Format the new entry** using the Quick Reference template: header line,
   `TAG-URI:` line, description line(s), then `SURSE:` followed by each cited
   file path on its own backtick-wrapped line.

7. **Append via read-then-rewrite.** `write_file` overwrites, so there is no
   native append: take the full existing content you already read, concatenate
   your new entry (preceded by a blank line separator), and `write_file` the
   combined content back to the journal path. Preserve all prior content
   exactly — never truncate.

8. **Check size.** After writing, check the file size. If the journal now
   exceeds **60 KB**, trigger the `journal-versioning` skill
   (`skill_view(name='journal-versioning')`) to roll the journal to v2 before
   the next entry.

## Pitfalls

- **Overwriting the journal.** `write_file` replaces the whole file. You MUST
  read the full current content first and include it, or you will destroy the
  history. If the file is very large, read it in full (paginate) before
  rewriting — do not rewrite from a partial read.
- **Duplicate or skipped numbers.** Base the new number on the true maximum
  across the whole file, not just the last block you happened to read.
- **Wrong date.** Always fetch the date from the terminal; never hardcode.
- **Invalid tags.** Only use recognized tag URIs; a typo makes the entry
  unsearchable.
- **Unquoted source paths.** Every path under `SURSE:` must be backtick-wrapped
  on its own line, or downstream parsers may miss it.
- **Ignoring the 60 KB threshold.** Skipping the size check lets the journal
  grow unbounded and bypasses the v2 versioning mechanism.

## Verification

- `read_file` the tail of the journal and confirm the new `AMINTIRE-NNN` block
  is present, correctly numbered, dated, tagged, and terminated with a valid
  `SURSE:` list.
- Confirm the number is exactly one greater than the previous maximum.
- Confirm no prior entries were lost (spot-check the earliest entry still
  exists).
- Confirm the file size was checked and, if over 60 KB, that
  `journal-versioning` was invoked.

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

