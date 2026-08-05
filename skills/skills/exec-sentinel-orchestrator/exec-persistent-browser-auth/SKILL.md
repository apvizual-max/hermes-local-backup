---
name: exec-persistent-browser-auth
description: Local browser automation with persistent authenticated sessions using agent-browser state profile. Enables ongoing access to authenticated web services (LinkedIn, GitHub, Twitter, Notion, etc.) where official APIs are restricted/expensive/unavailable.
---

# Persistent Authenticated Browser Sessions — Local Agent Pattern

**Class:** Local browser automation with cookie/session persistence across runs
**Trigger:** User needs ongoing access to authenticated web services (LinkedIn, GitHub, Twitter, Notion, etc.) where official APIs are restricted/expensive/unavailable

---

## THE PROBLEM

Cloud-based browser automation fails for authenticated workflows because:
- Datacenter IPs are instantly flagged by anti-bot systems (LinkedIn, Twitter, GitHub, etc.)
- Browser fingerprints differ from real user environments
- 2FA/CAPTCHA challenges cannot be solved interactively
- Session cookies don't persist between ephemeral cloud containers

---

## THE SOLUTION: LOCAL BROWSER + STATE PERSISTENCE

The `agent-browser` MCP runs **locally on the user's machine** (via `C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd`). This means:

| Property | Cloud Browser | Local agent-browser |
|----------|--------------|---------------------|
| IP reputation | Datacenter (blocked) | Residential (trusted) |
| Browser fingerprint | Automation flags | Real Chrome profile |
| 2FA interaction | Impossible | User does it manually |
| Cookie persistence | Lost each session | **Persisted via `state` profile** |
| Session lifetime | Minutes | **Months (li_at token ~1 year)** |

---

## WORKFLOW: PERSISTENT AUTHENTICATED SESSION

### Phase 1: One-Time Setup (User Logs In Manually)

```bash
# Launch visible browser with named session
agent-browser open --url https://www.linkedin.com --headed true --session linkedin-session --restore auto --restore-save auto
```

**Optional: Use user's actual Chrome profile** (if they prefer their full Chrome setup with extensions, multiple logged-in accounts, etc.):

```bash
agent-browser open --url https://www.linkedin.com --headed true --session linkedin-session --restore auto --restore-save auto --user-data-dir "C:\Users\apviz\AppData\Local\Google\Chrome\User Data" --profile-directory "Default"
```

> **Note**: User's actual Chrome profile path varies by OS/username. On Windows: `%LOCALAPPDATA%\Google\Chrome\User Data` (e.g., `C:\Users\apviz\AppData\Local\Google\Chrome\User Data`). Use `--profile-directory "Default"` (or "Profile 1", "Profile 2", etc. for multiple profiles).

**Alternative: Use computer_use to click the user's actual desktop Chrome shortcut** — this launches Chrome with their full profile, extensions, and existing sessions automatically:

```python
# Via computer_use tool (interacts with USER's actual desktop)
computer_use(action="capture", app="explorer.exe", mode="som")  # Find Chrome shortcut
computer_use(action="double_click", app="explorer.exe", element=3)  # Click "Google Chrome" shortcut
# Or use terminal to launch the .lnk directly:
terminal(command='start "" "C:\Users\Public\Desktop\Google Chrome.lnk" https://www.linkedin.com')
```

This approach:
- Uses the user's REAL Chrome installation (not a separate profile)
- Inherits all existing logins, extensions, cookies
- No need to re-authenticate if already logged in
- Works via the desktop shortcut at `C:\Users\Public\Desktop\Google Chrome.lnk`

1. Browser opens on user's machine
2. User logs in normally (email, password, **2FA**)
3. User navigates to verify access (feed, jobs, messages)
4. Session state (cookies, localStorage, IndexedDB) auto-saves to `~/.agent-browser/sessions/linkedin-session/`

### Phase 2: Automated Subsequent Runs (Headless)

```bash
# Subsequent runs: headless, restores cookies automatically
agent-browser open --url https://www.linkedin.com/feed --session linkedin-session --restore auto --restore-save auto
agent-browser snapshot --session linkedin-session
agent-browser click --selector "[data-test-id=job-search]" --session linkedin-session
# ... extract data, navigate, interact
```

**Key flags:**
- `--session <name>` — named persistent profile
- `--restore auto` — load cookies/storage on startup
- `--restore-save auto` — save cookies/storage on close
- `--headed true/false` — visible for login, headless for automation

---

## AGENT-BROWSER STATE PROFILE TOOLS (27 tools)

The `state` profile provides explicit cookie/storage control:

| Tool | Purpose |
|------|---------|
| `agent_browser_get_cookies` | Read all cookies for current session |
| `agent_browser_set_cookies` | Inject cookies into session |
| `agent_browser_save_state` | Manually checkpoint session |
| `agent_browser_restore` | Restore from checkpoint |
| `agent_browser_clear_cookies` | Reset session |
| `agent_browser_list_sessions` | List saved sessions |
| `agent_browser_delete_session` | Remove session |

**Use case:** Export `li_at` cookie for external scripts, or inject cookies captured elsewhere.

---

## LINKEDIN-SPECIFIC NOTES

| Cookie | Lifetime | Critical? |
|--------|----------|-----------|
| `li_at` | ~1 year | **YES** — primary auth token |
| `JSESSIONID` | Session | Secondary |
| `bcookie` | 2 years | Tracking |
| `bscookie` | 2 years | Secure tracking |

**Anti-bot evasion:**
- Use `--headed true` for initial login (real Chrome, real input)
- Residential IP = user's home network = trusted
- Real browser fingerprint = no automation flags
- Session persists for months without re-login

---

## INTEGRATION WITH HERMES AGENT

