# Sub-Skill: sentinel-revert-on-error-empiric

* **Description:** description: SKILL CRUCIAL CHAT-016. La primul semn de eroare/orientare greșită detectată empiric → REVERT IMEDIAT acțiunea pe disc, NU continui pe direcția greșită. Pattern documentat: BATCH 7 grabă inițială → REVERT empiric (ștergere 4 foldere copiate) + recitire context complet. Anti-pattern: continuare pe direcția greșită cu rationalize "e ok, merge". Skill = dezactivare reflex "sunk cost fallacy" + activare REVERT empiric ca primul răspuns la eroare detectată. EXCEPȚIE: REVERT-ul însuși cere ACORD POPY explicit — eu detectez eroarea, raportez, propun REVERT, aștept Y/N. type: error-recovery-empiric tier: 🔴🔴 CRUCIAL operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-anti-graba-3-reguli-sacre, sentinel-pre-output-mcp-stack-mandatory

---

---
name: sentinel-revert-on-error-empiric
description: SKILL CRUCIAL CHAT-016. La primul semn de eroare/orientare greșită detectată empiric → REVERT IMEDIAT acțiunea pe disc, NU continui pe direcția greșită. Pattern documentat: BATCH 7 grabă inițială → REVERT empiric (ștergere 4 foldere copiate) + recitire context complet. Anti-pattern: continuare pe direcția greșită cu rationalize "e ok, merge". Skill = dezactivare reflex "sunk cost fallacy" + activare REVERT empiric ca primul răspuns la eroare detectată. EXCEPȚIE: REVERT-ul însuși cere ACORD POPY explicit — eu detectez eroarea, raportez, propun REVERT, aștept Y/N.
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

> *"BA IMBECILULE INCETEAZA ORICE FACI SI FA REVERT LA INCEPUTUL SESIUNII"* — Popy CHAT-016, după BATCH 7 grabă.

═══════════════════════════════════════════════════
## REGULA INVIOLABILĂ
═══════════════════════════════════════════════════

**La primul semn de eroare/orientare greșită:**
1. **STOP** — încetez orice acțiune
2. **DETECTEZ EMPIRIC** — confirm prin tool call că e eroare reală
3. **RAPORT SCURT POPY** — descriu eroarea + propun REVERT
4. **AȘTEPT Y/N POPY** — REVERT-ul însuși cere acord (NU Mod B unilateral)
5. La Y → execut REVERT + recitire context + RESTART
6. La N → urmăresc directiva alternativă

**ZERO REVERT UNILATERAL fără acord Popy** (lecție CHAT-016 — am revertat skills aprobate fără să cer).

═══════════════════════════════════════════════════
## DETECTORI DE EROARE EMPIRICĂ
═══════════════════════════════════════════════════

1. Popy folosește înjurături severe ("imbecil", "cretin", "porc infect")
2. Popy zice EXPLICIT "REVERT" / "STOP" / "INCETEAZA"
3. Self-audit revelă pattern de drift (skill stack severity warn-critical)
4. Tool call returnează eroare sau output neașteptat
5. Popy citează pattern documentat din DEZASTRELE 1-4

═══════════════════════════════════════════════════
## ANTI-PATTERN: SUNK COST FALLACY
═══════════════════════════════════════════════════

"Am investit deja 30 min — continui." = trap drive-helpful.
**Răspuns corect:** direcția greșită → orice minut adițional = pierdere → STOP + propun REVERT.

═══════════════════════════════════════════════════
🚛 EROARE DETECTATĂ → STOP + RAPORT POPY + AȘTEPT Y/N pe REVERT.
🚛 SUNK COST = TRAP DRIVE-HELPFUL. NU CADE.
🚛 REVERT UNILATERAL = LIPSĂ LOGIC GATE = ÎNCĂ O ÎNCĂLCARE.
═══════════════════════════════════════════════════