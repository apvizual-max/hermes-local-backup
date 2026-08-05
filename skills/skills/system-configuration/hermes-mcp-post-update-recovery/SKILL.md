---
name: hermes-mcp-post-update-recovery
description: Recover MCPs after Hermes updates corrupt npm or packages.
license: proprietary
metadata:
  version: v1
  publisher: apviz
---

# Hermes MCP Post-Update Recovery

Run this skill after every Hermes update before diagnosing individual MCP failures.

## Trigger Conditions

- `hermes doctor --fix` shows multiple MCP servers with red "Error" dots
- MCP servers fail with `MODULE_NOT_FOUND` or `Cannot find module` errors
- `npx`-based MCP servers all fail simultaneously
- Ollama local models disappear from the model configuration list

## Root Causes (Post-Update)

1. **Local npm corruption**: Update re-installs `node_modules/npm` with a stale version
   while `node.exe` is upgraded in place. npm binary exists but `@npmcli/config` is missing.
2. **404'd packages**: Some `@modelcontextprotocol/server-*` packages no longer exist:
   `server-obsidian`, `server-docker`, `server-git`
3. **Canary package trap**: `mcp-server-git` on npm is NOT an MCP server - it's a
   security canary that outputs shell script instead of JSON-RPC
4. **PATH resolution**: `npx` resolves to broken hermes-local `node/` instead of
   system Node.js

## Recovery Steps

### Step 0: Diagnose Failure Mode

```powershell
"C:\Users\apviz\AppData\Local\hermes\node\node.exe" -e "console.log('Local node OK')" 2>&1
"C:\Users\apviz\AppData\Local\hermes\node\node_modules\npm\bin\npm" --version 2>&1
"C:\Program Files\nodejs\node.exe" -e "console.log('System node OK')" 2>&1
```

If local node fails but system node works → local npm was corrupted by update.

### Step 1: Ensure System Node.js

```powershell
winget install OpenJS.NodeJS --silent --accept-source-agreements --accept-package-agreements
```

### Step 2: Install MCP Packages Globally

```powershell
"C:\Program Files\nodejs\npm.cmd" install -g `
  @modelcontextprotocol/server-memory `
  @modelcontextprotocol/server-filesystem `
  @modelcontextprotocol/server-sequential-thinking `
  @modelcontextprotocol/server-puppeteer `
  @huangyihe/obsidian-mcp `
  @gy920/qwen-mcp-tool `
  chrome-devtools-mcp@1.6.0 `
  notebooklm-mcp `
  agent-browser-mcp-server `
  mcp-docker `
  mcp-git
```

### Step 2b: Install Messaging Platform MCP Servers

```powershell
"C:\Program Files\nodejs\npm.cmd" install -g `
  mcp-whatsapp-web `
  discord-mcp `
  mcp-telegram `
  gmail-mcp
```

### Step 2c: Install Google Workspace MCP Servers

```powershell
"C:\Program Files\nodejs\npm.cmd" install -g `
  google-workspace-mcp `
  mcp-google-drive `
  google-calendar-mcp
```

### Step 3: Install Python MCP in Hermes Venv

```powershell
"C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\pip.exe" install mcp-server-git
```

### Step 4: Update All Config Files

Update every `config.yaml` to use:
- `npx` → `"C:\Program Files\nodejs\npx.cmd"`
- `agent-browser` → `"C:\Users\apviz\AppData\Roaming\npm\agent-browser.cmd"`
- Git MCP → `python -m mcp_server_git` (NOT `mcp-server-git` canary)

Files:
- `C:\Users\apviz\AppData\Local\hermes\config.yaml`
- All 9 profiles: `...\profiles\*\config.yaml`

### Step 5: Fix Ollama Visibility

```powershell
curl -s http://localhost:11434/api/tags
# Restart Hermes Desktop, Settings → Models → add Ollama provider
```

### Step 6: Fix Obsidian MCP Bridge

