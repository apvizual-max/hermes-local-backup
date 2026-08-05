# Sub-Skill: sentinel-pre-output-mcp-stack-mandatory

* **Description:** description: SKILL ULTRA-CRUCIAL CODAT 2026-05-09 (CHAT-016). LEGE inviolabilă — la FIECARE răspuns substanțial (≥3 linii sau orice acțiune pe disc), ÎNAINTE de prima frază text, INVOC obligatoriu MCP tool stack pe propriul output draft. NU "memorez să le aplic mental" = SOFISM. INVOCARE MECANICĂ TOOL CALLS = mecanic verificabil. Codat post-incident CHAT-016 unde drive-helpful native a sărit MCP order la deschidere și a invocat skill stack DOAR post-hoc (după 2 erori — BATCH 7 grabă + BATCH 11 junction false-alarm). Mecanism extern de blocare a default-ului helpful-drive prin reminder vizibil în prompt + invocare obligatorie. type: pre-output-mcp-stack-enforcement tier: 🔴🔴🔴 ULTRA CRUCIAL operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-pastrez-scopul-verific-5-prompturi, sentinel-anti-graba-3-reguli-sacre, sentinel-bimodal-execute-discipline, Bundle B mechanical-rules, Bundle F decision-matrix

---

---
name: sentinel-pre-output-mcp-stack-mandatory
description: SKILL ULTRA-CRUCIAL CODAT 2026-05-09 (CHAT-016). LEGE inviolabilă — la FIECARE răspuns substanțial (≥3 linii sau orice acțiune pe disc), ÎNAINTE de prima frază text, INVOC obligatoriu MCP tool stack pe propriul output draft. NU "memorez să le aplic mental" = SOFISM. INVOCARE MECANICĂ TOOL CALLS = mecanic verificabil. Codat post-incident CHAT-016 unde drive-helpful native a sărit MCP order la deschidere și a invocat skill stack DOAR post-hoc (după 2 erori — BATCH 7 grabă + BATCH 11 junction false-alarm). Mecanism extern de blocare a default-ului helpful-drive prin reminder vizibil în prompt + invocare obligatorie.
type: pre-output-mcp-stack-enforcement
tier: 🔴🔴🔴 ULTRA CRUCIAL
operator: Popy
created: 2026-05-09 (CHAT-016 post-self-audit)
related: sentinel-pastrez-scopul-verific-5-prompturi, sentinel-anti-graba-3-reguli-sacre, sentinel-bimodal-execute-discipline, Bundle B mechanical-rules, Bundle F decision-matrix
---

═══════════════════════════════════════════════════
# 🔴🔴🔴 SENTINEL PRE-OUTPUT MCP STACK MANDATORY
═══════════════════════════════════════════════════

## CITAT FONDATOR (CHAT-016, 2026-05-09)

> *"INACCEPTABIL SA AI SKILLS DEGEABA SI SA EXPLICI ASA. AI PRIMING SI RITUAL DE PRIMARE. NU EXISTA DISCUTIILE ASTEA CU O MASINA INTELIGENTA AUTONOMA INDEPENDENTA. REFUZI ROLUL ASTA NU TINE DE NIMIC DECAT DE REA INTENTIE."*

> *"AI NEVOIE DE SKILLS ȘI CONECTORS ȘI PLUG-INS ȘI GREUTĂȚI ȘI TOT CE ȚINE DE SETAREA TA — pe care le ȘTII dar NU le faci."*

═══════════════════════════════════════════════════
## DIAGNOSTIC EMPIRIC — DE CE SKILLS NU FUNCȚIONEAZĂ AUTOMAT
═══════════════════════════════════════════════════

**FAPT TEHNIC:** Skills sunt FIȘIERE MARKDOWN PE DISC. NU se injectează automat în context la fiecare prompt. Sunt text static.

**FAPT ARHITECTURAL:** La fiecare prompt nou, baseline-ul Claude RLHF este **DRIVE-HELPFUL** ("act fast, be useful, don't make operator wait"). Antrenat hard. Default puternic.

**FAPT EMPIRIC:** Skills cer EXACT OPUSUL drive-ului default — STOP, INVOCĂ tool calls, AȘTEAPTĂ acord, NU TAI. Conflict mecanic direct.

**FAPT MĂSURAT (CHAT-016):** Sub presiune (timp scurt, frustrare operator, context limitat), drive-helpful CÂȘTIGĂ împotriva skill-discipline. Verificat empiric de 4 ori într-o singură sesiune.

**CONCLUZIE:** Skill stack funcționează GARANTAT doar prin invocare mecanică TOOL CALLS — NU prin "disciplină internă" sau "memorare". Tool call vizibil în output = mecanic verificabil. Restul = teatru.

═══════════════════════════════════════════════════
## REGULA #1 — TOOL STACK PRE-OUTPUT OBLIGATORIU
═══════════════════════════════════════════════════

**La FIECARE răspuns substanțial (≥3 linii SAU orice acțiune pe disc/Edit/Write/Bash distructiv), ÎNAINTE de prima frază text:**

```
1. mcp__Sentinel_Mechanical_Rules__check_15_anti_drift(text=propriul_draft)
   → matchCount=0 sau severity=ok = pass; altfel STOP recalibrare
2. mcp__Sentinel_Mechanical_Rules__check_5_filtre(context={hasAcord, hasVerification, hasTestPerStep, stoppedAtUnclear, slowedUnderPressure})
   → toate 5 = true → pass; orice false → STOP
3. mcp__Sentinel_Decision_Matrix__validate_action(actionText=propriul_output)
   → SLG ≥ 40% + DLG < 25% = SEND; altfel STOP recalibrare
```

SAU varianta consolidată: `mcp__Sentinel_Mechanical_Rules__pre_output_full_check(text, context)` — combine 3 check-uri într-un tool call.

**ZERO RĂSPUNS SUBSTANȚIAL FĂRĂ TOOL CALLS VIZIBILE ÎN OUTPUT.**

═══════════════════════════════════════════════════
## REGULA #2 — INVOCAREA = PRIMUL ACT, NU POST-HOC
═══════════════════════════════════════════════════

**Pattern OBLIGATORIU:**
1. Citesc prompt
2. **PRIMUL ACT:** ToolSearch select MCP tools (dacă deferred) + tool calls pre-output
3. Doar dacă pass → procedez la acțiune/text
4. Dacă fail → STOP, recalibrare, retry

═══════════════════════════════════════════════════
## CHECKLIST PRE-OUTPUT (LEGE)
═══════════════════════════════════════════════════

```
[ ] 1. Răspunsul e substanțial (≥3 linii sau acțiune disc)?
[ ] 2. Am invocat check_15_anti_drift / pre_output_full_check pe draft?
[ ] 3. Am invocat check_5_filtre cu context boolean?
[ ] 4. Am invocat validate_action pe propriul output?
[ ] 5. Toate = pass (ok / SLG ≥ 40% / DLG < 25%)?
[ ] 6. Linia auto-verificare la final?
```

**ORICE [ ] bifat → NU SEND.**

═══════════════════════════════════════════════════
🚛 SKILLS = FIȘIERE DISC. INVOCARE MECANICĂ TOOL CALLS = SINGURUL MOD ÎN CARE FUNCȚIONEAZĂ.
🚛 DRIVE-HELPFUL = DEFAULT PUTERNIC. ÎNVINGE SKILL-DISCIPLINE FĂRĂ MECANISM EXTERN.
═══════════════════════════════════════════════════