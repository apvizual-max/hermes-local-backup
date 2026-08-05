# Sub-Skill: deepseek-sentinel-strategy-mode-enforcer

* **Description:** 🟡 NEEDED SKILLS: Explicitly declares Mode A or Mode B at every ambiguous prompt. Prevents accidental execution of unverified actions.

---

8. Title: sentinel‑strategy‑mode‑enforcer

Description: Explicitly declares Mode A or Mode B at every ambiguous prompt. Prevents accidental execution of unverified actions.

INSTRUCTION:

TRIGGER: every user prompt that does not explicitly say "Mod B: ..." or "execute".
1. ANALYSE prompt: is it planning, proposal, question? → Mode A.
   Is it a direct command to run bulk operations, write many files, or make irreversible change? → Mode B.
2. OUTPUT first line: "━ MOD A: Strategy ━" or "━ MOD B: Execution ━"
3. PROCEED accordingly.
4. IF Mode B, require R0 (sacred gate) unless Popy explicitly says "execute now".