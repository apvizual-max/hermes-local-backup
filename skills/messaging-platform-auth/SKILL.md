---
name: messaging-platform-auth
description: WhatsApp auth via persistent QR browser + saved session reuse.
version: 2.0.0
author: Sentinel Default
license: MIT
platforms:
  - windows
metadata:
  hermes:
    tags:
      - whatsapp
      - authentication
      - mcp-server
      - qr-code
      - persistent-session
    category: messaging
---

# Messaging Platform Authentication for Hermes Agent

## Trigger
Use when setting up WhatsApp messaging on Hermes Agent. This skill covers the ONLY working authentication approach for `mcp-whatsapp-web` v1.1.0 with `whatsapp-web.js` v1.34.7 on the current WhatsApp Web version.

## Behavior
1. **Browser QR display**: Launch a *visible, persistent* Chrome browser window showing the WhatsApp Web QR code on screen; user **must** scan it with their phone and the operator must **wait for on-screen confirmation** (`AUTHENTICATED! Chats are visible`) before doing anything else.
2. **Session saved**: Auth data (IndexedDB ~25MB, 16+ .ldb files) persists to disk automatically at `WHATSAPP_SESSION_DIR/session/`.
3. **Future startups**: Server loads saved session — NO QR scan, NO pairing code, NO browser window shown. Auth is automatic.
4. **Tools available**: `check_auth_status` (returns authenticated), `search_contacts` (returns 9+ contacts), `get_qr_code` (if not authenticated). `list_chats` and `send_message` may fail due to `WAWebCollections` lazy-loading in whatsapp-web.js v1.34.7.
5. **NEVER wipe the session**: Once auth is saved, the session directory must persist across server restarts. Deleting it forces a full re-scan.

