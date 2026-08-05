---
title: Antigravity/Gemini CLI Integration Spec
version: 1.0.0
---

# Antigravity CLI (Google Gemini) - Full Integration Specification

## Overview
- **Binary**: `agy` (Antigravity CLI = Google Gemini CLI)
- **Version**: 1.1.1+
- **Auth**: Google OAuth via browser (OS keyring + browser sign-in)
- **Hermes Provider**: `gemini-oauth` (NEW - added for this integration)
- **Auth Type**: `oauth_external` (Hermes reads tokens from Antigravity CLI)
- **Note**: There is NO separate `gemini` binary - `agy` IS the Gemini CLI

## Installation
```bash
# Already installed at:
/c/Users/apviz/AppData/Local/agy/bin/agy
# Verify:
agy --version  # 1.1.1
# On PATH via ~/.hermes/node or system PATH
```

## Authentication Flow
```bash
# Antigravity uses Google OAuth via browser
agy auth login
# Opens browser to Google sign-in
# Tokens stored in OS keyring + ~/.gemini/oauth_creds.json
```

## Token Storage
- **Antigravity CLI**: `~/.gemini/oauth_creds.json` (primary)
  ```json
  {
    "access_token": "[REDACTED_YA29]",
    "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid https://www.googleapis.com/auth/cloud-platform",
    "token_type": "Bearer",
    "id_token": "eyJhbG...",
    "expiry_date": 1785362656119,  # milliseconds since epoch
    "refresh_token": "[REDACTED_GOOGLE_TOKEN]"
  }
  ```

- **Alternative location**: `~/.gemini/antigravity-cli/oauth_creds.json` (if exists)

- **Hermes Auth Store**: `~/.hermes/auth.json` (provider: `gemini-oauth`)
- **Credential Pool**: `manual:antigravity_cli` source entries

## Hermes Integration Points

### Provider Registry (`hermes_cli/auth.py`)
```python
"gemini-oauth": ProviderConfig(
    id="gemini-oauth",
    name="Google Gemini OAuth (via Antigravity CLI)",
    auth_type="oauth_external",
    inference_base_url="https://generativelanguage.googleapis.com/v1beta",
),
```

### Token Reading Functions (`hermes_cli/auth.py`)
```python
def _antigravity_cli_auth_path() -> Path:
    return Path.home() / ".gemini" / "oauth_creds.json"

def _read_antigravity_cli_tokens() -> Dict[str, Any]:
    auth_path = _antigravity_cli_auth_path()
    if not auth_path.exists():
        raise AuthError("Antigravity CLI credentials not found. Run 'gemini auth login' first.", provider="gemini-oauth", code="gemini_oauth_auth_missing")
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    # Returns dict with access_token, refresh_token, expiry_date
    return data

def _antigravity_access_token_is_expiring(access_token: str, skew_seconds: int = 120) -> bool:
    # Decodes JWT, checks exp claim
    ...

def get_gemini_oauth_auth_status() -> Dict[str, Any]:
    # Returns: logged_in, auth_store_path, source, api_key, access_token, refresh_token, expires_at, expires_at_ms, has_refresh_token
    # Warns if token expiring (refresh must be done via Antigravity CLI)

def resolve_gemini_oauth_runtime_credentials(
    *, force_refresh: bool = False, refresh_if_expiring: bool = True, refresh_skew_seconds: int = 120
) -> Dict[str, Any]:
    # Returns: provider, base_url, api_key, source, expires_at_ms
    # Logs warning if token expiring (refresh must be done via `agy auth login`)
```

### Model Entry (`hermes_cli/models.py`)
```python
ProviderEntry("gemini-oauth", "Google Gemini OAuth", 
              "Google Gemini OAuth (via Antigravity CLI / Google account)"),
```

### OAuth Catalog (`hermes_cli/web_server.py`)
```python
{
    "id": "gemini-oauth",
    "name": "Google Gemini OAuth (via Antigravity CLI)",
    "flow": "external",
    "cli_command": "hermes auth add gemini-oauth",
    "docs_url": "https://github.com/google-gemini/gemini-cli",
    "status_fn": None,  # dispatched via get_gemini_oauth_auth_status
},

# In _resolve_provider_status():
if provider_id == "gemini-oauth":
    raw = hauth.get_gemini_oauth_auth_status()
    return {
        "logged_in": bool(raw.get("logged_in")),
        "source": "antigravity_cli",
        "source_label": raw.get("auth_store_path") or "Antigravity CLI",
        "token_preview": _truncate_token(raw.get("access_token")),
        "expires_at": raw.get("expires_at"),
        "has_refresh_token": bool(raw.get("has_refresh_token")),
    }
```

### Auth Commands (`hermes_cli/auth_commands.py` lines 410-428)
```python
if provider == "gemini-oauth":
    creds = auth_mod.resolve_gemini_oauth_runtime_credentials(refresh_if_expiring=False)
    label = label or label_from_token(creds["api_key"], _oauth_default_label(...))
    entry = PooledCredential(
        provider=provider,
        id=uuid.uuid4().hex[:6],
        label=label,
        auth_type=AUTH_TYPE_OAUTH,
        priority=0,
        source=f"{SOURCE_MANUAL}:antigravity_cli",
        access_token=creds["api_key"],
        base_url=creds.get("base_url"),
    )
    pool.add_entry(entry)
```

### Doctor Check (`hermes_cli/doctor.py`)
```python
from hermes_cli.auth import get_gemini_oauth_auth_status
gemini_oauth_status = get_gemini_oauth_auth_status()
if gemini_oauth_status.get("logged_in"):
    check_ok("Google Gemini OAuth", "(logged in via Antigravity CLI)")
else:
    check_warn("Google Gemini OAuth", "(not logged in)")
    if gemini_oauth_status.get("error"):
        check_info(gemini_oauth_status["error"])
```

