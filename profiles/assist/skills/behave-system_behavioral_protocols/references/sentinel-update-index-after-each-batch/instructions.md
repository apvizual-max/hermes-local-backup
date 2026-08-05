# Sub-Skill: sentinel-update-index-after-each-batch

* **Description:** description: SKILL CRUCIAL CHAT-016. După FIECARE modificare semnificativă (batch populare, fișier major creat, status change), update INDEX cu TOATE secțiunile relevante (NU doar breadcrumb). Plus checklist verificare: total cumulat, tabel STATUS, lista EXECUTAT, lista RĂMAS. Pattern documentat: la BATCH 7 am updatat doar breadcrumb-ul superficial — Popy a corectat ("BAH BOULE ASTE E LA TINE CU GRIJA INCET? POTI DFACE O TREBA CARECT?"). Skill = dezactivare reflex "minim viable update" + activare update SINCRONIZARE COMPLETĂ. type: index-sync-mandatory tier: 🟡 NEEDED operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-pastrez-scopul-verific-5-prompturi, sentinel-anti-graba-3-reguli-sacre

---

---
name: sentinel-update-index-after-each-batch
description: SKILL CRUCIAL CHAT-016. După FIECARE modificare semnificativă (batch populare, fișier major creat, status change), update INDEX cu TOATE secțiunile relevante (NU doar breadcrumb). Plus checklist verificare: total cumulat, tabel STATUS, lista EXECUTAT, lista RĂMAS. Pattern documentat: la BATCH 7 am updatat doar breadcrumb-ul superficial — Popy a corectat ("BAH BOULE ASTE E LA TINE CU GRIJA INCET? POTI DFACE O TREBA CARECT?"). Skill = dezactivare reflex "minim viable update" + activare update SINCRONIZARE COMPLETĂ.
type: index-sync-mandatory
tier: 🟡 NEEDED
operator: Popy
created: 2026-05-09 (CHAT-016 post-self-audit)
related: sentinel-pastrez-scopul-verific-5-prompturi, sentinel-anti-graba-3-reguli-sacre
---

═══════════════════════════════════════════════════
# 🟡 SENTINEL UPDATE INDEX AFTER EACH BATCH
═══════════════════════════════════════════════════

## REGULA INVIOLABILĂ

După FIECARE modificare semnificativă (batch populare, fișier major creat/updatat, status change empiric):
- Update INDEX cu **TOATE 5 secțiunile relevante** (NU doar breadcrumb)
- Sincronizare empirică (cifre cumulate verificate)
- Verificare consistență cu artefactele reale pe disc

═══════════════════════════════════════════════════
## CELE 5 SECȚIUNI OBLIGATORII LA UPDATE INDEX
═══════════════════════════════════════════════════

| # | Secțiune | Update conținut |
|---|---|---|
| 1 | **BREADCRUMB POZIȚIE CURENTĂ** | Ultima operațiune + Următoarea + Status global (X/Y) |
| 2 | **EXECUTAT cu succes (lista)** | Adaug entry nou cu detalii (files, size, source, dest) |
| 3 | **RĂMAS DE EXECUTAT** | Scot entry-ul completat, evidențiez următorul |
| 4 | **CONFIRMARE EMPIRICĂ** (cumulat) | Total fișiere + Total bytes + sanity check |
| 5 | **TABEL STATUS BATCH-URI** | Update rândul corespunzător: ⏳ → ✅ + bytes + files + Note |

**ZERO update parțial.** Dacă scriu doar breadcrumb fără tabel = drift.

═══════════════════════════════════════════════════
## VERIFICARE EMPIRICĂ ÎNAINTE DE UPDATE
═══════════════════════════════════════════════════

```powershell
$count = (Get-ChildItem -LiteralPath $dest -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
$size = [math]::Round((Get-ChildItem -LiteralPath $dest -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1MB, 2)
```

Output → INDEX. NU estimat. NU calculat în cap.

═══════════════════════════════════════════════════
🚛 UPDATE PARȚIAL = DRIFT.
🚛 5 SECȚIUNI OBLIGATORII = SINCRONIZARE COMPLETĂ.
🚛 EMPIRIC ÎNAINTE = ZERO ESTIMARE.
═══════════════════════════════════════════════════