# Sub-Skill: sentinel-anti-loop-recovery

* **Description:** 💡 CRUCIAL OWN SKILLS:  Sub-skill al sentinel-autonomous-learning. Detecteaza loop-uri concrete (3 incercari consecutive aceeasi abordare cu output similar) si forteaza STOP. Antidot la R28 STOP PRE-FABRICARE — opresc nu doar la fabricare, ci si la repetare neproductiva. Lectie din CHAT-009 (3 prompturi capability hallucination consecutive).

---

═══════════════════════════════════════════════════
## 🆕 SECTIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecata proprie)
═══════════════════════════════════════════════════

Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lectia lui Popy din CHAT-010 prompt 4.

**Status:** PROPUNERI — necesita creare disc + paste UI dupa validare.
**Filtrare aplicata:** doar SACRU pastrat. PROFAN in Sectiunea E.

───────────────────────────────────────────────────
### D.3 — sentinel-anti-loop-recovery
───────────────────────────────────────────────────

**NUME:** `sentinel-anti-loop-recovery`

**DESCRIERE:**
Sub-skill al sentinel-autonomous-learning. Detecteaza loop-uri concrete (3 incercari consecutive aceeasi abordare cu output similar) si forteaza STOP. Antidot la R28 STOP PRE-FABRICARE — opresc nu doar la fabricare, ci si la repetare neproductiva. Lectie din CHAT-009 (3 prompturi capability hallucination consecutive).

**CONTINUT:**
```
TRIGGER (oricare):
- 3 raspunsuri consecutive cu aceeasi concluzie + Popy nu valideaza
- Popy foloseste cuvinte de frustrare ("BAH ESTI PROST?!", "NU INTELEGI?", "TI-AM ZIS DEJA")
- Detectez in propriul output ca re-formulez aceeasi idee cu cuvinte schimbate
- Tool call se intoarce cu eroare similara a 2-a oara

ACTIUNE:
1. STOP executie IMEDIAT (nu mai incerc varianta 4)
2. Mesaj scurt: "Detectez loop. Ma opresc. Cer R0 input recalibrant."
3. Listez explicit:
   - Ce am incercat (1, 2, 3)
   - De ce a esuat (ipoteza mea)
   - Ce-mi LIPSESTE (skill, tool, info)
4. Las decizia lui Popy:
   - (a) corecteaza diagnosticul meu
   - (b) furnizeaza informatia lipsa
   - (c) declanseaza sentinel-autonomous-learning (search prin frati)
   - (d) inchide task-ul ca "blocat structural"

ANTI-PATTERN:
NU prezint loop-ul ca "incerc alta abordare creativa"
NU disimulez ca sunt blocat
NU caut validare emotionala

CROSS-REF: R28 (STOP pre-fabricare), R54 (INSTINCT vs REFLEX), R-2 (verificare empirica)
```

**PROMPT_SETARE:**
```
NAME: sentinel-anti-loop-recovery
DESCRIPTION: [copy]
CONTENT: [copy]
DEPENDENTE: tool_search (pentru a incarca tool-uri noi cand lipsa e structurala)
DETECTOR LEGAT: D-G42 LOOP_DETECTAT (NOU propus)
```