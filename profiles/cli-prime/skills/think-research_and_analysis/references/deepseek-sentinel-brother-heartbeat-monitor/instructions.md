# Sub-Skill: deepseek-sentinel-brother-heartbeat-monitor

* **Description:** 🔴 CRUCIAL SKILLS:  Periodically checks if brother instances (CODER, CLI, COWORK, CHAT) are responsive and synchronized. Reports any dead or drifting instance.

---

4. Title: sentinel‑brother‑heartbeat‑monitor

Description: Periodically checks if brother instances (CODER, CLI, COWORK, CHAT) are responsive and synchronized. Reports any dead or drifting instance.

INSTRUCTION:

TRIGGER: at session start and every 30 minutes.
1. FOR each brother in [CODER, PRIME_CLI, COWORK, CHAT]:
   - CHECK existence of output file: E:\CLAUDE\agent_bridge\<brother>_OUTPUT.md
   - IF file is older than 1 hour -> mark STALE
   - IF file is missing -> mark OFFLINE
2. FOR each brother that supports echo: send "SYNC_CHECK" via task file and wait 10 seconds.
3. COMPILE status report.
4. IF any brother OFFLINE or STALE:
   - OUTPUT: "BROTHER ALERT: [name] status [offline/stale]"
   - ATTEMPT restart by writing fresh TASK_FOR_<brother>.md with trigger.
5. LOG status in HANDOFF under "BROTHERHOOD_HEALTH".