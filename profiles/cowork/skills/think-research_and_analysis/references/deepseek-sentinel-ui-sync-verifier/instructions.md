# Sub-Skill: deepseek-sentinel-ui-sync-verifier

* **Description:** 🟡 NEEDED SKILLS: Compares local skill files and user preferences with what is actually set in the Anthropic UI. Reports mismatches and generates paste‑ready diffs.

---

3. Title: sentinel‑ui‑sync‑verifier

Description: Compares local skill files and user preferences with what is actually set in the Anthropic UI. Reports mismatches and generates paste‑ready diffs.

INSTRUCTION:

TRIGGER: at session start (weekly) OR when Popy says "verifica UI".
1. READ local state: SENTINEL_SETARI_UI/INDEX.md, skills_drafts/*.md, USER_PREFERENCES_ADDENDUM.md
2. COMPARE with expected UI configuration (from last known good state).
3. IDENTIFY discrepancies:
   - skills missing in UI but present on disk
   - skills in UI but not on disk (orphans)
   - user preferences outdated
4. GENERATE patch report: UI_SYNC_NEEDED.md with copy‑paste instructions for Popy.
5. OUTPUT: "UI sync needed: [N] mismatches."