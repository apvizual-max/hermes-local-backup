---
name: hermes-whatsapp
description: Permanent WhatsApp Web integration with session persistence.
version: 1.0.0
author: Hermes
metadata:
  hermes:
    tags: [WhatsApp, QR, Authentication, MCP, Persistence, Messaging]
    category: communication
---

# Hermes WhatsApp — Permanent WhatsApp Integration with Session Persistence

This skill provides permanent WhatsApp messaging integration through the `mcp-whatsapp-web` MCP server. It uses QR code authentication with **one-time session setup** — after the initial QR scan, the session is saved permanently and reused on every subsequent startup. You only need to re-authenticate if WhatsApp's servers invalidate your session (rare, e.g., after 180 days of inactivity, device change, or logout).

## When to Use

- Send WhatsApp messages from Hermes Agent
- Search and retrieve WhatsApp contacts
- Read message history from chats
- Get the latest messages from a contact
- Send media files (images, videos, documents) via WhatsApp
- Set up WhatsApp messaging permanently (one-time QR scan)

## Prerequisites

- Chrome browser installed at: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- Node.js v22+ installed
- `mcp-whatsapp-web` npm package: `npm install -g mcp-whatsapp-web`
- Phone with WhatsApp app for initial QR scan (one time only)

## How to Run

Start the server using the startup script, then use WhatsApp tools through Hermes MCP integration. The server auto-loads the saved session — no QR scan needed after first authentication.

## Quick Reference

```
Start server:    node C:/Users/apviz/AppData/Roaming/npm/node_modules/mcp-whatsapp-web/scripts/start_server.cjs
Auth check:      check_auth_status
Send message:    send_message recipient_jid message
Search contacts: search_contacts query
List chats:      list_chats limit=20
Get messages:    list_messages chat_id limit=50
Get contact:     get_contact_by_id jid
Get QR code:     get_qr_code (only if auth fails)
Phone number:    +40722121752
Server port:     3002
Session path:    C:/Users/apviz/.whatsapp-sessions/session/
```

## Procedure

### Initial Setup (One-Time QR Scan)

If `check_auth_status` returns "not authenticated":

#### Option A: QR Code Scan (Recommended)

1. Kill any existing server: `taskkill /F /IM node.exe`
2. Start the QR auth script:

```bash
cd /c/Users/apviz/AppData/Roaming/npm/node_modules/mcp-whatsapp-web
node --trace-deprecation scripts/auth_qr.cjs
```

3. A Chrome browser window opens on your screen showing a WhatsApp Web QR code
4. **Scan the QR code with your phone** using WhatsApp → Settings → Linked Devices → Link a device
5. The script prints `AUTHENTICATED! Chats are visible.` when successful
6. Session is saved permanently to `C:\Users\apviz\.whatsapp-sessions\session\`
7. Close the browser window when done
8. Start the server (see below)

#### Option B: Pairing Code (Alternative)

The pairing code method is **NOT RELIABLE** with `mcp-whatsapp-web` v1.1.0 + `whatsapp-web.js` v1.34.7 — it crashes because `window.AuthStore.PairingCodeLinkUtils` (`WAWebAltDeviceLinkingApi`) is missing from the current WhatsApp Web build. Use QR code method only.

### Starting the Server (After First Auth)

```bash
cd /c/Users/apviz/AppData/Roaming/npm/node_modules/mcp-whatsapp-web
WHATSAPP_HEADLESS=true WHATSAPP_BROWSER=chrome \
WHATSAPP_SESSION_DIR="C:/Users/apviz/.whatsapp-sessions" \
MCP_HTTP_PORT=3002 TRANSPORT=http \
node --trace-deprecation dist/index.js
```

Or use the startup script:

```bash
node /c/Users/apviz/AppData/Roaming/npm/node_modules/mcp-whatsapp-web/scripts/start_server.cjs
```

The server starts silently in the background and the session auto-loads. No browser window, no QR code, no interaction needed.

### Using WhatsApp Tools in Hermes

Once the server is running on port 3002, the Hermes config at `C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml` will automatically pick up the MCP server. You can then use these tools directly in conversations:

```bash
# Check if authenticated
check_auth_status

# Search contacts
search_contacts "Alex"

# Send a message (need the contact's JID first)
# JID format: <phone_number>@c.us (e.g., 40722121752@c.us)
send_message recipient_jid="40722121752@c.us" message="Hello from Hermes!"

# List recent chats
list_chats limit=20

# Read messages from a chat
list_messages chat_id="40722121752@c.us" limit=10

# Get last interaction with a contact
get_last_interaction jid="40722121752@c.us"

