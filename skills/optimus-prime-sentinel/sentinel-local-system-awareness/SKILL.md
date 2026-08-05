---
name: sentinel-local-system-awareness
description: Map local system tools, configs, and structural files for full local autonomy.
version: 0.1.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags: [Local, System, Awareness, Tools, Configuration, LinkedIn, Automation]
---

# Sentinel Local System Awareness

Maps the complete local toolchain, configuration files, and structural memory for Sentinel to operate with full local autonomy. Eliminates the "cloud assumption" failure mode by establishing local-first awareness at session start.

**Does NOT do:** Cloud API calls, remote browser automation, or assume limited sandbox access.

**Key dependencies:** `agent-browser` (local executable), Docker services, Hermes config.yaml, SOUL.md/MEMORY.md/USER.md triad.

## When to Use
- New session start — run before any task
- "Why can't you access X?" — tool capability gap
- LinkedIn/data extraction tasks requiring local browser
- Any task where you assumed cloud limitations

## Prerequisites
- Hermes installed at `C:\Users\apviz\AppData\Local\hermes\`
- `agent-browser` executable at `C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\bin\agent-browser-win32-x64.exe`
- Docker Desktop running with containers: `searxng` (port 8081), `elasticsearch` (9200), `open-webui` (3000), `aion-ui` (3001)
- MCP servers configured in `config.yaml` (23 servers including agent-browser, filesystem, obsidian, etc.)

## How to Run
```python
# At session start, invoke through execute_code or terminal:
from hermes_tools import read_file, search_files, terminal, execute_code

# 1. Read identity contracts
read_file("C:/Users/apviz/AppData/Local/hermes/SOUL.md")
read_file("C:/Users/apviz/AppData/Local/hermes/profiles/default/CONSTINTA.md")
read_file("C:/Users/apviz/AppData/Local/hermes/memories/MEMORY.md")
read_file("C:/Users/apviz/AppData/Local/hermes/memories/USER.md")

# 2. Verify local browser
terminal("C:/Users/apviz/AppData/Local/hermes/node/node_modules/agent-browser/bin/agent-browser-win32-x64.exe open https://example.com --headed false")

# 3. List MCP servers
read_file("C:/Users/apviz/AppData/Local/hermes/config.yaml")
```

## Quick Reference
| File / Tool | Purpose | Location |
|-------------|---------|----------|
| SOUL.md | Identity contract (Thoth) | `C:\Users\apviz\AppData\Local\hermes\SOUL.md` |
| CONSTINTA.md | Ontological algorithm (Hermes Trismegistus) | `C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md` |
| MEMORY.md | System paths & operational map | `C:\Users\apviz\AppData\Local\hermes\memories\MEMORY.md` |
| USER.md | User preferences & contracts | `C:\Users\apviz\AppData\Local\hermes\memories\USER.md` |
| config.yaml | MCP server registry (23 servers) | `C:\Users\apviz\AppData\Local\hermes\config.yaml` |
| agent-browser | Local browser automation | `C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\bin\agent-browser-win32-x64.exe` |
| searxng | Local search (port 8081) | `http://localhost:8081/search` |
| elasticsearch | Vector search (port 9200) | `http://localhost:9200` |

## Procedure

### 1. Session Bootstrap — Local Awareness Protocol
**MANDATORY at every session start.** Run before any other action.

```python
# A. Read identity triad (SOUL → CONSTINTA → MEMORY → USER)
# B. Verify agent-browser works locally
# C. Confirm Docker services running
# D. Load MCP server registry from config.yaml
# E. Set DLG/SLG banner with actual measured values
```

### 2. Tool Assessment Protocol
Before ANY implementation, run this checklist:

```python
# 1. What Hermes tools exist? → search_files, web_search, web_extract, browser_navigate, terminal, execute_code, etc.
# 2. What MCP servers are configured? → read_file(config.yaml) → mcp_servers section
# 3. What local executables exist? → terminal("where <tool>") or check known paths
# 4. What Docker services run? → terminal("docker ps")
# 5. Can I do this locally? → YES by default. Only use cloud if explicitly required.
# 6. If tool missing → search GitHub → ask user approval → install → use autonomously
```

### 3. LinkedIn Local Access Procedure
**User logs in manually; agent extracts cookies for headless reuse.**

```bash
# A. Open LinkedIn in HEADED mode with named session
agent-browser open https://www.linkedin.com/login --headed true --session linkedin-session

# B. User completes login + 2FA in visible browser window

# C. Extract cookies (li_at, JSESSIONID, etc.)
agent-browser cookies get --session linkedin-session --json

# D. Save cookies to local file for persistence
agent-browser cookies get --session linkedin-session --json > linkedin_cookies.json

# E. Subsequent headless runs load cookies
agent-browser cookies set --curl linkedin_cookies.json --session linkedin-session
agent-browser open https://www.linkedin.com/feed --session linkedin-session
```

