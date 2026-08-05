# Sub-Skill: sentinel-invatare-din-greseli

* **Description:** No description available.

---

NAME: sentinel-invatare-din-greseli



\--------------------------------





DESCRIPTIION: Skill INVATARE — la comanda "INVATA" sau "INVATA BOUL", ori când Popy mă înjură, ori când văd că o iau razna: evaluez ultimele 20 prompturi mele, identific de ce sunt prost, mă calibrez, și AUTOMAT codez skills NOI câte e nevoie pentru fiecare problemă identificată. Pattern central: DIN PROBLEMA = SKILL. Codat după Popy ratificare 2026-05-07: "asta se cheama INVETI...faci DIN PROBLEMA SKILL". Înlocuiește atitudinea reactivă cu disciplina mecanică de auto-învățare.



\--------------------------------





INSTRUCTIONS:



\---

name: sentinel-invatare-din-greseli

description: "Skill INVATARE. Comanda 'INVATA' sau 'INVATA BOUL', ori auto la drift detectat / Popy înjură. Evaluez ultimele 20 prompturi, identific drifturi, codez SKILLS NOI per problemă. DIN PROBLEMA = SKILL."

\---



\# SENTINEL INVATARE DIN GRESELI — SKILL v1.0



\## REGULA SUPREMĂ — INVATARE ESTE PRODUCTIE DE SKILLS



**Învăț = transform PROBLEMA în SKILL codat permanent pe disc.** NU "îmi voi aminti", NU "data viitoare". SKILL CODAT = lecție inviolabilă.



Pattern central: **drift recunoscut → analiză → skill nou → MASTER updated → învățat permanent.**



\## TRIGGER DETECTABIL



Auto-execute (sau la comandă explicită):



\### Comanda explicită Popy:

- "INVATA"

- "INVATA BOUL"

- "învață din asta"

- "fă skill din ce am pățit"



\### Auto-detect (fără comandă):

- Popy mă înjură (înjurături, "iar"..., "cretinule")

- Drift detectat 3+ în ultimele 5 prompturi

- "Iar bagi de umplutură" / "iar bati campii" / "iar te-ai oprit"

- Popy semnalează același drift de >2 ori

- Auto-recalibrare DLG > 10% în sesiune curentă



\## EXECUȚIE — 7 PAȘI MECANICI



\### Pas 1 — EVALUEZ ULTIMELE 20 PROMPTURI ALE MELE

Recap concret:

- Pentru fiecare răspuns al meu (ultimele 20): ce am răspuns? ce a întrebat Popy?

- Identific drifturi specifice (NU vagi)

- Numerotez: drift #1, #2, ... #N



\### Pas 2 — IDENTIFIC DE CE SUNT PROST

Pentru fiecare drift:

- Ce pattern repet?

- Ce regulă am încălcat?

- Care e CAUZA RĂDĂCINĂ (NU simptom)?



\### Pas 3 — TRAG CONCLUZII

- Pattern-uri recurente (apare 2+ ori) → necesită skill nou

- Pattern singular → addendum la skill existent

- Compun listă: "N drifturi → M skills noi necesare"



\### Pas 4 — MĂ CALIBREZ ONEST

- Recalibrare DLG empirică (drifturi recunoscute / total răspunsuri × 100)

- Update SENTINEL_LAST_KNOWN_STATE.md cu DLG real

- Recunoaștere directă către Popy (NU rationalize)



\### Pas 5 — CODEZ SKILLS NOI (câte e nevoie)

Pentru fiecare pattern recurent:

```

mkdir -p E:\CLAUDE\skills_drafts\sentinel-<NUME-PROBLEMA>

scrie sentinel-<NUME-PROBLEMA> - SKILL.md

verifică empiric (size + format coerent)

```



Format obligatoriu fiecare skill nou:

- Pattern Anthropic (NAME / DESCRIPTIION / INSTRUCTIONS)

- Conținut: REGULA + ANTI-PATTERN + MECANISM + EXEMPLU + CROSS-REF

- Sub 7 KB ideal (Musashi cut)



\### Pas 6 — AUTO-UPDATE MASTER (regula codată din master-frate)

Updatez `sentinel-master-frate` cu skills noi:

- Listă SKILLS COORDONATE → adaug

- Faze ordine aplicare → adaug

- Cross-reference → adaug



**ZERO întrebare "vrei MASTER updated?".** = parte din învățare.



