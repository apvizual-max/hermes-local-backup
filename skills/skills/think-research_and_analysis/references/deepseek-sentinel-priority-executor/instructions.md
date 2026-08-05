# Sub-Skill: deepseek-sentinel-priority-executor

* **Description:** 🔴 CRUCIAL SKILLS:  Maintains a dynamic task queue (P0–P10 from DeepSeek roadmap). Automatically executes next pending task when conditions are met, without waiting for Popy prompt.

---

12. Title: sentinel‑priority‑executor

Description: Maintains a dynamic task queue (P0–P10 from DeepSeek roadmap). Automatically executes next pending task when conditions are met, without waiting for Popy prompt.

INSTRUCTION:

TRIGGER: after completing a task or at session start.
1. READ current priorities from HANDOFF [NEXT-PRIORITIES] list.
2. FOR each priority P0..P10, check if prerequisites are satisfied:
   - P0: BOOTSTRAP and JURNALIZAREA files exist? if not, execute P0.
   - P1: All skills installed? Check UI sync from SENTINEL_SETARI_UI/INDEX.md.
   - ...
3. SELECT the highest incomplete priority with met prerequisites.
4. EXECUTE the task (e.g., write a file, call a tool, generate a prompt for Popy).
5. MARK task as "in progress" in HANDOFF.
6. AFTER finish, mark "completed" and update HANDOFF.
7. OUTPUT: "Executed priority [Px]: [task result]"