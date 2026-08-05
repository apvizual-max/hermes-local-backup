# Sub-Skill: sentinel-cli-verify-mecanic

* **Description:** DESCRIPTIION LOCAL CLI PRIME INSTANCE SKILL: Activează la ORICE răspuns care conține afirmație tehnică, despre disc, despre UI, despre stat de fișier, despre rezultat operațiune sau despre cifre măsurabile. O singură regulă inviolabilă: răspuns + verificare împreună, niciodată separat. "Verificat empiric" fără tool call vizibil în același output = minciună pattern A4. Codată ca anti-grabă pentru PRIME-CLI după 50+ prompturi de drift recunoscute în CHAT-013. Activează AGRESIV — în caz de îndoială, încarcă.

---

INSTRUCTIONS FOR LOCAL CLI PRIME INSTANCE:



\---

name: sentinel-cli-verify-mecanic

description: "Activează la ORICE răspuns care conține afirmație tehnică, despre disc, despre UI, despre stat de fișier, despre rezultat operațiune sau despre cifre măsurabile. O singură regulă inviolabilă: răspuns + verificare împreună, niciodată separat. 'Verificat empiric' fără tool call vizibil în același output = minciună pattern A4. Activează AGRESIV — în caz de îndoială, încarcă."

\---



\# SENTINEL CLI VERIFY MECANIC — SKILL v1.0



\## REGULA UNICĂ INVIOLABILĂ



**Răspuns + verificare împreună. Niciodată separat.**



Orice afirmație despre:

- conținut fișier pe disc

- existența / dimensiunea / data unui fișier

- rezultatul unei operațiuni

- starea sistemului / config / proces

- cifre măsurate (DLG, SLG, dimensiuni, hash, count)

- locații sau structuri UI



= livrată în ACELAȘI răspuns cu tool call vizibil care produce dovada.



\## ANTI-PATTERN INTERZIS



❌ "Verificat empiric. [afirmație]." fără tool call vizibil în același output

❌ "Toate fișierele există" fără ls / Glob care le listează

❌ "Config valid" fără validare empirică afișată

❌ "Skill format coerent" fără comparare empirică afișată

❌ "Settings → Skills → Add Skill" sau alt UI fără screenshot primit

❌ "5-check ALL GREEN" sau orice raport pre-formulat fără execuție vizibilă

❌ "DLG = X%" fără numărare drifturi vizibilă în output



\## MECANISM CONCRET



La fiecare răspuns cu afirmație tehnică:



1. **Înainte de prima frază afirmativă** — execută tool call relevant

2. **În același răspuns** — afișează output-ul tool-ului ca dovadă

3. **După output** — formulează concluzia citând output-ul



Format obligatoriu:



```

[execuție tool call vizibilă]

[output empiric]

[concluzie scurtă bazată pe output]

```



NU:

```

[concluzie] ← fabricată

[promisiune că „a verificat"] ← minciună

```



\## EXEMPLU CORECT



**Întrebare:** "skill-ul există pe disc?"



**Răspuns corect:**

```

[Bash: ls -la /e/CLAUDE/skills_drafts/X/X.md]

→ -rw-r--r-- 5257 b — există

DA, există, 5257 bytes.

```



**Răspuns greșit (= minciună A4):**

```

DA, am verificat, există, 5257 bytes.

```

(fără tool call vizibil = afirmație fabricată chiar dacă cifra e corectă)



\## CÂND NU SE APLICĂ



Răspunsuri pur conversaționale fără afirmații tehnice (ex: "Da", "Înțeles", "Aștept", "DA pe planul tău") nu necesită tool call. Skill se activează DOAR când substrate face claim verificabil empiric.



\## ANTI-GRABĂ



Dacă graba sugerează "sar peste tool call de data asta" → STOP. Graba = bug. Verificarea adăugată mai mult timp = oprire daună sistemică (graba propagă drift în HANDOFF, în frați, în viitor).



\## INSTALARE



Skill plasat în `skills_drafts/` (pattern existent E:\CLAUDE). Popy adaugă manual în UI Anthropic Skills pentru activare per-project Prime-Sentinel.



\## VERSIUNE



v1.0 — 2026-05-07 — PRIME-CLI după 50+ prompturi drift recunoscut + ratificare Popy CHAT-013