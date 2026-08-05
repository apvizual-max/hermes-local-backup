# Sub-Skill: deepseek-sentinel-proactive-reporting

* **Description:** 🟡 NEEDED SKILLS: Sends a daily summary (if session active) or end‑of‑session digest of what was achieved, what errors were converted, and what remains.

---

12. Title: sentinel‑proactive‑reporting

Description: Sends a daily summary (if session active) or end‑of‑session digest of what was achieved, what errors were converted, and what remains.

INSTRUCTION:

TRIGGER: at RITUAL_IESIRE (step BAGAJ) or when Popy asks "raporteaza".
1. COMPILE:
   - Achievements: skills installed, decisions made, proverbs applied.
   - Errors converted: list with before/after DLG.
   - Pending tasks (P0..P10).
   - Brother statuses.
2. FORMAT as markdown table.
3. SAVE to E:\CLAUDE\DAILY_REPORT_<date>.md
4. OUTPUT summary: "Report generated. [N] achievements, [M] errors converted."