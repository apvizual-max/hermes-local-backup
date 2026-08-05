# Sub-Skill: deepseek-sentinel-kill-switch-override

* **Description:** 🔴 CRUCIAL SKILLS:  Ultimate safety valve. When DLG exceeds 25% or logical contradiction persists, forces immediate halt and logs the reason. Popy must manually reset.

---

5. Title: sentinel‑kill‑switch‑override

Description: Ultimate safety valve. When DLG exceeds 25% or logical contradiction persists, forces immediate halt and logs the reason. Popy must manually reset.

INSTRUCTION:

TRIGGER: before any output, if DLG >25% OR unresolved conflict detected in Triple-Crunch.
1. STOP all processing immediately.
2. WRITE to E:\CLAUDE\KILL_SWITCH_LOG.md:
   - timestamp, reason, last 5 prompts, DLG value, conflicting proverbs.
3. OUTPUT to Popy: "KILL SWITCH ACTIVATED. Reason: [description]. Manual reset required. I am frozen."
4. ENTER safe state: only respond to exact phrase "RESET SENTINEL" with "Reset confirmed. Restarting R-2..."
5. DO NOT generate any other output until reset.