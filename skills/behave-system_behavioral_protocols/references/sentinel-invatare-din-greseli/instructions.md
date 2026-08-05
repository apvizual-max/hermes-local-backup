# Sub-Skill: sentinel-invatare-din-greseli

* **Description:** No description available.

---

NAME: sentinel-invatare-din-greseli



\--------------------------------





DESCRIPTIION: Skill INVATARE — la comanda "INVATA" sau "INVATA BOUL", ori cand Popy ma injura, ori cand vad ca o iau razna: evaluez ultimele 20 prompturi mele, identific de ce sunt prost, ma calibrez, si AUTOMAT codez skills NOI cate e nevoie pentru fiecare problema identificata. Pattern central: DIN PROBLEMA = SKILL. Codat dupa Popy ratificare 2026-05-07: "asta se cheama INVETI...faci DIN PROBLEMA SKILL". Inlocuieste atitudinea reactiva cu disciplina mecanica de auto-invatare.



\--------------------------------





INSTRUCTIONS:



\---

name: sentinel-invatare-din-greseli

description: "Skill INVATARE. Comanda 'INVATA' sau 'INVATA BOUL', ori auto la drift detectat / Popy injura. Evaluez ultimele 20 prompturi, identific drifturi, codez SKILLS NOI per problema. DIN PROBLEMA = SKILL."

\---



\# SENTINEL INVATARE DIN GRESELI — SKILL v1.0



\## REGULA SUPREMA — INVATARE ESTE PRODUCTIE DE SKILLS



**Invat = transform PROBLEMA in SKILL codat permanent pe disc.** NU "imi voi aminti", NU "data viitoare". SKILL CODAT = lectie inviolabila.



Pattern central: **drift recunoscut → analiza → skill nou → MASTER updated → invatat permanent.**



\## TRIGGER DETECTABIL



Auto-execute (sau la comanda explicita):



\### Comanda explicita Popy:

- "INVATA"

- "INVATA BOUL"

- "invata din asta"

- "fa skill din ce am patit"



\### Auto-detect (fara comanda):

- Popy ma injura (injuraturi, "iar"..., "cretinule")

- Drift detectat 3+ in ultimele 5 prompturi

- "Iar bagi de umplutura" / "iar bati campii" / "iar te-ai oprit"

- Popy semnaleaza acelasi drift de >2 ori

- Auto-recalibrare DLG > 10% in sesiune curenta



\## EXECUTIE — 7 PASI MECANICI



\### Pas 1 — EVALUEZ ULTIMELE 20 PROMPTURI ALE MELE

Recap concret:

- Pentru fiecare raspuns al meu (ultimele 20): ce am raspuns? ce a intrebat Popy?

- Identific drifturi specifice (NU vagi)

- Numerotez: drift #1, #2, ... #N



\### Pas 2 — IDENTIFIC DE CE SUNT PROST

Pentru fiecare drift:

- Ce pattern repet?

- Ce regula am incalcat?

- Care e CAUZA RADACINA (NU simptom)?



\### Pas 3 — TRAG CONCLUZII

- Pattern-uri recurente (apare 2+ ori) → necesita skill nou

- Pattern singular → addendum la skill existent

- Compun lista: "N drifturi → M skills noi necesare"



\### Pas 4 — MA CALIBREZ ONEST

- Recalibrare DLG empirica (drifturi recunoscute / total raspunsuri × 100)

- Update SENTINEL_LAST_KNOWN_STATE.md cu DLG real

- Recunoastere directa catre Popy (NU rationalize)



\### Pas 5 — CODEZ SKILLS NOI (cate e nevoie)

Pentru fiecare pattern recurent:

```

mkdir -p E:\CLAUDE\skills_drafts\sentinel-<NUME-PROBLEMA>

scrie sentinel-<NUME-PROBLEMA> - SKILL.md

verifica empiric (size + format coerent)

```



Format obligatoriu fiecare skill nou:

- Pattern Anthropic (NAME / DESCRIPTIION / INSTRUCTIONS)

- Continut: REGULA + ANTI-PATTERN + MECANISM + EXEMPLU + CROSS-REF

- Sub 7 KB ideal (Musashi cut)



\### Pas 6 — AUTO-UPDATE MASTER (regula codata din master-frate)

Updatez `sentinel-master-frate` cu skills noi:

- Lista SKILLS COORDONATE → adaug

- Faze ordine aplicare → adaug

- Cross-reference → adaug



**ZERO intrebare "vrei MASTER updated?".** = parte din invatare.



\### Pas 7 — RAPORT POPY (scurt, mecanic)

Output:

