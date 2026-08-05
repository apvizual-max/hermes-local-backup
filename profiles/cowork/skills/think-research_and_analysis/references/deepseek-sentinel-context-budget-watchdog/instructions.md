# Sub-Skill: deepseek-sentinel-context-budget-watchdog

* **Description:** 🔴 CRUCIAL SKILLS:  Monitors context window usage; triggers compaction or forced ritual when thresholds are crossed. Prevents context overflow hallucinations.

---

3. Title: sentinel‑context‑budget‑watchdog

Description: Monitors context window usage; triggers compaction or forced ritual when thresholds are crossed. Prevents context overflow hallucinations.

INSTRUCTION:

TRIGGER: at end of every assistant response (after output).
1. ESTIMATE tokens used in current session (tool calls + text).
2. CALCULATE remaining headroom %.
3. IF headroom <30%:
   - OUTPUT warning in ticker: "CTX: <30%"
   - COMPRESS oldest part of conversation into reflex_archive\T4_preventiv\<session>_compact.md
   - SUGGEST to Popy: "Recommend session close or continue with high risk."
4. IF headroom <15%:
   - FORCE RITUAL_IESIRE steps (BAGAJ → SAVE → REFLEX → CLOSE)
   - EXIT session immediately.
5. LOG headroom in session log.