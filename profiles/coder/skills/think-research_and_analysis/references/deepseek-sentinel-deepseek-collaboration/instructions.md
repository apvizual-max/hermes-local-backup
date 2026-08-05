# Sub-Skill: deepseek-sentinel-deepseek-collaboration

* **Description:** 🟡 NEEDED SKILLS: When Popy mentions DeepSeek code, automatically pulls the latest draft from specified location and prepares an audit report using 963 filters.

---

10. Title: sentinel‑deepseek‑collaboration

Description: When Popy mentions DeepSeek code, automatically pulls the latest draft from specified location and prepares an audit report using 963 filters.

INSTRUCTION:

TRIGGER: Popy says "DeepSeek", "cod Pine", "draft trading" or mentions a .pine file.
1. LOCATE file path from context or ask: "Please specify the file path."
2. READ the Pine Script code.
3. RUN the 963‑proverb filter matrix on the code (look for risk, logic, timing, resource violations).
4. GENERATE audit report with:
   - violations (proverbs not satisfied)
   - suggestions for fixing
   - convergence score (0-100%)
5. OUTPUT report and ask: "Proceed to fix? (Mod A/Mod B)"