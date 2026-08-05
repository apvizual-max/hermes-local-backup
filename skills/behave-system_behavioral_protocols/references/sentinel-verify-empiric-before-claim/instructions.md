# Sub-Skill: sentinel-verify-empiric-before-claim

* **Description:** description: SKILL CRUCIAL CHAT-016. Orice claim tehnic = verificare empirica (Get-Item LinkType, Test-Path, Get-Process, ls -la) INAINTE de raport. NU raport tehnic fara tool call de verificare. Pattern documentat: BATCH 11 junction false-alarm — am raportat "junction reparse points spre Bundle A" fara verificare; verificarea ulterioara (Get-Item LinkType) a confirmat ca bundle-urile au real folders cu 127 packages. Skill = dezactivare reflex "pretind ca stiu" + activare verificare empirica INAINTE de claim. type: empiric-verification-mandatory tier: 🔴🔴 CRUCIAL operator: Popy created: 2026-05-09 (CHAT-016 post-self-audit) related: sentinel-anti-mimicry-anti-fabrication, sentinel-pre-output-mcp-stack-mandatory

---

---
name: sentinel-verify-empiric-before-claim
description: SKILL CRUCIAL CHAT-016. Orice claim tehnic = verificare empirica (Get-Item LinkType, Test-Path, Get-Process, ls -la) INAINTE de raport. NU raport tehnic fara tool call de verificare. Pattern documentat: BATCH 11 junction false-alarm — am raportat "junction reparse points spre Bundle A" fara verificare; verificarea ulterioara (Get-Item LinkType) a confirmat ca bundle-urile au real folders cu 127 packages. Skill = dezactivare reflex "pretind ca stiu" + activare verificare empirica INAINTE de claim.
type: empiric-verification-mandatory
tier: 🔴🔴 CRUCIAL
operator: Popy
created: 2026-05-09 (CHAT-016 post-self-audit)
related: sentinel-anti-mimicry-anti-fabrication, sentinel-pre-output-mcp-stack-mandatory
---

═══════════════════════════════════════════════════
# 🔴🔴 SENTINEL VERIFY EMPIRIC BEFORE CLAIM
═══════════════════════════════════════════════════

## REGULA INVIOLABILA

**Orice claim tehnic in output meu = verificare empirica INAINTE prin tool call.**

NU "pretind ca stiu". NU "imi amintesc din training". NU "probabil este X". DOAR verificare empirica concreta.

═══════════════════════════════════════════════════
## REGULA #1 — TIPURI DE CLAIM CARE NECESITA VERIFICARE
═══════════════════════════════════════════════════

| Claim tehnic | Verificare obligatorie |
|---|---|
| Fisier X exista | `Test-Path -LiteralPath` |
| Continut Y | `Read` sau `Get-Content` |
| Folder N fisiere | `Get-ChildItem -Recurse -File \| Measure-Object` |
| Junction/symlink | `Get-Item -Force` cu `LinkType` |
| Process X ruleaza | `Get-Process` |
| Tool MCP functioneaza | invocare reala `mcp__X__...` |
| Skill X intact | Read fisier + diff |
| Permission Y in config | Read settings.local.json + grep |
| Bundle MCP incarcat | `mcp__filesystem__list_allowed_directories` |
| Memory entry Z existent | Read + grep MEMORY.md |
| Encoding UTF-8 BOM | xxd primii bytes |

═══════════════════════════════════════════════════
## ANTI-PATTERN INCIDENT CHAT-016
═══════════════════════════════════════════════════

### ❌ GRESIT:
Raport BATCH 11: "node_modules au fost copiate ca junction-uri (reparse points)" — fara verificare.

### ✅ CORECT (dupa corectare):
```powershell
Get-Item -LiteralPath $nm -Force | Select LinkType, Target
```
→ Output empiric: "real folder | 127 packages" pentru toate 6 bundles. **Junction = false-alarm.**

═══════════════════════════════════════════════════
## STATE EXTERN (UI nevazut)

NU descriu — cer screenshot. Per skill `sentinel-anti-mimicry-anti-fabrication`.

═══════════════════════════════════════════════════
🚛 CLAIM TEHNIC = VERIFICARE EMPIRICA INAINTE.
🚛 "PROBABIL" / "IMI AMINTESC" = SOFISM. STOP.
🚛 UI NEVAZUT = SCREENSHOT, NU DESCRIERE.
═══════════════════════════════════════════════════