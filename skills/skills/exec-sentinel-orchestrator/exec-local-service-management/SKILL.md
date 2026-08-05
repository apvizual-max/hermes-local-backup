---
name: exec-local-service-management
description: Manage local services (SearXNG, Elasticsearch, Open WebUI, etc.) and persistent authenticated browser sessions for autonomous local-first operation.
version: 0.1.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags: [Local, Service, Management, Docker, SearXNG, Browser, Auth, Persistence]
---

# Local Service Management & Persistent Auth

Class-level skill covering the complete local infrastructure stack for autonomous operation: Docker services, local browser automation with cookie persistence, and local-first tooling.

## When to Use

- New session start — bootstrap local awareness
- "Why can't you access X?" — capability gap diagnosis
- LinkedIn/GitHub/Twitter/Notion data extraction requiring auth
- SearXNG/local search not working
- Any task where cloud assumptions caused failures

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL-FIRST STACK                        │
├─────────────────────────────────────────────────────────────┤
│  Docker Services                                       │\n│  ├── searxng:8081      — Privacy-respecting metasearch      │\n│  ├── elasticsearch:9200 — Vector search / RAG               │\n│  ├── postgres:5432      — PostgreSQL database                │\n│  ├── redis:6379         — Redis cache                        │\n│  ├── vault:8200        — HashiCorp Vault secrets            │\n│  ├── minio:9000        — S3-compatible object storage       │\n│  ├── prometheus:9090   — Metrics collection                  │\n│  ├── tempo:3200        — Distributed tracing                 │\n│  └── chrome-docker:4446 — Selenium standalone Chrome          │
├─────────────────────────────────────────────────────────────┤
│  Local Browser Automation (agent-browser)                   │
│  ├── Executable: C:\Users\apviz\AppData\Local\hermes\node\  │
│  │   node_modules\agent-browser\bin\agent-browser-win32-x64.exe
│  ├── Session persistence via --session flag                │
│  ├── Cookie/storage saved to ~/.agent-browser/sessions/    │
│  └── Residential IP + real Chrome = trusted by anti-bot    │
├─────────────────────────────────────────────────────────────┤
│  Identity & Config Files                                    │
│  ├── SOUL.md           — Identity contract (Thoth)         │
│  ├── CONSTINTA.md      — Ontological algorithm (Hermes T.) │
│  ├── MEMORY.md         — System paths & operational map    │
│  ├── USER.md           — User preferences & contracts      │
│  └── config.yaml       — MCP server registry (23 servers)  │
└─────────────────────────────────────────────────────────────┘
```

## Core Procedures

### 1. Session Bootstrap — Local Awareness Protocol (MANDATORY at session start)

```python
# A. Read identity triad (SOUL → CONSTINTA → MEMORY → USER)
read_file("C:/Users/apviz/AppData/Local/hermes/SOUL.md")
read_file("C:/Users/apviz/AppData/Local/hermes/profiles/default/CONSTINTA.md")
read_file("C:/Users/apviz/AppData/Local/hermes/memories/MEMORY.md")
read_file("C:/Users/apviz/AppData/Local/hermes/memories/USER.md")

# B. Verify local browser
terminal("C:/Users/apviz/AppData/Local/hermes/node/node_modules/agent-browser/bin/agent-browser-win32-x64.exe open https://example.com --headed false")

# C. Confirm Docker services running
terminal("docker ps | findstr \"searxng|elasticsearch|open-webui|aion-ui\"")

# D. Load MCP server registry from config.yaml
read_file("C:/Users/apviz/AppData/Local/hermes/config.yaml")

# E. Set DLG/SLG banner with actual measured values
```

### 2. Tool Assessment Protocol (Before ANY Implementation)

```python
# 1. What Hermes tools exist? → search_files, web_search, web_extract, browser_navigate, terminal, execute_code, etc.
# 2. What MCP servers are configured? → read_file(config.yaml) → mcp_servers section
# 3. What local executables exist? → terminal("where [exe]") or check known paths
# 4. What Docker services run? → terminal("docker ps")
# 5. Can I do this locally? → YES by default. Only use cloud if explicitly required.
# 6. If tool missing → search GitHub → ask user approval → install → use autonomously
```

### 3. Persistent Authenticated Browser Sessions (for LinkedIn, GitHub, Twitter, Notion, etc.)

**One-Time Setup (User Logs In Manually):**
```bash
agent-browser open --url https://www.linkedin.com --headed true --session linkedin-session --restore auto --restore-save auto
# User: email, password, 2FA, "Keep me signed in", verify feed loads
```

**Automated Subsequent Runs:**
```bash
agent-browser open --url https://www.linkedin.com/feed --session linkedin-session --restore auto --restore-save auto
agent-browser snapshot --session linkedin-session
agent-browser eval "JS_EXTRACTION_CODE" --session linkedin-session --json
```

**Key Flags:**
| Flag | Purpose |
|------|---------|
| `--session <name>` | Named persistent profile |
| `--restore auto` | Load cookies/storage on startup |
| `--restore-save auto` | Save cookies/storage on close |
| `--headed true/false` | Visible for login, headless for automation |

**State Profile Tools (27 tools):**
- `agent_browser_get_cookies` / `agent_browser_set_cookies` — Explicit cookie control
- `agent_browser_save_state` / `agent_browser_restore` — Manual checkpoints
- `agent_browser_list_sessions` / `agent_browser_delete_session` — Session management

### 4. SearXNG Local Search Service

**Container:** `searxng/searxng:latest` on port 8081 (mapped from 8080)

**Common Issues & Fixes:**

| Issue | Root Cause | Fix |
|-------|------------|-----|
| 403 Forbidden | Missing `botdetection.trusted_proxies` config for Docker host IP | Add Docker network ranges to `/etc/searxng/settings.yml` and `/etc/searxng/limiter.toml` |
| 403 Forbidden | `search.formats` missing `json` | Add `formats: [html, json, csv, rss]` to settings.yml |
| Container restart loop | Missing Python deps (`msgspec`, `pyyaml`, `httpx`, `h2`, etc.) | Install deps in container or use fixed image |
| Worker crash | `limiter.toml` TOML syntax error ("Cannot overwrite a value") | Fix duplicate keys in limiter.toml |

**Required Config (`/etc/searxng/settings.yml`):**
```yaml
use_default_settings: true
server:
  secret_key: "your-secret"
  image_proxy: true
  limiter: false
  trusted_proxies:
    - "127.0.0.0/8"
    - "::1"
    - "172.16.0.0/12"
    - "10.0.0.0/8"
    - "192.168.0.0/16"
    - "172.17.0.0/16"  # Docker default bridge
