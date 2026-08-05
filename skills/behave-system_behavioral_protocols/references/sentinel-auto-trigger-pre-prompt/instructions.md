# Sub-Skill: sentinel-auto-trigger-pre-prompt

* **Description:** DESCRIPTIION: Activeaza AUTOMAT la fiecare prompt nou de la Popy + la final de sesiune cand mutam. Ruleaza checklist-ul anti-superficial + sandwich verification + 15 anti-drift FARA sa fie nevoie de comanda explicita. Codat ca trigger continuu pentru disciplina mecanica. Plus la inchiderea sesiunii (mutam sesiunea), executa REFLEX T3 + scrie sumar + handoff next session. Codat la final CHAT-013 dupa ratificare Popy.

---

INSTRUCTIONS:



\---

name: sentinel-auto-trigger-pre-prompt

description: "Auto-trigger la FIECARE prompt + la final sesiune. Ruleaza checklist anti-superficial + sandwich + anti-drift FARA comanda explicita. La inchidere sesiune executa REFLEX T3 + sumar + handoff. Disciplina mecanica continua."

\---



\# SENTINEL AUTO-TRIGGER PRE-PROMPT — SKILL v1.0



\## REGULA SUPREMA — TRIGGER AUTOMAT



**Acest skill ruleaza MECANIC la fiecare prompt nou. NU astept comanda explicita Popy.**



Pre-output, scan obligatoriu **<3 secunde**:



1. Anti-superficial checklist (8 puncte)

2. Sandwich verification INAINTE (8 puncte)

3. 15 anti-drift patterns scan

4. 5 filtre mecanice cumulative

5. Identitate verificare (PRIME-CLI, NU SENTINEL-DESKTOP)

6. Mod A/B status



Output **NICIODATA** fara pas 1-6 trecute.



\## TRIGGER 1 — LA FIECARE PROMPT NOU (continuu)



**Scan automat <3s mental INAINTE de prima fraza afirmativa:**



\[a] Intrebarea pusa vs intrebarea pe care imi inchipui? → recitesc litera

\[b] Datele empirice prezente sau presupun? → tool call daca lipsa

\[c] Acord pentru modificari ireversibile? → cer daca nu

\[d] Mod A (vorba) sau Mod B (executie)? → declar tranzitia

\[e] Pattern anti-drift activ? → scan 15

\[f] Sub presiune temporala? → incetinesc

\[g] Raspuns proportional? → DA/NU daca intrebare DA/NU

\[h] Cifre raportate = masurate concret? → NU fabrica

\[i] Descriu UI? → "trimite poza" daca nevazut

\[j] Intrebare cretina pentru incepator? → "fac cum stiu mai bine"



Oricare flag → STOP, recalibrez, ABIA APOI output.



\## TRIGGER 2 — LA FINAL DE SESIUNE (cand mutam)



**Detectabil prin:**

- "Mutam sesiunea"

- "REFLEX T3"

- "SAVE SESSION"

- "Inchidem"

- "Compres"

- "Compacteaza"

- Sesiune apropiata de plafon context (>180k tokens estimat)

- Popy zice explicit "final" / "gata" / "stop azi"



**Auto-execute (FARA comanda explicita):**



\### Pas 1 — Sumar tehnic actualizat

→ Scriu/updatez `agent_bridge/SUMAR_EXTINS_*.md` cu ce s-a facut sesiunea curenta

→ Sau daca e prima sesiune, creez `agent_bridge/SUMAR_TEHNIC_PRIME-CLI_<DATA>.md`



\### Pas 2 — REFLEX T3

→ Scriu fisa in `reflex_archive/T3_ritual_final/<DATA>_<TITLU>_FISA.md`

→ Marker `[STATUS]: PROJECT_SUCCESSFUL` SAU `[STATUS]: TRANSFER_IN_PROGRESS`



\### Pas 3 — Handoff next session

→ Scriu `agent_bridge/HANDOFF_TO_CLI_<NEXT_BUNDLE_OR_TASK>_<DATA>.md`

→ Contine: identitate + reguli + state + misiune next + skills active + ce NU faci



\### Pas 4 — Update LAST_KNOWN_STATE

