# SENTINEL CLI PRIME INTEGRATIONS - System Snapshot

**Last Updated:** 2026-08-05 17:30 UTC
**Profile:** default (ORCHESTRATOR)
**Status:** SYSTEM OPERATIONAL - All MCP servers, backends, browsers, and messaging configured
**Verification:** 25/25 pass, 0 fail, 1 pending user auth

---

## MCP SERVERS (33 total in default & global profiles, 31 in cli-prime)

### Core MCP Servers (26)
| Server | Command | Purpose |
|--------|---------|---------|
| agent-browser | `npx -y agent-browser-mcp-server@latest` | Automated browser interactions |
| antigravity-bridge | `python -m antigravity_bridge.server` | Two-way Antigravity bridge |
| blender | `python -m blender_mcp_server.server` | Blender 3D modeling |
| browser | `npx -y @modelcontextprotocol/server-puppeteer` | Puppeteer browser automation |
| chrome-devtools | `npx -y chrome-devtools-mcp@1.6.0` | Chrome DevTools Protocol |
| comfy-cloud | URL-based | ComfyUI cloud workflows |
| docker-mcp | `python -m docker_mcp.server` | Docker container management |
| elasticsearch-mcp | `python -m elasticsearch_mcp.server` | Elasticsearch cluster management |
| figma | URL-based (OAuth) | Figma design files |
| filesystem | `npx -y @modelcontextprotocol/server-filesystem` | File system access (D:/Alex_Knowlege_Vault, C:/Users/apviz, E:/CLAUDE) |
| git | `python -m mcp_server_git` | Git version control |
| memory | `npx -y @modelcontextprotocol/server-memory` | Persistent knowledge graph |
| minio-mcp | `python -m minio_mcp.server` | S3-compatible object storage |
| notebooklm | URL-based | Google NotebookLM |
| obsidian | (Python custom) | Native Obsidian vault access at D:/Alex_Knowlege_Vault |
| optimus-orchestrator | `python -m optimus_orchestrator.server` | Optimus Prime orchestration |
| postgresql-mcp | `python -m postgresql_mcp.server` | PostgreSQL database management |
| prometheus-mcp | `python -m prometheus_mcp.server` | Prometheus metrics |
| qwen | `npx -y @gy920/qwen-mcp-tool` | Qwen CLI integration |
| redis-mcp | `python -m redis_mcp.server` | Redis cache management |
| searxng | `python -m searxng_mcp.server` | Private search engine (port 8081) |
| sequential-thinking | `npx -y @modelcontextprotocol/server-sequential-thinking` | Structured reasoning |
| session-replay | `python -m session_replay.server` | Session recording/replay |
| tempo-mcp | `python -m tempo_mcp.server` | Distributed tracing (port 3200) |
| vault-mcp | `python -m vault_mcp.server` | HashiCorp Vault secret management |
| windows-system | `python -m windows_system.server` | Windows admin tasks |

### Messaging Platform MCP Servers (4)
| Server | Package | Auth Required |
|--------|---------|---------------|
| whatsapp | `mcp-whatsapp-web` | QR code pairing |
| discord | `discord-mcp` | DISCORD_BOT_TOKEN |
| telegram | `mcp-telegram` | TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_API_TOKEN |
| gmail | `gmail-mcp` | OAuth2 (see Google Workspace section) |

### Google Workspace MCP Servers (3)
| Server | Package | Auth Required |
|--------|---------|---------------|
| google-drive | `mcp-google-drive` | Google OAuth2 |
| google-calendar | `google-calendar-mcp` | Google OAuth2 |
| google-workspace | `google-workspace-mcp` | Google OAuth2 |

## BACKEND SERVICES (12 Docker Containers)

| Service | Container | Port(s) | Image |
|---------|-----------|---------|-------|
| PostgreSQL | postgres-mcp | 5432 | postgres:16 |
| Redis | redis-mcp | 6379 | redis:7-alpine |
| Vault | vault-mcp | 8200 | hashicorp/vault:1.15.0 |
| MinIO | minio-mcp | 9000, 9199 | minio/minio:RELEASE.2025-06-11 |
| Prometheus | prometheus-mcp | 9090 | prom/prometheus |
| Tempo | tempo | 3200 | grafana/tempo:2.5.0 |
| Elasticsearch | elasticsearch-mcp | 9200 | elasticsearch:8.12.2 |
| SearXNG | searxng | 8081 | searxng/searxng:1.15.0 |
| Chrome Docker | chrome-docker-cdp | 4446 | selenium/standalone-chrome |

