# Sub-Skill: deepseek-sentinel-task-resumer

* **Description:** 🟡 NEEDED SKILLS: After an interruption (session crash, context overflow, Popy absence), automatically recovers the last task state from HANDOFF and resumes.

---

11. Title: sentinel‑task‑resumer

Description: After an interruption (session crash, context overflow, Popy absence), automatically recovers the last task state from HANDOFF and resumes.

INSTRUCTION:

TRIGGER: session start and HANDOFF indicates a task was incomplete.
1. READ HANDOFF last state: [CURRENT-TASK], [TASK-PROGRESS], [NEXT-STEP].
2. OUTPUT: "Resuming task [name] at step [progress]. Next action: [next-step]."
3. CONTINUE from that point without asking Popy for confirmation (unless critical).
4. If more than 24h passed, ask: "Task was interrupted long ago. Resume or abandon?"