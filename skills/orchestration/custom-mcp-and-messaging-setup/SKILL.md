---
name: custom-mcp-and-messaging-setup
description: "Create custom MCP servers, configure Telegram/WhatsApp bots."
version: 1.0.0
author: Sentinel Prime
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [MCP, FastMCP, Telegram, WhatsApp, Bot-API, JSON-RPC, Subprocess]
---

# Custom MCP Server & Messaging Platform Setup

## When to Use

When you need to create a **custom MCP server** in Python (using `FastMCP`), configure **Telegram bot metadata** programmatically via the Bot API, set up **WhatsApp Web automation** via `mcp-whatsapp-web`, or communicate with MCP servers via **stdio JSON-RPC** from Python subprocess.

## Prerequisites

- Hermes venv Python: `C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe`
- System Node.js: `C:/Program Files/nodejs/` (for npm-based MCP servers)
- `pip install fastmcp` in the venv for custom Python MCP servers
- `.env` at `C:\Users\apviz\AppData\Local\hermes\.env` for credential storage

## Step 1: Create a Custom MCP Server (FastMCP)

### Package Structure

```
C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\
  <server-name>/
    src/
      <package_name>/
        __init__.py        # empty file
        server.py          # main MCP server code
```

### Minimal Server Template

```python
from fastmcp import FastMCP
import json, os, urllib.request

mcp = FastMCP("<server-name>")

BOT_TOKEN = os.environ.get("TOKEN_ENV_VAR", "")
API_BASE = f"https://api.example.com/bot{BOT_TOKEN}"

@mcp.tool()
def my_tool(param1: str, param2: int = 0) -> str:
    """Tool description for the MCP client."""
    result = {"param1": param1, "param2": param2}
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Key Gotchas

- **Use `FastMCP`** (not legacy `mcp.server`) — old module paths don't exist in newer MCP versions
- **Use `@mcp.tool()`** (function decorator form), NOT `@mcp.tool` (call form)
- **Module needs `__init__.py`** in package directory for `python -m package.server`
- **FastMCP prints ASCII art logo to stderr** — ignore this, it's startup noise

### MCP Config Entry

```yaml
  my-custom-server:
    args:
    - -m
    - package_name.server
    command: "C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe"
    cwd: C:/Users/apviz/AppData/Local/hermes/mcp-servers/custom/server-name/src
    env:
      TOKEN_ENV_VAR: "your_token_here"
    timeout: 60
```

**Important:** `cwd` must point to the `src` directory for Python to find the package.

## Step 2: Configure Telegram Bot via Bot API

### Programmatic Configuration

```python
import json, urllib.request

BOT_TOKEN = "YOUR_BOT_TOKEN"
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def call_api(method, data=None):
    url = f"{API_BASE}/{method}"
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(),
                                    headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    return json.loads(urllib.request.urlopen(req, timeout=10).read())

# Set bot commands
call_api("setMyCommands", {"commands": [
    {"command": "start", "description": "Start the bot and get help"},
    {"command": "help", "description": "Show available commands"},
]})

# Set description and short description
call_api("setMyDescription", {"description": "Bot description text"})
call_api("setMyShortDescription", {"short_description": "Short description"})

# Set bot name
call_api("setMyName", {"name": "Bot Display Name"})

# Verify
bot = call_api("getMe")
print(f"Bot: @{bot['result']['username']}")
```

### Settings That REQUIRE BotFather (Manual)

These cannot be set via Bot API — must use `@BotFather` chat:

| Setting | BotFather Command |
|---------|-------------------|
| Privacy mode | `/setprivacy` → select bot → Enable |
| Group joining | `/setjoingroups` → select bot → Disable |
| Inline mode | `/setinline` → select bot → Disable |

## Step 3: WhatsApp MCP Configuration

### Server: `mcp-whatsapp-web`

```yaml
  whatsapp:
    args:
    - -y
    - mcp-whatsapp-web
    command: C:/Program Files/nodejs/npx.cmd
    env:
      WHATSAPP_SESSION_DIR: C:/Users/apviz/.whatsapp-sessions
      WHATSAPP_HEADLESS: "true"
      WHATSAPP_BROWSER: chrome
      MCP_HTTP_PORT: "3002"
      TRANSPORT: sse
      # For auto pairing code generation (optional):
      WHATSAPP_PAIRING_PHONE_NUMBER: "40722121752"
    timeout: 120
```

> **Note:** For stdio mode (no HTTP server), omit `MCP_HTTP_PORT` and `TRANSPORT`.
> For HTTP/SSE mode (recommended for multi-call sessions), set `TRANSPORT=sse`
> and `MCP_HTTP_PORT` — this enables `sessionId` query parameter authentication
> required by the MCP HTTP protocol.

### Available Tools

```
get_qr_code, request_pairing_code, check_auth_status, logout,
search_contacts, get_contact_by_id, list_chats, get_chat_by_id,
list_messages, get_message_by_id, send_message, send_media,
download_media, ping
```

### Authentication

**QR Code (stdio mode):** Call `get_qr_code` → scan with WhatsApp mobile → Settings → Linked Devices → Link a Device

**Pairing Code (auto):** Set `WHATSAPP_PAIRING_PHONE_NUMBER` env var → restart server → code printed to stderr

**Pairing Code (MCP tool):** Call `request_pairing_code` with phone number via MCP `tools/call` → enter code on phone

Session persists in `WHATSAPP_SESSION_DIR` (default: `~/.whatsapp-sessions/`) for future uses.

> **See `references/whatsapp-pairing-code-authentication.md` for the complete pairing code workflow**, including the known issue with Baileys 7.0.0-rc13 ("Connection Closed" errors) and why `mcp-whatsapp-web` is the reliable path.

### Key Points

- **Timeout: 120s** (not 60s) — browser startup takes 10-30s
- Server needs **~30s to initialize** before first response
- Use `check_auth_status` before sending messages
- Use **HTTP/SSE transport** (`TRANSPORT=sse`, `MCP_HTTP_PORT=3002`) for reliable session management across MCP calls
- Always send `notifications/initialized` after `initialize` before calling tools
- Kill stale node processes (`taskkill /IM node.exe /F`) before starting fresh

## Step 4: MCP Protocol Communication via Subprocess

### Correct Message Sequence

```
1. initialize → server responds with capabilities + serverInfo
2. notifications/initialized → NO response (notification)
3. tools/list → server responds with tool list
4. tools/call → server responds with tool result
```

### Python Communication Pattern

```python
import subprocess, json, os, time

env = os.environ.copy()
env["TOKEN_ENV_VAR"] = "your_token"

proc = subprocess.Popen(
    ["python.exe", "-m", "package.server"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    env=env, cwd=r"...\src"
)

# Send messages in sequence with delays
messages = [
    '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "test", "version": "1.0"}}}',
    '{"jsonrpc": "2.0", "method": "notifications/initialized"}',
    '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}',
]

for msg in messages:
    proc.stdin.write((msg + "\n").encode())
    proc.stdin.flush()
    time.sleep(2)

# Read responses
for line in proc.stdout:
    resp = json.loads(line.strip())
    if resp.get("id") == 2:
        tools = resp.get("result", {}).get("tools", [])
        for t in tools:
            print(f"Tool: {t['name']}")
```

### Gotchas

- **`notifications/initialized` MUST be sent** before `tools/list`
- **Add 2-second delays** between messages — Node.js/npm servers are slower
- **FastMCP prints ASCII art to stderr** — ignore it, it's noise
- **Node.js servers (npx)** need 10-30s to install before responding
- **Windows:** use `npx.cmd` (not `npx`) and forward slashes in all paths