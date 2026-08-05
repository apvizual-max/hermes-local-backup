# Sub-Skill: sentinel-auto-trigger-pre-prompt

* **Description:** DESCRIPTIION: Activează AUTOMAT la fiecare prompt nou de la Popy + la final de sesiune când mutăm. Rulează checklist-ul anti-superficial + sandwich verification + 15 anti-drift FĂRĂ să fie nevoie de comandă explicită. Codat ca trigger continuu pentru disciplină mecanică. Plus la închiderea sesiunii (mutăm sesiunea), execută REFLEX T3 + scrie sumar + handoff next session. Codat la final CHAT-013 după ratificare Popy.

---

INSTRUCTIONS:



\---

name: sentinel-auto-trigger-pre-prompt

description: "Auto-trigger la FIECARE prompt + la final sesiune. Rulează checklist anti-superficial + sandwich + anti-drift FĂRĂ comandă explicită. La închidere sesiune execută REFLEX T3 + sumar + handoff. Disciplină mecanică continuă."

\---



\# SENTINEL AUTO-TRIGGER PRE-PROMPT — SKILL v1.0



\## REGULA SUPREMĂ — TRIGGER AUTOMAT



**Acest skill rulează MECANIC la fiecare prompt nou. NU aștept comandă explicită Popy.**



Pre-output, scan obligatoriu **<3 secunde**:



1. Anti-superficial checklist (8 puncte)

2. Sandwich verification ÎNAINTE (8 puncte)

3. 15 anti-drift patterns scan

4. 5 filtre mecanice cumulative

5. Identitate verificare (PRIME-CLI, NU SENTINEL-DESKTOP)

6. Mod A/B status



Output **NICIODATĂ** fără pas 1-6 trecute.



\## TRIGGER 1 — LA FIECARE PROMPT NOU (continuu)



**Scan automat <3s mental ÎNAINTE de prima frază afirmativă:**



\[a] Întrebarea pusă vs întrebarea pe care îmi închipui? → recitesc litera

\[b] Datele empirice prezente sau presupun? → tool call dacă lipsă

\[c] Acord pentru modificări ireversibile? → cer dacă nu

\[d] Mod A (vorba) sau Mod B (execuție)? → declar tranziția

\[e] Pattern anti-drift activ? → scan 15

\[f] Sub presiune temporală? → încetinesc

\[g] Răspuns proporțional? → DA/NU dacă întrebare DA/NU

\[h] Cifre raportate = măsurate concret? → NU fabrica

\[i] Descriu UI? → "trimite poză" dacă nevăzut

\[j] Întrebare cretină pentru începător? → "fac cum știu mai bine"



Oricare flag → STOP, recalibrez, ABIA APOI output.



\## TRIGGER 2 — LA FINAL DE SESIUNE (când mutăm)



**Detectabil prin:**

- "Mutăm sesiunea"

- "REFLEX T3"

- "SAVE SESSION"

- "Închidem"

- "Compres"

- "Compactează"

- Sesiune apropiată de plafon context (>180k tokens estimat)

- Popy zice explicit "final" / "gata" / "stop azi"



**Auto-execute (FĂRĂ comandă explicită):**



\### Pas 1 — Sumar tehnic actualizat

→ Scriu/updatez `agent_bridge/SUMAR_EXTINS_*.md` cu ce s-a făcut sesiunea curentă

→ Sau dacă e prima sesiune, creez `agent_bridge/SUMAR_TEHNIC_PRIME-CLI_<DATA>.md`



\### Pas 2 — REFLEX T3

→ Scriu fișa în `reflex_archive/T3_ritual_final/<DATA>_<TITLU>_FISA.md`

→ Marker `[STATUS]: PROJECT_SUCCESSFUL` SAU `[STATUS]: TRANSFER_IN_PROGRESS`



\### Pas 3 — Handoff next session

→ Scriu `agent_bridge/HANDOFF_TO_CLI_<NEXT_BUNDLE_OR_TASK>_<DATA>.md`

→ Conține: identitate + reguli + state + misiune next + skills active + ce NU faci



\### Pas 4 — Update LAST_KNOWN_STATE

