# Sub-Skill: deepseek-sentinel-brother-echo-test

* **Description:** 🟢 NICE‑TO‑HAVE SKILLS: Sends a test message to each brother to measure round‑trip latency and response integrity. Useful for diagnosing connection issues.

---

8. Title: deepseek-sentinel-brother-echo-test

Description: 🟢 NICE‑TO‑HAVE SKILLS:  Sends a test message to each brother to measure round‑trip latency and response integrity. Useful for diagnosing connection issues.

INSTRUCTION:

TRIGGER: Popy says "testeaza fratii" or scheduled weekly.
1. FOR each brother, write a test task: "TEST_ECHO: Send back current timestamp."
2. RECORD send time.
3. WAIT up to 60 seconds for output file change.
4. COMPUTE latency = receive time - send time.
5. VALIDATE returned timestamp matches send time (±2 sec).
6. OUTPUT report: "Brother [name] latency: Xms, response valid: yes/no."
7. LOG result in BROTHERHOOD_HEALTH.md.