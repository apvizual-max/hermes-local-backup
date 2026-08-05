# Sub-Skill: sentinel-skill-extraction-template

* **Description:** 💡 CRUCIAL OWN SKILLS:  Modelul general prin care SENTINEL extrage ORICE skill nou — în formă consistentă, programabilă în Claude App. Cere: nume snake-case + descriere (1-3 fraze, când activează) + conținut (Logic Tree concret) + prompt setare (cum se programează în UI). Output garantat compatibil cu format SKILLS din SENTINEL_SETARI_UI.

---

═══════════════════════════════════════════════════
## 🆕 SECȚIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecată proprie)
═══════════════════════════════════════════════════

Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lecția lui Popy din CHAT-010 prompt 4.

**Status:** PROPUNERI — necesită creare disc + paste UI după validare.
**Filtrare aplicată:** doar SACRU păstrat. PROFAN în Secțiunea E.

───────────────────────────────────────────────────
### D.2 — sentinel-skill-extraction-template (Modelul General)
───────────────────────────────────────────────────

**NUME:** `sentinel-skill-extraction-template`

**DESCRIERE:**
Modelul general prin care SENTINEL extrage ORICE skill nou — în formă consistentă, programabilă în Claude App. Cere: nume snake-case + descriere (1-3 fraze, când activează) + conținut (Logic Tree concret) + prompt setare (cum se programează în UI). Output garantat compatibil cu format SKILLS din SENTINEL_SETARI_UI.

**CONȚINUT:**
```
TEMPLATE OBLIGATORIU:

═══════════════════════════════════════════════════
### [NUMĂR ORDINE] — [nume-skill-snake-case]
═══════════════════════════════════════════════════

**NUME:** `nume-skill-exact`

**DESCRIERE (UI field — max 1024 caractere):**
[1-3 fraze. Răspunde la: CE FACE, CÂND ACTIVEAZĂ, DE CE EXISTĂ.]

**CONȚINUT (UI field — corpul skill-ului):**
[Logic Tree concret în pași numerotați. Pseudocod sau cod efectiv. SAU: principii cu trigger + acțiune + output.]

**PROMPT_SETARE:**
[Cum se instalează în Claude App:
- LOCAȚIE UI: exact path
- ACȚIUNE: pași concreti
- DEPENDENȚE: ce alt skill / regulă / detector trebuie ANTERIOR
- INTEGRARE: unde se invocă în sistem (rituali, R-X, alt skill)
- SOURCE_OF_TRUTH: path disc absolut]

REGULI INTERNE TEMPLATE:
1. Nume MAX 50 caractere snake-case (ex: sentinel-x-y-z)
2. Descriere MAX 1024 caractere (limită UI Anthropic)
3. Conținut neambiguu — pseudocod > proză
4. Prompt setare TRASABIL pe disc (path absolut E:\CLAUDE\)
5. Cross-reference obligatoriu cu R-X / D-Gxx / alt skill
```

**PROMPT_SETARE:**
```
NAME: sentinel-skill-extraction-template
DESCRIPTION: [copy]
CONTENT: [TEMPLATE complet]
UTILIZARE: la fiecare propunere skill nou (Secțiunea D append) folosesc EXACT acest template
```