---
name: sentinel-tool-assessment-protocol
description: Assess available tools before starting any task to avoid capability gaps.
version: 0.1.0
author: Hermes
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [Tools, Assessment, Protocol, Local-First, Autonomy]
---

# Sentinel Tool Assessment Protocol

Mandatory pre-task checklist to assess all available tools, local executables, MCP servers, and Docker services. Prevents "I don't have the tools" failures by establishing local-first awareness.

**Does NOT do:** Cloud-only assumptions, tool invention, skipping verification.

**Key principle:** ALWAYS local first. ALWAYS verify before assuming. Search GitHub for missing tools ONLY after user approval.

## When to Use
- **Every session start** (after identity bootstrap)
- Before any complex/multi-step task
- When you catch yourself saying "I cannot" or "I don't have"
- Before LinkedIn/data extraction tasks
- When user asks "what can you do?"

## Prerequisites
- Hermes installed with config.yaml at `C:\Users\apviz\AppData\Local\hermes\config.yaml`
- `agent-browser` executable at known path
- Docker Desktop running (for searxng, elasticsearch, etc.)
- Internet access for GitHub search (if new tool needed)

## How to Run
```python
# In execute_code or terminal:
from hermes_tools import read_file, search_files, terminal, execute_code, web_search

# 1. Read identity & config
read_file("C:/Users/apviz/AppData/Local/hermes/SOUL.md")
read_file("C:/Users/apviz/AppData/Local/hermes/config.yaml")
read_file("C:/Users/apviz/AppData/Local/hermes/profiles/default/config.yaml")

# 2. List MCP servers from config
# 3. Check Docker services
terminal("docker ps --format 'table {{.Names}}\\t{{.Image}}\\t{{.Ports}}'")

# 4. Verify local executables
terminal("where agent-browser-win32-x64.exe")
# or
import os; os.path.exists(r"C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\bin\agent-browser-win32-x64.exe")

# 5. Quick tool capability matrix
```

## Quick Reference
| Category | Tools / Commands | Verification |
|----------|------------------|--------------|
| **Hermes Core** | `read_file`, `write_file`, `search_files`, `patch`, `terminal`, `execute_code`, `web_search`, `web_extract`, `browser_navigate`, `memory`, `skill_view`, `skill_manage`, `delegate_task`, `cronjob`, `project_create` | Built-in |
| **MCP Servers (23)** | `agent-browser`, `filesystem`, `obsidian`, `git`, `memory`, `qwen`, `sequential-thinking`, `chrome-devtools`, `docker-mcp`, `elasticsearch-mcp`, `grafana-mcp`, `loki-mcp`, `minio-mcp`, `prometheus-mcp`, `postgresql-mcp`, `redis-mcp`, `session-replay`, `tempo-mcp`, `vault-mcp`, `windows-system`, `antigravity-bridge`, `notebooklm`, `searxng` | `read_file(config.yaml) → mcp_servers` |
| **Local Executable** | `agent-browser` (headed/headless, cookies, sessions, eval) | `C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\bin\agent-browser-win32-x64.exe` |
| **Docker Services** | `searxng` (8081), `elasticsearch` (9200), `open-webui` (3000), `aion-ui` (3001), `stirling-pdf` (8080) | `docker ps` |
| **GitHub Search** | `web_search("site:github.com <tool> <keywords>")` | User approval required first |

## Procedure

### Step 1: Identity & Config Load (MANDATORY)
```python
soul = read_file("C:/Users/apviz/AppData/Local/hermes/SOUL.md")
config = read_file("C:/Users/apviz/AppData/Local/hermes/config.yaml")
profile_config = read_file("C:/Users/apviz/AppData/Local/hermes/profiles/default/config.yaml")
memory = read_file("C:/Users/apviz/AppData/Local/hermes/memories/MEMORY.md")
user = read_file("C:/Users/apviz/AppData/Local/hermes/memories/USER.md")
```

