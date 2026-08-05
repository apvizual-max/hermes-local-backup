# agent-browser LinkedIn Quirks — Verified 2026-07-15

## Environment
- OS: Windows 10
- agent-browser: `C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\bin\agent-browser-win32-x64.exe`
- Session flag used: `--session linkedin-session`

## Verified Behavior (facts, not opinions)

### 1. Cookie extraction command returns empty
```
agent-browser cookies get --session linkedin-session --json
=> {"success":true,"data":{"cookies":[],"lifecycle":{...,"relaunchedBrowser":true,"restoreStatus":"not_configured",...}}}
```
The tool relaunches a fresh Chrome instead of reconnecting to the logged-in window.

### 2. Real cookies are on disk (name DOUBLES)
Path: `C:\Users\apviz\.agent-browser\sessions\linkedin-session-linkedin-session.json`
Contains: `li_at`, `JSESSIONID`, `lang`, `bcookie`, `bscookie`, `li_gc`, `lidc`, `__cf_bm`, `li_alerts`.
Verified `li_at` value (redacted) present and `httpOnly:true, secure:true, expires:~1815618554`.

### 3. Headless reuse drops to login
```
agent-browser open https://www.linkedin.com/feed/ --session linkedin-session --headless true
=> snapshot shows "LinkedIn Login, Sign in"
=> url redirected to https://www.linkedin.com/uas/login?session_redirect=...
```
New launch does NOT inject saved cookies.

### 4. Raw curl with li_at -> HTTP 429
```
curl -sL -H "Cookie: li_at=...; JSESSIONID=..." https://www.linkedin.com/feed/
=> HTTP 429 (Too Many Requests) from server/datacenter IP
```

## Reliable Pattern
- Manual login in HEADED window (user does 2FA).
- Keep that window alive.
- Drive it: `agent-browser snapshot/eval/open --session linkedin-session`.
- For headless later: parse `li_at` from the JSON file, inject via CDP `Network.setCookie` before navigating.

## What does NOT work
- `cookies get` to harvest cookies (returns empty).
- `--session X --headless` to restore auth (drops to login).
- Raw `curl` with cookie from host IP (429 rate-limit).

## Notes
- Session file naming: `<profile>-<session>`. With `--session linkedin-session` and no `--profile`, both fields
  took `linkedin-session` -> file `linkedin-session-linkedin-session.json`. Use a distinct short name
  (e.g. `--session li`) for a predictable filename, or just read the doubled-name file.
- The headed window process exits -> in-memory session dies; only the on-disk JSON survives.
