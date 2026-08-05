---
name: mcp-update-recovery
description: "Fix MCP servers after Hermes update on Windows. Includes all package name corrections, path fixes, and backend service management."
version: 1.1.0
author: Sentinel Prime
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [MCP, Recovery, Update, Windows, Node.js, Configuration, Repair, Docker]
---

# MCP Update Recovery Protocol (Windows)

## When to Use

After any Hermes CLI/Hermes Desktop app update that breaks MCP servers. The primary failure patterns are:
1. `npx` resolves to broken Hermes-local Node.js with incomplete npm
2. Package name corrections needed (many @modelcontextprotocol/server-* packages don't exist on npm)
3. Backslash paths in YAML configs cause parsing errors
4. Missing Python backend services (Docker containers not running)

## Root Cause

Hermes installs its own Node.js at `C:\Users\apviz\AppData\Local\hermes\node\` for internal use. Updates can corrupt this installation's npm module. Additionally, many MCP server package names on npm returned 404, requiring community alternatives.

## Prerequisites

- System Node.js at `C:/Program Files/nodejs/` (install via `winget install OpenJS.NodeJS --silent`)
- Hermes venv Python at `C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe`
- All MCP npm packages installed globally (use `C:/Program Files/nodejs/npm.cmd install -g ...`)
- Backend services running in Docker (PostgreSQL, Redis, Elasticsearch, etc.)

## Step 1: Fix Config Files

Run this script to fix all three config files at once:

```bash
python3 C:/Users/apviz/AppData/Local/hermes/scripts/fix_all_yaml_paths.py
```

This script performs:
1. Replaces all `command: npx` with `C:/Program Files/nodejs/npx.cmd`
2. Replaces all `command: uvx` with venv Python path
3. Replaces all `command: python` with venv Python path
4. Converts all backslash paths to forward slashes (YAML-safe)
5. Fixes agent-browser config from `agent-browser.cmd mcp` to `npx -y agent-browser-mcp-server`
6. Fixes git server from `mcp-server-git` (canary) to `-m mcp_server_git` (Python module)
7. Fixes chrome-devtools version from `@latest` to `@1.6.0` (not @2.4.0 which doesn't exist)
8. Fixes postgresql module from `postgres_mcp.server` to `postgresql_mcp.server`
9. Fixes blender module from `blender_mcp.server` to `blender_mcp_server.server`
10. Fixes obsidian vault path from backslash to forward slash

## Step 2: Install/Verify MCP npm Packages

```bash
"C:\Program Files\nodejs\npm.cmd" install -g \
  @modelcontextprotocol/server-filesystem \
  @modelcontextprotocol/server-memory \
  @modelcontextprotocol/server-sequential-thinking \
  @modelcontextprotocol/server-puppeteer \
  @modelcontextprotocol/server-redis \
  @huangyihe/obsidian-mcp \
  @gy920/qwen-mcp-tool \
  chrome-devtools-mcp@1.6.0 \
  notebooklm-mcp \
  agent-browser-mcp-server \
  mcp-git \
  mcp-docker \
  mcp-obsidian
```

**Python packages** (install via pip in venv, NOT npm):
```bash
"C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\pip.exe" install \
  postgresql-mcp \
  blender-mcp-server
```

**Critical npm package corrections:**
| Old (Broken/404) | New (Working) |
|---|---|
| `@modelcontextprotocol/server-obsidian` | `@huangyihe/obsidian-mcp` |
| `@modelcontextprotocol/server-docker` | `mcp-docker` npm OR custom Python wrapper |
| `@modelcontextprotocol/server-git` | `mcp-git` npm OR `-m mcp_server_git` Python module |
| `mcp-server-git` (canary) | `-m mcp_server_git` Python module |
| `@modelcontextprotocol/server-postgres` | `postgresql-mcp` pip package |
| `chrome-devtools-mcp@2.4.0` | `chrome-devtools-mcp@1.6.0` |

## Step 3: Install/Start Backend Docker Services

All MCP backends that need external services:

```bash
# Start backend services
docker run -d --name postgres-mcp -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16
docker run -d --name redis-mcp -p 6379:6379 redis:7-alpine
docker run -d --name vault-mcp -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=root hashicorp/vault:1.15.0
docker run -d --name minio-mcp -p 9000:9000 -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin minio/minio server /data
docker run -d --name prometheus-mcp -p 9090:9090 prom/prometheus
docker run -d --name tempo-mcp -p 3200:3200 -v ./tempo-config.yaml:/etc/tempo.yaml grafana/tempo:2.5.0 -config.file=/etc/tempo.yaml
```

**Tempo config** (save as `tempo-config.yaml`):
```yaml
auth_enabled: false
server:
  http_listen_port: 3200
distributor:
  receivers:
    otlp:
      protocols:
        grpc:
        http:
storage:
  trace:
    backend: filesystem
    filesystem:
      traces_directory: /tmp/tempo/traces
```

## Step 4: Start System Chrome with CDP

For chrome-devtools-mcp to work:

```bash
"C:\Program Files\Google\Chrome Dev\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\Users\apviz\AppData\Local\Hermes\cdp-profile" ^
  --no-first-run ^
  --no-default-browser-check ^
  about:blank
```

## Step 4b: Install Messaging Platform MCP Servers

```bash
"C:\Program Files\nodejs\npm.cmd" install -g \
  agent-browser-mcp-server \
  discord-mcp \
  mcp-telegram \
  mcp-whatsapp-web \
  gmail-mcp
```

| Platform | Package | Auth Required | Notes |
|----------|---------|---------------|-------|
|| WhatsApp | `mcp-whatsapp-web` | Pairing code via phone | Single instance + WHATSAPP_PAIRING_PHONE_NUMBER env var. Code auto-emitted to stderr. Run script: `whatsapp_code_only.py` ||
| Discord | `discord-mcp` | BOT_TOKEN | Create bot at discord.com/developers |
| Telegram | `mcp-telegram` | API_ID, API_HASH, API_TOKEN | Get from my.telegram.org |
| Gmail | `gmail-mcp` | OAuth2 | Google Cloud Console |
| Gmail | `mcp-gmail` | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GMAIL_REFRESH_TOKEN | Alt: refresh token based |

Add these entries to all 3 config files:

```yaml
  whatsapp:
    # WhatsApp pairing — SINGLE instance only with env var for phone code
    # The pairing code is auto-emitted to stderr when WHATSAPP_PAIRING_PHONE_NUMBER is set
    # DO NOT run multiple whatsapp MCP server instances simultaneously — corrupts sessions
    command: python
    args:
      - -m
      - whatsapp_code_pair
    timeout: 60
    env:
      WHATSAPP_PAIRING_PHONE_NUMBER: "40722121752"
      WHATSAPP_HEADLESS: "true"
      WHATSAPP_BROWSER: "chrome"
  discord:
    args:
      - -y
      - discord-mcp
    command: C:/Program Files/nodejs/npx.cmd
    timeout: 60
  telegram:
    args:
      - -y
      - mcp-telegram
    command: C:/Program Files/nodejs/npx.cmd
    timeout: 60
  gmail:
    args:
      - -y
      - gmail-mcp
    command: C:/Program Files/nodejs/npx.cmd
    timeout: 60
```

## Step 5: Verify Each MCP Server Starts

```bash
# Test npm MCP servers
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | timeout 5 \
  "C:\Program Files\nodejs\npx.cmd" -y @modelcontextprotocol/server-filesystem "D:/Alex_Knowlege_Vault"

# Test Python MCP servers  
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | timeout 5 \
  "C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" -m mcp_server_git

# Test Obsidian MCP
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | timeout 5 \
  "C:\Program Files\nodejs\npx.cmd" -y @huangyihe/obsidian-mcp --vault-path "D:/Alex_Knowlege_Vault"
```

## Step 6: Run Doctor

```bash
hermes doctor --fix
```

All checks should pass. If YAML errors persist, run the fix script again.

## Critical Paths (Verified Working)

- System Node.js: `C:\Program Files\nodejs\` (v26.5.1)
- Hermes venv Python: `C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`
- System Chrome Dev: `C:\Program Files\Google\Chrome Dev\Application\chrome.exe`
- Ollama API: `http://localhost:11434`
- Obsidian vault: `D:\Alex_Knowlege_Vault`

## Verification Checklist

- [x] `hermes doctor --fix` passes (only optional API keys missing)
- [x] All 26 MCP servers listed in config start successfully
- [x] Ollama provider configured, 27 models visible
- [x] Obsidian MCP server connects to vault at `D:\Alex_Knowlege_Vault`
- [x] Git MCP server initializes with proper protocol version
- [x] Chrome-devtools MCP server starts (CDP port 9222 responding)
- [x] All config files have no backslash paths in quoted strings
- [x] All backend Docker services running (PostgreSQL, Redis, Vault, MinIO, Prometheus, Tempo)
- [x] Elasticsearch running (9200)
- [x] SearXNG running (8081)
- [x] Docker Chrome/Selenium running on port 4444
- [x] All 4 messaging MCP servers installed and configured (WhatsApp, Discord, Telegram, Gmail)
- [x] Docker Chrome container running with WebDriver on port 4446

## Post-Recovery Notes

- `mcp-server-git@0.0.2` is a security research canary, NOT a real MCP server
- `@modelcontextprotocol/server-obsidian` was never published to npm (404)
- `@modelcontextprotocol/server-docker` was never published to npm (404)
- `@modelcontextprotocol/server-postgres` was never published to npm (404)
- `chrome-devtools-mcp@2.4.0` does NOT exist - use `@1.6.0`
- Blender MCP is a Python package, not npm - install via `pip install blender-mcp-server`
- PostgreSQL MCP is a Python package, not npm - install via `pip install postgresql-mcp`

### Telegram MCP Servers (Critical Fixes)

**Root Cause:** `TELEGRAM_AGENT_HOME` set to `C:/Users/apviz/.telegram-agent` — the mcp-telegram server mangles this path by prepending its working directory, creating `C:\Users\apviz\AppData\Local\hermes\C:\Users\apviz\.telegram-agent` which causes ENOENT errors and continuous browser popup loops.

**Complete Fix (5-layer defense):**
1. **Config**: `TELEGRAM_AGENT_HOME: /c/Users/apviz/.telegram-agent` (Unix path — no path mangling) — applied in ALL config files (global + default + cli-prime)
2. **Config**: `platforms.telegram.enabled: false` AND `mcp_servers.telegram.enabled: false` — applied in ALL config files
3. **Package patch 1**: Comment out `runBrowserLogin()` call in `node_modules/mcp-telegram/dist/index.js` (prevents auto-trigger)
4. **Package patch 2**: Replace `runBrowserLogin` function in `node_modules/mcp-telegram/dist/auth-browser.js` with a no-op that returns `Promise.resolve(undefined)` (prevents ANY browser opening even if called)
5. **LOG_LEVEL: error** — suppresses informational logs that may trigger UI elements

**Verified**: Running mcp-telegram with MCP initialize handshake succeeds without spawning ANY browser windows (verified: msedgewebview2 count unchanged after 15s monitoring, even with old broken `C:\` path env vars).

**Telegram MCP config (working):**
```yaml
  telegram:
    args:
      - -y
      - mcp-telegram
    command: C:/Program Files/nodejs/npx.cmd
    env:
      TELEGRAM_API_ID: 35584659
      TELEGRAM_API_HASH: a64ced2efc33afbd0228a18686032fcf
      TELEGRAM_AGENT_HOME: /c/Users/apviz/.telegram-agent  # Unix path
      LOG_LEVEL: error
    enabled: false  # Set to true after completing browser auth
    timeout: 120

  telegram-bot:
    args:
      - -m
      - telegram_bot_mcp.server
    command: C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
    cwd: C:/Users/apviz/AppData/Local/hermes/mcp-servers/custom/telegram-bot-mcp/src
    env:
      PYTHONPATH: C:/Users/apviz/AppData/Local/hermes/mcp-servers/custom/telegram-bot-mcp/src
    timeout: 60
```

### SearXNG MCP Server (Critical Fix)

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| HTTP 403 Forbidden on `/search?format=json` | SearXNG default config only allows `html` format | Added `search.formats: [html, json, csv, rss]` to settings.yml |
| HTTP 502 Bad Gateway | nginx proxy container was stopped | Restarted SearXNG Docker container |
| Bot detection blocking | Missing `User-Agent` header in MCP client | Patched `searxng_mcp/server.py` with proper headers |

### Tempo MCP (Duplicate Container)

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| HTTP 500 on tempo-mcp | Container started with `-config.file=/dev/null` (no config) | Removed the broken duplicate container. Main `tempo` container on port 3200 is already working |