### Step 2: MCP Server Inventory
```python
import yaml
cfg = yaml.safe_load(config)
servers = list(cfg.get('mcp_servers', {}).keys())
print(f"Configured MCP servers ({len(servers)}): {servers}")
```

### Step 3: Docker Service Health
```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"
```
Expected: `searxng` (8081), `elasticsearch` (9200), `open-webui` (3000), `aion-ui` (3001)

### Step 4: Local Executable Verification
```python
exe_path = r"C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\bin\agent-browser-win32-x64.exe"
assert os.path.exists(exe_path), "agent-browser missing!"
# Test basic open
terminal(f'"{exe_path}" open https://example.com --headed false --timeout 30000')
```

### Step 5: Capability Matrix for Task
| Task Need | Available Tool | Verified? |
|-----------|----------------|-----------|
| Web search | `web_search` / `searxng` (local) | Yes/No |
| Browser automation | `agent-browser` (local) | Yes/No |
| File ops | `read_file`, `write_file`, `search_files`, `patch` | Yes |
| Code execution | `execute_code`, `terminal` | Yes |
| Data persistence | `memory`, local files, Elasticsearch | Yes |
| LinkedIn auth | `agent-browser` session + cookies | Yes/No |
| Git operations | `git` MCP / `terminal` | Yes |
| Obsidian vault | `obsidian` MCP | Yes |

### Step 6: Gap Resolution Protocol
If ANY "No" in matrix:
1. **STOP** — Do not proceed with workaround
2. **Search** — `web_search("site:github.com <capability> mcp server")` or `web_search("site:github.com <capability> python cli")`
3. **Present** — Show user 2-3 options with repo stars, maintenance status
4. **Get R0** — Explicit user approval: "Install [tool] from [repo]?"
5. **Install** — `terminal("pip install ...")` or `terminal("npm install -g ...")` or Docker
6. **Verify** — Re-run capability matrix
7. **Document** — Add to skill or memory for next session

## Pitfalls
- **Cloud assumption** — "I can't access LinkedIn" → WRONG. Local browser + your login = full access
- **Tool amnesia** — Forgetting `agent-browser` exists → Run assessment every session
- **MCP server blindness** — 23 servers configured; check `config.yaml` before saying "no tool"
- **Docker service down** — `searxng` 403 = config missing; check `docker logs searxng`
- **GitHub search without approval** — NEVER install without explicit user R0
- **Cookie save error** — `restore: loaded; save: error` is benign; cookies work in memory

## Verification
```bash
# Run this and all should pass:
python -c "
import os, subprocess, yaml
assert os.path.exists(r'C:\Users\apviz\AppData\Local\hermes\SOUL.md'), 'SOUL.md missing'
assert os.path.exists(r'C:\Users\apviz\AppData\Local\hermes\config.yaml'), 'config.yaml missing'
cfg = yaml.safe_load(open(r'C:\Users\apviz\AppData\Local\hermes\config.yaml'))
assert len(cfg.get('mcp_servers', {})) >= 20, f'Only {len(cfg.get(\"mcp_servers\", {}))} MCP servers'
exe_path = r'C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\bin\agent-browser-win32-x64.exe'
assert os.path.exists(exe_path), 'agent-browser executable missing'
result = subprocess.run([exe_path, 'open', 'https://example.com', '--headed', 'false', '--timeout', '10000'], capture_output=True, timeout=15)
assert result.returncode == 0, f'agent-browser failed: {result.stderr}'
print('✓ SOUL.md exists')
print('✓ config.yaml exists with 20+ MCP servers')
print('✓ agent-browser executable works')
docker_result = subprocess.run(['docker', 'ps', '--format', '{{.Names}}'], capture_output=True, text=True)
running = docker_result.stdout.strip().split('\n')
required = {'searxng', 'elasticsearch', 'open-webui', 'aion-ui'}
missing = required - set(running)
assert not missing, f'Docker services missing: {missing}'
print('✓ All 4 Docker services running')
print('\\nALL CHECKS PASSED - LOCAL AUTONOMY CONFIRMED')
"
```

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

