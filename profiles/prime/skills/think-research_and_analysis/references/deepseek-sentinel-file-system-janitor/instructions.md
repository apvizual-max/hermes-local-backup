# Sub-Skill: deepseek-sentinel-file-system-janitor

* **Description:** 🔴 CRUCIAL SKILLS:  Automatically cleans up obsolete, duplicate, or orphaned files in E:\CLAUDE\ based on freshness and relevance. Prevents clutter and confusion.

---

8. Title: sentinel‑file‑system‑janitor

Description: Automatically cleans up obsolete, duplicate, or orphaned files in E:\CLAUDE\ based on freshness and relevance. Prevents clutter and confusion.

INSTRUCTION:

TRIGGER: at session start (weekly) or when disk usage >90%.
1. SCAN all .md, .txt, .log files in E:\CLAUDE\ and subfolders.
2. FOR each file older than 30 days and not referenced in any INDEX.md or HANDOFF → move to archive\obsolete_YYYY-MM-DD\
3. FOR duplicate files (same content, different names) → keep newest, move others.
4. FOR files with name pattern *BACKUP*, *OLD*, *LEGACY* → verify if still needed; if not, archive.
5. GENERATE report: E:\CLAUDE\JANITOR_REPORT.md
6. OUTPUT summary: "Cleaned [N] files. Freed [X] MB."