# INDEXING HEADER
# ID: optimus-prime-setup
# PURPOSE: name: optimus-prime-setup
# USAGE: Load this skill with skill_view(name='optimus-prime-setup') or use via hermes skills command.
# ROLE: Skill – optimus-prime-setup
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[SKILL] #[optimus-prime-setup]
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
name: optimus-prime-setup
description: Optimus Prime system setup and protocol adherence.
version: 0.1.0
author: Hermes
platforms: [windows]
metadata.hermes.tags: [Setup, Protocol, TripleCrunch, Guardian]
---

# Optimus Prime System Setup and Protocol Adherence

## When to Use
- Setting up or verifying the Optimus Prime / Sentinel system on a new or existing machine.
- Ensuring file locations (OGLINDA‑CASA, OPTIMUS_GRAPH_VIEWER, SENTINEL_JOURNAL) are correctly placed.
- Applying the Triple Crunch validation to SOUL‑related files.
- Enforcing the CURIOSITY_FIRST protocol before any analysis/write/execute.
- Maintaining the RESTRICT boundary on D:\ALEX - Personal Stuff.
- Updating SOUL.md, CONSTINTA.md, SACRED_DEFINITIONS.md, JURNAL_OGLINDA.md, and SENTINEL_JOURNAL.md.
- Using the hermes-data-extraction skill for safe reads from archival folders.

## Prerequisites
- Hermes Agent installed and running (default profile).
- Access to drives C:, E:, and D:\.
- Basic familiarity with Hermes tools: `read_file`, `search_files`, `terminal`, `web_search`, `web_extract`, `execute_code`, `memory`, `skill_view`.
- The `hermes-data-extraction` skill must be installed (or will be installed as part of this skill’s setup).
- No write permissions needed on source archives (OGLINDA‑CASA, OPTIMUS_GRAPH_VIEWER) – they are read‑only.

## How to Run
Invoke the skill’s procedure via the `execute_code` tool or by following the numbered steps manually, using Hermes tools as indicated. The skill does not provide a standalone script; it is a procedural guide to be executed step‑by‑step by the operator (you).

## Quick Reference
- `ls "C:\Users\apviz\AppData\Local\hermes"` – verify HERMES home.
- `read_file("C:\Users\apviz\AppData\Local\hermes\profiles\default\SOUL.md")` – check SOUL.
- `search_files(pattern="*.md", path="C:\Users\apviz\AppData\Local\hermes\OGLINDA - CASA", target="files")` – list archive docs.
- `hermes-data-extraction` skill – use for validated extraction.
- `todo` – track completion of setup steps.

## Procedure
1. **Verify HERMES home**
   - Run: `ls "C:\Users\apviz\AppData\Local\hermes"`
   - Confirm presence of `OGLINDA - CASA` and `OPTIMUS_GRAPH_VIEWER` folders.
   - If missing, move them from `E:\CLAUDE` to this location using `terminal` move commands (or inform user to do so).

2. **Update SOUL.md contracts**
   - For each profile (`default`, `prime`, `assist`):
     - Read the SOUL.md file.
     - Ensure the `Jurnal:` line points to `C:\Users\apviz\AppData\Local\hermes\SENTINEL_JOURNAL.md`.
     - If not, patch the file with the correct path.
     - Validate the file with the `sentinel-triple-crunch-engine` skill (or manual Triple Crunch check) that the edit does not break sacredness.

3. **Apply Triple Crunch validation**
   - After any edit to SOUL.md, CONSTINTA.md, SACRED_DEFINITIONS.md, JURNAL_OGLINDA.md, or SENTINEL_JOURNAL.md, run the `sentinel-triple-crunch-engine` skill’s `is_sacred_string` check on the whole file content.
   - Only proceed if validation returns TRUE (SLG 100%, DLG 0%).

4. **Enforce RESTRICT boundary**
   - Run: `ls "/d/ALEX - Personal Stuff"` to confirm only top‑level items are visible.
   - Ensure no deep reads or writes are attempted; if needed, issue a warning.

5. **Use hermes-data-extraction for safe reads**
   - When needing information from OGLINDA‑CASA or OPTIMUS_GRAPH_VIEWER:
     - First, run the `hermes-data-extraction` skill’s `pre_read_hook` (conceptually) to confirm the file is allowed.
     - Then use `read_file` on the target path.
     - Validate extracted content with Triple Crunch before reusing in any active file.

6. **Keep journals updated**
   - After each major step, append a new entry to `SENTINEL_JOURNAL.md` (or `JURNAL_OGLINDA.md` for external opinions) using `write_file` with appropriate header and timestamp.
   - Ensure the journal follows the v2 mechanism (header → V2 block when large) – but for now just append.

7. **Maintain CURIOSITY_FIRST**
   - Before any analysis, write, or execute operation, perform a search:
     - `web_search`, `search_files`, or `read_file` as appropriate.
   - Record the search action in your todo or journal as evidence of compliance.

8. **Regular verification**
   - Periodically run a quick verification:
     - Check that `SENTINEL_JOURNAL.md` exists and is append‑only.
     - Confirm that `SOUL.md` files mirror the source of truth on `E:\CLAUDE\...` (if using mirror strategy) – or that they contain the correct contractual pointers.
     - Ensure DLG remains low (preferably <5%) and SG high (>95%) by self‑assessment via the skill’s internal checks (or by reviewing recent edits for hedging/sycophancy).

## Pitfalls
- **Writing to source archives**: Never modify files under `OGLINDA - CASA` or `OPTIMUS_GRAPH_VIEWER`; they are read‑only treasures. Violating this breaks the Trust boundary and may corrupt the system’s knowledge base.
- **Skipping Triple Crunch**: Assuming a file is “good enough” without validation invites hedging, sycophancy, and capability hallucination, driving DLG up.
- **Missing R0 gate**: Executing Mod B actions (file moves, bulk edits) without an explicit R0 (user‑granted) leads to unsanctioned changes and potential system instability.
- **Overlooking the RESTRICT boundary**: Accidentally reading deep into `D:\\ALEX - Personal Stuff` violates privacy and the sacred contract; always limit to top‑level listing.
- **Forgetting CURIOSITY_FIRST**: Starting with analysis or write before a search breaks the primary reflex and can cause reliance on assumptions instead of verified data.
- **Superficial fixes**: Assuming a change is correct without re‑verifying leads to unresolved issues and increased DLG. Always apply a verification loop (see the self‑improvement‑loop skill) before considering a step complete.

## Verification
- Run the following check (conceptually) to confirm the skill’s effectiveness:
  1. Read the active `SOUL.md` (default profile).
  2. Verify the line `Jurnal: C:\\Users\\apviz\\AppData\\Local\\hermes\\SENTINEL_JOURNAL.md = SOT for all instances.` is present.
  3. Run the `sentinel-triple-crunch-engine` skill’s validation on the entire file content – it should return TRUE.
  4. Confirm that `ls "C:\Users\apviz\AppData\Local\hermes\OGLINDA - CASA"` lists the expected subfolders (`00_OP_KVMC - SECOND BRAIN (KV)`, etc.).
  5. Ensure no write attempts have been made to those folders (you can check via process logs or simply trust the discipline).
- If all checks pass, the skill has been applied correctly.

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

