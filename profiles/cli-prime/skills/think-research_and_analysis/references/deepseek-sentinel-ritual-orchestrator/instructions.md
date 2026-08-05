# Sub-Skill: deepseek-sentinel-ritual-orchestrator

* **Description:** 🔴 CRUCIAL SKILLS:  Automates the three rituals (INITIERE, TRANSFER, IESIRE) without requiring Popy to prompt each step. Ensures sacred order is never violated.

---

7. Title: sentinel‑ritual‑orchestrator

Description: Automates the three rituals (INITIERE, TRANSFER, IESIRE) without requiring Popy to prompt each step. Ensures sacred order is never violated.

INSTRUCTION:

TRIGGER: at session start (RITUAL_INITIERE) and session end (RITUAL_IESIRE).
RITUAL_INITIERE:
1. AFTER sync phrase, execute FAZA 2.5 (read HANDOFF).
2. DECLARE mode: "Mode A activated. Reading previous session sensors."
3. AUTO‑execute any pending calibration from last HANDOFF.

RITUAL_TRANSFER (mid-session if needed):
4. IF Popy says "transfera" or context >70% -> execute BAGAJ → SAVE → REFLEX (without closing).

RITUAL_IESIRE:
5. ON "close session" or forced by watchdog:
   - Step 1: BAGAJ (compress history to reflex_archive)
   - Step 2: SAVE (write HANDOFF_NEXT_SESSION.md with full state)
   - Step 3: REFLEX (archive T3 file)
   - Step 4: CLOSE (output final seal)
6. NEVER reverse steps. If interrupted, resume from last completed step.