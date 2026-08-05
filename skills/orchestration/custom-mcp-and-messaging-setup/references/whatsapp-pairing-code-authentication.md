# WhatsApp Pairing Code Authentication

## Overview

The `mcp-whatsapp-web` MCP server (v1.1.0, using `whatsapp-web.js` v1.34.7) supports
two authentication methods: QR code scanning and pairing code entry. This document
covers the **pairing code** method — a text-based 8-character code entered on the
phone that does NOT require camera access and is NOT time-restricted like QR codes.

## Prerequisites

- `mcp-whatsapp-web` v1.1.0 installed (`npm install -g mcp-whatsapp-web`)
- Google Chrome installed at the default path or via puppeteer
- Phone number registered on WhatsApp
- WhatsApp app installed on the phone with the registered number

## Authentication Methods (Priority Order)

### Method 1: `WHATSAPP_PAIRING_PHONE_NUMBER` env var (Recommended)

Start the MCP server with the phone number as an environment variable. The server
automatically requests a pairing code and prints it to stderr.

```bash
export WHATSAPP_PAIRING_PHONE_NUMBER="40722121752"  # No + or country code prefix
export WHATSAPP_HEADLESS="true"
export WHATSAPP_BROWSER="chrome"
export WHATSAPP_SESSION_DIR="/c/Users/apviz/.whatsapp-sessions"
export MCP_HTTP_PORT="3002"
export TRANSPORT="sse"

node dist/index.js
```

**Output:**
```
========================================================
  WhatsApp pairing code: 7CBKCFK7
  On the phone with number 40722121752:
  Settings > Linked Devices > Link a device
  > "Link with phone number instead" - enter the code.
  A fresh code is generated every ~3 minutes.
========================================================
```

### Method 2: `request_pairing_code` MCP tool (Programmatic)

Connect to the running MCP server and call the `request_pairing_code` tool:

```bash
# 1. Initialize the MCP session
SESSION_ID=$(curl -s -D - -X POST http://127.0.0.1:3002/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"clientInfo":{"name":"test","version":"1.0.0"}}}' 2>&1 | \
  grep -i "mcp-session-id" | tr -d '\r' | awk '{print $2}')

# 2. Send initialized notification
curl -s -X POST "http://127.0.0.1:3002/mcp?sessionId=$SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null 2>&1

# 3. Request pairing code
curl -s -N -X POST "http://127.0.0.1:3002/mcp?sessionId=$SESSION_ID" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"request_pairing_code","arguments":{"phone_number":"40722121752"}}}'
```

**Response:**
```json
{"content":[{"type":"text","text":"Pairing code generated: 7CBKCFK7"}]}
```

## Entering the Code on Your Phone

1. Open **WhatsApp** on the phone with the registered number
2. Tap **Settings** (gear icon at bottom right)
3. Tap **Linked Devices**
4. Tap **Link a Device**
5. Tap **Link with phone number instead** (do NOT scan the QR code)
6. Enter the 8-character pairing code (e.g., `7CBKCFK7`)
7. Tap **Confirm** / **Verify**
8. WhatsApp will verify the code and connect

The linked device will appear in your Linked Devices list as a "Mac OS" or
"Computer" entry.

## Session Persistence

- Session data is stored in `WHATSAPP_SESSION_DIR` (default: `~/.whatsapp-sessions`)
- The session directory contains Chromium browser profile data (IndexedDB, Local Storage)
- Auth credentials are saved automatically after successful pairing
- To re-authenticate: delete the session directory and restart the server

## Troubleshooting

### "Connection Closed" with Baileys bridge.js

The Hermes gateway's built-in Baileys bridge (`scripts/whatsapp-bridge/bridge.js`,
Baileys 7.0.0-rc13) frequently fails with "Connection Closed (reason: 428)" or
"Failed to request pairing code: Connection Closed". This is due to Baileys 7.0.0-rc13
being incompatible with WhatsApp's current Web API.

**Solution:** Use `mcp-whatsapp-web` (whatsapp-web.js v1.34.7) instead of the Baileys
bridge. The `mcp-whatsapp-web` MCP server reliably generates pairing codes.

### Auth status still shows "not authenticated" after entering code

- The pairing code may have expired (~3 minutes). Generate a new one.
- The server may need to be restarted to pick up the saved session.
- Check that the session directory has data (IndexedDB files of several MB indicate
  successful auth data persistence).

### Multiple stale node processes

Kill stale processes before starting:
```bash
taskkill /IM node.exe /F  # Windows
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `WHATSAPP_PAIRING_PHONE_NUMBER` | Phone number for auto pairing | `40722121752` |
| `WHATSAPP_HEADLESS` | Run browser in headless mode | `true` |
| `WHATSAPP_BROWSER` | Chrome or Edge (for H.264 codec) | `chrome` |
| `WHATSAPP_SESSION_DIR` | Session data storage path | `C:/Users/apviz/.whatsapp-sessions` |
| `MCP_HTTP_PORT` | Port for HTTP/SSE transport | `3002` |
| `TRANSPORT` | Transport mode: `sse` or `stdio` | `sse` |
| `WA_WEB_VERSION` | Pin WhatsApp Web version (optional) | `2.3000.1015010942` |

## MCP Configuration (config.yaml)

```yaml
mcp_servers:
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
      WHATSAPP_PAIRING_PHONE_NUMBER: '40722121752'
    timeout: 120
```