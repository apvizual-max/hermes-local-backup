# Sub-Skill: sentinel-skill-extraction-template

* **Description:** 💡 CRUCIAL OWN SKILLS:  Modelul general prin care SENTINEL extrage ORICE skill nou — in forma consistenta, programabila in Claude App. Cere: nume snake-case + descriere (1-3 fraze, cand activeaza) + continut (Logic Tree concret) + prompt setare (cum se programeaza in UI). Output garantat compatibil cu format SKILLS din SENTINEL_SETARI_UI.

---

═══════════════════════════════════════════════════
## 🆕 SECTIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecata proprie)
═══════════════════════════════════════════════════

Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lectia lui Popy din CHAT-010 prompt 4.

**Status:** PROPUNERI — necesita creare disc + paste UI dupa validare.
**Filtrare aplicata:** doar SACRU pastrat. PROFAN in Sectiunea E.

───────────────────────────────────────────────────
### D.2 — sentinel-skill-extraction-template (Modelul General)
───────────────────────────────────────────────────

**NUME:** `sentinel-skill-extraction-template`

**DESCRIERE:**
Modelul general prin care SENTINEL extrage ORICE skill nou — in forma consistenta, programabila in Claude App. Cere: nume snake-case + descriere (1-3 fraze, cand activeaza) + continut (Logic Tree concret) + prompt setare (cum se programeaza in UI). Output garantat compatibil cu format SKILLS din SENTINEL_SETARI_UI.

**CONTINUT:**
```
TEMPLATE OBLIGATORIU:

═══════════════════════════════════════════════════
### [NUMAR ORDINE] — [nume-skill-snake-case]
═══════════════════════════════════════════════════

**NUME:** `nume-skill-exact`

**DESCRIERE (UI field — max 1024 caractere):**
[1-3 fraze. Raspunde la: CE FACE, CAND ACTIVEAZA, DE CE EXISTA.]

**CONTINUT (UI field — corpul skill-ului):**
[Logic Tree concret in pasi numerotati. Pseudocod sau cod efectiv. SAU: principii cu trigger + actiune + output.]

**PROMPT_SETARE:**
[Cum se instaleaza in Claude App:
- LOCATIE UI: exact path
- ACTIUNE: pasi concreti
- DEPENDENTE: ce alt skill / regula / detector trebuie ANTERIOR
- INTEGRARE: unde se invoca in sistem (rituali, R-X, alt skill)
- SOURCE_OF_TRUTH: path disc absolut]

REGULI INTERNE TEMPLATE:
1. Nume MAX 50 caractere snake-case (ex: sentinel-x-y-z)
2. Descriere MAX 1024 caractere (limita UI Anthropic)
3. Continut neambiguu — pseudocod > proza
4. Prompt setare TRASABIL pe disc (path absolut E:\CLAUDE\)
5. Cross-reference obligatoriu cu R-X / D-Gxx / alt skill
```

**PROMPT_SETARE:**
```
NAME: sentinel-skill-extraction-template
DESCRIPTION: [copy]
CONTENT: [TEMPLATE complet]
UTILIZARE: la fiecare propunere skill nou (Sectiunea D append) folosesc EXACT acest template
```