## Credential Pool Behavior
- **Source**: `manual:antigravity_cli` (independent accounts)
- **Rotation**: Multiple accounts supported
- **Refresh**: **Hermes CANNOT refresh** - requires `agy auth login` (needs Google OAuth client_id/secret)
- **Token expiry**: ~1 hour (3600 seconds); `expiry_date` in milliseconds
- **Warning**: Hermes logs warning if token expiring; user must run `agy auth login`

## CLI Usage Patterns
```bash
# Version check
agy --version

# One-shot prompt (non-interactive)
agy -p "Summarize the repo in 3 bullets"

# With model selection
agy -p "Review this diff" --model "Gemini 3.1 Pro (High)"

# Available models
agy models

# Background long-running
terminal(command="agy -p 'Implement TASK.md' --dangerously-skip-permissions", background=true, notify_on_complete=true)

# Interactive PTY session
# Use pty=true with tmux for capture/monitoring

# Plugin management
agy plugin list
agy plugin install <target>
agy plugin import <source>

# In-session slash commands
agy  # then: /config, /permissions, /model, /keybindings, /skills, /mcp, /agents
```

## Key Files & Paths
| File | Purpose |
|------|---------|
| `~/.gemini/oauth_creds.json` | Primary OAuth tokens |
| `~/.gemini/antigravity-cli/oauth_creds.json` | Secondary token location |
| `~/.gemini/antigravity-cli/settings.json` | Settings (colorScheme, trustedWorkspaces) |
| `~/.gemini/antigravity-cli/keybindings.json` | Keybindings |
| `~/.gemini/antigravity-cli/log/cli-*.log` | Logs |
| `~/.gemini/antigravity-cli/conversations/` | Conversation history |
| `~/.gemini/antigravity-cli/plugins/` | Plugin staging |
| `~/.hermes/auth.json` | Hermes auth store + credential pool |
| `hermes_cli/auth.py` | Provider config, token reading, status |
| `hermes_cli/models.py` | Model picker entry |
| `hermes_cli/web_server.py` | OAuth catalog, API endpoints |
| `hermes_cli/auth_commands.py` | `hermes auth add` command handler |
| `hermes_cli/doctor.py` | Health check |

## Antigravity Bridge MCP (Two-Way Communication)

### Configuration (`config.yaml`)
```yaml
mcp_servers:
  antigravity-bridge:
    args:
      - -m
      - antigravity_bridge.server
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\antigravity-bridge\src
    timeout: 60
```

### Location
`~/.hermes/mcp-servers/custom/antigravity-bridge/src/antigravity_bridge/server.py`

### Tools Exposed to Hermes
| Tool | Purpose |
|------|---------|
| `ag_delegate_task` | Post task to Antigravity inbox |
| `ag_poll_response` | Check for completion |
| `ag_list_pending` | List pending tasks |
| `ag_read_response` | Read completed response |
| `ag_cancel_task` | Cancel pending task |
| `ag_send_message` | Send freeform message |
| `ag_get_status` | Bridge status & queue stats |
| `ag_list_history` | Task history |
| `ag_clear_history` | Clear history |

### File-based IPC Structure
```
~HERMES_HOME/pairing/antigravity/
├── inbox/     # Tasks for Antigravity (JSON)
├── outbox/    # Responses from Antigravity (JSON)
├── history/   # Archived tasks
└── status.json
```

### Task Delegation Flow
```python
# 1. Delegate task
task = ag_delegate_task(
    task="Review this PR for security issues",
    task_type="code",  # code, analysis, search, file_ops, system, research, general
    priority="normal",  # low, normal, high, urgent
    context={"file_paths": ["src/auth.py"], "project": "hermes-agent"}
)
# Returns task_id

# 2. Poll for response
response = ag_poll_response(task_id=task.task_id, archive_on_read=True)
# Returns: status (PENDING/COMPLETED/ARCHIVED/NOT_FOUND), response data

# 3. Read completed response
response = ag_read_response(task_id=task.task_id)
```

## Lessons Learned
1. **Antigravity = Gemini CLI**: Don't look for separate `gemini` binary
2. **Token format**: Google OAuth tokens (JWT access_token + refresh_token)
3. **Token expiry**: Tokens expire ~1 hour; refresh must be done via `agy auth login` (Hermes can't refresh - needs client_id/secret)
4. **External auth type**: `oauth_external` means Hermes reads tokens but doesn't manage the OAuth flow
5. **Credential pool source**: `manual:antigravity_cli` for independent multi-account support
6. **Two integration modes**: Direct CLI (terminal) + MCP Bridge (async)
7. **MCP Bridge** enables true orchestration: delegate → poll → read response
8. **File-based IPC** is simple, reliable, works across processes
9. **Antigravity watches inbox** - must be running to process tasks
10. **No `--output-format json`** on `agy -p` - parse stdout as plain text
11. **No `--max-turns`** - use `--print-timeout` (default 5m) for bounding
12. **Worktree fan-out** pattern works same as Codex for parallel tasks

## Troubleshooting
| Problem | Solution |
|---------|----------|
| `agy` not found | Check `/c/Users/apviz/AppData/Local/agy/bin/agy` on PATH |
| Auth expired | Run `agy auth login` in terminal (browser opens) |
| Hermes shows logged out | `hermes auth add gemini-oauth` (reads fresh tokens) |
| Token refresh needed | Must run `agy auth login` - Hermes can't refresh (no client_id/secret) |
| Bridge not responding | Check `ag_get_status()` - verify inbox/outbox paths |
| Tasks stuck pending | Antigravity must be running to process inbox |
| MCP not loaded | Verify `antigravity-bridge` in `config.yaml` mcp_servers |