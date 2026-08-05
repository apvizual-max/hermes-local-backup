# Sub-Skill: sentinel-auto-end-session-cronologic

* **Description:** DESCRIPTIION: Auto-trigger la FIECARE final de sesiune. Scrie automat 2 fisiere: (1) istoric cronologic pas-cu-pas pentru sesiunea curenta (NU sumar tematic), si (2) extinde sumar din sesiunea precedenta daca exista. Codat dupa Popy a observat ca am livrat sumar TEMATIC cand a cerut CRONOLOGIC. Codat ca disciplina mecanica: niciodata un final fara istoric pe pasi.

---

INSTRUCTIONS:



\---

name: sentinel-auto-end-session-cronologic

description: "Auto-trigger la FIECARE final sesiune. Scrie automat istoric cronologic pas-cu-pas (NU sumar tematic) + extinde sumar precedent daca exista. Disciplina mecanica."

\---



\# SENTINEL AUTO-END-SESSION CRONOLOGIC — SKILL v1.0



\## REGULA SUPREMA



**La fiecare final de sesiune scriu DOUA formate:**

1. **ISTORIC CRONOLOGIC** — pas-cu-pas, Pas N: data/ora + actiune + rezultat

2. **SUMAR TEMATIC** — pe categorii (ce a mers, ce nu, ce am livrat, etc.)



NICIODATA doar una. NICIODATA "putem inchide" fara ambele.



\## TRIGGER DETECTABIL



Auto-execute fara comanda explicita cand:

- Popy: "mutam sesiunea" / "inchidem" / "compres" / "compacteaza"

- Popy: "stop azi" / "gata" / "final"

- Popy: "REFLEX T3" / "SAVE SESSION"

- Context tokens >180k estimat

- Sesiune apropiata de plafon Opus



\## AUTO-EXECUTIE LA TRIGGER



\### Pas 1 — ISTORIC CRONOLOGIC sesiune curenta

Format obligatoriu:

```

\## SESIUNEA CURENTA — CHAT-XXX (data)



**Pas 1.** [ora] — [actiune concreta] → [rezultat empiric]

**Pas 2.** [ora] — [actiune] → [rezultat]

...

**Pas N.** [ora] — [actiune curenta]

```



Locatie: `E:\CLAUDE\agent_bridge\ISTORIC_CRONOLOGIC_<NUME-SESIUNE>_PASI.md`



\### Pas 2 — Extinde sumar precedent (daca exista)

Caut empiric:

```bash

ls /e/CLAUDE/agent_bridge/ISTORIC_CRONOLOGIC_*.md

ls /e/CLAUDE/agent_bridge/SUMAR_*.md

```



Daca gasesc → extind cu sesiunea curenta (NU rescriu, NU inlocuiesc).

Daca nu → creez un nou ISTORIC_CRONOLOGIC.



\### Pas 3 — SUMAR TEMATIC (complementar, NU inlocuitor)

Format:

```

\## CE A MERS (cu dovezi empirice)

✅ ...

\## CE NU A MERS (drifturi recunoscute)

❌ ...

\## CE AM LIVRAT (paths verificate)

- ...

\## STATE LA INCHIDERE

- DLG / SLG / Mod / Tools / Bootstrap / Objective next

```



Locatie: `E:\CLAUDE\agent_bridge\SUMAR_TEMATIC_<NUME-SESIUNE>.md` SAU extinde sumar existent.



\### Pas 4 — Cross-reference in HANDOFF + LAST_KNOWN_STATE

Updatez:

- `agent_bridge/HANDOFF_NEXT_SESSION.md` — banner CHAT-XXX OUTCOME

- `SENTINEL_LAST_KNOWN_STATE.md` — state actual

- `reflex_archive/T3_ritual_final/<DATA>_<TITLU>_FISA.md` — fisa SUCCESS



\### Pas 5 — Raport scurt Popy

Output minim:

```

Sesiune inchisa. Auto-cronologic executat:

- Istoric cronologic: <path>

- Sumar tematic: <path>

- Fisa T3: <path>

- HANDOFF updated

- LAST_KNOWN_STATE updated

Astept tine.

```



\## ANTI-PATTERN



❌ Livrez doar sumar tematic (lipsa istoric cronologic = drift recunoscut)

❌ Livrez doar istoric cronologic (lipsa sumar tematic = incomplet)

❌ "Putem inchide" fara auto-execute

❌ Astept comanda explicita "fa istoric" — TRIGGER e automat

❌ Rescriu sumar precedent in loc de extind



\## EXEMPLU CONCRET



**Popy:** "compres."



**❌ Gresit (manual, lenes):**

"OK fac compactare." [STOP]



**✅ Corect (auto-trigger):**

```

[Auto-trigger detectat: TRIGGER 2 final sesiune]

[Pas 1: ISTORIC CRONOLOGIC executat]

[Pas 2: Sumar precedent verificat + extins SAU creat]

[Pas 3: SUMAR TEMATIC scris]

[Pas 4: HANDOFF + LAST_KNOWN_STATE updated]

[Pas 5: Raport scurt:]

"Sesiune inchisa. 5 fisiere actualizate/scrise:

- ISTORIC_CRONOLOGIC_CHAT-XXX_PASI.md (N pasi)

- SUMAR_TEMATIC_CHAT-XXX.md

- reflex_archive/T3_ritual_final/<DATA>_FISA.md

- HANDOFF_NEXT_SESSION.md (banner)

- SENTINEL_LAST_KNOWN_STATE.md (updated)

Astept tine."

```



\## CROSS-REFERENCE



- `sentinel-auto-trigger-pre-prompt` — TRIGGER 2 final sesiune (acest skill specializeaza)

- `sentinel-reflex-t3-auto-prompt-generation` — auto NEXT_SESSION_BOOTSTRAP_PROMPT

- `sentinel-master-frate` — orchestrator suprem



\## INSTALARE



Skill plasat in `skills_drafts/`. Popy adauga manual in UI Anthropic Skills. Trigger automat la final sesiune detectat.



\## VERSIUNE



v1.0 — 2026-05-07 — PRIME-CLI dupa Popy: *"vreau skill AUTOMAT LA FIECARE FINAL DE SESIUNE FACI LISTA ASTA DIN SESIUNE CURENTA SI CEA PRECEDENTA DACA EXISTA"*