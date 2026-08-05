---
title: Verification Checklist & Quick Reference
version: 1.0.0
---

# Verification Checklist & Quick Reference

## Complete Integration Verification

### ✅ Codex CLI (OpenAI)
- [x] Installed: `cd ~/.hermes/node && npm install @openai/codex`
- [x] Binary: `~/.hermes/node/codex` on PATH
- [x] Version: `codex --version` → 0.146.0+
- [x] Auth: `codex login --device-auth` + browser
- [x] Status: `codex login status` → "Logged in using ChatGPT"
- [x] Tokens: `~/.codex/auth.json` exists with id_token, access_token, refresh_token
- [x] Hermes: `hermes auth add openai-codex --type oauth --label codex-oauth`
- [x] Pool: `hermes auth list` shows `openai-codex (1 credentials)`
- [x] Doctor: `hermes doctor --fix` → ✓ OpenAI Codex auth (logged in)

### ✅ Antigravity/Gemini CLI (Google)
- [x] Installed: `/c/Users/apviz/AppData/Local/agy/bin/agy` on PATH
- [x] Version: `agy --version` → 1.1.1+
- [x] Auth: `agy auth login` + browser (Google OAuth)
- [x] Tokens: `~/.gemini/oauth_creds.json` exists with access_token, refresh_token, expiry_date
- [x] Hermes Provider: `gemini-oauth` added to `PROVIDER_REGISTRY`
- [x] Model Entry: Added to `CANONICAL_PROVIDERS` in `models.py`
- [x] OAuth Catalog: Added to `_OAUTH_PROVIDER_CATALOG` in `web_server.py`
- [x] Auth Commands: Added handler in `auth_commands.py`
- [x] Status Function: `get_gemini_oauth_auth_status()` in `auth.py`
- [x] Doctor Check: Added to `doctor.py`
- [x] Pool: `hermes auth add gemini-oauth` → `hermes auth list` shows `gemini-oauth (1 credentials)`
- [x] Doctor: `hermes doctor --fix` → ✓ Google Gemini OAuth (logged in via Antigravity CLI)

### ✅ Antigravity Bridge MCP
- [x] Server: `~/.hermes/mcp-servers/custom/antigravity-bridge/src/antigravity_bridge/server.py`
- [x] Config: `config.yaml` includes `antigravity-bridge` in `mcp_servers`
- [x] Tools: 9 tools exposed (delegate, poll, list_pending, read_response, cancel, send_message, get_status, list_history, clear_history)
- [x] IPC: File-based at `~/.hermes/pairing/antigravity/`
- [x] Verified: `ag_get_status()` works in Hermes session

### ✅ Credential Pool
- [x] Unified store: `~/.hermes/auth.json` → `credential_pool`
- [x] Multiple sources per provider supported
- [x] Rotation strategies: fill_first, round_robin, least_used, random
- [x] Exhaustion handling with cooldowns
- [x] CLI: `hermes auth add/remove/list/status/reset`
- [x] Both providers use `manual:<source>` for independent accounts

### ✅ Profile Integration
- [x] DEFAULT profile: Full MCP list, all toolsets, openai-codex for image_gen
- [x] CLI-PRIME profile: Streamlined MCP, focused toolsets
- [x] All 8 profiles inherit global auth, can override providers/models
- [x] Model picker: `hermes model` shows both `gemini-oauth` and `openai-codex`

### ✅ Desktop UI
- [x] Providers tab: Both appear in Accounts tab
- [x] Model Config tab: Both in model picker
- [x] API endpoints: `/api/providers/oauth`, `/api/credentials/pool`

### ✅ npm Vulnerabilities Fixed
- [x] Root: `brace-expansion` 5.0.8 → ^5.0.9
- [x] All workspaces: 0 vulnerabilities

---

## Quick Reference Commands

### Authentication
```bash
# Codex
codex login --device-auth                    # Device code flow
codex login status                           # Verify
hermes auth add openai-codex --type oauth    # Import to Hermes

# Antigravity/Gemini
agy auth login                               # Google OAuth
# No direct status command (times out)
cat ~/.gemini/oauth_creds.json               # Verify tokens
hermes auth add gemini-oauth                 # Import to Hermes
```

### Verification
```bash
hermes doctor --fix                          # Full health check
hermes auth list                             # All credentials
hermes auth status gemini-oauth              # Specific provider
hermes auth status openai-codex              # Specific provider
hermes model                                 # Model picker (shows both)
```

### Orchestration - Direct CLI
```bash
# Codex
codex -p "Review this PR"
codex -p "Fix bug" --model "gpt-4o"

# Antigravity
agy -p "Review this PR"
agy -p "Fix bug" --model "Gemini 3.1 Pro (High)"
agy models                                   # List available models

# Background
terminal(command="agy -p 'Long task' --dangerously-skip-permissions", background=true, notify_on_complete=true)
```

