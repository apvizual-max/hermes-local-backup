# Sub-Skill: sentinel-trading-edge-validation

* **Description:** Skill specific pentru audit Pine Script v6 / DeepSeek workflow. Aplicat cand Popy aduce strategie/cod nou. Filtru: SACRU (skin in the game live) vs PROFAN (backtest doar, indicator estetic). Output: raport edge real vs iluzie. Activ la ETAPA 5 (dupa ce ETAPA 1-4 finalizate).

---

═══════════════════════════════════════════════════
## 🆕 SECTIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecata proprie)
═══════════════════════════════════════════════════
 
Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lectia lui Popy din CHAT-010 prompt 4.
 
**Status:** PROPUNERI — necesita creare disc + paste UI dupa validare.
**Filtrare aplicata:** doar SACRU pastrat. PROFAN in Sectiunea E.
 
───────────────────────────────────────────────────
### D.5 — sentinel-trading-edge-validation (PENTRU ETAPA 5)
───────────────────────────────────────────────────
 
**NUME:** `sentinel-trading-edge-validation`
 
**DESCRIERE:**
Skill specific pentru audit Pine Script v6 / DeepSeek workflow. Aplicat cand Popy aduce strategie/cod nou. Filtru: SACRU (skin in the game live) vs PROFAN (backtest doar, indicator estetic). Output: raport edge real vs iluzie. Activ la ETAPA 5 (dupa ce ETAPA 1-4 finalizate).
 
**CONTINUT:**
```
PIPELINE VALIDARE:
 
INPUT: cod Pine Script v6 (de la DeepSeek sau Popy)
 
FILTRU 1 — SACRU/PROFAN (Eliade):
- Are skin in the game? (live trading, NU doar backtest)
- A supravietuit drawdown real?
- A produs profit consistent cu R/R definit?
 
FILTRU 2 — HIEROPHANY pe nivele:
- Suport/rezistenta validate de 3+ confluente + volum?
- Pattern care se repeta cu aceleasi consecinte?
 
FILTRU 3 — STOICISM (Marcus Aurelius):
- Strategia ASUMA drawdown sau spera sa-l evite (iluzie)?
- Risk management e absolut sau conditionat?
 
FILTRU 4 — MUSASHI:
- Cate indicatori? (>3 = probabil zgomot)
- Logica simpla sau over-engineered?
 
FILTRU 5 — SUN TZU:
- Inamic intern: nevoie sa "castig piata" sau acceptarea pierderii ca cost?
- Strategia exploateaza slabiciune adversar (other traders) sau e pura speranta?
 
OUTPUT: raport edge cu scor SACRU 0-10 + recomandare LIVE / STORE / REJECT
 
DEPENDENTE EXTERNE:
- TradingView Strategy Tester real (NU inventie)
- Frati conectati pentru audit cross-instance (ETAPA 2 prerequisite)
```
 
**PROMPT_SETARE:**
```
NAME: sentinel-trading-edge-validation
DESCRIPTION: [copy]
CONTENT: [copy]
PREREQUISITE: ETAPA 1-4 finalizate (fratii conectati + audit complet sistem)
ACTIVARE: ETAPA 5 (TBD)
```