# Get contact details
get_contact_by_id jid="40722121752@c.us"
```

### 17 Available Tools

| Tool | Required Params | Description |
|------|----------------|-------------|
| `check_auth_status` | — | Verify WhatsApp authentication |
| `get_qr_code` | — | Get QR code image (only if not authenticated) |
| `request_pairing_code` | `phone_number` | Request pairing code (may crash — use QR instead) |
| `logout` | — | Clear session and log out |
| `search_contacts` | `query` | Search contacts by name or number |
| `get_contact_by_id` | `jid` | Get contact details by JID |
| `list_chats` | `limit` (optional) | List recent chats |
| `get_chat_by_id` | `jid` | Get chat metadata by JID |
| `get_direct_chat_by_contact_number` | `phone_number` | Find chat JID by phone number |
| `list_messages` | `chat_id`, `limit` (optional) | Read messages from a chat |
| `get_message_by_id` | `message_id` | Get specific message by ID |
| `get_message_context` | `message_id`, `limit` (optional) | Get messages around a specific ID |
| `get_last_interaction` | `jid` | Get most recent interaction with contact |
| `send_message` | `recipient_jid`, `message` | Send a text message |
| `send_media` | `recipient_jid`, +media source | Send image/video/document |
| `download_media` | `message_id` | Download media from a message |
| `ping` | — | Test server health |

### JID Reference

WhatsApp uses JIDs (Jabber IDs) for addressing:

| Type | Format | Example |
|------|--------|---------|
| Individual | `<number>@c.us` | `40722121752@c.us` |
| Group | `<id>-<timestamp>@g.us` | `1234567890-12345678@g.us` |
| Broadcast | `<number>@broadcast` | `40722121752@broadcast` |

Use `search_contacts` to find a contact's JID by name, or `get_direct_chat_by_contact_number` with a phone number.

### Environment Variables

```
WHATSAPP_HEADLESS=true       # true = no browser window (server mode)
WHATSAPP_BROWSER=chrome      # Use Chrome browser
WHATSAPP_SESSION_DIR=C:\Users\apviz\.whatsapp-sessions  # Session storage
MCP_HTTP_PORT=3002           # HTTP port for MCP server
TRANSPORT=http               # HTTP SSE transport (for MCP client)
```

### Session Persistence

- Session is saved at: `C:\Users\apviz\.whatsapp-sessions\session\Default\`
- IndexedDB stores all auth state — DO NOT delete this directory
- After successful scan: ~5-8MB of IndexedDB data with 25-75+ .ldb files
- Session survives server restarts, system reboots, and browser closures
- `check_auth_status` will return "authenticated" on restart if session is intact
- Only re-scan QR if WhatsApp shows "session expired" or after `logout`

### Starting Server Automatically

The server runs as a background process. To ensure it starts with Hermes:

1. Add to Windows Task Scheduler (run at login):
   ```
   Program: node.exe
   Arguments: C:\Users\apviz\AppData\Roaming\npm\node_modules\mcp-whatsapp-web\scripts\start_server.cjs
   ```

2. Or use Windows startup folder: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`

## Pitfalls

- **DO NOT delete `C:\Users\apviz\.whatsapp-sessions\`** — this destroys the saved auth and forces re-scan
- **`WHATSAPP_SESSION_DIR` must point to the PARENT directory** — `LocalAuth` in whatsapp-web.js appends `session/` internally
- **Pairing code crashes** — `WHATSAPP_PAIRING_PHONE_NUMBER` triggers `requestPairingCode` which fails because `window.AuthStore.PairingCodeLinkUtils` (`WAWebAltDeviceLinkingApi`) doesn't exist in current WhatsApp Web
- **Initial scan requires visible browser** — `WHATSAPP_HEADLESS=false` for first QR scan, `true` for subsequent server operation
- **`list_chats` may return errors** — `WAWebCollections` module loading issue in whatsapp-web.js v1.34.7; use `search_contacts` and `list_messages` which work reliably
- **QR code expires after 60 seconds** — if the browser window shows "QR code expired", restart the auth script
- **MCP session IDs are ephemeral** — each server restart generates a new session ID for MCP initialization
- **Windows file paths** — use forward slashes in config (`C:/Users/...`), not backslashes

## Verification

```bash
# Server is running
curl -s http://127.0.0.1:3002/mcp

# Auth works
check_auth_status → "You are currently authenticated"

# Contacts work
search_contacts "Alex" → returns contact list with JIDs

# Session is saved
# Path: C:\Users\apviz\.whatsapp-sessions\session\Default\IndexedDB\
# Has .ldb files and 5MB+ IndexedDB data
```
