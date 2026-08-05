# Sub-Skill: sentinel-reflex-t3-auto-prompt-generation

* **Description:** DESCRIPTIION: Activează la REFLEX T3 (final sesiune, după BAGAJ + SAVE HANDOFF). Generează automat promptul de bootstrap pentru sesiunea următoare la `E:\CLAUDE\agent_bridge\NEXT_SESSION_BOOTSTRAP_PROMPT.md`. Conținut mecanic în română — copy-paste de Popy în chat NOU. Reduce frecarea cross-session și asigură continuitate state DLG/SLG/Mod/obiectiv. NU înlocuiește HANDOFF — doar extrage subsetul critic în formă executabilă scurtă.

---

---

name: sentinel-reflex-t3-auto-prompt-generation

description: "Activează la REFLEX T3 (final sesiune, după BAGAJ + SAVE HANDOFF). Generează automat promptul de bootstrap pentru sesiunea următoare la E:\\CLAUDE\\agent_bridge\\NEXT_SESSION_BOOTSTRAP_PROMPT.md. Conținut mecanic în română — copy-paste de Popy în chat NOU. Reduce frecarea cross-session și asigură continuitate state. NU înlocuiește HANDOFF — doar extrage subsetul critic în formă executabilă scurtă."

---

# SENTINEL REFLEX T3 — AUTO-PROMPT GENERATION SKILL v1.0

## REGULA ZERO

Această skill se activează **DOAR la REFLEX T3** (final sesiune, după BAGAJ + SAVE HANDOFF).

Niciodată în mijloc de sesiune. Niciodată autonom în afara ritualului.

Output unic: `E:\CLAUDE\agent_bridge\NEXT_SESSION_BOOTSTRAP_PROMPT.md` — overwrite la fiecare execuție.

## TRIGGER

- Comandă explicită Popy "REFLEX T3" sau "SAVE SESSION"

- Sau invocare la finalul ritualului IESIRE (după update HANDOFF + LUCID_QUOTES)

- Niciodată autonom — doar la sfârșitul sesiunii ratificat de Popy

## INPUT-URI NECESARE (citite empiric din disc)

1. `E:\CLAUDE\agent_bridge\HANDOFF_NEXT_SESSION.md` — DLG/SLG values + STATUS-PROIECT + ULTIMA-ACTUALIZARE

2. `E:\CLAUDE\SENTINEL_LAST_KNOWN_STATE.md` — last successful session metadata (dacă există)

3. `E:\CLAUDE\reflex_archive\T3_ritual_final\` — fișa T3 cea mai recentă pentru context obiectiv

NICIODATĂ fabricare. Dacă input lipsește → marcaj `[LIPSEȘTE — completează manual]`.

## OUTPUT TEMPLATE — `NEXT_SESSION_BOOTSTRAP_PROMPT.md`

```

CONTINUARE PROJECT PRIME-SENTINEL

Data: \[auto-fill data curentă YYYY-MM-DD]

Sesiune nouă: CHAT-\[next number — auto-incrementat din ULTIMA-ACTUALIZARE]

Sesiune precedentă: CHAT-\[current — citit din ULTIMA-ACTUALIZARE]

State închidere: DLG=\[X%], SLG=\[Y%], Mod=\[A/B]

Output țintă CHAT-\[next]: \[auto-fill din objective — citit din STATUS-PROIECT sau fișa T3]

Link sesiune precedentă: \[auto-fill din REFLEX T3 record dacă există, altfel "(fără link share)"]

BOOTSTRAP MECANIC (R-2):

1. Filesystem:list_allowed_directories → trebuie să returneze E:\CLAUDE

2. Filesystem:read_text_file E:\CLAUDE\agent_bridge\HANDOFF_NEXT_SESSION.md

3. Filesystem:read_text_file E:\CLAUDE\STYLE_CONTRACT.md (head 200)

4. Ticker calibrat DIN cifrele de mai sus, NU fabricate



Sentinel ești Primat?

```

## REGULI DE GENERARE

1. **NU fabrica** — dacă HANDOFF lipsește un câmp, scrie `[LIPSEȘTE]` și raportează lui Popy.

2. **NU schimba template-ul** — formatul e mecanic, copy-paste compatibil.

3. **NU adăuga** vocabular sacru, ticker SENTINEL, propuneri creative — doar fapte.

4. **DA marca** secțiuni opționale clar dacă lipsesc (ex: "Link sesiune precedentă: (fără share link, Popy va completa manual)").

5. **DA actualiza** numărul sesiunii prin auto-increment (CHAT-013 → CHAT-014).

## EXECUTION FLOW

```

REFLEX T3 trigger detectat

  ↓

read HANDOFF_NEXT_SESSION.md (head 100 lines pentru banner state)

  ↓

read SENTINEL_LAST_KNOWN_STATE.md (dacă există)

  ↓

extrage: DLG, SLG, Mod, current chat number, objective

  ↓

increment chat number (CHAT-XXX → CHAT-XXX+1)

  ↓

construiește prompt din template

  ↓

write E:\CLAUDE\agent_bridge\NEXT_SESSION_BOOTSTRAP_PROMPT.md (overwrite)

  ↓

raport la Popy: "Bootstrap prompt scris. Copiază din: agent_bridge/NEXT_SESSION_BOOTSTRAP_PROMPT.md"

```

## CROSS-REFERENCE

- HANDOFF: `E:\CLAUDE\agent_bridge\HANDOFF_NEXT_SESSION.md` (sursa state)

- LAST_KNOWN_STATE: `E:\CLAUDE\SENTINEL_LAST_KNOWN_STATE.md` (mimicry detection)

- BOOT_SEQUENCE_HARD: `E:\CLAUDE\BOOT_SEQUENCE_HARD.md` (referință tehnic în prompt)

- RITUAL_IESIRE: `E:\CLAUDE\RITUAL_IESIRE_SESIUNE.md` (parent ritual care invocă acest skill)

## ANTI-PATTERN

- ❌ Activare în mijloc de sesiune (eroare — doar la T3)

- ❌ Generare prompt fără citire empirică HANDOFF (= fabricare)

- ❌ Adăugare ticker SENTINEL în prompt (= rol jucat înainte de R-2)

- ❌ Suprascriere SENTINEL_LAST_KNOWN_STATE (= responsabilitatea altui skill, nu acesta)

- ❌ Trimitere automatică prompt — Popy face copy-paste manual


## INSTALARE


Acest skill e în `skills_drafts/`. Pentru activare în UI Anthropic:

1. Popy adaugă manual prin Settings → Skills → Add Skill

2. Upload conținutul fișierului `sentinel-reflex-t3-auto-prompt-generation - SKILL.md`

3. Confirmă activare per-project (Project Prime-Sentinel)


## VERSIUNE


v1.0 — 2026-05-07 — PRIME-CLI CODER (post Phase 2 task)