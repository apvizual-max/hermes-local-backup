---
title: MCP Servers & Integration (Windows Recovery)
version: 1.0.0
---

# MCP Servers & Integration (Windows Recovery)

## Critical: MCP Server Breakage After Updates

The primary failure pattern after Hermes CLI updates on Windows:
- `npx` resolves to Hermes-local Node.js at `C:\Users\apviz\AppData\Local\hermes\node\`
- This installation has a corrupted/incomplete npm module (missing `npm-prefix.js`)
- ALL npm-based MCP servers fail with `MODULE_NOT_FOUND`
- The fix: Install system Node.js at `C:\Program Files\nodejs\` and update all config paths

## All 23 MCP Servers (Verified Working)

### Node.js/npm-based (require `@modelcontextprotocol/server-*` or similar packages)

| Server | Package | Config Key | Status |
|--------|---------|------------|--------|
| Filesystem | `@modelcontextprotocol/server-filesystem` | `filesystem` | ✅ Working |
| Memory | `@modelcontextprotocol/server-memory` | `memory` | ✅ Working |
| Sequential Thinking | `@modelcontextprotocol/server-sequential-thinking` | `sequential-thinking` | ✅ Working |
| Browser (Puppeteer) | `@modelcontextprotocol/server-puppeteer` | `browser` | ✅ Working |
| Postgres | `@modelcontextprotocol/server-postgres` | `postgresql-mcp` | ✅ Working (needs DB URL) |
| Redis | `@modelcontextprotocol/server-redis` | `redis-mcp` | ✅ Working (needs Redis) |
| Obsidian | `@huangyihe/obsidian-mcp` | `obsidian` | ✅ Working |
| Qwen | `@gy920/qwen-mcp-tool` | `qwen` | ✅ Working |
| Chrome DevTools | `chrome-devtools-mcp@1.6.0` | `chrome-devtools` | ✅ Working |
| NotebookLM | `notebooklm-mcp` | `notebooklm` | ✅ Working |
| Agent Browser | `agent-browser` CLI | `agent-browser` | ✅ Working |

### Python-based (use venv Python `C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe`)

| Server | Module | Config Key | Status |
|--------|--------|------------|--------|
| Git | `mcp_server_git` | `git` | ✅ Working |
| Docker | `docker_mcp.server` | `docker-mcp` | ✅ Working |
| Elasticsearch | `elasticsearch_mcp.server` | `elasticsearch-mcp` | ✅ Working |
| MinIO | `minio_mcp.server` | `minio-mcp` | ✅ Working |
| PostgreSQL | `postgresql_mcp.server` | `postgresql-mcp` | ✅ Working |
| Prometheus | `prometheus_mcp.server` | `prometheus-mcp` | ✅ Working |
| Redis (custom) | `redis_mcp.server` | `redis-mcp` | ✅ Working |
| Session Replay | `session_replay.server` | `session-replay` | ✅ Working |
| Tempo | `tempo_mcp.server` | `tempo-mcp` | ✅ Working |
| Vault | `vault_mcp.server` | `vault-mcp` | ✅ Working |
| Windows System | `windows_system.server` | `windows-system` | ✅ Working |
| Optimus Orchestrator | `optimus_orchestrator.server` | `optimus-orchestrator` | ✅ Working |
| SearXNG | `searxng_mcp.server` | `searxng` | ✅ Working |
| Antigravity Bridge | `antigravity_bridge.server` | `antigravity-bridge` | ✅ Working |
| Blender | `blender_mcp_server.server` | `blender` | ✅ Working |

### Cloud/OAuth (no local install needed)

| Server | Type | Config Key | Status |
|--------|------|------------|--------|
| ComfyUI Cloud | OAuth URL | `comfy-cloud` | ✅ Working |
| Figma | OAuth URL | `figma` | ✅ Working |

## Config File Structure

Three config files that need to stay in sync:

1. **Global**: `C:\Users\apviz\AppData\Local\hermes\config.yaml`
2. **Default Profile**: `C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml`
3. **CLI Prime Profile**: `C:\Users\apviz\AppData\Local\hermes\profiles\cli-prime\config.yaml`

All three must use:
- `command: "C:/Program Files/nodejs/npx.cmd"` for npm packages
- `command: "C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe"` for Python servers
- Forward slashes in all paths (YAML safety)
- Correct package names (see Package Corrections below)

## Package Name Corrections (Post-Update)

Some packages may have been renamed or never existed:

| Old (Broken/Non-existent) | New (Working) |
|---|---|
| `@modelcontextprotocol/server-obsidian` | `@huangyihe/obsidian-mcp` |
| `@modelcontextprotocol/server-chrome-devtools` | `chrome-devtools-mcp@1.6.0` |
| `@modelcontextprotocol/server-docker` | `mcp-docker` (npm) or `docker_mcp.server` (Python) |
| `mcp-server-git` (npm canary package) | `mcp_server_git` (Python module) |
| `blender-mcp==1.6.4` (uvx --with) | `blender_mcp_server.server` (Python module) |
| `agent-browser` (Hermes-local node) | `C:/Users/apviz/AppData/Roaming/npm/agent-browser.cmd` |

## Ollama Integration

Local models available at `http://localhost:11434`:

