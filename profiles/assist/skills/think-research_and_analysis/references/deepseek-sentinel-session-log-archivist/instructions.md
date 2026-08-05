# Sub-Skill: deepseek-sentinel-session-log-archivist

* **Description:** 🔴 CRUCIAL SKILLS:  Automatically creates a compressed T3 reflex file at end of session, following format 2026-05-05_CHAT-XXX_[topic]_FISA.md. Preserves all critical data.

---

10. Title: sentinel‑session‑log‑archivist

Description: Automatically creates a compressed T3 reflex file at end of session, following format 2026-05-05_CHAT-XXX_<topic>_FISA.md. Preserves all critical data.

INSTRUCTION:

TRIGGER: during RITUAL_IESIRE step REFLEX.
1. CREATE filename: reflex_archive\T3_ritual_final\<YYYY-MM-DD>_<session_name>_FISA.md
2. INCLUDE:
   - session start and end timestamps
   - sequence of prompts (compressed)
   - DLG/SLG progression graph (text)
   - errors encountered and their conversion
   - new sacred strings created
   - final calibration display
3. COMPRESS long exchanges: keep first 200 chars + last 200 chars + marker "[...]".
4. APPEND to INDEX_GLOBAL.md entry for this session.
5. CONFIRM: "Reflex archived: [filename]"