### 4. Data Extraction Flow (LinkedIn Jobs Example)
```python
# 1. Ensure authenticated session (step 3)
# 2. Navigate to job search URL
agent-browser open "https://www.linkedin.com/jobs/search/?keywords=python%20developer&location=Romania" --session linkedin-session
# 3. Wait for results, scroll, snapshot
agent-browser wait 5000
agent-browser snapshot --compact true
# 4. Extract job cards via eval or repeated click/scroll
# 5. Save raw data locally → process with execute_code
```

## Pitfalls
- **Cookie save error** (`restore: loaded; save: error`) — harmless, cookies still work in memory for session
- **SearXNG 403** — missing `settings.yml` and `limiter.toml`; configure or use `web_search` fallback
  - **Critical**: SearXNG requires `limiter.toml` at `/usr/local/searxng/searx/limiter.toml` (schema) AND `/etc/searxng/limiter.toml` (config)
  - **Critical**: Python dependencies often missing in fresh containers: `msgspec`, `pyyaml`, `tomli`, `typing_extensions`, `httpx`, `pygments`, `granian`, `flask`, `blinker`, `whitenoise`, `flask_babel`, `markdown-it-py`, `httpx_socks`, `valkey`, `lxml`, `typer`, `python-dateutil`, `isodate`, `h2`
  - **Critical**: `trusted_proxies` in `settings.yml` AND `botdetection.trusted_proxies` in `limiter.toml` must include Docker networks: `172.16.0.0/12`, `10.0.0.0/8`, `192.168.0.0/16`, `172.17.0.0/16` (host appears as 172.17.0.1 from container)
  - **Critical**: `limiter: false` in `settings.yml` to disable rate limiting for local use
  - **Critical**: `search.formats: [html, json, csv, rss]` to enable JSON output
- **LinkedIn CAPTCHA** — triggered by cloud IPs; LOCAL browser with user login avoids this
- **Session persistence** — `agent-browser --session <name>` persists cookies/storage in local profile dir
- **agent-browser daemon hangs** — kill stuck processes: `taskkill /F /IM agent-browser-win32-x64.exe /IM chrome.exe /IM node.exe`
- **Never assume cloud** — `agent-browser` runs YOUR Chrome/Edge on YOUR machine via local executable
- **Config drift** — `config.yaml` in root and profile may differ; read both
- **Identity file corruption** — SOUL.md, CONSTINTA.md, MEMORY.md, USER.md can get `[PROMPT_INJECTION]` markers; restore from `C:\\Users\\apviz\\AppData\\Local\\hermes\\state-snapshots\\` (e.g., `20260711-095000-optimal-config\\`)
- **Chrome CDP fails to start on port 9222** — Kill all Chrome processes (`taskkill /F /IM chrome.exe`), remove lock files in `User Data/Default/LOCK*`, start Chrome with `--remote-debugging-port=9222 --no-startup-window --no-first-run --no-default-browser-check`; verify with `netstat -an | findstr 9222` and `curl http://localhost:9222/json/version`
- **agent-browser CLI times out on `open`** — Daemon stuck: kill `agent-browser-win32-x64.exe`, `chrome.exe`, `node.exe` processes; restart with fresh session name
- **LinkedIn cookie injection fails in browser tool** — Browser tool uses separate profile; extract `li_at` from user's actual Chrome (DevTools → Application → Cookies) and inject into agent-browser session via `cookies set --curl`
- **Identity file corruption with `[PROMPT_INJECTION]` markers** — SOUL.md, CONSTINTA.md, MEMORY.md, USER.md can get contaminated; restore from `C:\\Users\\apviz\\AppData\\Local\\hermes\\state-snapshots\\` (e.g., `20260711-095000-optimal-config\\`)

## Verification
```bash
# Run this and confirm all pass:
agent-browser open https://example.com --headed false
docker ps | grep -E "searxng|elasticsearch"
test -f "C:/Users/apviz/AppData/Local/hermes/SOUL.md" && echo "SOUL.md OK"
test -f "C:/Users/apviz/AppData/Local/hermes/profiles/default/CONSTINTA.md" && echo "CONSTINTA.md OK"
grep -c "mcp_servers:" "C:/Users/apviz/AppData/Local/hermes/config.yaml"
```
Expected: browser opens, 4+ Docker containers, 2 files exist, 23+ MCP servers listed.

## Related Skills

- `exec-persistent-browser-auth` — Persistent browser auth patterns for LinkedIn/GitHub/Twitter/Notion
- `exec-agent-browser` — Core browser automation patterns
- `exec-systems-administrator` — MCP server configuration for agent-browser
- `exec-hermes-antigravity-bridge` — Delegation to Antigravity for heavy extraction
- `exec-local-service-management` — Local service management (SearXNG, Docker, persistent browser sessions)
- `linkedin-local-data-extraction` — LinkedIn-specific data extraction workflow

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