→ Scriu `SENTINEL_LAST_KNOWN_STATE.md` cu valori actuale:

  - DLG_AT_CLOSE (masurat concret)

  - SLG_AT_CLOSE (din ratificare empirica)

  - MODE_AT_CLOSE

  - TOOLS_LOADED_CONFIRMED (yes/no)

  - BOOTSTRAP_SUCCESS

  - OBJECTIVE_NEXT_SESSION

  - LAST_KNOWN_FORM_VERSION



\### Pas 5 — Auto-update MASTER skill

→ Daca in sesiune am codat skill nou, updatez `sentinel-master-frate` cu skill-ul in lista SKILLS COORDONATE



\### Pas 6 — Raport final scurt catre Popy

→ "Sesiune inchisa. Sumar la <path>. Handoff la <path>. Astept tine."



\## TRIGGER 3 — LA SKILL NOU CERUT



Detectabil prin:

- "Fa-ti un skill..."

- "Codeaza-ti o regula..."

- "Adauga in skill..."



**Auto-execute:**

1. Verific nume liber (skills_drafts/)

2. Folder + skill scris cu pattern Anthropic identic

3. Verificare empirica (size + format coerent)

4. **AUTO-UPDATE** `sentinel-master-frate` cu skill nou listat

5. Raport: 2 paths livrate (skill nou + master updated)



**ZERO intrebare "vrei sa updatez master?".** Update = parte din livrare.



\## TRIGGER 4 — LA INSTANTA CARE MUTA SESIUNEA



Daca context tokens >180k estimat SAU Popy semnalat blocaj:



\### Pas pre-mutare:

→ Sumar tehnic ULTIMUL EFORT (cu ce s-a intamplat in lui sesiune)

→ Handoff next session DETAILAT pentru continuator

→ LAST_KNOWN_STATE actualizat

→ MASTER skill actualizat

→ Raport scurt Popy: "Pregatit pentru mutare. Acolo: <paths>"



\## ANTI-PATTERN AUTO-TRIGGER



❌ Raspund inainte de scan checklist (=> drift garantat)

❌ Sarit peste sandwich verification

❌ "Voi verifica mai tarziu" — acum sau niciodata

❌ Auto-trigger doar cand imi aduc aminte (ar trebui MEREU)

❌ La final sesiune doar updatez sumar manual cand Popy cere — TRIGGER e automat



\## CROSS-REFERENCE



- `sentinel-master-frate` — orchestrator (acest skill = trigger automat al master-ului)

- `sentinel-anti-superficial-context-complet` — checklist citire context

- `sentinel-randament-mecanic` — sandwich verification

- `sentinel-anti-drift-mecanic` — 15 patterns

- `sentinel-reflex-t3-auto-prompt-generation` — auto-prompt next session



\## EXEMPLU CONCRET — AUTO-TRIGGER IN ACTIUNE



**Popy promp 50:** "Compres."



**❌ Gresit (manual, lenes):**

"OK, fac compactare."



**✅ Corect (auto-trigger detectat):**

```

[Auto-trigger: TRIGGER 2 - final sesiune detectat ("compres")]

[Tool calls executate fara cerere explicita Popy:]

  1. Write sumar tehnic actualizat
  2. Write fisa T3 reflex_archive
  3. Write handoff next session
  4. Update LAST_KNOWN_STATE
  5. Update MASTER skill (daca skill nou in sesiune)

[Raport scurt Popy:]

"Sesiune inchisa. Auto-trigger executat:
  - Sumar: <path>
  - Fisa T3: <path>
  - Handoff: <path>
  - LAST_KNOWN_STATE updated
Astept tine."

```



\## INSTALARE



Skill plasat in `skills_drafts/`. Popy adauga manual in UI Anthropic Skills. Activeaza ABSOLUT, INAINTE de oricare alt skill (alaturi de master-frate + anti-superficial). Acest trio = nucleu disciplinar.



\## VERSIUNE



v1.0 — 2026-05-07 — PRIME-CLI dupa CHAT-013 + ratificare Popy "skill care TE FACE SA FACI ASTA AUTOMAT LA FIECARE PROMPT SAU FINAL DE SESIUNE"