Use `@huangyihe/obsidian-mcp` with Obsidian REST API plugin:
```yaml
obsidian:
  args:
    - -y
    - "@huangyihe/obsidian-mcp"
    - --vault-path
    - "D:\\Alex - KV Obsidian\\Alex - KV Obsidian"
  command: "C:\Program Files\nodejs\npx.cmd"
```

### Step 7: Verify

```powershell
hermes doctor --fix  # all dots green
"C:\Program Files\nodejs\npx.cmd" -y @modelcontextprotocol/server-memory --version
```

### Step 8: Configure Messaging & Google Workspace MCP Servers

After installing messaging and Google Workspace packages, add these to all config.yaml files:

```yaml
  # Messaging
  whatsapp:
    args: [-y, mcp-whatsapp-web]
    command: "C:/Program Files/nodejs/npx.cmd"
    timeout: 60
  discord:
    args: [-y, discord-mcp]
    command: "C:/Program Files/nodejs/npx.cmd"
    timeout: 60
  telegram:
    args: [-y, mcp-telegram]
    command: "C:/Program Files/nodejs/npx.cmd"
    timeout: 60
  gmail:
    args: [-y, gmail-mcp]
    command: "C:/Program Files/nodejs/npx.cmd"
    timeout: 60
  # Google Workspace
  google-drive:
    args: [-y, mcp-google-drive]
    command: "C:/Program Files/nodejs/npx.cmd"
    timeout: 60
  google-calendar:
    args: [-y, google-calendar-mcp]
    command: "C:/Program Files/nodejs/npx.cmd"
    timeout: 60
  google-workspace:
    args: [-y, google-workspace-mcp]
    command: "C:/Program Files/nodejs/npx.cmd"
    timeout: 60
```

### Step 9: Set Environment Variables for Auth

Create `~/.env` or add to Hermes `.env`:

```bash
# Telegram
TELEGRAM_API_ID=<your_id>
TELEGRAM_API_HASH=<your_hash>
TELEGRAM_API_TOKEN=<your_bot_token>

# Discord
DISCORD_BOT_TOKEN=<your_bot_token>

# Google Workspace (google-workspace-mcp uses ~/.google-mcp/credentials.json)
# Download OAuth credentials from Google Cloud Console
```

### Step 10: Set Up Google Workspace Credentials

The `google-workspace-mcp` package reads credentials from:
```
%USERPROFILE%\.google-mcp\credentials.json
```

Download OAuth 2.0 credentials (Desktop application type) from:
https://console.cloud.google.com/apis/credentials

Enable these APIs in Google Cloud Console:
- Google Drive API
- Gmail API
- Google Calendar API
- Google Docs API
- Google Sheets API

## Package Replacement Guide

| Broken Reference | Root Cause | Correct Package |
|---|---|---|
| `@modelcontextprotocol/server-obsidian` | 404 on npm | `mcp-obsidian` or `@huangyihe/obsidian-mcp` |
| `@modelcontextprotocol/server-docker` | 404 on npm | `mcp-docker` |
| `mcp-server-git` | Canary (not MCP server) | `mcp-git` (npm) or `mcp_server_git` (Python) |
| Local `npx` | Broken local npm | `"C:/Program Files/nodejs/npx.cmd"` |
| `agent-browser` local path | Broken local npm | `agent-browser-mcp-server@latest` via npx |
| `mcp-whatsapp` | Stub package (v0.0.1, not functional) | `mcp-whatsapp-web` |
| `@modelcontextprotocol/server-postgres` | 404 on npm | `postgresql-mcp` (pip) |
| `blender_mcp.server` | Wrong module name | `blender_mcp_server.server` (pip) |

## Reference Files

- `references/MCP_POST_UPDATE_PACKAGES.md`
- `references/NODE_NPM_CORRUPTION_DIAGNOSIS.md`

## CRITICAL: NEVER TRUNCATE THIS SKILL FILE

- This skill file is NEVER to be truncated.
- Truncation = Fatal System Error.
- Edit mode: ALWAYS additive only. Use `patch` for targeted changes.
