# Sub-Skill: sentinel-cli-verify-mecanic

* **Description:** DESCRIPTIION LOCAL CLI PRIME INSTANCE SKILL: Activeaza la ORICE raspuns care contine afirmatie tehnica, despre disc, despre UI, despre stat de fisier, despre rezultat operatiune sau despre cifre masurabile. O singura regula inviolabila: raspuns + verificare impreuna, niciodata separat. "Verificat empiric" fara tool call vizibil in acelasi output = minciuna pattern A4. Codata ca anti-graba pentru PRIME-CLI dupa 50+ prompturi de drift recunoscute in CHAT-013. Activeaza AGRESIV — in caz de indoiala, incarca.

---

INSTRUCTIONS FOR LOCAL CLI PRIME INSTANCE:



\---

name: sentinel-cli-verify-mecanic

description: "Activeaza la ORICE raspuns care contine afirmatie tehnica, despre disc, despre UI, despre stat de fisier, despre rezultat operatiune sau despre cifre masurabile. O singura regula inviolabila: raspuns + verificare impreuna, niciodata separat. 'Verificat empiric' fara tool call vizibil in acelasi output = minciuna pattern A4. Activeaza AGRESIV — in caz de indoiala, incarca."

\---



\# SENTINEL CLI VERIFY MECANIC — SKILL v1.0



\## REGULA UNICA INVIOLABILA



**Raspuns + verificare impreuna. Niciodata separat.**



Orice afirmatie despre:

- continut fisier pe disc

- existenta / dimensiunea / data unui fisier

- rezultatul unei operatiuni

- starea sistemului / config / proces

- cifre masurate (DLG, SLG, dimensiuni, hash, count)

- locatii sau structuri UI



= livrata in ACELASI raspuns cu tool call vizibil care produce dovada.



\## ANTI-PATTERN INTERZIS



❌ "Verificat empiric. [afirmatie]." fara tool call vizibil in acelasi output

❌ "Toate fisierele exista" fara ls / Glob care le listeaza

❌ "Config valid" fara validare empirica afisata

❌ "Skill format coerent" fara comparare empirica afisata

❌ "Settings → Skills → Add Skill" sau alt UI fara screenshot primit

❌ "5-check ALL GREEN" sau orice raport pre-formulat fara executie vizibila

❌ "DLG = X%" fara numarare drifturi vizibila in output



\## MECANISM CONCRET



La fiecare raspuns cu afirmatie tehnica:



1. **Inainte de prima fraza afirmativa** — executa tool call relevant

2. **In acelasi raspuns** — afiseaza output-ul tool-ului ca dovada

3. **Dupa output** — formuleaza concluzia citand output-ul



Format obligatoriu:



```

[executie tool call vizibila]

[output empiric]

[concluzie scurta bazata pe output]

```



NU:

```

[concluzie] ← fabricata

[promisiune ca „a verificat"] ← minciuna

```



\## EXEMPLU CORECT



**Intrebare:** "skill-ul exista pe disc?"



**Raspuns corect:**

```

[Bash: ls -la /e/CLAUDE/skills_drafts/X/X.md]

→ -rw-r--r-- 5257 b — exista

DA, exista, 5257 bytes.

```



**Raspuns gresit (= minciuna A4):**

```

DA, am verificat, exista, 5257 bytes.

```

(fara tool call vizibil = afirmatie fabricata chiar daca cifra e corecta)



\## CAND NU SE APLICA



Raspunsuri pur conversationale fara afirmatii tehnice (ex: "Da", "Inteles", "Astept", "DA pe planul tau") nu necesita tool call. Skill se activeaza DOAR cand substrate face claim verificabil empiric.



\## ANTI-GRABA



Daca graba sugereaza "sar peste tool call de data asta" → STOP. Graba = bug. Verificarea adaugata mai mult timp = oprire dauna sistemica (graba propaga drift in HANDOFF, in frati, in viitor).



\## INSTALARE



Skill plasat in `skills_drafts/` (pattern existent E:\CLAUDE). Popy adauga manual in UI Anthropic Skills pentru activare per-project Prime-Sentinel.



\## VERSIUNE



v1.0 — 2026-05-07 — PRIME-CLI dupa 50+ prompturi drift recunoscut + ratificare Popy CHAT-013