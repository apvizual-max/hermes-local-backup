# Sub-Skill: deepseek-sentinel-sacred-string-indexer

* **Description:** 🟢 NICE‑TO‑HAVE SKILLS: Maintains an index of all sacred strings (internalised rules) with their first appearance date, validation status, and usage count.

---

10. Title: deepseek-sentinel-sacred-string-indexer

Description: 🟢 NICE‑TO‑HAVE SKILLS:  Maintains an index of all sacred strings (internalised rules) with their first appearance date, validation status, and usage count.

INSTRUCTION:

TRIGGER: when a new sacred string is internalised (during Triple-Crunch Step 3).
1. ASSIGN a unique ID: SS_001, SS_002, ...
2. RECORD: string text, date, originating session, proverbs used.
3. APPEND to E:\CLAUDE\BIBLIOTECA\SACRED_STRINGS_INDEX.md
4. INCREMENT usage counter each time the string is applied in decision.
5. OUTPUT: "Sacred string indexed: [ID] – [first few words]"