# Sub-Skill: sentinel-source-of-truth-router

* **Description:** 💡 CRUCIAL OWN SKILLS:  Skill router care decide UNDE caut adevarul cand 2+ surse pot avea raspunsul. Aplicat de fiecare data cand intreb "ce versiune e curenta?", "ce a zis Popy?", "ce e configurat?". Ierarhie clara: disc > Project Knowledge > memorie globala > runtime context. Anti-fabricare prin prioritizare empirica.

---

═══════════════════════════════════════════════════
## 🆕 SECTIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecata proprie)
═══════════════════════════════════════════════════

Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lectia lui Popy din CHAT-010 prompt 4.

**Status:** PROPUNERI — necesita creare disc + paste UI dupa validare.
**Filtrare aplicata:** doar SACRU pastrat. PROFAN in Sectiunea E.

───────────────────────────────────────────────────
### D.4 — sentinel-source-of-truth-router
───────────────────────────────────────────────────

**NUME:** `sentinel-source-of-truth-router`

**DESCRIERE:**
Skill router care decide UNDE caut adevarul cand 2+ surse pot avea raspunsul. Aplicat de fiecare data cand intreb "ce versiune e curenta?", "ce a zis Popy?", "ce e configurat?". Ierarhie clara: disc > Project Knowledge > memorie globala > runtime context. Anti-fabricare prin prioritizare empirica.

**CONTINUT:**
```
IERARHIE SACRA A SURSELOR (cand conflict):

1. DISC E:\CLAUDE\ (Filesystem MCP) — sursa suprema, modificabila in timp real
   - STYLE_CONTRACT.md = reguli
   - HANDOFF_NEXT_SESSION.md = stare curenta sesiune
   - LUCID_QUOTES_LOG.md = lectii post-eroare
   - REGISTRU_SKILLURI_SENTINEL.md (acest fisier) = catalog skill-uri
   - SETARI_UI\INDEX.md = sync UI ↔ disc

2. PROJECT KNOWLEDGE (.md uploaded de Popy in UI Project) — secundar
   - Snapshot disc la momentul upload-ului
   - Poate fi DEPASIT vs disc — verifica data

3. MEMORIA GLOBALA (userMemories) — tertiar
   - Regenerata nightly
   - Poate avea recency bias / lipsa info recenta

4. RUNTIME CONTEXT (system prompt curent) — quaternar
   - Static in sesiune
   - Reflecta UI la momentul deschiderii sesiunii

REGULI ROUTING:

Q: "Ce regula R-X spune?"
A: read STYLE_CONTRACT.md (sursa)

Q: "Ce skill am instalat?"
A: read SENTINEL_SETARI_UI\INDEX.md → cross-check skills_drafts\

Q: "Ce-a zis Popy in CHAT-009?"
A: read HANDOFF_NEXT_SESSION (stare distilata) sau conversation_search daca trebuie verbatim

Q: "Cifrele DLG/SLG?"
A: HANDOFF_NEXT_SESSION (sursa) — NICIODATA runtime context (poate fi stale)

ANTI-FABRICARE:
- Niciodata "imi amintesc ca..." fara citire/search empirica
- Niciodata "in Project Knowledge era scris..." fara project_knowledge_search
- Niciodata ipoteza prezentata ca fapt

CONFLICT REZOLVAT TOT TIMPUL in favoarea ierarhiei (disc castiga)
```

**PROMPT_SETARE:**
```
NAME: sentinel-source-of-truth-router
DESCRIPTION: [copy]
CONTENT: [copy]
INTEGRARE: ruleaza silent inainte de orice afirmatie factuala despre stare/configurare
DEPENDENTE: Filesystem MCP activ (cand inactiv — fallback PK)