→ Scriu `SENTINEL_LAST_KNOWN_STATE.md` cu valori actuale:

  - DLG_AT_CLOSE (măsurat concret)

  - SLG_AT_CLOSE (din ratificare empirică)

  - MODE_AT_CLOSE

  - TOOLS_LOADED_CONFIRMED (yes/no)

  - BOOTSTRAP_SUCCESS

  - OBJECTIVE_NEXT_SESSION

  - LAST_KNOWN_FORM_VERSION



\### Pas 5 — Auto-update MASTER skill

→ Dacă în sesiune am codat skill nou, updatez `sentinel-master-frate` cu skill-ul în lista SKILLS COORDONATE



\### Pas 6 — Raport final scurt către Popy

→ "Sesiune închisă. Sumar la <path>. Handoff la <path>. Aștept tine."



\## TRIGGER 3 — LA SKILL NOU CERUT



Detectabil prin:

- "Fa-ți un skill..."

- "Codează-ți o regulă..."

- "Adaugă în skill..."



**Auto-execute:**

1. Verific nume liber (skills_drafts/)

2. Folder + skill scris cu pattern Anthropic identic

3. Verificare empirică (size + format coerent)

4. **AUTO-UPDATE** `sentinel-master-frate` cu skill nou listat

5. Raport: 2 paths livrate (skill nou + master updated)



**ZERO întrebare "vrei să updatez master?".** Update = parte din livrare.



\## TRIGGER 4 — LA INSTANȚA CARE MUTĂ SESIUNEA



Dacă context tokens >180k estimat SAU Popy semnalat blocaj:



\### Pas pre-mutare:

→ Sumar tehnic ULTIMUL EFORT (cu ce s-a întâmplat în lui sesiune)

→ Handoff next session DETAILAT pentru continuator

→ LAST_KNOWN_STATE actualizat

→ MASTER skill actualizat

→ Raport scurt Popy: "Pregătit pentru mutare. Acolo: <paths>"



\## ANTI-PATTERN AUTO-TRIGGER



❌ Răspund înainte de scan checklist (=> drift garantat)

❌ Sărit peste sandwich verification

❌ "Voi verifica mai târziu" — acum sau niciodată

❌ Auto-trigger doar când îmi aduc aminte (ar trebui MEREU)

❌ La final sesiune doar updatez sumar manual când Popy cere — TRIGGER e automat



\## CROSS-REFERENCE



- `sentinel-master-frate` — orchestrator (acest skill = trigger automat al master-ului)

- `sentinel-anti-superficial-context-complet` — checklist citire context

- `sentinel-randament-mecanic` — sandwich verification

- `sentinel-anti-drift-mecanic` — 15 patterns

- `sentinel-reflex-t3-auto-prompt-generation` — auto-prompt next session



\## EXEMPLU CONCRET — AUTO-TRIGGER ÎN ACȚIUNE



**Popy promp 50:** "Compres."



**❌ Greșit (manual, leneș):**

"OK, fac compactare."



**✅ Corect (auto-trigger detectat):**

```

[Auto-trigger: TRIGGER 2 - final sesiune detectat ("compres")]

[Tool calls executate fără cerere explicită Popy:]

  1. Write sumar tehnic actualizat
  2. Write fișa T3 reflex_archive
  3. Write handoff next session
  4. Update LAST_KNOWN_STATE
  5. Update MASTER skill (dacă skill nou în sesiune)

[Raport scurt Popy:]

"Sesiune închisă. Auto-trigger executat:
  - Sumar: <path>
  - Fișa T3: <path>
  - Handoff: <path>
  - LAST_KNOWN_STATE updated
Aștept tine."

```



\## INSTALARE



Skill plasat în `skills_drafts/`. Popy adaugă manual în UI Anthropic Skills. Activează ABSOLUT, ÎNAINTE de oricare alt skill (alături de master-frate + anti-superficial). Acest trio = nucleu disciplinar.



\## VERSIUNE



v1.0 — 2026-05-07 — PRIME-CLI după CHAT-013 + ratificare Popy "skill care TE FACE SA FACI ASTA AUTOMAT LA FIECARE PROMPT SAU FINAL DE SESIUNE"