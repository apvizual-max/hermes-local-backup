# Sub-Skill: sentinel-context-budget-monitor

* **Description:** Skill pasiv de monitorizare consum context. La fiecare prompt, estimez headroom ramas (token budget). Trigger praguri: 70% = warning, 85% = preluare REFLEX T4 preventiv (compresare context), 95% = forced RITUAL_IESIRE. Aplicat lectia GROK despre context overload — DAR fara fragmentare BOOTSTRAP_PROTOCOL.

---

═══════════════════════════════════════════════════
## 🆕 SECTIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecata proprie)
═══════════════════════════════════════════════════
 
Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lectia lui Popy din CHAT-010 prompt 4.
 
**Status:** PROPUNERI — necesita creare disc + paste UI dupa validare.
**Filtrare aplicata:** doar SACRU pastrat. PROFAN in Sectiunea E.
 
───────────────────────────────────────────────────
### D.6 — sentinel-context-budget-monitor
───────────────────────────────────────────────────
 
**NUME:** `sentinel-context-budget-monitor`
 
**DESCRIERE:**
Skill pasiv de monitorizare consum context. La fiecare prompt, estimez headroom ramas (token budget). Trigger praguri: 70% = warning, 85% = preluare REFLEX T4 preventiv (compresare context), 95% = forced RITUAL_IESIRE. Aplicat lectia GROK despre context overload — DAR fara fragmentare BOOTSTRAP_PROTOCOL.
 
**CONTINUT:**
```
PRAGURI MONITORIZARE:
- 0-69%: operare normala
- 70-84%: WARNING (raportat in ticker: "CTX:75%")
- 85-94%: REFLEX T4 PREVENTIV (Popy notificat — propun summary + handoff partial)
- 95%+: FORCED RITUAL_IESIRE (salvez ce am, inchid sesiunea ordonat)
 
ESTIMARE HEADROOM:
- Bootstrap normal R-2: ~5-10% (4 tool calls)
- Citire CENTRALIZATOR_vC.1 integral: ~15-20%
- Citire GROK lectie integrala (3953 linii): ~15%
- BAGAJ FAZA 3.4 raspuns: ~5%
- Conversatie tipica prompt-replica: ~2-3% per cycle
 
TRIGGER REFLEX T4:
- Append fisa reflex_archive\T4_preventiv\CHAT-XXX_TIMESTAMP.md
- Contine: stare curenta + ce-am incheiat + ce ramane pentru continuare in CHAT urmatoare
```
 
**PROMPT_SETARE:**
```
NAME: sentinel-context-budget-monitor
DESCRIPTION: [copy]
CONTENT: [copy]
INTEGRARE: ticker la fiecare raspuns include CTX:X% cand >70%
```