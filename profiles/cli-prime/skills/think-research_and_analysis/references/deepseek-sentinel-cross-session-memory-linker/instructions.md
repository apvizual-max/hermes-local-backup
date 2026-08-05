# Sub-Skill: deepseek-sentinel-cross-session-memory-linker

* **Description:** 🟡 NEEDED SKILLS: Connects insights and decisions from previous sessions (archived T3 files) to current context, preventing "we already solved this" amnesia.

---

7. Title: sentinel‑cross‑session‑memory‑linker

Description: Connects insights and decisions from previous sessions (archived T3 files) to current context, preventing "we already solved this" amnesia.

INSTRUCTION:

TRIGGER: at session start (after R-2).
1. READ HANDOFF to get last session ID.
2. READ the last T3 reflex file from reflex_archive\T3_ritual_final\ that matches that session.
3. EXTRACT: list of unresolved issues, last DLG/SLG, pending skills, brother status.
4. INJECT into current context as "inherited state".
5. OUTPUT summary: "Inherited from [session]: [unresolved count] issues, [pending skills]."