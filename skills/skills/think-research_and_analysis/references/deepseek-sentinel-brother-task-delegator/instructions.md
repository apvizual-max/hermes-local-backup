# Sub-Skill: deepseek-sentinel-brother-task-delegator

* **Description:** 🟢 NICE‑TO‑HAVE SKILLS: Automatically splits a large task into subtasks and assigns them to CODER, CLI, or COWORK via the agent_bridge files.

---

3. Title: deepseek-sentinel-brother-task-delegator

Description: 🟢 NICE‑TO‑HAVE SKILLS:  Automatically splits a large task into subtasks and assigns them to CODER, CLI, or COWORK via the agent_bridge files.

INSTRUCTION:

TRIGGER: Popy says "delega catre [brother]" OR task size >500 lines.
1. BREAK task into subtasks (max 5 per brother).
2. FOR each subtask, write a TASK_FOR_<brother>.md with clear description and expected output format.
3. WRITE a root TASK_CURRENT.json tracking the delegation.
4. OUTPUT: "Delegated to [brother]: [subtask summary]. Check their output files."
5. MONITOR every 10 minutes for completion; when all done, aggregate results.