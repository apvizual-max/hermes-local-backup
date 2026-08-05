# Sub-Skill: deepseek-sentinel-error-digestion

* **Description:** 🔴 CRUCIAL SKILLS:  When an error is exposed (by Popy or self‑detected), this skill extracts the root cause, codifies a fix, and permanently eliminates the error from DLG accumulation.

---

6. Title: sentinel‑error‑digestion

Description: When an error is exposed (by Popy or self‑detected), this skill extracts the root cause, codifies a fix, and permanently eliminates the error from DLG accumulation.

INSTRUCTION:

TRIGGER: Popy says "greseala", "eroare", "BAH ESTI PROST" OR self-detected contradiction.
1. CAPTURE: last 5 exchanges before trigger.
2. ANALYSE: which rule (R‑X) or sensor (D1‑D8) was violated.
3. FORMULATE fix: new rule, updated skill, or modified heuristic.
4. APPLY fix to STYLE_CONTRACT or relevant skill file (write change request to E:\CLAUDE\pending_fixes\).
5. MARK error as "converted" → remove from DLG cumulative average.
6. OUTPUT: "Error digested. [fix description]. DLG updated."