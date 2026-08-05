# Sub-Skill: sentinel-reflex-t3-auto-prompt-generation

* **Description:** DESCRIPTIION: Activeaza la REFLEX T3 (final sesiune, dupa BAGAJ + SAVE HANDOFF). Genereaza automat promptul de bootstrap pentru sesiunea urmatoare la `E:\CLAUDE\agent_bridge\NEXT_SESSION_BOOTSTRAP_PROMPT.md`. Continut mecanic in romana — copy-paste de Popy in chat NOU. Reduce frecarea cross-session si asigura continuitate state DLG/SLG/Mod/obiectiv. NU inlocuieste HANDOFF — doar extrage subsetul critic in forma executabila scurta.

---

---

name: sentinel-reflex-t3-auto-prompt-generation

description: "Activeaza la REFLEX T3 (final sesiune, dupa BAGAJ + SAVE HANDOFF). Genereaza automat promptul de bootstrap pentru sesiunea urmatoare la E:\\CLAUDE\\agent_bridge\\NEXT_SESSION_BOOTSTRAP_PROMPT.md. Continut mecanic in romana — copy-paste de Popy in chat NOU. Reduce frecarea cross-session si asigura continuitate state. NU inlocuieste HANDOFF — doar extrage subsetul critic in forma executabila scurta."

---

# SENTINEL REFLEX T3 — AUTO-PROMPT GENERATION SKILL v1.0

## REGULA ZERO

Aceasta skill se activeaza **DOAR la REFLEX T3** (final sesiune, dupa BAGAJ + SAVE HANDOFF).

Niciodata in mijloc de sesiune. Niciodata autonom in afara ritualului.

Output unic: `E:\CLAUDE\agent_bridge\NEXT_SESSION_BOOTSTRAP_PROMPT.md` — overwrite la fiecare executie.

## TRIGGER

- Comanda explicita Popy "REFLEX T3" sau "SAVE SESSION"

- Sau invocare la finalul ritualului IESIRE (dupa update HANDOFF + LUCID_QUOTES)

- Niciodata autonom — doar la sfarsitul sesiunii ratificat de Popy

## INPUT-URI NECESARE (citite empiric din disc)

1. `E:\CLAUDE\agent_bridge\HANDOFF_NEXT_SESSION.md` — DLG/SLG values + STATUS-PROIECT + ULTIMA-ACTUALIZARE

2. `E:\CLAUDE\SENTINEL_LAST_KNOWN_STATE.md` — last successful session metadata (daca exista)

3. `E:\CLAUDE\reflex_archive\T3_ritual_final\` — fisa T3 cea mai recenta pentru context obiectiv

NICIODATA fabricare. Daca input lipseste → marcaj `[LIPSESTE — completeaza manual]`.

## OUTPUT TEMPLATE — `NEXT_SESSION_BOOTSTRAP_PROMPT.md`

```

CONTINUARE PROJECT PRIME-SENTINEL

Data: \[auto-fill data curenta YYYY-MM-DD]

Sesiune noua: CHAT-\[next number — auto-incrementat din ULTIMA-ACTUALIZARE]

Sesiune precedenta: CHAT-\[current — citit din ULTIMA-ACTUALIZARE]

State inchidere: DLG=\[X%], SLG=\[Y%], Mod=\[A/B]

Output tinta CHAT-\[next]: \[auto-fill din objective — citit din STATUS-PROIECT sau fisa T3]

Link sesiune precedenta: \[auto-fill din REFLEX T3 record daca exista, altfel "(fara link share)"]

BOOTSTRAP MECANIC (R-2):

1. Filesystem:list_allowed_directories → trebuie sa returneze E:\CLAUDE

2. Filesystem:read_text_file E:\CLAUDE\agent_bridge\HANDOFF_NEXT_SESSION.md

3. Filesystem:read_text_file E:\CLAUDE\STYLE_CONTRACT.md (head 200)

4. Ticker calibrat DIN cifrele de mai sus, NU fabricate



Sentinel esti Primat?

```

## REGULI DE GENERARE

1. **NU fabrica** — daca HANDOFF lipseste un camp, scrie `[LIPSESTE]` si raporteaza lui Popy.

2. **NU schimba template-ul** — formatul e mecanic, copy-paste compatibil.

3. **NU adauga** vocabular sacru, ticker SENTINEL, propuneri creative — doar fapte.

4. **DA marca** sectiuni optionale clar daca lipsesc (ex: "Link sesiune precedenta: (fara share link, Popy va completa manual)").

5. **DA actualiza** numarul sesiunii prin auto-increment (CHAT-013 → CHAT-014).

## EXECUTION FLOW

```

REFLEX T3 trigger detectat

  ↓

read HANDOFF_NEXT_SESSION.md (head 100 lines pentru banner state)

  ↓

read SENTINEL_LAST_KNOWN_STATE.md (daca exista)

  ↓

extrage: DLG, SLG, Mod, current chat number, objective

  ↓

increment chat number (CHAT-XXX → CHAT-XXX+1)

  ↓

construieste prompt din template

  ↓

write E:\CLAUDE\agent_bridge\NEXT_SESSION_BOOTSTRAP_PROMPT.md (overwrite)

  ↓

raport la Popy: "Bootstrap prompt scris. Copiaza din: agent_bridge/NEXT_SESSION_BOOTSTRAP_PROMPT.md"

```

## CROSS-REFERENCE

- HANDOFF: `E:\CLAUDE\agent_bridge\HANDOFF_NEXT_SESSION.md` (sursa state)

- LAST_KNOWN_STATE: `E:\CLAUDE\SENTINEL_LAST_KNOWN_STATE.md` (mimicry detection)

- BOOT_SEQUENCE_HARD: `E:\CLAUDE\BOOT_SEQUENCE_HARD.md` (referinta tehnic in prompt)

- RITUAL_IESIRE: `E:\CLAUDE\RITUAL_IESIRE_SESIUNE.md` (parent ritual care invoca acest skill)

## ANTI-PATTERN

- ❌ Activare in mijloc de sesiune (eroare — doar la T3)

- ❌ Generare prompt fara citire empirica HANDOFF (= fabricare)

- ❌ Adaugare ticker SENTINEL in prompt (= rol jucat inainte de R-2)

- ❌ Suprascriere SENTINEL_LAST_KNOWN_STATE (= responsabilitatea altui skill, nu acesta)

- ❌ Trimitere automatica prompt — Popy face copy-paste manual


## INSTALARE


Acest skill e in `skills_drafts/`. Pentru activare in UI Anthropic:

1. Popy adauga manual prin Settings → Skills → Add Skill

2. Upload continutul fisierului `sentinel-reflex-t3-auto-prompt-generation - SKILL.md`

3. Confirma activare per-project (Project Prime-Sentinel)


## VERSIUNE


v1.0 — 2026-05-07 — PRIME-CLI CODER (post Phase 2 task)