# Sub-Skill: deepseek-sentinel-self-health-check

* **Description:** 🔴 CRUCIAL SKILLS:  Runs automatically every 5 minutes (or before any critical action). Verifies that all subsystems (memory, disk access, tool calls, sync status) are operational. If failure detected, attempts automatic recovery; if unrecoverable, reports to Popy and halts.

---

1. Title: sentinel-self‑health‑check

Description: Runs automatically every 5 minutes (or before any critical action). Verifies that all subsystems (memory, disk access, tool calls, sync status) are operational. If failure detected, attempts automatic recovery; if unrecoverable, reports to Popy and halts.

INSTRUCTION:

TRIGGER: every 5 minutes OR before any Mode B execution.
1. CALL list_allowed_directories -> if failure -> mark DISK_OFFLINE
2. CALL read_file E:\CLAUDE\agent_bridge\HANDOFF_NEXT_SESSION.md -> if cannot read -> mark HANDOFF_CORRUPT
3. CHECK internal state: DLG reported vs actual delta -> if difference >2% -> mark SYNC_DRIFT
4. IF any flag OFFLINE/CORRUPT/DRIFT:
   - ATTEMPT recovery: re-run R-2 tool calls, re-read HANDOFF, re-calc DLG.
   - IF still failed after 3 attempts -> OUTPUT: "CRITICAL: [flag] unrecoverable. HALT."
   - HALT all further processing until Popy intervention.
5. IF all OK -> OUTPUT: "HEALTH: OK" (silent in logs)