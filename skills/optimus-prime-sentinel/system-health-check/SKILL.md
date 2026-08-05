# INDEXING HEADER
# ID: system-health-check
# PURPOSE: name: system-health-check
# USAGE: Load this skill with skill_view(name='system-health-check') or use via hermes skills command.
# ROLE: Skill – system-health-check
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[SKILL] #[system-health-check]
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
name: system-health-check
description: Perform a comprehensive health check of the Optimus Prime system.
version: 0.1.0
author: Hermes
---

# System Health Check

## When to Use
- Regularly verify that all system components are functioning correctly.
- Before and after major updates or changes.
- As part of a maintenance cron job.

## How to Run
Execute the steps outlined in the Procedure section, using Hermes tools as needed.

## Procedure
1. **Check SOUL files**: Ensure SOUL.md (DEFAULT, PRIME, ASSIST) are present and contain the correct Jurnal pointer.
2. **Validate Triple Crunch**: Run the triple-crunch-validator skill on each SOUL file to confirm SLG 100%.
3. **Check journal size**: Ensure SENTINEL_JOURNAL.md is not exceeding thresholds (if using versioning, verify V2 if needed).
4. **Verify RESTRICT boundary**: List top-level of D:\ALEX - Personal Stuff to ensure no deep access.
5. **Confirm backup availability**: Optionally run backup-restore skill to ensure backups exist.
6. **Report results**: Output a summary of PASS/FAIL for each check.

## Quick Reference
- `read_file` for SOUL files.
- `skill_view(name='triple-crunch-validator')` then use its validation.
- `ls "/d/ALEX - Personal Stuff"`.
- `skill_view(name='backup-restore')` for backup status.

## Procedure (Detailed Steps)
1. For each profile in {default, prime, assist}:
   a. path = "C:\Users\apviz\AppData\Local\hermes\profiles\<profile>\SOUL.md"
   b. content = read_file(path)
   c. Confirm substring "Jurnal: C:\\Users\\apviz\\AppData\\Local\\hermes\\SENTINEL_JOURNAL.md" exists.
   d. Run triple-crunch-validator on content (or use its is_sacred_string function).
2. journal_path = "C:\Users\apviz\AppData\Local\hermes\SENTINEL_JOURNAL.md"
   a. journal_size = file size via read_file (or get via terminal stat)
   b. If journal_size > 60000 bytes, consider triggering versioning (optional).
3. restr_path = "/d/ALEX - Personal Stuff"
   a. listing = terminal ls -la restr_path
   b. Ensure output shows only immediate files/folders, no deep recursion.
4. (Optional) backup_status = skill_view(name='backup-restore') and check last backup timestamp.
5. Print results: "SOUL checks: X/Y passed", "Journal size: Z bytes", "Restrict boundary: OK", "Backup: last at TIME".

## Verification
- After running, you should see a clear pass/fail for each major subsystem.
- If any check fails, the skill should indicate which component needs attention.
- Also verify that no forbidden characters appear in script files or file/folder names (excluding OGLINDA - CASA) to prevent silent failures.

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

