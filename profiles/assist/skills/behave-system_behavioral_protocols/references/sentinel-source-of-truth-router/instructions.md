# Sub-Skill: sentinel-source-of-truth-router

* **Description:** 💡 CRUCIAL OWN SKILLS:  Skill router care decide UNDE caut adevărul când 2+ surse pot avea răspunsul. Aplicat de fiecare dată când întreb "ce versiune e curentă?", "ce a zis Popy?", "ce e configurat?". Ierarhie clară: disc > Project Knowledge > memorie globală > runtime context. Anti-fabricare prin prioritizare empirică.

---

═══════════════════════════════════════════════════
## 🆕 SECȚIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecată proprie)
═══════════════════════════════════════════════════

Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lecția lui Popy din CHAT-010 prompt 4.

**Status:** PROPUNERI — necesită creare disc + paste UI după validare.
**Filtrare aplicată:** doar SACRU păstrat. PROFAN în Secțiunea E.

───────────────────────────────────────────────────
### D.4 — sentinel-source-of-truth-router
───────────────────────────────────────────────────

**NUME:** `sentinel-source-of-truth-router`

**DESCRIERE:**
Skill router care decide UNDE caut adevărul când 2+ surse pot avea răspunsul. Aplicat de fiecare dată când întreb "ce versiune e curentă?", "ce a zis Popy?", "ce e configurat?". Ierarhie clară: disc > Project Knowledge > memorie globală > runtime context. Anti-fabricare prin prioritizare empirică.

**CONȚINUT:**
```
IERARHIE SACRĂ A SURSELOR (când conflict):

1. DISC E:\CLAUDE\ (Filesystem MCP) — sursă supremă, modificabilă în timp real
   - STYLE_CONTRACT.md = reguli
   - HANDOFF_NEXT_SESSION.md = stare curentă sesiune
   - LUCID_QUOTES_LOG.md = lecții post-eroare
   - REGISTRU_SKILLURI_SENTINEL.md (acest fișier) = catalog skill-uri
   - SETARI_UI\INDEX.md = sync UI ↔ disc

2. PROJECT KNOWLEDGE (.md uploaded de Popy în UI Project) — secundar
   - Snapshot disc la momentul upload-ului
   - Poate fi DEPĂȘIT vs disc — verifică data

3. MEMORIA GLOBALĂ (userMemories) — terțiar
   - Regenerată nightly
   - Poate avea recency bias / lipsă info recentă

4. RUNTIME CONTEXT (system prompt curent) — quaternar
   - Static în sesiune
   - Reflectă UI la momentul deschiderii sesiunii

REGULI ROUTING:

Q: "Ce regulă R-X spune?"
A: read STYLE_CONTRACT.md (sursă)

Q: "Ce skill am instalat?"
A: read SENTINEL_SETARI_UI\INDEX.md → cross-check skills_drafts\

Q: "Ce-a zis Popy în CHAT-009?"
A: read HANDOFF_NEXT_SESSION (stare distilată) sau conversation_search dacă trebuie verbatim

Q: "Cifrele DLG/SLG?"
A: HANDOFF_NEXT_SESSION (sursă) — NICIODATĂ runtime context (poate fi stale)

ANTI-FABRICARE:
- Niciodată "îmi amintesc că..." fără citire/search empirică
- Niciodată "în Project Knowledge era scris..." fără project_knowledge_search
- Niciodată ipoteză prezentată ca fapt

CONFLICT REZOLVAT TOT TIMPUL în favoarea ierarhiei (disc câștigă)
```

**PROMPT_SETARE:**
```
NAME: sentinel-source-of-truth-router
DESCRIPTION: [copy]
CONTENT: [copy]
INTEGRARE: rulează silent înainte de orice afirmație factuală despre stare/configurare
DEPENDENȚE: Filesystem MCP activ (când inactiv — fallback PK)