## Prerequisites
- Chrome at `C:\Program Files\Google\Chrome\Application\chrome.exe`
- `mcp-whatsapp-web` npm package installed
- Phone with WhatsApp app
- `WHATSAPP_SESSION_DIR` set to `C:\Users\apviz\.whatsapp-sessions` (PARENT of `\session\`)

## Quick Reference

### Working approach (PROVEN)
```bash
# ONE-TIME: Scan QR code with persistent browser
node qr_persistent_v2.cjs   # Opens Chrome browser, shows QR, user scans

# ONGOING: Start server with saved session (NO QR, NO pairing code)
WHATSAPP_HEADLESS=true \
WHATSAPP_BROWSER=chrome \
WHATSAPP_SESSION_DIR=C:/Users/apviz/.whatsapp-sessions \
MCP_HTTP_PORT=3002 TRANSPORT=http \
node dist/index.js
```

### Environment Variables
```bash
# DO NOT set WHATSAPP_PAIRING_PHONE_NUMBER — it crashes the server
# (see Pitfalls: "requestPairingCode is BROKEN")
WHATSAPP_HEADLESS=true
WHATSAPP_BROWSER=chrome
WHATSAPP_SESSION_DIR=C:/Users/apviz/.whatsapp-sessions
MCP_HTTP_PORT=3002
TRANSPORT=http
```

## Procedure

### Phase 1: Initial QR Authentication (ONE TIME ONLY)
1. **Kill ALL processes** — `taskkill /IM node.exe /F` and `taskkill /IM chrome.exe /F`
2. **Clean session** (first time only): `rm -rf C:\Users\apviz\.whatsapp-sessions`
3. **Run the QR script** — opens a visible Chrome browser tab with the QR code:
   ```bash
   node qr_persistent_v2.cjs
   ```
4. **Scan the QR code** — user uses WhatsApp phone app to scan the QR shown on screen
5. **Wait for confirmation** — script prints `[QR] AUTHENTICATED! Chats are visible.`
6. **Kill the browser process** (optional) — session data is saved to IndexedDB at `C:\Users\apviz\.whatsapp-sessions\session\`

### Phase 2: Start Server with Saved Session (EVERY OTHER TIME)
```bash
WHATSAPP_HEADLESS=true WHATSAPP_BROWSER=chrome \
WHATSAPP_SESSION_DIR=C:/Users/apviz/.whatsapp-sessions \
MCP_HTTP_PORT=3002 TRANSPORT=http \
node dist/index.js
```
- Server launches headless Chrome with `userDataDir = session/`
- Loads saved IndexedDB auth data (no new QR code!)
- Ready in ~30 seconds with auth already active

### Phase 3: Verify
```bash
# Initialize MCP session, then:
# check_auth_status -> "You are currently authenticated with WhatsApp"
# search_contacts -> returns 50+ contacts
# list_chats -> may error (see Pitfalls)
```

## Pitfalls
- **NEVER set WHATSAPP_PAIRING_PHONE_NUMBER** — It triggers `requestPairingCode()` which crashes immediately. Pairing code flow is **completely broken** with current WhatsApp Web.
- **CRITICAL: `requestPairingCode` is broken** — `whatsapp-web.js` v1.34.7's `Client.requestPairingCode` accesses `window.AuthStore.PairingCodeLinkUtils` from module `WAWebAltDeviceLinkingApi` which doesn't exist in current WhatsApp Web. Crash: `Runtime.evaluate error: t: t` at `Client.js:527`. Cannot be fixed by patching.
- **WHATSAPP_SESSION_DIR must be PARENT** — `LocalAuth` creates `session/` inside `dataPath`. Setting it to `...\session` creates nested `...\session\session\`. Correct: `WHATSAPP_SESSION_DIR=C:\Users\apviz\.whatsapp-sessions`.
- **`list_chats` returns error "r"** — `WWebJS.getChats()` calls `window.require('WAWebCollections')` which throws (lazy loading). Patched `Client.js` and `Utils.js` with retry logic (up to 15s wait) — may help but not guaranteed.
- **`send_message` may fail** — Same `WAWebCollections` lazy-loading issue as `list_chats`.
- **`check_auth_status` and `search_contacts` work reliably** — These don't depend on `WAWebCollections`.
- **DO NOT wipe session after successful auth** — `C:\Users\apviz\.whatsapp-sessions\session\` contains ~25MB of IndexedDB auth data. Deleting destroys the session.
- **Use TRANSPORT=http** — stdio mode shuts down when stdin closes.
- **Always kill ALL node/chrome processes** before starting — 50+ orphaned processes observed.
- **QR codes are NOT time-limited** — Unlike pairing codes (3-min expiry), QR remains valid until browser session expires (~30 min). No rush.
- **ALWAYS wait for user confirmation** — After showing the QR browser window, WAIT for the user to physically scan the QR code with their phone and confirm. NEVER assume scan succeeded. NEVER close browser before user confirms.
- **ALWAYS use visible browser for initial QR** — QR must be visible on desktop (`headless: false`). Headless QR codes are not scannable.

## Verification
1. Server running on port 3002: responds to MCP initialize
2. Auth active: `check_auth_status` returns authenticated
3. Contacts accessible: `search_contacts` returns contacts with names and JIDs
4. Session persists: `C:\Users\apviz\.whatsapp-sessions\session\Default\IndexedDB\` has 6MB+ of .ldb files
5. No QR on restart: starting with existing session requires NO user interaction

## Script Files
- `qr_persistent_v2.cjs` — Opens Chrome browser, navigates to web.whatsapp.com, waits for QR scan
- `start_whatsapp.sh` — Startup script checking session and starting server
- `patch-utils-getChats.cjs` — Patches Utils.js with retry logic for WAWebCollections

## Config for Hermes MCP
Add to `profiles/default/config.yaml`:
```yaml
  whatsapp:
    args:
      - -y
      - mcp-whatsapp-web
    command: C:/Program Files/nodejs/npx.cmd
    env:
      WHATSAPP_HEADLESS: 'true'
      WHATSAPP_BROWSER: chrome
      WHATSAPP_SESSION_DIR: C:/Users/apviz/.whatsapp-sessions
      MCP_HTTP_PORT: '3002'
      TRANSPORT: http
    timeout: 120
```
**IMPORTANT**: Do NOT include `WHATSAPP_PAIRING_PHONE_NUMBER` — it crashes the server.