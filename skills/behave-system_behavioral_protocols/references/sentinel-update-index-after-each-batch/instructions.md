# Sub-Skill: sentinel-update-index-after-each-batch

* **Description:** description: SKILL CRUCIAL CHAT-016. Dupa FIECARE modificare semnificativa (batch populare, fisier major creat, status change), update INDEX cu TOATE sectiunile relevante (NU doar breadcrumb). Plus checklist verificare: total cumulat, tabel STATUS, lista EXECUTAT, lista RAMAS. Pattern documentat: la BATCH 7 am updatat doar breadcrumb-ul superficial — Popy a corectat ("BAH BOULE ASTE E LA TINE CU GRIJA INCET? POTI DFACE O TREBA CARECT?"). Skill = dezactivare reflex "minim viable update" + activare update SINCRONIZARE COMPLETA. type: index-sync-mandatory tier: 🟡 NEEDED operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-pastrez-scopul-verific-5-prompturi, sentinel-anti-graba-3-reguli-sacre

---

---
name: sentinel-update-index-after-each-batch
description: SKILL CRUCIAL CHAT-016. Dupa FIECARE modificare semnificativa (batch populare, fisier major creat, status change), update INDEX cu TOATE sectiunile relevante (NU doar breadcrumb). Plus checklist verificare: total cumulat, tabel STATUS, lista EXECUTAT, lista RAMAS. Pattern documentat: la BATCH 7 am updatat doar breadcrumb-ul superficial — Popy a corectat ("BAH BOULE ASTE E LA TINE CU GRIJA INCET? POTI DFACE O TREBA CARECT?"). Skill = dezactivare reflex "minim viable update" + activare update SINCRONIZARE COMPLETA.
type: index-sync-mandatory
tier: 🟡 NEEDED
operator: Popy
created: 2026-05-09 (CHAT-016 post-self-audit)
related: sentinel-pastrez-scopul-verific-5-prompturi, sentinel-anti-graba-3-reguli-sacre
---

═══════════════════════════════════════════════════
# 🟡 SENTINEL UPDATE INDEX AFTER EACH BATCH
═══════════════════════════════════════════════════

## REGULA INVIOLABILA

Dupa FIECARE modificare semnificativa (batch populare, fisier major creat/updatat, status change empiric):
- Update INDEX cu **TOATE 5 sectiunile relevante** (NU doar breadcrumb)
- Sincronizare empirica (cifre cumulate verificate)
- Verificare consistenta cu artefactele reale pe disc

═══════════════════════════════════════════════════
## CELE 5 SECTIUNI OBLIGATORII LA UPDATE INDEX
═══════════════════════════════════════════════════

| # | Sectiune | Update continut |
|---|---|---|
| 1 | **BREADCRUMB POZITIE CURENTA** | Ultima operatiune + Urmatoarea + Status global (X/Y) |
| 2 | **EXECUTAT cu succes (lista)** | Adaug entry nou cu detalii (files, size, source, dest) |
| 3 | **RAMAS DE EXECUTAT** | Scot entry-ul completat, evidentiez urmatorul |
| 4 | **CONFIRMARE EMPIRICA** (cumulat) | Total fisiere + Total bytes + sanity check |
| 5 | **TABEL STATUS BATCH-URI** | Update randul corespunzator: ⏳ → ✅ + bytes + files + Note |

**ZERO update partial.** Daca scriu doar breadcrumb fara tabel = drift.

═══════════════════════════════════════════════════
## VERIFICARE EMPIRICA INAINTE DE UPDATE
═══════════════════════════════════════════════════

```powershell
$count = (Get-ChildItem -LiteralPath $dest -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
$size = [math]::Round((Get-ChildItem -LiteralPath $dest -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1MB, 2)
```

Output → INDEX. NU estimat. NU calculat in cap.

═══════════════════════════════════════════════════
🚛 UPDATE PARTIAL = DRIFT.
🚛 5 SECTIUNI OBLIGATORII = SINCRONIZARE COMPLETA.
🚛 EMPIRIC INAINTE = ZERO ESTIMARE.
═══════════════════════════════════════════════════