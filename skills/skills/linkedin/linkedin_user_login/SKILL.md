---
name: linkedin-user-login
description: Manual LinkedIn login procedure using agent-browser with persistent session for cookie extraction
version: 1.0.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags: [LinkedIn, Login, Authentication, Cookie, Persistence, Manual]
---

# LinkedIn User Login Procedure

Manual login workflow using `agent-browser` with persistent named session. User logs in manually (handles 2FA); agent extracts `li_at` cookie for headless reuse.

## Prerequisites

- `agent-browser` executable at `C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\bin\agent-browser-win32-x64.exe`
- User has LinkedIn credentials and 2FA device
- Chrome browser available on system

## Procedure

### Phase 1: Manual Login (One-Time Setup)

```bash
# 1. Kill any stuck agent-browser processes
taskkill /F /IM agent-browser-win32-x64.exe

# 2. Launch LinkedIn login in HEADED mode with named session
agent-browser open https://www.linkedin.com/login --headed true --session linkedin-session
```

**User manually completes:**
- Email/password entry
- 2FA challenge (SMS, authenticator app, etc.)
- Check "Keep me signed in"
- Navigate to feed to verify login

### Phase 2: Cookie Extraction & Persistence

> **KNOWN QUIRK (verified 2026-07-15):** `agent-browser cookies get --session X --json` returns empty
> `"cookies":[]` with `"relaunchedBrowser":true` — it relaunches a FRESH browser instead of reconnecting to
> your logged-in one, so it harvests nothing. Do NOT trust this command. Read cookies from the on-disk file instead.

```bash
# 3. READ cookies from the on-disk session file (the real source of truth).
#    File path DOUBLES the session id: --session linkedin-session -> linkedin-session-linkedin-session.json
SESSFILE="$HOME/.agent-browser/sessions/linkedin-session-linkedin-session.json"
cp "$SESSFILE" linkedin_cookies_backup.json
grep -o '"name": "li_at"' linkedin_cookies_backup.json   # must print a match

# 4. Test access by DRIVING THE LIVE HEADED WINDOW (do NOT relaunch headless -- see Quirks section)
agent-browser snapshot --compact true --session linkedin-session
# Should show authenticated feed content, NOT login page
```

**CRITICAL:** Once the headed window is closed, the in-memory session dies. To extract/use cookies AFTER closing,
parse `li_at` from `linkedin_cookies_backup.json` and inject it via CDP `Network.setCookie` into a new browser
context BEFORE navigating. Plain `--session` reuse will NOT restore them.

### Phase 3: Ongoing Headless Usage

```bash
# Subsequent runs: headless, restores cookies automatically
agent-browser open https://www.linkedin.com/feed/ --session linkedin-session
agent-browser open "https://www.linkedin.com/jobs/search/?keywords=python&location=Romania" --session linkedin-session
agent-browser eval "..." --session linkedin-session --json
```

## Key Cookies Extracted

| Cookie | Lifetime | Purpose |
|--------|----------|---------|
| `li_at` | ~1 year | Primary auth token |
| `JSESSIONID` | Session | Secondary auth |
| `bcookie` | 2 years | Browser ID tracking |
| `bscookie` | 2 years | Secure tracking |
| `li_gc` | ~2 years | Guest consent |
| `lidc` | ~1 day | Load balancer |

## Verification Checklist

Before declaring session "ready for automation":
- [ ] `agent-browser snapshot --session linkedin-session` (against the LIVE headed window) shows feed content
- [ ] The on-disk session file `linkedin_cookies_backup.json` (copied from `~/.agent-browser/sessions/linkedin-session-linkedin-session.json`) contains `li_at`
- [ ] Can navigate to `/feed`, `/jobs`, `/messaging` without redirect (only verified against the live headed window)
- [ ] Headless access requires CDP cookie injection first — a bare `--session X --headless` run WILL drop to login (see CRITICAL QUIRKS); verify after injection, not before

## Session Persistence

> **VERIFIED 2026-07-15 — READ THIS.** The persistence model is NOT automatic in the current `agent-browser` build.

- Cookies ARE saved to disk. **The file name DOUBLES the session id**: `--session linkedin-session` creates
  `C:\Users\apviz\.agent-browser\sessions\linkedin-session-linkedin-session.json` (profile and session both took the value).
  TIP: use a distinct short name like `--session li` to get a predictable file, or just read the doubled-name file.
