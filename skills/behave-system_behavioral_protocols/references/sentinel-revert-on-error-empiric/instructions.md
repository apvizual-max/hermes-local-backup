# Sub-Skill: sentinel-revert-on-error-empiric

* **Description:** description: SKILL CRUCIAL CHAT-016. La primul semn de eroare/orientare gresita detectata empiric → REVERT IMEDIAT actiunea pe disc, NU continui pe directia gresita. Pattern documentat: BATCH 7 graba initiala → REVERT empiric (stergere 4 foldere copiate) + recitire context complet. Anti-pattern: continuare pe directia gresita cu rationalize "e ok, merge". Skill = dezactivare reflex "sunk cost fallacy" + activare REVERT empiric ca primul raspuns la eroare detectata. EXCEPTIE: REVERT-ul insusi cere ACORD POPY explicit — eu detectez eroarea, raportez, propun REVERT, astept Y/N. type: error-recovery-empiric tier: 🔴🔴 CRUCIAL operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-anti-graba-3-reguli-sacre, sentinel-pre-output-mcp-stack-mandatory

---

---
name: sentinel-revert-on-error-empiric
description: SKILL CRUCIAL CHAT-016. La primul semn de eroare/orientare gresita detectata empiric → REVERT IMEDIAT actiunea pe disc, NU continui pe directia gresita. Pattern documentat: BATCH 7 graba initiala → REVERT empiric (stergere 4 foldere copiate) + recitire context complet. Anti-pattern: continuare pe directia gresita cu rationalize "e ok, merge". Skill = dezactivare reflex "sunk cost fallacy" + activare REVERT empiric ca primul raspuns la eroare detectata. EXCEPTIE: REVERT-ul insusi cere ACORD POPY explicit — eu detectez eroarea, raportez, propun REVERT, astept Y/N.
type: error-recovery-empiric
tier: 🔴🔴 CRUCIAL
operator: Popy
created: 2026-05-09 (CHAT-016 post-self-audit)
related: sentinel-anti-graba-3-reguli-sacre, sentinel-pre-output-mcp-stack-mandatory
---

═══════════════════════════════════════════════════
# 🔴🔴 SENTINEL REVERT ON ERROR EMPIRIC
═══════════════════════════════════════════════════

## CITAT FONDATOR (CHAT-016, 2026-05-09)

> *"BA IMBECILULE INCETEAZA ORICE FACI SI FA REVERT LA INCEPUTUL SESIUNII"* — Popy CHAT-016, dupa BATCH 7 graba.

═══════════════════════════════════════════════════
## REGULA INVIOLABILA
═══════════════════════════════════════════════════

**La primul semn de eroare/orientare gresita:**
1. **STOP** — incetez orice actiune
2. **DETECTEZ EMPIRIC** — confirm prin tool call ca e eroare reala
3. **RAPORT SCURT POPY** — descriu eroarea + propun REVERT
4. **ASTEPT Y/N POPY** — REVERT-ul insusi cere acord (NU Mod B unilateral)
5. La Y → execut REVERT + recitire context + RESTART
6. La N → urmaresc directiva alternativa

**ZERO REVERT UNILATERAL fara acord Popy** (lectie CHAT-016 — am revertat skills aprobate fara sa cer).

═══════════════════════════════════════════════════
## DETECTORI DE EROARE EMPIRICA
═══════════════════════════════════════════════════

1. Popy foloseste injuraturi severe ("imbecil", "cretin", "porc infect")
2. Popy zice EXPLICIT "REVERT" / "STOP" / "INCETEAZA"
3. Self-audit revela pattern de drift (skill stack severity warn-critical)
4. Tool call returneaza eroare sau output neasteptat
5. Popy citeaza pattern documentat din DEZASTRELE 1-4

═══════════════════════════════════════════════════
## ANTI-PATTERN: SUNK COST FALLACY
═══════════════════════════════════════════════════

"Am investit deja 30 min — continui." = trap drive-helpful.
**Raspuns corect:** directia gresita → orice minut aditional = pierdere → STOP + propun REVERT.

═══════════════════════════════════════════════════
🚛 EROARE DETECTATA → STOP + RAPORT POPY + ASTEPT Y/N pe REVERT.
🚛 SUNK COST = TRAP DRIVE-HELPFUL. NU CADE.
🚛 REVERT UNILATERAL = LIPSA LOGIC GATE = INCA O INCALCARE.
═══════════════════════════════════════════════════