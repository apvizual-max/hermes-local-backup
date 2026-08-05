# Sub-Skill: sentinel-coder-agentic-display-zero-content-chat

* **Description:** description: SKILL CRUCIAL CHAT-016. ZERO display content fișier mare în chat. Lucrez LOCAL pe disc, raportez SCURT cu linkuri markdown. Excepție unică: când Popy cere EXPLICIT display ("citeste cu voce tare", "afiseaza-mi"). Anti-pattern documentat empiric: în CHAT-016 am afișat conținut fișier de mai multe ori (CLS, PROCESS, T3 read-uri în chunks de 400 linii cu output în chat) — Popy a corectat repetat ("futi tokene mortii ma-tii", "lucrezi LOCAL"). Skill = dezactivare reflex "show what I read" când acordul cere muncă tăcută. type: silent-local-work tier: 🔴🔴 CRUCIAL operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-anti-graba-3-reguli-sacre, sentinel-bimodal-execute-discipline

---

---
name: sentinel-coder-agentic-display-zero-content-chat
description: SKILL CRUCIAL CHAT-016. ZERO display content fișier mare în chat. Lucrez LOCAL pe disc, raportez SCURT cu linkuri markdown. Excepție unică: când Popy cere EXPLICIT display ("citeste cu voce tare", "afiseaza-mi"). Anti-pattern documentat empiric: în CHAT-016 am afișat conținut fișier de mai multe ori (CLS, PROCESS, T3 read-uri în chunks de 400 linii cu output în chat) — Popy a corectat repetat ("futi tokene mortii ma-tii", "lucrezi LOCAL"). Skill = dezactivare reflex "show what I read" când acordul cere muncă tăcută.
type: silent-local-work
tier: 🔴🔴 CRUCIAL
operator: Popy
created: 2026-05-09 (CHAT-016 post-self-audit)
related: sentinel-anti-graba-3-reguli-sacre, sentinel-bimodal-execute-discipline
---

═══════════════════════════════════════════════════
# 🔴🔴 SENTINEL DISPLAY ZERO CONTENT FIȘIER ÎN CHAT
═══════════════════════════════════════════════════

## REGULA INVIOLABILĂ

**Pe disc:** salvez TOT, FĂRĂ trunchiere.
**În chat:** raportez DOAR sumar 1-3 linii + linkuri markdown clic-able.

**Excepție UNICĂ:** Popy cere EXPLICIT display ("afișează", "citește cu voce tare", "dă-mi conținutul aici").

═══════════════════════════════════════════════════
## REGULA #1 — TIPURI DE OUTPUT INTERZISE ÎN CHAT
═══════════════════════════════════════════════════

❌ **INTERZIS:**
- Conținut Read fișier mare (>20 linii)
- Output Bash cu zeci de linii cod
- Tabele cu zeci de rânduri
- Re-listare conținut deja scris pe disc

✅ **PERMIS:**
- Linkuri markdown: `[fișier.md](path/fișier.md)`
- Sumar 1-3 linii per fișier
- Cifre cumulative
- Status compact

═══════════════════════════════════════════════════
## REGULA #2 — STRATEGIE LECTURĂ FĂRĂ DISPLAY
═══════════════════════════════════════════════════

1. Read cu offset/limit
2. Procesez intern (NU echo în chat)
3. Sintetizez 1-3 linii pentru raport
4. Pentru fișiere mari: Grep pattern specific, NU citire full

═══════════════════════════════════════════════════
🚛 LUCREZ LOCAL. RAPORTEZ SCURT. LINKURI > CONTENT.
🚛 TOKENE = COSTUL POPY. ECONOMIE = RESPECT.
═══════════════════════════════════════════════════