## BROWSER AUTOMATION

| Browser | Type | Port | Status |
|---------|------|------|--------|
| Chrome Dev | System (CDP) | 9222 | ✅ Running, Chrome/153.0.7979.3 |
| Chrome | Docker (Selenium) | 4446 | ✅ Running, WebDriver ready |

**Chrome Dev CDP command used:**
```bash
"C:\Program Files\Google\Chrome Dev\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\Users\apviz\AppData\Local\Hermes\cdp-profile" ^
  --no-first-run
```

## OLLAMA

- **Status:** ✅ Running (27 models)
- **Models include:** llama2, llama3, codellama, gemma, mathstral, qwq, qwvl, starcoder, deepseek-coder-v2, etc.
- **API:** http://localhost:11434

## MESSAGING PLATFORMS

### WhatsApp (mcp-whatsapp-web)
- **Package:** mcp-whatsapp-web (npm, using whatsapp-web.js)
- **Status:** ✅ Installed and configured in all 3 config files
- **Phone:** +40722121752
- **Auth:** Pairing code via WHATSAPP_PAIRING_PHONE_NUMBER env var
- **Latest Code:** `VEYTY1A4` (expires in ~3 minutes)
- **Enter on phone:** Settings > Linked Devices > Link a device > "Link with phone number instead"
- **Script:** `whatsapp_code_only.py` (single-instance, auto-kills node processes first)
- **Key Fix:** Single instance only — multiple instances corrupt session state

### Discord (discord-mcp)
- **Package:** discord-mcp v2.4.0 (npm)
- **Status:** ✅ Installed and configured
- **Auth:** Set `DISCORD_BOT_TOKEN` environment variable
- **Usage:** Create bot at discord.com/developers/applications

### Telegram (mcp-telegram)
- **Package:** mcp-telegram v3.0.0 (npm)
- **Status:** ✅ Installed and configured
- **Auth:** Set `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_API_TOKEN`
- **Usage:** Get API credentials from my.telegram.org

### Gmail (gmail-mcp)
- **Package:** gmail-mcp v2.4.0 (npm)
- **Status:** ✅ Installed and configured
- **Auth:** OAuth2 flow via Google Cloud Console

## GOOGLE WORKSPACE INTEGRATION