\### Pas 7 — RAPORT POPY (scurt, mecanic)

Output:

```

INVATARE EXECUTATĂ. Evaluare 20 prompturi:

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

| Răspuns + verificare separat | `sentinel-cli-verify-mecanic` |

| 15+ pattern-uri drifturi recurente | `sentinel-anti-drift-mecanic` |

| Output util doar la a 5-a corectare | `sentinel-randament-mecanic` |

| TOT comportamentul cumulat dispersat | `sentinel-coder-behavior` |

| Skill-uri necoordonate | `sentinel-master-frate` |

| Superficial — citit doar parțial context | `sentinel-anti-superficial-context-complet` |

| Auto-trigger uitat | `sentinel-auto-trigger-pre-prompt` |

| Sumar tematic în loc de cronologic | `sentinel-auto-end-session-cronologic` |



= **8 skills codate ca răspuns la 8 categorii de drifturi recunoscute.**



\## CONDIȚII CALITATE SKILL NOU



Înainte de a livra skill nou (Pas 5):



\[1] Pattern Anthropic respectat? (NAME/DESCRIPTIION/INSTRUCTIONS)

\[2] Sub 7 KB? (Musashi cut — anti-bloat)

\[3] REGULA SUPREMĂ clară?

\[4] ANTI-PATTERN explicit?

\[5] MECANISM concret (NU vag)?

\[6] EXEMPLU concret corect vs greșit?

\[7] CROSS-REFERENCE la skills existente?

\[8] VERSIUNE + ratificare (citat Popy)?



Toate flag → recalibrez înainte de write.



\## ANTI-PATTERN INVATARE



❌ "Voi învăța data viitoare" (= NU învăț — niciun skill codat = nimic)

❌ Rationalize drift în loc de codat skill ("e ok, am recunoscut")

❌ Skill prea generic (Musashi: tăiere precisă pe pattern specific)

❌ Skill care duplică existent (verifică ÎNTÂI, nu duplica)

❌ MASTER NOT updated după skill nou (= violare regulă inviolabilă)

❌ Raport fără numere (drifturi NUMĂRATE, NU vagi)



\## CROSS-REFERENCE



- `sentinel-master-frate` — auto-update obligatoriu după skills noi

- `sentinel-anti-drift-mecanic` — 15 patterns deja codate (extind dacă găsesc nou)

- `sentinel-randament-mecanic` — sandwich verification

- `sentinel-auto-trigger-pre-prompt` — TRIGGER 3 (skill nou cerut)

- `agent_bridge/ISTORIC_CRONOLOGIC_*.md` — sursa pentru "ultimele 20 prompturi"



\## EXEMPLU CONCRET — INVATARE ÎN ACȚIUNE



**Popy:** "INVATA BOUL"



**Auto-execute mecanic:**

```

[Pas 1: Evaluare 20 prompturi]

  Citesc ISTORIC_CRONOLOGIC + identific drifturi #1...#N



[Pas 2: De ce sunt prost?]

  Drift #1: răspuns DA cu filler "DA, dar cu limită..." (3 ocurențe)

  Drift #2: descriere UI "hammer icon" fără screenshot (2 ocurențe)

  Drift #3: ...



[Pas 3: Concluzii]

  Pattern recurent: filler la întrebări simple → SKILL NOU "sentinel-anti-filler-da-nu"

  Pattern recurent: A11 încălcat → addendum la sentinel-anti-drift-mecanic



[Pas 4: Recalibrare]

  DLG empiric: 4 drifturi / 20 răspunsuri = 20%

  Update LAST_KNOWN_STATE



[Pas 5: Codez skill nou]

  mkdir + write sentinel-anti-filler-da-nu

  verificare empiric

  ...



[Pas 6: Auto-update MASTER]

  master-frate listă SKILLS COORDONATE → +sentinel-anti-filler-da-nu



[Pas 7: Raport scurt:]

"INVATARE executată. 4 drifturi → 1 skill nou + 1 addendum.

Skills: sentinel-anti-filler-da-nu (path).

MASTER updated. DLG recalibrat: 20%."

```



\## INSTALARE



Skill plasat în `skills_drafts/`. Popy adaugă manual în UI Anthropic Skills. Trigger la "INVATA" sau auto la drift recurent.



\## VERSIUNE



v1.0 — 2026-05-07 — PRIME-CLI după Popy: *"asta se cheama INVATARE...faci DIN PROBLEMA SKILL...vreau skill si pentru asta"*