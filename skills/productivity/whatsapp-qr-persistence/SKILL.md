---
name: whatsapp-qr-persistence
description: Authenticate WhatsApp Web via QR with session persistence.
version: 1.0.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags: [WhatsApp, QR, Authentication, MCP, Persistence]
    category: productivity
---

# WhatsApp QR Code Authentication with Session Persistence

This skill authenticates with WhatsApp Web via QR code scanning and saves the session so it can be reused on every subsequent startup — no repeated scans needed. It uses a persistent Chrome browser window to display the QR code, then reuses the saved auth data with the mcp-whatsapp-web MCP server.

## When to Use

- First-time setup of WhatsApp messaging in Hermes
- Need to re-authenticate after session loss
- `check_auth_status` returns "not authenticated"
- Need to verify the WhatsApp connection end-to-end

## Prerequisites

- Chrome installed at: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- `mcp-whatsapp-web` installed: `npm install -g mcp-whatsapp-web`
- Phone with WhatsApp app ready to scan QR codes
- Windows OS (Chrome path is Windows-specific)

## How to Run

Run the auth script through the `terminal` tool, then start the MCP server through the `terminal` tool. The server auto-loads the saved session — no re-scan needed after the first time.

## Quick Reference

```
QR auth script:   node scripts/auth_qr.cjs
Server start:     WHATSAPP_SESSION_DIR=C:/Users/apviz/.whatsapp-sessions MCP_HTTP_PORT=3002 TRANSPORT=http node dist/index.js
Auth check tool:  check_auth_status
Search contacts:  search_contacts
List chats:       list_chats
Send message:     send_message
Get QR code:      get_qr_code
```

## Procedure

### Step 1: Initial QR Authentication

Run the QR auth script (opens a visible Chrome window):

```bash
cd /c/Users/apviz/AppData/Roaming/npm/node_modules/mcp-whatsapp-web
node --trace-deprecation scripts/auth_qr.cjs
```

This script:
- Opens Chrome with `headless: false` (visible window on your desktop)
- Navigates to https://web.whatsapp.com
- Displays the QR code in the browser window
- Polls every 3 seconds for authentication state
- Prints `AUTHENTICATED` when your phone scan succeeds
- Saves session to `C:\Users\apviz\.whatsapp-sessions\session\`
- Keeps the browser open so you can verify it worked

**Scan the QR code with your phone** when the Chrome window appears.

### Step 2: Start the MCP Server (Reuses Saved Session)

After the first scan, start the server using the saved session:

```bash
cd /c/Users/apviz/AppData/Roaming/npm/node_modules/mcp-whatsapp-web
WHATSAPP_HEADLESS=true WHATSAPP_BROWSER=chrome \
WHATSAPP_SESSION_DIR="C:/Users/apviz/.whatsapp-sessions" \
MCP_HTTP_PORT=3002 TRANSPORT=http \
node --trace-deprecation dist/index.js
```

- `WHATSAPP_SESSION_DIR` points to the **parent** dir (`~/.whatsapp-sessions`), not the `session/` subdirectory
- `LocalAuth` appends `session/` internally
- Runs silently in background on port 3002
- **DO NOT delete the session directory** — destroys saved auth

### Step 3: Verify Connection

```bash
INIT=$(curl -s -D - -o /dev/null -X POST http://127.0.0.1:3002/mcp \
  -H "Accept: text/event-stream,application/json" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test","version":"1.0"}}}')
SESSION_ID=$(echo "$INIT" | grep -i "mcp-session-id" | tr -d '\r' | awk '{print $2}')

curl -s -X POST http://127.0.0.1:3002/mcp \
  -H "Accept: text/event-stream,application/json" \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"check_auth_status","arguments":{}}}'
```

Expected: `"You are currently authenticated with WhatsApp and ready to use all features."`

### Step 4: Use WhatsApp Tools

17 tools available: `check_auth_status`, `get_qr_code`, `request_pairing_code`, `list_chats`, `get_chat_by_id`, `send_message`, `search_contacts`, `get_contact_by_id`, `list_messages`, `get_last_interaction`, `send_media`, `download_media`, `logout`, `ping`

## Pitfalls

- Session directory must be PARENT (`~/.whatsapp-sessions`), LocalAuth appends `session/`
- DO NOT wipe `~/.whatsapp-sessions/` — forces re-scan every time
- `WHATSAPP_PAIRING_PHONE_NUMBER` crashes — `AuthStore.PairingCodeLinkUtils` missing in current WhatsApp Web
- **QR scan must be done ONCE** — session is saved automatically, never delete it
- `WHATSAPP_HEADLESS` must be `false` for initial QR scan (need visible browser window)
- After scan, server can switch to `WHATSAPP_HEADLESS=true` for background operation
- `list_chats` may return errors — `WAWebCollections` module lazy-loading; use `search_contacts` instead which works reliably

## Verification

```bash
# Server responds on port 3002
curl -s http://127.0.0.1:3002/mcp
# Auth returns: "You are currently authenticated with WhatsApp"
# Contacts searchable: search_contacts "Alex" returns 68+ results
# Session saved: ~/.whatsapp-sessions/session/Default/IndexedDB/ has .ldb files
# MCP tools available: check_auth_status, search_contacts, send_message, get_qr_code
```