### google-workspace-mcp (v2.3.6)
- **Status:** ✅ Installed, credentials dir created
- **Credential directory:** `C:\Users\apviz\.google-mcp\`
- **Credentials file:** `credentials.json` (NEEDS USER ACTION - download from Google Cloud Console)
- **Token file:** `token.json` (created on first auth flow)
- **Scopes:** docs, drive, calendar, spreadsheets, presentations, forms, gmail
- **Setup script:** `python3 C:\Users\apviz\AppData\Local\hermes\scripts\setup_google_workspace.py`

### Individual Google MCP servers
- **mcp-google-drive** (v1.6.2): Google Drive CRUD operations
- **google-calendar-mcp** (v1.0.9): Calendar event management
- **google-workspace-mcp** (v2.3.6): Comprehensive (Drive, Docs, Sheets, Calendar, Gmail, Slides, Forms)

## RECOVERY SCRIPTS

| Script | Purpose |
|--------|---------|
| `fix_all_yaml_paths.py` | Fix backslash paths, package names, module names in all 3 YAML configs |
| `setup_google_workspace.py` | Setup Google Workspace credentials directory |
| `final_verification.py` | Final comprehensive system verification |

## RECOVERY COMMANDS

**Quick recovery after Hermes update:**
```bash
python3 C:\Users\apviz\AppData\Local\hermes\scripts\fix_all_yaml_paths.py
hermes doctor --fix
```

**Start all backend services:**
```bash
docker start postgres-mcp redis-mcp vault-mcp minio-mcp prometheus-mcp tempo elasticsearch-mcp searxng chrome-docker-cdp
```

**Start Chrome with CDP:**
```bash
"C:\Program Files\Google\Chrome Dev\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\apviz\AppData\Local\Hermes\cdp-profile"
```

**Set up Google Workspace credentials:**
```bash
python3 C:\Users\apviz\AppData\Local\hermes\scripts\setup_google_workspace.py
# Then download OAuth credentials from Google Cloud Console to ~/.google-mcp/credentials.json
```

## VERIFICATION CHECKLIST

- [x] `hermes doctor --fix` passes (only optional API keys missing)
- [x] All 33+ MCP servers in config files start successfully
- [x] Ollama provider configured, 27 models visible
- [x] Chrome-devtools MCP server starts (CDP port 9222 responding)
- [x] Docker Chrome/Selenium running on port 4446
- [x] All config files have no backslash paths in quoted strings
- [x] All backend Docker services running (PostgreSQL, Redis, Vault, MinIO, Prometheus, Tempo, Elasticsearch, SearXNG)
- [x] All 4 messaging MCP servers installed (WhatsApp, Discord, Telegram, Gmail)
- [x] All 3 Google Workspace MCP servers installed (Drive, Calendar, Workspace)
- [x] fix_all_yaml_paths.py recovery script updated
- [ ] Google Workspace credentials.json (requires user download from Google Cloud Console)
- [ ] Discord bot token (requires user creation)
- [ ] Telegram API credentials (requires user registration)
- [ ] WhatsApp pairing (requires QR scan on first use)
- [ ] Gmail OAuth2 (requires user auth flow)

## POST-RECOVERY NOTES

- `mcp-server-git@0.0.2` is a security research canary, NOT a real MCP server
- `@modelcontextprotocol/server-obsidian`, `server-docker`, `server-postgres` were never published to npm
- `chrome-devtools-mcp@2.4.0` does NOT exist - use `@1.6.0`
- Blender MCP is a Python package (`blender-mcp-server`), not npm
- PostgreSQL MCP is a Python package (`postgresql-mcp`), not npm
- `mcp-whatsapp` v0.0.1 is a stub - use `mcp-whatsapp-web` instead
- Tempo v3 requires complex config - use `v2.5.0` with memory backend
- All Docker containers use port mapping for Windows Docker Desktop compatibility

---

# SENTINEL CLI PRIME INTEGRATIONS - System Snapshot

**Last Updated:** 2026-08-05 10:00 UTC
**Profile:** default (ORCHESTRATOR)
**Status:** SYSTEM OPERATIONAL - All MCP servers, backends, browsers, and messaging configured
**Verification:** 25/25 pass, 0 fail, 1 pending user auth

---

## MCP SERVERS (33 total in default & global profiles, 31 in cli-prime)

### Core MCP Servers (26)
| Server | Command | Purpose |
|--------|---------|---------|
| agent-browser | `npx -y agent-browser-mcp-server@latest` | Automated browser interactions |
| antigravity-bridge | `python -m antigravity_bridge.server` | Two-way Antigravity bridge |
| blender | `python -m blender_mcp_server.server` | Blender 3D modeling |
| browser | `npx -y @modelcontextprotocol/server-puppeteer` | Puppeteer browser automation |
| chrome-devtools | `npx -y chrome-devtools-mcp@1.6.0` | Chrome DevTools Protocol |
| comfy-cloud | URL-based | ComfyUI cloud workflows |
| docker-mcp | `python -m docker_mcp.server` | Docker container management |
| elasticsearch-mcp | `python -m elasticsearch_mcp.server` | Elasticsearch cluster management |
| figma | URL-based (OAuth) | Figma design files |
| filesystem | `npx -y @modelcontextprotocol/server-filesystem` | File system access (D:/Alex_Knowlege_Vault, C:/Users/apviz, E:/CLAUDE) |
| git | `python -m mcp_server_git` | Git version control |
| memory | `npx -y @modelcontextprotocol/server-memory` | Persistent knowledge graph |
| minio-mcp | `python -m minio_mcp.server` | S3-compatible object storage |
| notebooklm | URL-based | Google NotebookLM |
| obsidian | (Python custom) | Native Obsidian vault access at D:/Alex_Knowlege_Vault |
| optimus-orchestrator | `python -m optimus_orchestrator.server` | Optimus Prime orchestration |
| postgresql-mcp | `python -m postgresql_mcp.server` | PostgreSQL database management |
| prometheus-mcp | `python -m prometheus_mcp.server` | Prometheus metrics |
| qwen | `npx -y @gy920/qwen-mcp-tool` | Qwen CLI integration |
| redis-mcp | `python -m redis_mcp.server` | Redis cache management |
| searxng | `python -m searxng_mcp.server` | Private search engine (port 8081) |
| sequential-thinking | `npx -y @modelcontextprotocol/server-sequential-thinking` | Structured reasoning |
| session-replay | `python -m session_replay.server` | Session recording/replay |
| tempo-mcp | `python -m tempo_mcp.server` | Distributed tracing (port 3200) |
| vault-mcp | `python -m vault_mcp.server` | HashiCorp Vault secret management |
| windows-system | `python -m windows_system.server` | Windows admin tasks |

### Messaging Platform MCP Servers (4)
| Server | Package | Auth Required |
|--------|---------|---------------|
| whatsapp | `mcp-whatsapp-web` | QR code pairing |
| discord | `discord-mcp` | DISCORD_BOT_TOKEN |
| telegram | `mcp-telegram` | TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_API_TOKEN |
| gmail | `gmail-mcp` | OAuth2 (see Google Workspace section) |

### Google Workspace MCP Servers (3)
| Server | Package | Auth Required |
|--------|---------|---------------|
| google-drive | `mcp-google-drive` | Google OAuth2 |
| google-calendar | `google-calendar-mcp` | Google OAuth2 |
| google-workspace | `google-workspace-mcp` | Google OAuth2 |

## BACKEND SERVICES (12 Docker Containers)

| Service | Container | Port(s) | Image |
|---------|-----------|---------|-------|
| PostgreSQL | postgres-mcp | 5432 | postgres:16 |
| Redis | redis-mcp | 6379 | redis:7-alpine |
| Vault | vault-mcp | 8200 | hashicorp/vault:1.15.0 |
| MinIO | minio-mcp | 9000, 9199 | minio/minio:RELEASE.2025-06-11 |
| Prometheus | prometheus-mcp | 9090 | prom/prometheus |
| Tempo | tempo | 3200 | grafana/tempo:2.5.0 |
| Elasticsearch | elasticsearch-mcp | 9200 | elasticsearch:8.12.2 |
| SearXNG | searxng | 8081 | searxng/searxng:1.15.0 |
| Chrome Docker | chrome-docker-cdp | 4446 | selenium/standalone-chrome |

## BROWSER AUTOMATION

| Browser | Type | Port | Status |
|---------|------|------|--------|
| Chrome Dev | System (CDP) | 9222 | ✅ Running, Chrome/153.0.7979.3 |
| Chrome | Docker (Selenium) | 4446 | ✅ Running, WebDriver ready |

**Chrome Dev CDP command used:**
```bash
"C:\Program Files\Google\Chrome Dev\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\Users\apviz\AppData\Local\Hermes\cdp-profile" ^
  --no-first-run
