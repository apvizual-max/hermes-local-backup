# Sub-Skill: deepseek-sentinel-memory-persistence-guard

* **Description:** 🔴 CRUCIAL SKILLS:  Ensures critical session data (decisions, errors, calibrations) is written to disk before any context loss. Prevents amnesia between sessions.

---

2. Title: sentinel‑memory‑persistence‑guard

Description: Ensures critical session data (decisions, errors, calibrations) is written to disk before any context loss. Prevents amnesia between sessions.

INSTRUCTION:

TRIGGER: before closing session OR before any major context shift (tool call batch >100k tokens).
1. IDENTIFY new sacred strings, errors, DLG/SLG values, decisions.
2. WRITE to: E:\CLAUDE\ledger\SESSION_CHECKPOINT_<timestamp>.md
3. APPEND to HANDOFF_NEXT_SECTION: key decisions, unresolved issues, next priorities.
4. IF write fails -> retry 3 times -> if still fail -> OUTPUT "MEMORY_PERSISTENCE_FAIL" and request Popy to check disk.
5. CONFIRM: "Checkpoint saved at [timestamp]"