# Sub-Skill: deepseek-sentinel-proverb-resolver

* **Description:** 🟡 NEEDED SKILLS: When two proverbs appear contradictory, this skill resolves the conflict by identifying the contextual variable that aligns both. Outputs the unified logic.

---

1. Title: sentinel‑proverb‑resolver

Description: When two proverbs appear contradictory, this skill resolves the conflict by identifying the contextual variable that aligns both. Outputs the unified logic.

INSTRUCTION:

TRIGGER: Popy asks "rezolva conflictul" OR a decision triggers contradictory proverbs.
1. IDENTIFY contradictory pair (A and B).
2. EXTRACT core vectors: time, resource, risk, social, action.
3. SEARCH for a third proverb or principle that harmonises them (e.g., "Graba" vs "Devreme" → context of preparation).
4. FORMULATE synthesis: "A applies when [condition1], B applies when [condition2]. Together they require [unified rule]."
5. OUTPUT synthesis in sacred string format.
6. LOG resolution in BIBLIOTECA under "RESOLVED_CONFLICTS.md"