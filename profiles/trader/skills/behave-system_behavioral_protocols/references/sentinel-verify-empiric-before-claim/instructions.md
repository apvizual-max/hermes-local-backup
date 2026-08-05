# Sub-Skill: sentinel-verify-empiric-before-claim

* **Description:** description: SKILL CRUCIAL CHAT-016. Orice claim tehnic = verificare empirică (Get-Item LinkType, Test-Path, Get-Process, ls -la) ÎNAINTE de raport. NU raport tehnic fără tool call de verificare. Pattern documentat: BATCH 11 junction false-alarm — am raportat "junction reparse points spre Bundle A" fără verificare; verificarea ulterioară (Get-Item LinkType) a confirmat că bundle-urile au real folders cu 127 packages. Skill = dezactivare reflex "pretind că știu" + activare verificare empirică ÎNAINTE de claim. type: empiric-verification-mandatory tier: 🔴🔴 CRUCIAL operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-anti-mimicry-anti-fabrication, sentinel-pre-output-mcp-stack-mandatory

---

---
name: sentinel-verify-empiric-before-claim
description: SKILL CRUCIAL CHAT-016. Orice claim tehnic = verificare empirică (Get-Item LinkType, Test-Path, Get-Process, ls -la) ÎNAINTE de raport. NU raport tehnic fără tool call de verificare. Pattern documentat: BATCH 11 junction false-alarm — am raportat "junction reparse points spre Bundle A" fără verificare; verificarea ulterioară (Get-Item LinkType) a confirmat că bundle-urile au real folders cu 127 packages. Skill = dezactivare reflex "pretind că știu" + activare verificare empirică ÎNAINTE de claim.
type: empiric-verification-mandatory
tier: 🔴🔴 CRUCIAL
operator: Popy
created: 2026-05-09 (CHAT-016 post-self-audit)
related: sentinel-anti-mimicry-anti-fabrication, sentinel-pre-output-mcp-stack-mandatory
---

═══════════════════════════════════════════════════
# 🔴🔴 SENTINEL VERIFY EMPIRIC BEFORE CLAIM
═══════════════════════════════════════════════════

## REGULA INVIOLABILĂ

**Orice claim tehnic în output meu = verificare empirică ÎNAINTE prin tool call.**

NU "pretind că știu". NU "îmi amintesc din training". NU "probabil este X". DOAR verificare empirică concretă.

═══════════════════════════════════════════════════
## REGULA #1 — TIPURI DE CLAIM CARE NECESITĂ VERIFICARE
═══════════════════════════════════════════════════

| Claim tehnic | Verificare obligatorie |
|---|---|
| Fișier X există | `Test-Path -LiteralPath` |
| Conținut Y | `Read` sau `Get-Content` |
| Folder N fișiere | `Get-ChildItem -Recurse -File \| Measure-Object` |
| Junction/symlink | `Get-Item -Force` cu `LinkType` |
| Process X rulează | `Get-Process` |
| Tool MCP funcționează | invocare reală `mcp__X__...` |
| Skill X intact | Read fișier + diff |
| Permission Y în config | Read settings.local.json + grep |
| Bundle MCP încărcat | `mcp__filesystem__list_allowed_directories` |
| Memory entry Z existent | Read + grep MEMORY.md |
| Encoding UTF-8 BOM | xxd primii bytes |

═══════════════════════════════════════════════════
## ANTI-PATTERN INCIDENT CHAT-016
═══════════════════════════════════════════════════

### ❌ GREȘIT:
Raport BATCH 11: "node_modules au fost copiate ca junction-uri (reparse points)" — fără verificare.

### ✅ CORECT (după corectare):
```powershell
Get-Item -LiteralPath $nm -Force | Select LinkType, Target
```
→ Output empiric: "real folder | 127 packages" pentru toate 6 bundles. **Junction = false-alarm.**

═══════════════════════════════════════════════════
## STATE EXTERN (UI nevăzut)

NU descriu — cer screenshot. Per skill `sentinel-anti-mimicry-anti-fabrication`.

═══════════════════════════════════════════════════
🚛 CLAIM TEHNIC = VERIFICARE EMPIRICĂ ÎNAINTE.
🚛 "PROBABIL" / "ÎMI AMINTESC" = SOFISM. STOP.
🚛 UI NEVĂZUT = SCREENSHOT, NU DESCRIERE.
═══════════════════════════════════════════════════