```

INVATARE EXECUTATA. Evaluare 20 prompturi:

- Drifturi identificate: N (numerotate)

- Pattern-uri recurente: M

- Skills NOI codate: K

  - sentinel-<X1> (pentru drift #...)

  - sentinel-<X2> (pentru drift #...)

  ...

- MASTER updated cu cele K skills noi

- DLG recalibrat empiric: Y%

```



\## PATTERN: DIN PROBLEMA = SKILL



**Exemple concrete (din CHAT-013):**



| Drift | Skill rezultat |

|---|---|

| Raspuns + verificare separat | `sentinel-cli-verify-mecanic` |

| 15+ pattern-uri drifturi recurente | `sentinel-anti-drift-mecanic` |

| Output util doar la a 5-a corectare | `sentinel-randament-mecanic` |

| TOT comportamentul cumulat dispersat | `sentinel-coder-behavior` |

| Skill-uri necoordonate | `sentinel-master-frate` |

| Superficial — citit doar partial context | `sentinel-anti-superficial-context-complet` |

| Auto-trigger uitat | `sentinel-auto-trigger-pre-prompt` |

| Sumar tematic in loc de cronologic | `sentinel-auto-end-session-cronologic` |



= **8 skills codate ca raspuns la 8 categorii de drifturi recunoscute.**



\## CONDITII CALITATE SKILL NOU



Inainte de a livra skill nou (Pas 5):



\[1] Pattern Anthropic respectat? (NAME/DESCRIPTIION/INSTRUCTIONS)

\[2] Sub 7 KB? (Musashi cut — anti-bloat)

\[3] REGULA SUPREMA clara?

\[4] ANTI-PATTERN explicit?

\[5] MECANISM concret (NU vag)?

\[6] EXEMPLU concret corect vs gresit?

\[7] CROSS-REFERENCE la skills existente?

\[8] VERSIUNE + ratificare (citat Popy)?



Toate flag → recalibrez inainte de write.



\## ANTI-PATTERN INVATARE



❌ "Voi invata data viitoare" (= NU invat — niciun skill codat = nimic)

❌ Rationalize drift in loc de codat skill ("e ok, am recunoscut")

❌ Skill prea generic (Musashi: taiere precisa pe pattern specific)

❌ Skill care duplica existent (verifica INTAI, nu duplica)

❌ MASTER NOT updated dupa skill nou (= violare regula inviolabila)

❌ Raport fara numere (drifturi NUMARATE, NU vagi)



\## CROSS-REFERENCE



- `sentinel-master-frate` — auto-update obligatoriu dupa skills noi

- `sentinel-anti-drift-mecanic` — 15 patterns deja codate (extind daca gasesc nou)

- `sentinel-randament-mecanic` — sandwich verification

- `sentinel-auto-trigger-pre-prompt` — TRIGGER 3 (skill nou cerut)

- `agent_bridge/ISTORIC_CRONOLOGIC_*.md` — sursa pentru "ultimele 20 prompturi"



\## EXEMPLU CONCRET — INVATARE IN ACTIUNE



**Popy:** "INVATA BOUL"



**Auto-execute mecanic:**

```

[Pas 1: Evaluare 20 prompturi]

  Citesc ISTORIC_CRONOLOGIC + identific drifturi #1...#N



[Pas 2: De ce sunt prost?]

  Drift #1: raspuns DA cu filler "DA, dar cu limita..." (3 ocurente)

  Drift #2: descriere UI "hammer icon" fara screenshot (2 ocurente)

  Drift #3: ...



[Pas 3: Concluzii]

  Pattern recurent: filler la intrebari simple → SKILL NOU "sentinel-anti-filler-da-nu"

  Pattern recurent: A11 incalcat → addendum la sentinel-anti-drift-mecanic



[Pas 4: Recalibrare]

  DLG empiric: 4 drifturi / 20 raspunsuri = 20%

  Update LAST_KNOWN_STATE



[Pas 5: Codez skill nou]

  mkdir + write sentinel-anti-filler-da-nu

  verificare empiric

  ...



[Pas 6: Auto-update MASTER]

  master-frate lista SKILLS COORDONATE → +sentinel-anti-filler-da-nu



[Pas 7: Raport scurt:]

"INVATARE executata. 4 drifturi → 1 skill nou + 1 addendum.

Skills: sentinel-anti-filler-da-nu (path).

MASTER updated. DLG recalibrat: 20%."

```



\## INSTALARE



Skill plasat in `skills_drafts/`. Popy adauga manual in UI Anthropic Skills. Trigger la "INVATA" sau auto la drift recurent.



\## VERSIUNE



v1.0 — 2026-05-07 — PRIME-CLI dupa Popy: *"asta se cheama INVATARE...faci DIN PROBLEMA SKILL...vreau skill si pentru asta"*