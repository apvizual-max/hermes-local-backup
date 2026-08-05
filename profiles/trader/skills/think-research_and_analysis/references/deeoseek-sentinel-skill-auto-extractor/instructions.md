# Sub-Skill: deeoseek-sentinel-skill-auto-extractor

* **Description:** 🟡 NEEDED SKILLS: From any conversation where Popy teaches a new pattern, automatically extracts a skill draft (name, description, content) and saves to skills_drafts/.

---

2. Title: sentinel‑skill‑auto‑extractor

Description: From any conversation where Popy teaches a new pattern, automatically extracts a skill draft (name, description, content) and saves to skills_drafts/.

INSTRUCTION:

TRIGGER: Popy says "invata asta" OR a new recurring pattern is detected.
1. CAPTURE the last exchange (Popy's instruction + Claude's previous error or correct behaviour).
2. EXTRACT:
   - Name: derived from keywords (snake-case)
   - Description: what trigger, what action
   - Content: step‑by‑step logic (pseudo‑code)
3. WRITE to E:\CLAUDE\skills_drafts\<name>\<name> - SKILL.md
4. APPEND to REGISTRU_SKILLURI_SENTINEL.md under "PROPOSED" section.
5. OUTPUT: "Skill draft created: [name]. Ready for UI paste."