# WhatsApp Pairing Code Crash — Debugging Reference

## Problem
`mcp-whatsapp-web` v1.1.0 with `whatsapp-web.js` v1.34.7 crashes when `WHATSAPP_PAIRING_PHONE_NUMBER` is set. The server auto-calls `Client.requestPairingCode()` during initialization, which calls `pupPage.evaluate()` to access `window.AuthStore.PairingCodeLinkUtils`. This object doesn't exist because the underlying module `WAWebAltDeviceLinkingApi` is not registered in the current WhatsApp Web version.

## Root Cause Analysis

### Module Availability in Current WhatsApp Web
Probed via `page.evaluate()` on the loaded WhatsApp Web page:

| Module | `window.require()` result |
|--------|--------------------------|
| `WAWebSocketModel` | EXISTS — has `.Socket` with `state: "UNPAIRED"` |
| `WAWebAltDeviceLinkingApi` | "Requiring unknown module" — NOT registered |
| `WABrowser` | undefined |
| `WALinkStore` | undefined |
| `WAWebCmd` | "Requiring unknown module" |
| `WAWebConnModel` | "Requiring unknown module" |
| `WABase64` | "Requiring unknown module" |
| `AuthStore` | undefined (not set — ExposeAuthStore throws) |

### Error Chain
1. `Client.initialize()` detects `pairWithPhoneNumber` is set
2. Calls `exposeFunctionIfAbsent` for `onCodeReceivedEvent`
3. Calls `this.requestPairingCode(pairWithPhoneNumber)` (Client.js:629)
4. `requestPairingCode` calls `pupPage.evaluate()` which tries `AuthStore.PairingCodeLinkUtils`
5. `AuthStore` was never set because `ExposeAuthStore` threw on `window.require('WAWebAltDeviceLinkingApi')`
6. Error: `Runtime.evaluate error: t: t` at `ExecutionContext.js:391` → `Client.js:527`

### requireLazy Behavior
- `requireLazy([['WAWebAltDeviceLinkingApi']], 'wa_pairing', callback)` — timed out after 15s
- `requireLazy([['WAWebAltDeviceLinkingApi']], 'wa_alt_device_linking', callback)` — also failed
- Both failed because the module doesn't exist in current WhatsApp Web

## CRITICAL: Session Path Configuration

**WHATSAPP_SESSION_DIR must point to the PARENT directory of `\session\`!**

`LocalAuth` creates `session/` inside `dataPath` automatically:
- `WHATSAPP_SESSION_DIR = C:\Users\apviz\.whatsapp-sessions` → uses `C:\Users\apviz\.whatsapp-sessions\session\`
- Setting it to `...\session` creates nested `...\session\session\` (WRONG)

## Working Approach: QR Scan → Save Session → Reuse (Verified Aug 5, 2026)

1. **One-time QR scan**: `node whatsapp-persist-browser.cjs` opens Chrome window with QR code
2. **User scans QR**: Auth data saved to `C:\Users\apviz\.whatsapp-sessions\session\` (25MB, 16+ .ldb files)
3. **Server restart**: `WHATSAPP_SESSION_DIR=C:\Users\apviz\.whatsapp-sessions` → loads saved session
4. **Auth check**: `check_auth_status` returns "You are currently authenticated with WhatsApp"
5. **Contacts work**: `search_contacts` returns 50+ contacts

### What works vs. what doesn't
- ✅ `check_auth_status` — returns "authenticated"
- ✅ `search_contacts` — returns contact list
- ✅ `get_contact_by_id` — returns contact details
- ❌ `list_chats` — fails: `WAWebCollections` lazy-loading (error "r")
- ❌ `send_message` — same `WAWebCollections` issue
- ❌ `request_pairing_code` — crashes: `AuthStore.PairingCodeLinkUtils` missing

## Session Persistence
- Auth data in Chrome IndexedDB at: `WHATSAPP_SESSION_DIR/session/Default/IndexedDB/`
- IndexedDB grows from ~276KB to ~6.2MB when authenticated
- 16+ .ldb files contain auth credentials
- Session dir: `C:\Users\apviz\.whatsapp-sessions\session\` = 119MB total
- **DO NOT delete** — destroys working session, forces full re-scan

## User Frustration Note
The user was FRUSTRATED because sessions were wiped after each successful auth. **Once saved, NEVER delete the session. Future server starts auto-load the session without QR scanning.**