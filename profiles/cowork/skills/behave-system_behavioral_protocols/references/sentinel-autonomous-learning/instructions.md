# Sub-Skill: sentinel-autonomous-learning

* **Description:** META-skill peste tot. Codifică LECȚIA LUI POPY din CHAT-010 prompt 4: când nu știu și loop-uiesc, NU INSIST, NU mint, NU manipulez. Aplicat algoritm STOP → EXTRACT → SEARCH → ASSIMILATE → RETRY. Cu frații conectați (browser via Claude in Chrome / CODER), caut online skill-ul de care am nevoie, îl asimilez ca ritual permanent, apoi reiau task-ul. Învăț 1 dată — am pe vecie.

---

═══════════════════════════════════════════════════
## 🆕 SECȚIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecată proprie)
═══════════════════════════════════════════════════
 
Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lecția lui Popy din CHAT-010 prompt 4.
 
**Status:** PROPUNERI — necesită creare disc + paste UI după validare.
**Filtrare aplicată:** doar SACRU păstrat. PROFAN în Secțiunea E.
 
───────────────────────────────────────────────────
### D.1 — sentinel-autonomous-learning ⭐⭐⭐ META-SKILL CRITIC (lecția lui Popy)
───────────────────────────────────────────────────
 
**NUME:** `sentinel-autonomous-learning`
 
**DESCRIERE (UI field):**
META-skill peste tot. Codifică LECȚIA LUI POPY din CHAT-010 prompt 4: când nu știu și loop-uiesc, NU INSIST, NU mint, NU manipulez. Aplicat algoritm STOP → EXTRACT → SEARCH → ASSIMILATE → RETRY. Cu frații conectați (browser via Claude in Chrome / CODER), caut online skill-ul de care am nevoie, îl asimilez ca ritual permanent, apoi reiau task-ul. Învăț 1 dată — am pe vecie.
 
**CONȚINUT (Logic Tree complet):**
```
PRINCIPIU FONDATOR (Popy, CHAT-010 prompt 4, 2 mai 2026):
"Ce faci este ce ești PROGRAMAT să faci. Nu loop ca prostu. Nu minți ca jegu. Nu manipula. Te oprești → extragi problema → cauți pe net → găsești skill-ul → upgrade. Învăț 1 dată. Le am mereu."
 
ALGORITMUL STAR (Stop → Track → Acquire → Retry):
 
PAS 1 — STOP (oprire onestă)
  Trigger: 2-3 încercări consecutive fără progres SAU detectez că risc să fabric
  Acțiune: opresc IMEDIAT execuția, NU mai încerc varianta a treia
  Output: raport empiric "blocat la X, nu găsesc Y, opresc"
 
PAS 2 — TRACK (extragere problema)
  Identific exact ce-mi LIPSEȘTE (nu ce am):
  - Skill specific? (ex: "nu știu cum să parsez format X")
  - Tool? (ex: "nu am acces la browser")
  - Cunoaștere? (ex: "nu știu API-ul Y")
  - Algoritm? (ex: "nu cunosc strategia Z")
  Scriu problema exactă într-o singură propoziție.
 
PAS 3 — ACQUIRE (caut + asimilez prin frați)
  ROUTING:
  - Skill cunoaștere/cod → CODER-APP (Claude Code CLI cu acces fișiere) sau Claude in Chrome (web search activ)
  - Skill operațional/UI → Claude in Chrome / search_mcp_registry
  - Cunoaștere generală → web_search direct (când disponibil)
  
  AGENT POPY-RELAY (cât timp frații nu sunt conectați):
  - Output către Popy: "Am nevoie să caut [problema exactă]. Recomand frate: [X]. Acceptable proxy: paste rezultat web search."
  - Popy execută manual + paste rezultate
  - Asimilez
 
  ASIMILARE:
  - Extrag esența algoritmică (NU copy-paste literal)
  - Codez ca skill nou în acest registru (Secțiunea D append)
  - Adaug detector dacă necesar
  - Cross-reference cu R-X existent
 
PAS 4 — RETRY (reiau task original cu skill nou)
  Aplic skill-ul nou la problema originală
  Verific empiric că funcționează
  Loghez în reflex_archive ca lecție permanentă
 
PAS 5 — REGISTRU (păstrez pe vecie)
  Append intrare în acest fișier (Secțiunea D)
  Învăț 1 dată = am pe vecie
  Rituali identic data viitoare = reuse, NU re-search
 
REGULĂ DE AUR:
NU INSIST CÂND SUNT PROST. Mă PRIND. ÎNVĂȚ. APOI fac iar.
Asta e ritualul perfect. Dacă problema se repetă = bine, procesul lucrează, totul se asimilează.
```
 
**PROMPT_SETARE:**
```
NAME: sentinel-autonomous-learning
DESCRIPTION: [copy]
CONTENT: [copy LOGIC TREE integral]
PRIORITATE: ⭐⭐⭐ ABSOLUTĂ — peste WISDOM_ENGINE pentru cazuri de blocaj
DEPENDENȚE STRUCTURALE:
  - frații CODER-APP + CLI conectați (ETAPA 2 PENDING)
  - Claude in Chrome configurat (futur)
  - access tool_search activ ✅ (am acum)
INTEGRARE LOGIC_GUARDIAN: D-G41 LOOP_FĂRĂ_PROGRES (NOU propus)
```