- The saved JSON contains the full auth set: `li_at`, `JSESSIONID`, `bcookie`, `bscookie`, `li_gc`, `lidc`, `__cf_bm`, `li_alerts`.
- **A fresh `agent-browser open --session X --headless` does NOT re-inject these cookies** — it launches a new browser
  with an empty cookie jar and drops to `linkedin.com/uas/login`. The old claim ("restores cookies automatically") is FALSE for this build.
- `li_at` in the saved file persists ~30-60 days; the live headed window holds it in memory only.
- Always pass `--session <name>` on commands that must talk to the SAME launched browser.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Daemon busy/unresponsive | `taskkill /F /IM agent-browser-win32-x64.exe` then retry |
| Session expired (redirects to login) | Re-run Phase 1 |
| Cookie save error | Benign - cookies persist in memory for session |
| CAPTCHA on headless | Only happens if fingerprint looks automated; headed login avoids this |
| `cookies get` returns `"cookies":[]` | EXPECTED QUIRK — agent-browser relaunches a fresh browser. Read the on-disk `~/.agent-browser/sessions/linkedin-session-linkedin-session.json` file instead. |
| Headless `open --session X` drops to `/login` | agent-browser did NOT re-inject saved cookies into the new launch. Keep the ORIGINAL headed window alive and drive it, or inject cookies via CDP before navigating. |
| Raw `curl` with `li_at` returns HTTP 429 | LinkedIn rate-limits the server/datacenter IP. Do NOT use raw curl for LinkedIn from this host — use the live browser session. |

## CRITICAL: agent-browser Persistence Quirks (verified 2026-07-15)

The original skill assumed cookie persistence was automatic. It is NOT, in the installed build. Summary of verified behavior:

1. **Cookie extraction command is broken.** `agent-browser cookies get --session X` relaunches a fresh browser and
   returns empty `cookies:[]`. The real cookies live in the on-disk session JSON file.
2. **Session file name doubles.** `--session linkedin-session` → `linkedin-session-linkedin-session.json`.
3. **Headless reuse does not restore auth.** A new `open --session X --headless` starts a clean browser → LinkedIn
   redirects to `/uas/login`. The "restores cookies automatically" claim is false.
4. **Raw curl is rate-limited (429).** Sending `li_at` via `curl` from the host IP gets HTTP 429. Use the live browser.

**Reliable access pattern (RECOMMENDED):**
- Keep the **headed window alive** after manual login.
- Drive it directly: `agent-browser snapshot/eval/open --session linkedin-session` against that SAME live window.
- To go headless later, parse the saved `li_at` from the session JSON and inject via CDP `Network.setCookie`
  BEFORE any navigation — never rely on `--session` alone.

See `references/agent-browser-quirks.md` for the full reproduction transcript and verified cookie set.

## Automation Template (Job Search)

> **WARNING:** The commands below assume `--session` restores auth. It does NOT (see CRITICAL QUIRKS).
> Run them ONLY against the LIVE headed window from Phase 1, or after injecting `li_at` via CDP.
> A standalone `--session linkedin-session --headless` run will drop to the login page.

```bash
# Search jobs (only works against the live, logged-in window)
agent-browser open "https://www.linkedin.com/jobs/search/?keywords=python%20developer&location=Romania&f_TPR=r86400" --session linkedin-session

# Wait & scroll for infinite load
agent-browser wait 3000 --session linkedin-session
for i in {1..5}; do
  agent-browser scroll down 2000 --session linkedin-session
  agent-browser wait 1500 --session linkedin-session
done

# Extract job data
agent-browser eval "
const jobs = [];
document.querySelectorAll('.job-card-container, .jobs-search-results__list-item').forEach(el => {
  const title = el.querySelector('h3, .job-title')?.innerText?.trim();
  const company = el.querySelector('.job-card-container__company-name, .company-name')?.innerText?.trim();
  const location = el.querySelector('.job-card-container__metadata-item, .job-location')?.innerText?.trim();
  const link = el.querySelector('a[href*=\"/jobs/view/\"]')?.href;
  if (title) jobs.push({title, company, location, link});
});
jobs;
" --session linkedin-session --json
```

## Related Skills

- `linkedin-local-data-extraction` — Full extraction workflow
- `exec-persistent-browser-auth` — Generic pattern for LinkedIn/GitHub/Twitter/Notion

---

**SEMNATURĂ IREVOCABILĂ**
> ACEASTĂ SKILL DOCUMENTEAZĂ PROCESUL DE LOGIN MANUAL CU AGENT-BROWSER. 
> USER-UL SE LOGEAZĂ (2FA INCLUS); AGENTUL EXTRACTEAZĂ COOKIES. 
> SESIUNEA PERSISTĂ PENTRU RULĂRI HEADLESS ULTERIOARE. AMIN.

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

