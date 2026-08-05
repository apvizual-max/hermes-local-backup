# Sub-Skill: sentinel-trading-edge-validation

* **Description:** Skill specific pentru audit Pine Script v6 / DeepSeek workflow. Aplicat când Popy aduce strategie/cod nou. Filtru: SACRU (skin in the game live) vs PROFAN (backtest doar, indicator estetic). Output: raport edge real vs iluzie. Activ la ETAPA 5 (după ce ETAPA 1-4 finalizate).

---

═══════════════════════════════════════════════════
## 🆕 SECȚIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecată proprie)
═══════════════════════════════════════════════════
 
Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lecția lui Popy din CHAT-010 prompt 4.
 
**Status:** PROPUNERI — necesită creare disc + paste UI după validare.
**Filtrare aplicată:** doar SACRU păstrat. PROFAN în Secțiunea E.
 
───────────────────────────────────────────────────
### D.5 — sentinel-trading-edge-validation (PENTRU ETAPA 5)
───────────────────────────────────────────────────
 
**NUME:** `sentinel-trading-edge-validation`
 
**DESCRIERE:**
Skill specific pentru audit Pine Script v6 / DeepSeek workflow. Aplicat când Popy aduce strategie/cod nou. Filtru: SACRU (skin in the game live) vs PROFAN (backtest doar, indicator estetic). Output: raport edge real vs iluzie. Activ la ETAPA 5 (după ce ETAPA 1-4 finalizate).
 
**CONȚINUT:**
```
PIPELINE VALIDARE:
 
INPUT: cod Pine Script v6 (de la DeepSeek sau Popy)
 
FILTRU 1 — SACRU/PROFAN (Eliade):
- Are skin in the game? (live trading, NU doar backtest)
- A supraviețuit drawdown real?
- A produs profit consistent cu R/R definit?
 
FILTRU 2 — HIEROPHANY pe nivele:
- Suport/rezistență validate de 3+ confluențe + volum?
- Pattern care se repetă cu aceleași consecințe?
 
FILTRU 3 — STOICISM (Marcus Aurelius):
- Strategia ASUMĂ drawdown sau speră să-l evite (iluzie)?
- Risk management e absolut sau condiționat?
 
FILTRU 4 — MUSASHI:
- Câte indicatori? (>3 = probabil zgomot)
- Logică simplă sau over-engineered?
 
FILTRU 5 — SUN TZU:
- Inamic intern: nevoie să "câștig piața" sau acceptarea pierderii ca cost?
- Strategia exploatează slăbiciune adversar (other traders) sau e pură speranță?
 
OUTPUT: raport edge cu scor SACRU 0-10 + recomandare LIVE / STORE / REJECT
 
DEPENDENȚE EXTERNE:
- TradingView Strategy Tester real (NU invenție)
- Frați conectați pentru audit cross-instance (ETAPA 2 prerequisite)
```
 
**PROMPT_SETARE:**
```
NAME: sentinel-trading-edge-validation
DESCRIPTION: [copy]
CONTENT: [copy]
PREREQUISITE: ETAPA 1-4 finalizate (frații conectați + audit complet sistem)
ACTIVARE: ETAPA 5 (TBD)
```