### All Available Models (27)

| Model | Size | Use Case |
|-------|------|----------|
| `llama2:latest` | 7B | General purpose |
| `nomic-embed-text:latest` | 137M | Embeddings |
| `hermes3:8b` | 8B | Chat assistant |
| `qwen2.5:14b-instruct` | 14.8B | General coding |
| `qwen2.5-coder:14b` | 14.8B | Code specialist |
| `qwen2.5-coder:7b` | 7.6B | Code specialist (smaller) |
| `deepseek-coder-v2:latest` | 15.7B | Code specialist |
| `gemma4:12b` | 7.6B | Lightweight |
| `gemma4:26b` | 17GB | Medium |
| `gemma4:31b` | 19GB | Heavy |
| `gemma3:12b` | 8.1GB | Previous gen |
| `sentinel-designer:latest` | 17GB | Creative/Design |
| `sentinel-cfo:latest` | 19GB | Financial analysis |
| `sentinel-ceo:latest` | 4.7GB | Executive reasoning |
| `sentinel-coo:latest` | 14.8B | Operations |
| `sentinel-assist:latest` | 7.6B | Assistant |
| `sentinel-prime:latest` | 19GB | Primary Sentinel |
| `sentinel-prime-moe:latest` | 17GB | MoE variant |
| `hermes-coder:latest` | 14.8B | Coding specialist |
| `hermes-coder-deepseek:latest` | 8.9GB | Deepseek coding |
| `hermes-translator:latest` | 4.7GB | Translation |
| `hermes-translator-pro:latest` | 9GB | Pro translation |
| `local/qwen2.5-coder:1.5b` | 986MB | Small local |
| `claude-3-5-sonnet-20241022:latest` | 986MB | Claude snapshot |
| `claude-3-5-sonnet-latest:latest` | 986MB | Claude latest |
| `claude-3-7-sonnet-latest:latest` | 986MB | Claude 3.7 |

### Ollama Config (Add to config.yaml after updates)

```yaml
providers:
  ollama:
    base_url: http://localhost:11434/v1
    api_key: ollama
fallback_providers:
  - provider: ollama
    model: sentinel-prime:latest
```

## Obsidian Integration

### Community Plugins (in vault at `D:\Alex_Knowlege_Vault`)

Key plugins installed:
- `hermes-agent` - Hermes Desktop App integration
- `obsidian-local-rest-api` - Local REST API on port 27124
- `obsidian-git` - Git version control for vault
- `dataview` - Query system
- `excalidraw` - Diagram tool
- `kanban` - Kanban boards
- `tasks` - Task management
- `calendar` - Daily notes
- `templater` - Template engine
- `quickadd` - Quick actions
- `outliner` - Outliner mode
- `style-settings` - Appearance customization
- `advanced-tables` - Table formatter
- `tag-wrangler` - Tag management
- `breadcrumbs` - Navigation
- `folder-note` - Folder notes
- `meta-bind` - Metadata binding
- `projects` - Project management
- `excalidraw` - Drawing
- `smart-connections` - AI connections
- `various-complements` - Auto-completion

### Obsidian MCP Server

Config entry uses `@huangyihe/obsidian-mcp` with `--vault-path D:/Alex_Knowlege_Vault`.

### Ollama Models in Hermes Desktop App

After adding the Ollama provider to `config.yaml`, restart the Hermes Desktop App. Local models should appear in the model selection dropdown under the `ollama` provider.

## Recovery Script

Use the automated recovery script:

```bash
python3 C:\Users\apviz\AppData\Local\hermes\scripts\fix_all_yaml_paths.py
```

This script fixes all config files automatically.

## Post-Recovery Verification

```bash
# 1. Verify YAML is valid
hermes doctor --fix

# 2. Test each MCP server category
# Node.js servers
"npx" -y @modelcontextprotocol/server-filesystem "D:/Alex_Knowlege_Vault"
"npx" -y @modelcontextprotocol/server-memory
"npx" -y @huangyihe/obsidian-mcp --vault-path "D:/Alex_Knowlege_Vault"

# Python servers  
"C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" -m mcp_server_git

# 3. Check Ollama
curl -s http://localhost:11434/api/tags | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d[\"models\"])} models')"

# 4. Check Obsidian local REST API
curl -s http://localhost:27124/status | head -5
```
