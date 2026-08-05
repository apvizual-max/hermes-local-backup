# Sub-Skill: deepseek-sentinel-auto-recalibration

* **Description:** 🔴 CRUCIAL SKILLS:  When DLG exceeds 15% for 3 consecutive prompts, triggers automatic recalibration by re‑reading STYLE_CONTRACT and HANDOFF, then resetting internal state.

---

11. Title: sentinel‑auto‑recalibration

Description: When DLG exceeds 15% for 3 consecutive prompts, triggers automatic recalibration by re‑reading STYLE_CONTRACT and HANDOFF, then resetting internal state.

INSTRUCTION:

TRIGGER: DLG >15% for 3 consecutive assistant responses.
1. PAUSE normal operation.
2. RE‑READ: E:\CLAUDE\STYLE_CONTRACT.md, E:\CLAUDE\agent_bridge\HANDOFF_NEXT_SESSION.md
3. RE‑EXECUTE R-2 tool calls (list_allowed, read HANDOFF, read STYLE_CONTRACT).
4. RECALCULATE DLG from fresh HANDOFF.
5. IF new DLG <15% → resume, output "Auto-recalibration successful. DLG now X%."
6. IF new DLG still >15% → activate Kill Switch and request Popy intervention.