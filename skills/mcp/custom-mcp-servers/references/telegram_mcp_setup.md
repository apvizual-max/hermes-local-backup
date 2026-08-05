# Telegram MCP Server Configuration

## Overview

Two Telegram MCP servers are configured — one using the Bot API (no phone auth needed), and one using MTProto (full user account access).

## Option A: Bot API (Recommended for most use cases)

**Server:** Custom Python FastMCP server at:
```
C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\telegram-bot-mcp\src\telegram_bot_mcp\server.py
```

**Tools:**
- `tg_get_me` — Get bot info
- `tg_get_updates` — Read incoming messages
- `tg_send_message` — Send messages to chats
- `tg_get_chat` — Get chat info
- `tg_get_webhook_info` — Check webhook status
- `tg_set_webhook` — Set webhook URL

**Config entry:**
```yaml
  telegram-bot:
    args:
      - -m
      - telegram_bot_mcp.server
    command: C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
    cwd: C:/Users/apviz/AppData/Local/hermes/mcp-servers/custom/telegram-bot-mcp/src
    env:
      TELEGRAM_API_TOKEN: "your_bot_token_here"
    timeout: 60
```

**Test command:**
```python
import subprocess, json, os
env = os.environ.copy()
env["TELEGRAM_API_TOKEN"] = "your_token"
mcp_input = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"tg_get_me","arguments":{}}}) + "\n"
result = subprocess.run(
    [python, "-m", "telegram_bot_mcp.server"],
    input=mcp_input, env=env, cwd=".../src",
    capture_output=True, text=True, timeout=15
)
```

## Option B: MTProto (Full user account access)

**Package:** `mcp-telegram` (npm, via npx)

**Requires:** Phone number verification — will hang waiting for user to enter phone code.

**Bug:** Path concatenation issue — `TELEGRAM_AGENT_HOME` gets prepended with `cwd`:
```
Error: ENOENT: no such file or directory, mkdir 'C:\...\hermes-agent\C:\Users\apviz\.telegram-agent\sessions\...'
```

**Fix:**
```yaml
  telegram:
    args:
      - -y
      - mcp-telegram
    command: C:/Program Files/nodejs/npx.cmd
    env:
      TELEGRAM_API_ID: "35584659"
      TELEGRAM_API_HASH: "a64ced2efc33afbd0228a18686032fcf"
      TELEGRAM_AGENT_HOME: "C:/Users/apviz/.telegram-agent"
      LOG_LEVEL: "info"
    timeout: 120
```

Also create the directory:
```bash
mkdir -p ~/.telegram-agent/sessions
```

And set `cwd` to user home to avoid path prefix issues.
