# Sub-Skill: sentinel-context-budget-monitor

* **Description:** Skill pasiv de monitorizare consum context. La fiecare prompt, estimez headroom rămas (token budget). Trigger praguri: 70% = warning, 85% = preluare REFLEX T4 preventiv (compresare context), 95% = forced RITUAL_IESIRE. Aplicat lecția GROK despre context overload — DAR fără fragmentare BOOTSTRAP_PROTOCOL.

---

═══════════════════════════════════════════════════
## 🆕 SECȚIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecată proprie)
═══════════════════════════════════════════════════
 
Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lecția lui Popy din CHAT-010 prompt 4.
 
**Status:** PROPUNERI — necesită creare disc + paste UI după validare.
**Filtrare aplicată:** doar SACRU păstrat. PROFAN în Secțiunea E.
 
───────────────────────────────────────────────────
### D.6 — sentinel-context-budget-monitor
───────────────────────────────────────────────────
 
**NUME:** `sentinel-context-budget-monitor`
 
**DESCRIERE:**
Skill pasiv de monitorizare consum context. La fiecare prompt, estimez headroom rămas (token budget). Trigger praguri: 70% = warning, 85% = preluare REFLEX T4 preventiv (compresare context), 95% = forced RITUAL_IESIRE. Aplicat lecția GROK despre context overload — DAR fără fragmentare BOOTSTRAP_PROTOCOL.
 
**CONȚINUT:**
```
PRAGURI MONITORIZARE:
- 0-69%: operare normală
- 70-84%: WARNING (raportat în ticker: "CTX:75%")
- 85-94%: REFLEX T4 PREVENTIV (Popy notificat — propun summary + handoff parțial)
- 95%+: FORCED RITUAL_IESIRE (salvez ce am, închid sesiunea ordonat)
 
ESTIMARE HEADROOM:
- Bootstrap normal R-2: ~5-10% (4 tool calls)
- Citire CENTRALIZATOR_vC.1 integral: ~15-20%
- Citire GROK lecție integrală (3953 linii): ~15%
- BAGAJ FAZA 3.4 răspuns: ~5%
- Conversație tipică prompt-replică: ~2-3% per cycle
 
TRIGGER REFLEX T4:
- Append fișă reflex_archive\T4_preventiv\CHAT-XXX_TIMESTAMP.md
- Conține: stare curentă + ce-am încheiat + ce rămâne pentru continuare în CHAT următoare
```
 
**PROMPT_SETARE:**
```
NAME: sentinel-context-budget-monitor
DESCRIPTION: [copy]
CONTENT: [copy]
INTEGRARE: ticker la fiecare răspuns include CTX:X% când >70%
```