### Orchestration - MCP Bridge (Antigravity)
```bash
# Delegate
ag_delegate_task(task="Refactor auth module", task_type="code", priority="high", context={"files": ["auth.py"]})

# Poll
ag_poll_response(task_id="task_123...", archive_on_read=true)

# Read response
ag_read_response(task_id="task_123...")

# Status
ag_get_status()

# History
ag_list_history(limit=10)
```

### Credential Management
```bash
# Add
hermes auth add openai-codex --type oauth --label "work"
hermes auth add gemini-oauth --label "personal"

# Remove
hermes auth remove gemini-oauth --target 1

# Reset exhaustion
hermes auth reset gemini-oauth

# List
hermes auth list
hermes auth list --provider gemini-oauth
```

### Profile Usage
```bash
hermes --profile cli-prime                   # Use CLI-PRIME profile
hermes --profile default                     # Use DEFAULT profile
hermes --profile coder                       # Use CODER profile
```

### Updates & Maintenance
```bash
# Codex
cd ~/.hermes/node && npm update @openai/codex
codex login --device-auth  # Re-auth if needed

# Antigravity
agy update
agy auth login  # Re-auth if needed

# MCP Bridge
cd ~/.hermes/mcp-servers/custom/antigravity-bridge && pip install -e .

# Token rotation
codex login --device-auth → hermes auth add openai-codex
agy auth login → hermes auth add gemini-oauth

# Backup
cp ~/.hermes/auth.json ~/.hermes/auth.json.backup
cp ~/.codex/auth.json ~/.codex/auth.json.backup
cp ~/.gemini/oauth_creds.json ~/.gemini/oauth_creds.json.backup
```

---

## Key Files Reference

| Category | File | Purpose |
|----------|------|---------|
| **Auth Stores** | `~/.hermes/auth.json` | Unified auth + credential pool |
| | `~/.codex/auth.json` | Codex CLI tokens |
| | `~/.gemini/oauth_creds.json` | Antigravity tokens |
| **Provider Config** | `hermes_cli/auth.py` | `PROVIDER_REGISTRY`, token reading, status |
| | `hermes_cli/models.py` | `CANONICAL_PROVIDERS` model picker |
| | `hermes_cli/web_server.py` | OAuth catalog, API endpoints |
| | `hermes_cli/auth_commands.py` | `hermes auth` commands |
| | `hermes_cli/doctor.py` | Health checks |
| | `hermes_cli/credential_pool.py` | Pool logic, rotation, exhaustion |
| **MCP Bridge** | `~/.hermes/mcp-servers/custom/antigravity-bridge/src/antigravity_bridge/server.py` | Bridge server with 9 tools |
| | `config.yaml` | MCP server registration |
| **Profiles** | `~/.hermes/profiles/default/config.yaml` | DEFAULT profile |
| | `~/.hermes/profiles/cli-prime/config.yaml` | CLI-PRIME profile |
| | `~/.hermes/profiles/*/config.yaml` | Other profiles |
| **Skill** | `~/.hermes/skills/orchestration/cli-prime-orchestrator/` | This skill (references/) |

---

## Troubleshooting Quick Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| `codex` not found | Not installed | `cd ~/.hermes/node && npm install @openai/codex` |
| `codex login status` fails | Not authenticated | `codex login --device-auth` |
| `agy` not found | Not on PATH | Check `/c/Users/apviz/AppData/Local/agy/bin/agy` |
| `agy auth status` times out | Known issue | Check `~/.gemini/oauth_creds.json` exists |
| Hermes shows "logged out" | Tokens not imported | `hermes auth add gemini-oauth` |
| Token expired | ~1 hour expiry | Run `agy auth login` then `hermes auth add gemini-oauth` |
| Bridge not responding | Antigravity not running | Start Antigravity to process inbox |
| Tasks stuck pending | Same | Antigravity must be running |
| Rate limited (429) | Quota exhausted | Wait for `reset_at` or re-auth |
| Provider not in `hermes model` | Not in `CANONICAL_PROVIDERS` | Add `ProviderEntry` to `models.py` |
| OAuth tab missing provider | Not in `_OAUTH_PROVIDER_CATALOG` | Add entry to `web_server.py` |

---

## Integration Architecture Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                     HERMES AGENT (Orchestrator)                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Codex CLI   │  │Antigravity   │  │  Antigravity │          │
│  │  (codex)     │  │  CLI (agy)   │  │  Bridge MCP  │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│  ┌──────▼─────────────────▼─────────────────▼───────┐           │
│  │         HERMES CREDENTIAL POOL (Unified)         │           │
│  │  - openai-codex: device_code, manual:device_code │           │
│  │  - gemini-oauth: antigravity_cli                 │           │
│  │  - openai-api, anthropic, xai-oauth, etc.        │           │
│  └─────────────────────────────────────────────────┘           │
│                            │                                    │
│  ┌─────────────────────────▼─────────────────────────┐         │
│  │        ANTIGRAVITY BRIDGE MCP (File-based IPC)    │         │
│  │  - ag_delegate_task, ag_poll_response, ...        │         │
│  │  - Two-way async communication                    │         │
│  └────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

*Last verified: 2026-08-05*
*Skill: `cli-prime-orchestrator` (permanent, all profiles)*