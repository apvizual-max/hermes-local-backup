---
name: linkedin-automation-playbook
description: Class-level playbook for LinkedIn authentication and automation from the Sentinel/Windows station. Documents the REAL working paths (live-Chrome CDP, Puppeteer+browser with manual CAPTCHA) and the failures to avoid (agent-browser cookie myth, unsolvable reCAPTCHA, IP soft-block). Use whenever a task touches LinkedIn login, session reuse, or data extraction.
version: 1.0.0
author: Sentinel
platforms: [windows]
metadata:
  hermes:
    tags: [LinkedIn, Login, Authentication, Cookie, CDP, CAPTCHA, Automation]
---

# LinkedIn Automation Playbook (v1 — field-corrected 2026-07-15)

## DO NOT REPEAT (autopsy of 2026-07-15 session)
1. **agent-browser cookie persistence is FALSE.** Each `agent-browser <cmd>` is a SEPARATE daemon; cookies set in one call are lost in the next unless chained with `&&` in ONE shell. The saved `~/.agent-browser/sessions/<name>-<name>.json` may hold a `li_at` but it goes STALE fast and `--restore` still redirects to `/login`. BANNED for LinkedIn by user directive ("STOP USING AGENT BROWSER... IT BLOCKS US NOW").
2. **reCAPTCHA v2 is UNSOLVABLE here.** Checkbox sits in a cross-origin iframe → JS eval can't reach it; coordinate clicks rejected by AX ("Element not found"). Let the USER solve it in the visible browser.
3. **Repeated failed logins soft-block the egress IP** (raw curl → HTTP 429). After 2 failures, STOP — you are now the blocker.
4. **Live Chrome's cookie DB is LOCKED** while Chrome runs (`Device or resource busy`). Can't copy it. CDP against the running Chrome is the only way to read live cookies.
5. **`browser_console` eval is sandboxed** — `fetch`/`localStorage` blocked. Can't set cookies or make network calls via eval.

## WORKING PATHS (priority order)
### Path A — LIVE Chrome via CDP (BEST, no CAPTCHA)
- Relaunch: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222`
- Verify: `curl -s http://127.0.0.1:9222/json/version`
- Attach browser stack via CDP. Live `li_at` already in context → no login, no CAPTCHA.

### Path B — Puppeteer `browser` stack + USER solves CAPTCHA
- `browser_navigate` `https://www.linkedin.com/login`
- `browser_type` email+password from `D:\Alex_Knowlege_Vault\LinkedIn_Access.md`
- `browser_click` Sign in → user completes CAPTCHA in visible browser → continue.
- Keep ONE browser session alive (stack doesn't persist across separate `browser_navigate` calls).

### Path C — COMPUTER_USE mouse cursor on PWA (user-preferred when available)
When the user has a LinkedIn PWA desktop shortcut (e.g., "LinkedIn Feed"):
1. `computer_use(action='capture', mode='som')` — find the desktop shortcut
2. `computer_use(action='double_click', element=N)` — launch the PWA
3. Wait 3-5 seconds for PWA to load
4. **Check monitor placement** (see `references/multi-monitor-pitfalls.md`) — if capture shows only desktop icons, PWA is on secondary monitor
5. `computer_use(action='focus_app', app='Chrome', raise_window=true)` to bring it forward
6. Capture again — if PWA content appears, drive it with mouse clicks and keyboard

**User expectation**: "computer use means MOUSE CURSOR on screen" — ALWAYS prefer `computer_use` over PowerShell Win32 API hacks or headless approaches. User wants to SEE the cursor moving.

**Session isolation warning**: `browser_navigate` (Puppeteer) runs a SEPARATE browser — no shared cookies with user's real Chrome/PWA. Never mix them expecting shared auth.

## STOP / PIVOT RULE (mandatory — user demanded autonomy)
- Method fails 2x → do NOT retry a 3rd time, do NOT present A/B/C choice menus.
- Autonomously switch to the next path (A → B → C). If all exhausted, report blocker ONCE with exact failure, then wait.
- "FIGURE IT OUT... STOP ASKING FOR GUIDANCE" = the autonomy contract for stuck states.

## KEY COOKIES
`li_at` (primary, ~1yr), `JSESSIONID` (session), `bcookie`/`bscookie` (tracking), `li_gc`/`lidc`/`__cf_bm` (consent/LB/CF).

## References
- `references/linkedin_failure_autopsy.md` — full transcripts of each failure and the exact commands tried.
- `references/multi-monitor-pitfalls.md` — cua-driver multi-monitor blind spot, browser_navigate vs computer_use session isolation, user cursor preference.

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