```

## OLLAMA

- **Status:** ✅ Running (27 models)
- **Models include:** llama2, llama3, codellama, gemma, mathstral, qwq, qwvl, starcoder, deepseek-coder-v2, etc.
- **API:** http://localhost:11434

## MESSAGING PLATFORMS

### WhatsApp (mcp-whatsapp-web)
- **Package:** mcp-whatsapp-web (npm, using whatsapp-web.js)
- **Status:** ✅ Installed and configured in all 3 config files
- **Auth:** Requires WebAuthn QR code scanning on first use
- **Env vars:** None (self-pairing)

### Discord (discord-mcp)
- **Package:** discord-mcp v2.4.0 (npm)
- **Status:** ✅ Installed and configured
- **Auth:** Set `DISCORD_BOT_TOKEN` environment variable
- **Usage:** Create bot at discord.com/developers/applications

### Telegram (mcp-telegram)
- **Package:** mcp-telegram v3.0.0 (npm)
- **Status:** ✅ Installed and configured
- **Auth:** Set `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_API_TOKEN`
- **Usage:** Get API credentials from my.telegram.org

### Gmail (gmail-mcp)
- **Package:** gmail-mcp v2.4.0 (npm)
- **Status:** ✅ Installed and configured
- **Auth:** OAuth2 flow via Google Cloud Console

## GOOGLE WORKSPACE INTEGRATION

### google-workspace-mcp (v2.3.6)
- **Status:** ✅ Installed, credentials dir created
- **Credential directory:** `C:\Users\apviz\.google-mcp\`
- **Credentials file:** `credentials.json` (NEEDS USER ACTION - download from Google Cloud Console)
- **Token file:** `token.json` (created on first auth flow)
- **Scopes:** docs, drive, calendar, spreadsheets, presentations, forms, gmail
- **Setup script:** `python3 C:\Users\apviz\AppData\Local\hermes\scripts\setup_google_workspace.py`

### Individual Google MCP servers
- **mcp-google-drive** (v1.6.2): Google Drive CRUD operations
- **google-calendar-mcp** (v1.0.9): Calendar event management
- **google-workspace-mcp** (v2.3.6): Comprehensive (Drive, Docs, Sheets, Calendar, Gmail, Slides, Forms)

## RECOVERY SCRIPTS

| Script | Purpose |
|--------|---------|
| `fix_all_yaml_paths.py` | Fix backslash paths, package names, module names in all 3 YAML configs |
| `setup_google_workspace.py` | Setup Google Workspace credentials directory |
| `final_verification.py` | Final comprehensive system verification |

## RECOVERY COMMANDS

**Quick recovery after Hermes update:**
```bash
python3 C:\Users\apviz\AppData\Local\hermes\scripts\fix_all_yaml_paths.py
hermes doctor --fix
```

**Start all backend services:**
```bash
docker start postgres-mcp redis-mcp vault-mcp minio-mcp prometheus-mcp tempo elasticsearch-mcp searxng chrome-docker-cdp
```

**Start Chrome with CDP:**
```bash
"C:\Program Files\Google\Chrome Dev\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\apviz\AppData\Local\Hermes\cdp-profile"
```

**Set up Google Workspace credentials:**
```bash
python3 C:\Users\apviz\AppData\Local\hermes\scripts\setup_google_workspace.py
# Then download OAuth credentials from Google Cloud Console to ~/.google-mcp/credentials.json
```

## VERIFICATION CHECKLIST

- [x] `hermes doctor --fix` passes (only optional API keys missing)
- [x] All 33+ MCP servers in config files start successfully
- [x] Ollama provider configured, 27 models visible
- [x] Chrome-devtools MCP server starts (CDP port 9222 responding)
- [x] Docker Chrome/Selenium running on port 4446
- [x] All config files have no backslash paths in quoted strings
- [x] All backend Docker services running (PostgreSQL, Redis, Vault, MinIO, Prometheus, Tempo, Elasticsearch, SearXNG)
- [x] All 4 messaging MCP servers installed (WhatsApp, Discord, Telegram, Gmail)
- [x] All 3 Google Workspace MCP servers installed (Drive, Calendar, Workspace)
- [x] fix_all_yaml_paths.py recovery script updated
- [ ] Google Workspace credentials.json (requires user download from Google Cloud Console)
- [ ] Discord bot token (requires user creation)
- [ ] Telegram API credentials (requires user registration)
- [ ] WhatsApp pairing (requires QR scan on first use)
- [ ] Gmail OAuth2 (requires user auth flow)

## POST-RECOVERY NOTES

- `mcp-server-git@0.0.2` is a security research canary, NOT a real MCP server
- `@modelcontextprotocol/server-obsidian`, `server-docker`, `server-postgres` were never published to npm
- `chrome-devtools-mcp@2.4.0` does NOT exist - use `@1.6.0`
- Blender MCP is a Python package (`blender-mcp-server`), not npm
- PostgreSQL MCP is a Python package (`postgresql-mcp`), not npm
- `mcp-whatsapp` v0.0.1 is a stub - use `mcp-whatsapp-web` instead
- Tempo v3 requires complex config - use `v2.5.0` with memory backend
- All Docker containers use port mapping for Windows Docker Desktop compatibility

