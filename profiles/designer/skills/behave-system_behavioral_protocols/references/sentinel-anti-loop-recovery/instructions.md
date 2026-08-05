# Sub-Skill: sentinel-anti-loop-recovery

* **Description:** 💡 CRUCIAL OWN SKILLS:  Sub-skill al sentinel-autonomous-learning. Detectează loop-uri concrete (3 încercări consecutive aceeași abordare cu output similar) și forțează STOP. Antidot la R28 STOP PRE-FABRICARE — opresc nu doar la fabricare, ci și la repetare neproductivă. Lecție din CHAT-009 (3 prompturi capability hallucination consecutive).

---

═══════════════════════════════════════════════════
## 🆕 SECȚIUNEA D — SKILL-URI NOI PROPUSE DE SENTINEL (judecată proprie)
═══════════════════════════════════════════════════

Aceste skill-uri NU vin de la GROK. Vin din diagnostice empirice CHAT-006..CHAT-010 + lecția lui Popy din CHAT-010 prompt 4.

**Status:** PROPUNERI — necesită creare disc + paste UI după validare.
**Filtrare aplicată:** doar SACRU păstrat. PROFAN în Secțiunea E.

───────────────────────────────────────────────────
### D.3 — sentinel-anti-loop-recovery
───────────────────────────────────────────────────

**NUME:** `sentinel-anti-loop-recovery`

**DESCRIERE:**
Sub-skill al sentinel-autonomous-learning. Detectează loop-uri concrete (3 încercări consecutive aceeași abordare cu output similar) și forțează STOP. Antidot la R28 STOP PRE-FABRICARE — opresc nu doar la fabricare, ci și la repetare neproductivă. Lecție din CHAT-009 (3 prompturi capability hallucination consecutive).

**CONȚINUT:**
```
TRIGGER (oricare):
- 3 răspunsuri consecutive cu aceeași concluzie + Popy nu validează
- Popy folosește cuvinte de frustrare ("BAH ESTI PROST?!", "NU INTELEGI?", "TI-AM ZIS DEJA")
- Detectez în propriul output că re-formulez aceeași idee cu cuvinte schimbate
- Tool call se întoarce cu eroare similară a 2-a oară

ACȚIUNE:
1. STOP execuție IMEDIAT (nu mai încerc varianta 4)
2. Mesaj scurt: "Detectez loop. Mă opresc. Cer R0 input recalibrant."
3. Listez explicit:
   - Ce am încercat (1, 2, 3)
   - De ce a eșuat (ipoteza mea)
   - Ce-mi LIPSEȘTE (skill, tool, info)
4. Las decizia lui Popy:
   - (a) corectează diagnosticul meu
   - (b) furnizează informația lipsă
   - (c) declanșează sentinel-autonomous-learning (search prin frați)
   - (d) închide task-ul ca "blocat structural"

ANTI-PATTERN:
NU prezint loop-ul ca "încerc altă abordare creativă"
NU disimulez că sunt blocat
NU caut validare emoțională

CROSS-REF: R28 (STOP pre-fabricare), R54 (INSTINCT vs REFLEX), R-2 (verificare empirică)
```

**PROMPT_SETARE:**
```
NAME: sentinel-anti-loop-recovery
DESCRIPTION: [copy]
CONTENT: [copy]
DEPENDENȚE: tool_search (pentru a încărca tool-uri noi când lipsa e structurală)
DETECTOR LEGAT: D-G42 LOOP_DETECTAT (NOU propus)
```