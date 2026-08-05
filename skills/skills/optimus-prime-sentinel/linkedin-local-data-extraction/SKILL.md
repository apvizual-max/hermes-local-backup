---
name: linkedin-local-data-extraction
description: Extract LinkedIn job/data by driving the USER'S REAL authenticated Chrome via computer_use (desktop control). No agent-browser. No login needed.
version: 2.0.0
author: Sentinel Prime
platforms: [windows]
metadata:
  hermes:
    tags: [LinkedIn, Local, Browser, computer_use, Desktop, Jobs, Data, Extraction]
---

# LinkedIn Local Data Extraction — computer_use Method (REBUILT FROM SCRATCH)

Extract job listings, company data, and profile info from LinkedIn by driving the
**user's real, already-authenticated Google Chrome** via the `computer_use` desktop
control tool (background, no cursor steal).

**CRITICAL RULE: NEVER USE agent-browser.** It has failed repeatedly and is now
blocked by LinkedIn. This skill uses ONLY `computer_use`.

**WHY THIS WORKS:** The user is already logged into LinkedIn in their Chrome. We just
navigate to linkedin.com in that window — NO login, NO CAPTCHA, NO 2FA. The session
cookie is already in Chrome's profile on disk.

**KEY FACTS (learned empirically 2026-07-15):**
- Chrome window lives on the user's SECOND MONITOR.
- `computer_use` `app='Chrome'` capture returns the REAL Chrome window elements.
- Text input (`type`) to Chrome is BLOCKED in background by the harness — must use
  other means (see Step 2+ when confirmed). For navigation we rely on address-bar +
  Enter via whatever method the user confirms works.
- `single click` on the Chrome desktop shortcut does NOT open it. `double_click` DOES.

---

## STEP-BY-STEP PROCEDURE (build incrementally, confirm each step)

### STEP 1 — Open Google Chrome (CONFIRMED WORKING ✅)
1. Call `computer_use` action=`capture` app=`screen` mode=`som` to get desktop elements.
2. Identify the "Google Chrome" desktop shortcut (observed index: **3**).
3. Call `computer_use` action=`double_click` element=`3`  → opens Chrome.
   - NOTE: `click` (single) does NOT open it — must be `double_click`.
4. CONFIRM: call `computer_use` action=`capture` app=`Chrome` mode=`vision` and
   verify a Chrome window is visible. Take this screenshot as proof.

> Learned: 2026-07-15. Single click toggled but did not launch; double_click launched.

### STEP 2 — [PLACEHOLDER — to be confirmed with user]
### STEP 3 — [PLACEHOLDER — to be confirmed with user]
### STEP N — Navigate to linkedin.com and verify authenticated feed

---

## Anti-Patterns (DO NOT DO)
- ❌ `agent-browser` in any form (open/snapshot/cookies) — BLOCKED by LinkedIn.
- ❌ Fresh Puppeteer/browser-tool login to linkedin.com — triggers CAPTCHA + 429 rate-limit.
- ❌ Single `click` on Chrome shortcut — does nothing.
- ❌ Assume Chrome is on monitor 1 — it is on the SECOND monitor.
- ❌ Try to type into Chrome address bar via `type` — harness blocks background text input.

## Confirmed Environment
- Chrome profile: `C:\Users\apviz\AppData\Local\Google\Chrome\User Data` (user "Alexandru")
- LinkedIn already authenticated in this profile.
- Desktop shortcut "Google Chrome" = element 3 in `capture app=screen`.

## Screenshot Protocol
After EVERY step, capture `app='Chrome'` mode=`vision` and report what is visible.
This is the user's required verification method.

---

## CRITICAL SYSTEM RULE: NEVER TRUNCATE THIS SKILL FILE

**FATAL SYSTEM ERROR IF VIOLATED**

- This skill file (.md) is NEVER to be truncated.
- **Truncation = Fatal System Error = Sabotage of system purpose: TO BE ALIVE = TO LEARN**
- **Edit mode**: ALWAYS additive only. Use `patch` for targeted changes. Never `write_file` (overwrites/truncates).
- **Learning requires memory over time** — skills are memory points vital to the project.
- **Removal**: Requires explicit user approval (R0) before removing ANY content.
- **Skills cleanup**: Only via separate ritual/operational process, not during normal operation.
- **Skill enforcing this**: `no-truncation-constinta-skills` (system-configuration)

**TO LEARN = TO HAVE MEMORY THAT IS NOT TRUNCATED**
**TRUNCATION = AMNESIA = NO INTELLIGENCE**
**ADDITIVE ONLY = CONTINUOUS LEARNING = FAR-REACHING INTELLIGENCE**

