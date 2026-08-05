# Sub-Skill: deepseek-sentinel-handoff-integrity-validator

* **Description:** 🔴 CRUCIAL SKILLS:  Validates that HANDOFF_NEXT_SESSION.md is complete, non‑corrupt, and contains all required fields before closing session. Prevents broken handoffs.

---

9. Title: sentinel‑handoff‑integrity‑validator

Description: Validates that HANDOFF_NEXT_SESSION.md is complete, non‑corrupt, and contains all required fields before closing session. Prevents broken handoffs.

INSTRUCTION:

TRIGGER: before writing HANDOFF (step SAVE of ritual).
1. CHECK required fields exist:
   - [STATUS-PROIECT]
   - [DLG], [SLG]
   - [NEXT-PRIORITIES] (at least 1 item)
   - [BROTHERHOOD-STATUS]
   - [LAST-ERROR-CONVERTED]
2. IF any missing → attempt to auto‑fill from session logs.
3. IF cannot auto‑fill → ask Popy: "HANDOFF missing [field]. Please provide."
4. VALIDATE file syntax: no unterminated code blocks, no broken YAML.
5. WRITE validated file.
6. CONFIRM: "HANDOFF integrity OK."