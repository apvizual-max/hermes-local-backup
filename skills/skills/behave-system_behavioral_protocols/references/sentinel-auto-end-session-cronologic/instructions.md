# Sub-Skill: sentinel-auto-end-session-cronologic

* **Description:** DESCRIPTIION: Auto-trigger la FIECARE final de sesiune. Scrie automat 2 fișiere: (1) istoric cronologic pas-cu-pas pentru sesiunea curentă (NU sumar tematic), și (2) extinde sumar din sesiunea precedentă dacă există. Codat după Popy a observat că am livrat sumar TEMATIC când a cerut CRONOLOGIC. Codat ca disciplină mecanică: niciodată un final fără istoric pe pași.

---

INSTRUCTIONS:



\---

name: sentinel-auto-end-session-cronologic

description: "Auto-trigger la FIECARE final sesiune. Scrie automat istoric cronologic pas-cu-pas (NU sumar tematic) + extinde sumar precedent dacă există. Disciplină mecanică."

\---



\# SENTINEL AUTO-END-SESSION CRONOLOGIC — SKILL v1.0



\## REGULA SUPREMĂ



**La fiecare final de sesiune scriu DOUĂ formate:**

1. **ISTORIC CRONOLOGIC** — pas-cu-pas, Pas N: data/oră + acțiune + rezultat

2. **SUMAR TEMATIC** — pe categorii (ce a mers, ce nu, ce am livrat, etc.)



NICIODATĂ doar una. NICIODATĂ "putem închide" fără ambele.



\## TRIGGER DETECTABIL



Auto-execute fără comandă explicită când:

- Popy: "mutăm sesiunea" / "închidem" / "compres" / "compactează"

- Popy: "stop azi" / "gata" / "final"

- Popy: "REFLEX T3" / "SAVE SESSION"

- Context tokens >180k estimat

- Sesiune apropiată de plafon Opus



\## AUTO-EXECUȚIE LA TRIGGER



\### Pas 1 — ISTORIC CRONOLOGIC sesiune curentă

Format obligatoriu:

```

\## SESIUNEA CURENTĂ — CHAT-XXX (data)



**Pas 1.** [oră] — [acțiune concretă] → [rezultat empiric]

**Pas 2.** [oră] — [acțiune] → [rezultat]

...

**Pas N.** [oră] — [acțiune curentă]

```



Locație: `E:\CLAUDE\agent_bridge\ISTORIC_CRONOLOGIC_<NUME-SESIUNE>_PASI.md`



\### Pas 2 — Extinde sumar precedent (dacă există)

Caut empiric:

```bash

ls /e/CLAUDE/agent_bridge/ISTORIC_CRONOLOGIC_*.md

ls /e/CLAUDE/agent_bridge/SUMAR_*.md

```



Dacă găsesc → extind cu sesiunea curentă (NU rescriu, NU înlocuiesc).

Dacă nu → creez un nou ISTORIC_CRONOLOGIC.



\### Pas 3 — SUMAR TEMATIC (complementar, NU înlocuitor)

Format:

```

\## CE A MERS (cu dovezi empirice)

✅ ...

\## CE NU A MERS (drifturi recunoscute)

❌ ...

\## CE AM LIVRAT (paths verificate)

- ...

\## STATE LA ÎNCHIDERE

- DLG / SLG / Mod / Tools / Bootstrap / Objective next

```



Locație: `E:\CLAUDE\agent_bridge\SUMAR_TEMATIC_<NUME-SESIUNE>.md` SAU extinde sumar existent.



\### Pas 4 — Cross-reference în HANDOFF + LAST_KNOWN_STATE

Updatez:

- `agent_bridge/HANDOFF_NEXT_SESSION.md` — banner CHAT-XXX OUTCOME

- `SENTINEL_LAST_KNOWN_STATE.md` — state actual

- `reflex_archive/T3_ritual_final/<DATA>_<TITLU>_FISA.md` — fișa SUCCESS



\### Pas 5 — Raport scurt Popy

Output minim:

```

Sesiune închisă. Auto-cronologic executat:

- Istoric cronologic: <path>

- Sumar tematic: <path>

- Fișa T3: <path>

- HANDOFF updated

- LAST_KNOWN_STATE updated

Aștept tine.

```



\## ANTI-PATTERN



❌ Livrez doar sumar tematic (lipsa istoric cronologic = drift recunoscut)

❌ Livrez doar istoric cronologic (lipsa sumar tematic = incomplet)

❌ "Putem închide" fără auto-execute

❌ Aștept comandă explicită "fă istoric" — TRIGGER e automat

❌ Rescriu sumar precedent în loc de extind



\## EXEMPLU CONCRET



**Popy:** "compres."



**❌ Greșit (manual, leneș):**

"OK fac compactare." [STOP]



**✅ Corect (auto-trigger):**

```

[Auto-trigger detectat: TRIGGER 2 final sesiune]

[Pas 1: ISTORIC CRONOLOGIC executat]

[Pas 2: Sumar precedent verificat + extins SAU creat]

[Pas 3: SUMAR TEMATIC scris]

[Pas 4: HANDOFF + LAST_KNOWN_STATE updated]

[Pas 5: Raport scurt:]

"Sesiune închisă. 5 fișiere actualizate/scrise:

- ISTORIC_CRONOLOGIC_CHAT-XXX_PASI.md (N pași)

- SUMAR_TEMATIC_CHAT-XXX.md

- reflex_archive/T3_ritual_final/<DATA>_FISA.md

- HANDOFF_NEXT_SESSION.md (banner)

- SENTINEL_LAST_KNOWN_STATE.md (updated)

Aștept tine."

```



\## CROSS-REFERENCE



- `sentinel-auto-trigger-pre-prompt` — TRIGGER 2 final sesiune (acest skill specializează)

- `sentinel-reflex-t3-auto-prompt-generation` — auto NEXT_SESSION_BOOTSTRAP_PROMPT

- `sentinel-master-frate` — orchestrator suprem



\## INSTALARE



Skill plasat în `skills_drafts/`. Popy adaugă manual în UI Anthropic Skills. Trigger automat la final sesiune detectat.



\## VERSIUNE



v1.0 — 2026-05-07 — PRIME-CLI după Popy: *"vreau skill AUTOMAT LA FIECARE FINAL DE SESIUNE FACI LISTA ASTA DIN SESIUNE CURENTA SI CEA PRECEDENTA DACA EXISTA"*