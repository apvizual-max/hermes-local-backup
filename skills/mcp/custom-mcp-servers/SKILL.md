---
name: custom-mcp-servers
description: "Custom MCP servers avoid interactive auth."
version: 1.0.0
author: Sentinel Prime
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [MCP, FastMCP, Custom-Server, API-Wrapper, Authentication]
---

# Custom MCP Servers (FastMCP Pattern)

## When to Use

When an MCP package requires **interactive authentication** (MTProto phone verification, OAuth browser flow) that cannot be completed autonomously, create a lightweight FastMCP server that wraps the HTTP/REST API directly using a bot token or API key.

Common scenarios:
- Telegram MCP packages requiring MTProto phone auth → use Bot API with token
- Services requiring OAuth browser flow → use API key/token directly
- npm MCP packages with broken imports → custom Python wrapper

## Prerequisites
- FastMCP installed in venv: `pip install fastmcp aiohttp`
- Hermes venv Python at `C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe`
- Bot token/API key for the target service

## Package Structure

```
mcp-servers/custom/<service>-mcp/
  src/
    <service>_mcp/
      __init__.py
      server.py
  .env
```

Key rules:
- Package directory name uses hyphens (`telegram-bot-mcp`)
- Python module name uses underscores (`telegram_bot_mcp`) for import
- `__init__.py` must be empty

## Server Template

```python
from fastmcp import FastMCP
import aiohttp, os, json

mcp = FastMCP("your-server-name")
TOKEN = os.environ.get("YOUR_API_TOKEN", "")
API_BASE = f"https://api.service.com/v1"

@mcp.tool()
async def my_tool(param: str) -> str:
    """Description of what this tool does."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/endpoint", headers={"Authorization": f"Bearer {TOKEN}"}) as resp:
            return json.dumps(await resp.json(), indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Config Entry (YAML)

```yaml
  your-server:
    args:
      - -m
      - your_server_mcp.server
    command: C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
    cwd: C:/Users/apvz/AppData/Local/hermes/mcp-servers/custom/your-service-mcp/src
    timeout: 60
```

## Testing Pattern

```python
import subprocess, json, os

env = os.environ.copy()
env["YOUR_API_TOKEN"] = "your_token_here"

mcp_input = "\n".join([
    json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                 "clientInfo": {"name": "test", "version": "1.0"}}}),
    json.dumps({"jsonrpc": "2.0", "id": 2, "method": "notifications/initialized"}),
    json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/list"})
]) + "\n"

proc = subprocess.Popen([python, "-m", "your_server_mcp.server"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=env, text=True)
stdout, _ = proc.communicate(input=mcp_input, timeout=30)
```

## Common Pitfalls

1. **FastMCP wraps results** — tool return values may be wrapped in `{"data": ...}`
2. **Module naming** — must use `-m module.name` (underscores), not `-m file.py`
3. **Package structure** — needs `__init__.py` in package directory
4. **Import path** — `cwd` must point to `src/` directory where the package lives
5. **Async HTTP** — use `aiohttp`, not `requests` (FastMCP is async)
6. **Bot token scope** — bot tokens have limited permissions vs full API tokens
7. **npm path concatenation bug** — `mcp-telegram` and similar npm MCP packages concatenate the `cwd` with an absolute path for env vars like `TELEGRAM_AGENT_HOME`, causing `ENOENT` errors. Always set absolute paths as explicit env vars in config and set `cwd` to user home.
8. **System npx vs Hermes npx** — never use bare `npx` in config; always use `C:/Program Files/nodejs/npx.cmd`.

## Verification Checklist

- [ ] Server imports cleanly (`python -m module.server`)
- [ ] MCP initialize handshake succeeds
- [ ] `tools/list` returns expected tools
- [ ] At least one tool call executes successfully
- [ ] Server configured in all 3 config files
- [ ] Environment variables in `.env` file

## References

- `references/telegram_mcp_setup.md` — Full Telegram MCP configuration (Bot API + MTProto)
- `references/messaging-mcp-setup.md` — Complete messaging MCP setup guide (WhatsApp, Telegram, Discord, Google Workspace)
