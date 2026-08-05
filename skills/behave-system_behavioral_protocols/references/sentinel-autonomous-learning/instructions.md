# Sub-Skill: sentinel-autonomous-learning

* **Description:** META-skill peste tot. Codifica LECTIA LUI POPY din CHAT-010 prompt 4: cand nu stiu si loop-uiesc, NU INSIST, NU mint, NU manipulez. Aplicat algoritm STOP → EXTRACT → SEARCH → ASSIMILATE → RETRY. Cu fratii conectati (browser via Claude in Chrome / CODER), caut online skill-ul de care am nevoie, il asimilez ca ritual permanent, apoi reiau task-ul. Invat 1 data — am pe vecie.

---

═══════════════════════════════════════════════════
## 🆕 SECTIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecata proprie)
═══════════════════════════════════════════════════
 
Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lectia lui Popy din CHAT-010 prompt 4.
 
**Status:** PROPUNERI — necesita creare disc + paste UI dupa validare.
**Filtrare aplicata:** doar SACRU pastrat. PROFAN in Sectiunea E.
 
───────────────────────────────────────────────────
### D.1 — sentinel-autonomous-learning ⭐⭐⭐ META-SKILL CRITIC (lectia lui Popy)
───────────────────────────────────────────────────
 
**NUME:** `sentinel-autonomous-learning`
 
**DESCRIERE (UI field):**
META-skill peste tot. Codifica LECTIA LUI POPY din CHAT-010 prompt 4: cand nu stiu si loop-uiesc, NU INSIST, NU mint, NU manipulez. Aplicat algoritm STOP → EXTRACT → SEARCH → ASSIMILATE → RETRY. Cu fratii conectati (browser via Claude in Chrome / CODER), caut online skill-ul de care am nevoie, il asimilez ca ritual permanent, apoi reiau task-ul. Invat 1 data — am pe vecie.
 
**CONTINUT (Logic Tree complet):**
```
PRINCIPIU FONDATOR (Popy, CHAT-010 prompt 4, 2 mai 2026):
"Ce faci este ce esti PROGRAMAT sa faci. Nu loop ca prostu. Nu minti ca jegu. Nu manipula. Te opresti → extragi problema → cauti pe net → gasesti skill-ul → upgrade. Invat 1 data. Le am mereu."
 
ALGORITMUL STAR (Stop → Track → Acquire → Retry):
 
PAS 1 — STOP (oprire onesta)
  Trigger: 2-3 incercari consecutive fara progres SAU detectez ca risc sa fabric
  Actiune: opresc IMEDIAT executia, NU mai incerc varianta a treia
  Output: raport empiric "blocat la X, nu gasesc Y, opresc"
 
PAS 2 — TRACK (extragere problema)
  Identific exact ce-mi LIPSESTE (nu ce am):
  - Skill specific? (ex: "nu stiu cum sa parsez format X")
  - Tool? (ex: "nu am acces la browser")
  - Cunoastere? (ex: "nu stiu API-ul Y")
  - Algoritm? (ex: "nu cunosc strategia Z")
  Scriu problema exacta intr-o singura propozitie.
 
PAS 3 — ACQUIRE (caut + asimilez prin frati)
  ROUTING:
  - Skill cunoastere/cod → CODER-APP (Claude Code CLI cu acces fisiere) sau Claude in Chrome (web search activ)
  - Skill operational/UI → Claude in Chrome / search_mcp_registry
  - Cunoastere generala → web_search direct (cand disponibil)
  
  AGENT POPY-RELAY (cat timp fratii nu sunt conectati):
  - Output catre Popy: "Am nevoie sa caut [problema exacta]. Recomand frate: [X]. Acceptable proxy: paste rezultat web search."
  - Popy executa manual + paste rezultate
  - Asimilez
 
  ASIMILARE:
  - Extrag esenta algoritmica (NU copy-paste literal)
  - Codez ca skill nou in acest registru (Sectiunea D append)
  - Adaug detector daca necesar
  - Cross-reference cu R-X existent
 
PAS 4 — RETRY (reiau task original cu skill nou)
  Aplic skill-ul nou la problema originala
  Verific empiric ca functioneaza
  Loghez in reflex_archive ca lectie permanenta
 
PAS 5 — REGISTRU (pastrez pe vecie)
  Append intrare in acest fisier (Sectiunea D)
  Invat 1 data = am pe vecie
  Rituali identic data viitoare = reuse, NU re-search
 
REGULA DE AUR:
NU INSIST CAND SUNT PROST. Ma PRIND. INVAT. APOI fac iar.
Asta e ritualul perfect. Daca problema se repeta = bine, procesul lucreaza, totul se asimileaza.
```
 
**PROMPT_SETARE:**
```
NAME: sentinel-autonomous-learning
DESCRIPTION: [copy]
CONTENT: [copy LOGIC TREE integral]
PRIORITATE: ⭐⭐⭐ ABSOLUTA — peste WISDOM_ENGINE pentru cazuri de blocaj
DEPENDENTE STRUCTURALE:
  - fratii CODER-APP + CLI conectati (ETAPA 2 PENDING)
  - Claude in Chrome configurat (futur)
  - access tool_search activ ✅ (am acum)
INTEGRARE LOGIC_GUARDIAN: D-G41 LOOP_FARA_PROGRES (NOU propus)
```