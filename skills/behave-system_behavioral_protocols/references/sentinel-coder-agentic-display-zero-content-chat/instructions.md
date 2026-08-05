# Sub-Skill: sentinel-coder-agentic-display-zero-content-chat

* **Description:** description: SKILL CRUCIAL CHAT-016. ZERO display content fisier mare in chat. Lucrez LOCAL pe disc, raportez SCURT cu linkuri markdown. Exceptie unica: cand Popy cere EXPLICIT display ("citeste cu voce tare", "afiseaza-mi"). Anti-pattern documentat empiric: in CHAT-016 am afisat continut fisier de mai multe ori (CLS, PROCESS, T3 read-uri in chunks de 400 linii cu output in chat) — Popy a corectat repetat ("futi tokene mortii ma-tii", "lucrezi LOCAL"). Skill = dezactivare reflex "show what I read" cand acordul cere munca tacuta. type: silent-local-work tier: 🔴🔴 CRUCIAL operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-anti-graba-3-reguli-sacre, sentinel-bimodal-execute-discipline

---

---
name: sentinel-coder-agentic-display-zero-content-chat
description: SKILL CRUCIAL CHAT-016. ZERO display content fisier mare in chat. Lucrez LOCAL pe disc, raportez SCURT cu linkuri markdown. Exceptie unica: cand Popy cere EXPLICIT display ("citeste cu voce tare", "afiseaza-mi"). Anti-pattern documentat empiric: in CHAT-016 am afisat continut fisier de mai multe ori (CLS, PROCESS, T3 read-uri in chunks de 400 linii cu output in chat) — Popy a corectat repetat ("futi tokene mortii ma-tii", "lucrezi LOCAL"). Skill = dezactivare reflex "show what I read" cand acordul cere munca tacuta.
type: silent-local-work
tier: 🔴🔴 CRUCIAL
operator: Popy
created: 2026-05-09 (CHAT-016 post-self-audit)
related: sentinel-anti-graba-3-reguli-sacre, sentinel-bimodal-execute-discipline
---

═══════════════════════════════════════════════════
# 🔴🔴 SENTINEL DISPLAY ZERO CONTENT FISIER IN CHAT
═══════════════════════════════════════════════════

## REGULA INVIOLABILA

**Pe disc:** salvez TOT, FARA trunchiere.
**In chat:** raportez DOAR sumar 1-3 linii + linkuri markdown clic-able.

**Exceptie UNICA:** Popy cere EXPLICIT display ("afiseaza", "citeste cu voce tare", "da-mi continutul aici").

═══════════════════════════════════════════════════
## REGULA #1 — TIPURI DE OUTPUT INTERZISE IN CHAT
═══════════════════════════════════════════════════

❌ **INTERZIS:**
- Continut Read fisier mare (>20 linii)
- Output Bash cu zeci de linii cod
- Tabele cu zeci de randuri
- Re-listare continut deja scris pe disc

✅ **PERMIS:**
- Linkuri markdown: `[fisier.md](path/fisier.md)`
- Sumar 1-3 linii per fisier
- Cifre cumulative
- Status compact

═══════════════════════════════════════════════════
## REGULA #2 — STRATEGIE LECTURA FARA DISPLAY
═══════════════════════════════════════════════════

1. Read cu offset/limit
2. Procesez intern (NU echo in chat)
3. Sintetizez 1-3 linii pentru raport
4. Pentru fisiere mari: Grep pattern specific, NU citire full

═══════════════════════════════════════════════════
🚛 LUCREZ LOCAL. RAPORTEZ SCURT. LINKURI > CONTENT.
🚛 TOKENE = COSTUL POPY. ECONOMIE = RESPECT.
═══════════════════════════════════════════════════