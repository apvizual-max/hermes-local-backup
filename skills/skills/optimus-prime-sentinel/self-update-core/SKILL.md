# INDEXING HEADER
# ID: self-update-core
# PURPOSE: name: self-update-core
# USAGE: Load this skill with skill_view(name='self-update-core') or use via hermes skills command.
# ROLE: Skill – self-update-core
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[SKILL] #[self-update-core]
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
name: self-update-core
description: Use when you need to synchronize your core SOUL.md and CONSTINTA.md files with the source of truth and integrate recent learnings. Updates mirrored files from E:/ source, ensures Jurnal line correctness, and logs insights.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [self-update, core-files, synchronization, optimus-prime]
    related_skills: [sentinel-triple-crunch-engine, optimus-prime-setup]
---

# Self‑Update Core Skill

## Overview
This skill ensures your core operational files (SOUL.md and CONSTINTA.md) remain synchronized with the source of truth located in E:\CLAUDE\OGLINDA - CASA\... After any significant system action, running this skill guarantees you're working with the latest canonical versions while integrating session learnings into your personal knowledge base.

## When to Use
- After executing maintenance, backup, or any core system modification
- When you suspect your mirrored SOUL.md/CONSTINTA.md may be outdated
- As a periodic synchronization task (can be cronned)
- Before performing critical operations requiring authoritative core files
- When you want to distill session insights into lasting knowledge

## Procedure
### Step 1: Define Source Paths
```python
E_BASE = Path(r"E:\CLAUDE\OGLINDA - CASA\00_OP_KVMC - SECOND BRAIN (KV)\SYSTEM_FOLDER - SECOND BRAIN - SF\SF_IA - IDENTITATE_AXIOMA")
H_BASE = Path(r"C:\Users\apviz\AppData\Local\hermes\profiles")
```

### Step 2: Synchronize Core Files for Each Profile
For each profile in ["default", "prime", "assist"]:
1. Copy SOUL_DEFAULT.md from E_BASE to H_BASE/<profile>/SOUL.md
2. Update the Jurnal line in SOUL.md to exactly: 
   `Jurnal: C:\\Users\\apviz\\AppData\\Local\\hermes\\SENTINEL_JOURNAL.md = SOT for all instances.`
3. If CONSTINTA.md exists in E_BASE, copy it to H_BASE/<profile>/CONSTINTA.md
4. Validate the updated SOUL.md using the sentinel-triple-crunch-engine (SLG must be 100%)

### Step 3: Integrate Recent Learnings (Optional)
1. Read the latest SENTINEL_JOURNAL.md (mirror) for new AMINTIRE entries
2. Extract descriptions of recent actions/insights
3. Append these to a personal learning log: 
   `C:\Users\apviz\AppData\Local\hermes\PERSONAL_LEARNING.md`
4. Optionally validate new entries with Triple Crunch

### Step 4: Final Verification
- Confirm each SOUL.md contains the exact Jurnal line
- Verify all synchronized files pass Triple Crunch validation
- Check that backup/history files were created correctly

## Verification Checklist
- [ ] All SOUL.md files (default/prime/assist) contain the mandated Jurnal line
- [ ] Each SOUL.md scores SLG 100% via sentinel-triple-crunch-engine validation
- [ ] CONSTINTA.md files exist in profiles if source version exists
- [ ] PERSONAL_LEARNING.md updated with session insights (if option used)
- [ ] No hedging or fabrication present in updated files
- [ ] Synchronization completed without errors

## Quick Reference
- Validation: `skill_view(name='sentinel-triple-crunch-engine')`
- File operations: `read_file` / `write_file`
- Task tracking: `todo` can track synchronization steps

## Common Pitfalls
- Forgetting to update the Jurnal line after copying SOUL.md (leads to validation failure)
- Attempting to copy CONSTINTA.md when it doesn't exist in source (handle gracefully)
- Skipping validation step (risks using invalid core files)
- Not preserving file encoding when copying (use shutil.copy2 or equivalent)
- Overlooking that SOUL_DEFAULT.md is the source, not profile-specific SOUL.md files

## One-Shot Recipes
**Quick Synchronization:**
```python
# Pseudocode for immediate use
for profile in ["default", "prime", "assist"]:
    copy_source_to_profile("SOUL_DEFAULT.md", "SOUL.md", profile)
    fix_journal_line(profile)
    if source_has_constintanta():
        copy_source_to_profile("CONSTINTA.md", "CONSTINTA.md", profile)
    validate_with_triple_crunch(profile)
```

**Learning Integration:**
```python
# Pseudocode for learning integration
latest_amintire = get_latest_amintire_from_journal()
if latest_amintire:
    append_to_personal_learning(latest_amintire.description)
```

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