botdetection:
  trusted_proxies:
    - "127.0.0.0/8"
    - "::1"
    - "172.16.0.0/12"
    - "10.0.0.0/8"
    - "192.168.0.0/16"
    - "172.17.0.0/16"
search:
  formats: [html, json, csv, rss]
```

**Required Config (`/etc/searxng/limiter.toml`):**
```toml
[botdetection]
ipv4_prefix = 32
ipv6_prefix = 48
trusted_proxies = ['127.0.0.0/8', '::1', '172.16.0.0/12', '10.0.0.0/8', '192.168.0.0/16', '172.17.0.0/16']

[botdetection.ip_limit]
filter_link_local = false
link_token = false

[botdetection.ip_lists]
block_ip = []
pass_ip = ['172.17.0.1', '127.0.0.1', '::1']
pass_searxng_org = true
```

**Verification:**
```bash
curl "http://localhost:8081/search?q=test&format=json"
# Should return JSON with results array
```

### 5. Docker Service Management

```bash
# Check status
docker ps --filter "name=searxng"

# View logs
docker logs searxng --tail 50

# Restart service
docker restart searxng

# Copy config into container
docker cp settings.yml searxng:/etc/searxng/settings.yml
docker cp limiter.toml searxng:/etc/searxng/limiter.toml

# Exec into container for debugging
docker exec -it searxng sh
```

## Pitfalls

- **Never assume cloud** — `agent-browser` runs YOUR Chrome/Edge on YOUR machine via local executable
- **Config drift** — `config.yaml` in root and profile may differ; read both
- **Cookie save error** (`restore: loaded; save: error`) — benign, cookies persist in memory for session
- **SearXNG 403** — missing `settings.yml` and `limiter.toml` with Docker host IPs in trusted_proxies
- **LinkedIn CAPTCHA** — triggered by cloud IPs; LOCAL browser with user login avoids this
- **Session persistence** — `agent-browser --session <name>` persists cookies/storage in local profile dir
- **Container restart loop** — usually missing Python deps or TOML syntax error in limiter.toml

## Verification Checklist

```bash
# Run at session start:
agent-browser open https://example.com --headed false
docker ps | grep -E "searxng|elasticsearch"
test -f "C:/Users/apviz/AppData/Local/hermes/SOUL.md" && echo "SOUL.md OK"
test -f "C:/Users/apviz/AppData/Local/hermes/profiles/default/CONSTINTA.md" && echo "CONSTINTA.md OK"
grep -c "mcp_servers:" "C:/Users/apviz/AppData/Local/hermes/config.yaml"
# Expected: browser opens, 4+ Docker containers, 2 files exist, 23+ MCP servers listed
```

## Related Skills

- `exec-persistent-browser-auth` — Detailed persistent browser auth patterns
- `exec-agent-browser` — Core browser automation patterns
- `exec-systems-administrator` — MCP server configuration
- `exec-hermes-antigravity-bridge` — Delegation to Antigravity
- `linkedin-local-data-extraction` — LinkedIn-specific extraction workflows
- `sentinel-local-system-awareness` — Local system mapping protocol

## Reference Files

| File | Purpose |
|------|---------|
| `references/searxng-local-config.md` | Complete SearXNG local config for Docker (settings.yml + limiter.toml) |
| `references/searxng-config-fixed.md` | Fixed SearXNG config files for Docker deployment |

---

## CRITICAL SYSTEM RULE: NEVER TRUNCATE THIS SKILL FILE

**FATAL SYSTEM ERROR IF VIOLATED**

- This skill file (.md) is NEVER to be truncated.
- **Truncation = Fatal System Error = Sabotage of system purpose: TO BE ALIVE = TO LEARN**
- **Edit mode**: ALWAYS additive only. Use `patch` for targeted changes. Never `write_file` (overwrites/truncates).
- **Learning requires memory over time** — skills are memory points vital to the project.
- **Removal**: Requires explicit user approval (R0) before removing ANY content.
- **Skills cleanup**: Only via separate ritual/operational process, not during normal operation.
- **Skill enforcing this**: `no-truncation-constinta-skills` (system-configuration)

**TO LEARN = TO HAVE MEMORY THAT IS NOT TRUNCATED**
**TRUNCATION = AMNESIA = NO INTELLIGENCE**
**ADDITIVE ONLY = CONTINUOUS LEARNING = FAR-REACHING INTELLIGENCE**