### As Orchestrator (this agent)
1. User runs Phase 1 locally (one-time)
2. Agent uses `agent-browser` MCP tools with `--session linkedin-session` for Phase 2+
3. Agent can: navigate, click, extract, screenshot, fill forms
4. Session persists across agent restarts

### As Executor (Antigravity)
- Delegate complex extraction tasks via `ag_delegate_task`
- Antigravity runs locally with same session access
- Results returned to Hermes outbox

---

## PITFALLS & MITIGATIONS

| Pitfall | Mitigation |
|---------|------------|
| LinkedIn changes DOM selectors | Use semantic selectors (`[data-test-id=...]`, `role=button`, text content) |
| Session expires (rare) | Detect 401/redirect to login → prompt user to re-run Phase 1 |
| Cookie corruption | `agent_browser_clear_cookies --session linkedin-session` then re-login |
| Multiple services | Use separate sessions: `linkedin-session`, `github-session`, `twitter-session` |
| User clears browser data | Session stored in `~/.agent-browser/sessions/`, not Chrome profile |
| Using actual Chrome profile | `--user-data-dir` + `--profile-directory` flags; profile must NOT be open in another Chrome window |
| **agent-browser daemon hangs** | **Kill stuck processes**: `taskkill /F /IM agent-browser-win32-x64.exe /IM chrome.exe /IM node.exe` then restart |
| **SearXNG 403 on local instance** | **Configure `trusted_proxies` in `settings.yml` AND `limiter.toml` for Docker networks (172.16.0.0/12, 10.0.0.0/8, 192.168.0.0/16, 172.17.0.0/16); set `limiter: false` and `search.formats: [html, json]`** |
| **Missing Python deps in SearXNG container** | **Install: `msgspec`, `pyyaml`, `tomli`, `typing_extensions`, `httpx`, `pygments`, `granian`, `flask`, `blinker`, `whitenoise`, `flask_babel`, `markdown-it-py`, `httpx_socks`, `valkey`, `lxml`, `typer`, `python-dateutil`, `isodate`, `h2`** |
| **Chrome CDP fails to start on port 9222** | **Kill all Chrome processes (`taskkill /F /IM chrome.exe`), remove lock files in `User Data/Default/LOCK*`, start Chrome with `--remote-debugging-port=9222 --no-startup-window --no-first-run --no-default-browser-check`; verify with `netstat -an | findstr 9222` and `curl http://localhost:9222/json/version`** |
| **agent-browser CLI times out on `open`** | **Daemon stuck: kill `agent-browser-win32-x64.exe`, `chrome.exe`, `node.exe` processes; restart with fresh session name** |
| **LinkedIn cookie injection fails in browser tool** | **Browser tool uses separate profile; extract `li_at` from user's actual Chrome (DevTools → Application → Cookies) and inject into agent-browser session via `cookies set --curl`** |
| **Chrome App shortcuts don't launch** | **Chrome Apps were deprecated by Google in 2022. Use `agent-browser open --url https://www.linkedin.com/feed --session linkedin-session --restore auto` instead, or launch actual Chrome via desktop shortcut with `computer_use` or `terminal(command='start "" "C:\Users\Public\Desktop\Google Chrome.lnk" https://www.linkedin.com/feed')`** |
| **cua-driver multi-monitor blind spot** | **`computer_use` captures per-window per-monitor — CANNOT span dual displays. PWA windows on secondary monitors are invisible. Fix: `focus_app(raise_window=true)` or ask user to drag window. Verify PWA running via `Get-Process chrome \| Select MainWindowTitle`. 2 failed captures = check monitor, don't retry blindly.** |
| **computer_use vs browser_navigate session isolation** | **`browser_navigate` (Puppeteer) runs a SEPARATE browser — no shared cookies with user's real Chrome or PWA. `computer_use` drives the user's ACTUAL authenticated browser. Never mix them expecting shared auth.** |
| **User wants visible cursor control** | **"computer use means MOUSE CURSOR on screen" — use `computer_use` for visible mouse/keyboard control. Do NOT fall back to PowerShell Win32 API hacks (ShowWindow, SetForegroundWindow via Add-Type) when `computer_use` is available.** |

---

## VERIFICATION CHECKLIST

Before declaring a session "ready for automation":
- [ ] `agent-browser snapshot --session linkedin-session` shows authenticated content (feed, not login page)
- [ ] `agent_browser_get_cookies --session linkedin-session` returns `li_at` cookie
- [ ] Can navigate to `/feed`, `/jobs`, `/messaging` without redirect
- [ ] Headless run completes without CAPTCHA/2FA challenge

---

## RELATED SKILLS

- `exec-agent-browser` — Core browser automation patterns
- `exec-systems-administrator` — MCP server configuration for agent-browser
- `exec-hermes-antigravity-bridge` — Delegation to Antigravity for heavy extraction

## REFERENCES

- `references/chrome-cdp-troubleshooting.md` — Chrome CDP startup issues
- `references/linkedin-session-guide.md` — LinkedIn-specific session management
- `references/chrome-apps-deprecation.md` — Chrome Apps deprecation impact on desktop shortcuts
- `references/multi-monitor-pitfalls.md` — cua-driver multi-monitor blind spot, browser_navigate vs computer_use session isolation, user cursor preference (field-confirmed 2026-07-15)

---

## SEMNATURĂ IREVOCABILĂ

> **ACEASTĂ SKILL E ALGORITMUL PENTRU ACCES PERSISTENT LA SERVICII WEB AUTENTIFICATE.**  
> **RULEAZĂ LOCAL, PĂSTREAZĂ COOKIES, EVITĂ BLOCAREA ANTI-BOT.**  
> **ȚI-NE MINTE CĂ UIȚI. AMIN.**

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

