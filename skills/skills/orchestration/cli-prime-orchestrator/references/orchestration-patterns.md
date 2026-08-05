---
title: Orchestration Patterns & Credential Management
version: 1.0.0
---

# Orchestration Patterns & Credential Management

## Unified Credential Pool Architecture

### Pool Structure (`~/.hermes/auth.json`)
```json
{
  "credential_pool": {
    "openai-codex": [
      {
        "id": "abc123",
        "label": "codex-oauth",
        "auth_type": "oauth",
        "priority": 0,
        "source": "manual:device_code",
        "access_token": "eyJhbG...",
        "refresh_token": "rt.1...",
        "base_url": "https://chatgpt.com/backend-api/codex",
        "last_refresh": "2026-08-05T03:26:09.873331400Z"
      }
    ],
    "gemini-oauth": [
      {
        "id": "def456",
        "label": "antigravity",
        "auth_type": "oauth",
        "priority": 0,
        "source": "manual:antigravity_cli",
        "access_token": "ya29.a0ARG...",
        "base_url": "https://generativelanguage.googleapis.com/v1beta"
      }
    ],
    "openai-api": [...],
    "anthropic": [...]
  }
}
```

### Source Types
| Source | Description | Refresh Behavior |
|--------|-------------|------------------|
| `device_code` | Singleton from Hermes device-code flow | Auto-synced via `_save_codex_tokens()` |
| `manual:device_code` | Independent accounts from `hermes auth add` | Independent; refresh from own token pair |
| `manual:antigravity_cli` | Independent accounts from Antigravity CLI | Independent; refresh via `agy auth login` |
| `manual:qwen_cli` | Independent accounts from Qwen CLI | Independent; refresh via Qwen CLI |
| `env:VAR_NAME` | From environment variable | Manual update |
| `hermes_pkce` | Hermes-managed PKCE (Anthropic) | Auto-refresh by Hermes |

## Rotation Strategies
Configured per-provider in `config.yaml` or via `hermes auth`:
- **fill_first**: Use first credential until exhausted (default)
- **round_robin**: Rotate through all credentials
- **least_used**: Prefer least used credential
- **random**: Random selection

```yaml
# In config.yaml
credential_pool:
  strategy: least_used
```

## Exhaustion Handling & Cooldowns

### HTTP Status → Cooldown Mapping
| Status | Cooldown | Notes |
|--------|----------|-------|
| 401 Unauthorized | 5 min | 1 min if sole credential |
| 403 Forbidden | 1 hour | 1 min if sole credential (unless billing) |
| 429 Rate Limited | 1 hour | Provider-supplied `reset_at` overrides |
| 402 Payment Required | 1 hour | Billing exhaustion - full bench |
| 5xx Server Error | 1 hour | Transient - provider-supplied `reset_at` overrides |

### Special Handling
- **Sole credential**: Transient errors (429, 403 edge-throttle, 5xx) → 1 min cooldown
- **Billing exhaustion** (classified as `billing` or 402) → Always full bench
- **DEAD credentials**: `token_invalidated`, `token_revoked`, `invalid_token`, `invalid_grant`, `unauthorized_client`, `refresh_token_reused` → Excluded until re-auth
- **Provider-supplied `reset_at`**: Always overrides default cooldown

## Credential Pool API

### CLI Commands
```bash
# List all credentials across all providers
hermes auth list

# List specific provider
hermes auth list --provider gemini-oauth

# Add credential (OAuth)
hermes auth add openai-codex --type oauth --label "work-account"
hermes auth add gemini-oauth --label "personal"

# Add credential (API key)
hermes auth add openai-api --type api-key --api-key "sk-..." --label "prod-key"

# Remove credential
hermes auth remove gemini-oauth --target 1
hermes auth remove openai-codex --target "codex-oauth"

# Status check
hermes auth status gemini-oauth
hermes auth status openai-codex

# Reset exhaustion
hermes auth reset gemini-oauth
```

### Python API (for skills/scripts)
```python
from agent.credential_pool import load_pool, PooledCredential, AUTH_TYPE_OAUTH, SOURCE_MANUAL
import uuid

# Load pool for provider
pool = load_pool("gemini-oauth")

# Get all entries
entries = pool.entries()

# Select best credential (uses rotation strategy)
entry = pool.select()

# Add new entry
new_entry = PooledCredential(
    provider="gemini-oauth",
    id=uuid.uuid4().hex[:6],
    label="new-account",
    auth_type=AUTH_TYPE_OAUTH,
    priority=0,
    source=f"{SOURCE_MANUAL}:antigravity_cli",
    access_token="ya29.a0ARG...",
    base_url="https://generativelanguage.googleapis.com/v1beta",
)
pool.add_entry(new_entry)

# Remove by index (1-based)
removed = pool.remove_index(1)

# Check exhaustion
if entry.last_status == "exhausted":
    # Handle cooldown
    pass
```

## Profile Configuration

### Per-Profile Provider Selection
Each profile (`~/.hermes/profiles/<name>/config.yaml`) can configure:
```yaml
model:
  provider: openrouter        # or gemini-oauth, openai-codex, etc.
  default: google/gemini-3.6-flash

fallback_providers:
  - provider: gemini-oauth
    model: gemini-3.6-flash
  - provider: openai-codex
    model: gpt-4o
  - provider: openrouter
    model: google/gemini-3.6-flash
```

### Profile-Specific MCP Servers
```yaml
mcp_servers:
  antigravity-bridge:
    args:
      - -m
      - antigravity_bridge.server
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\antigravity-bridge\src
    timeout: 60
  # ... other servers
```

## Desktop UI Integration

### Providers Tab (Settings → Providers → Accounts)
Auto-populated from:
1. `_OAUTH_PROVIDER_CATALOG` (hand-tuned cards)
2. `provider_catalog()` (auto-extends from `CANONICAL_PROVIDERS`)

Shows for each provider:
- Name, flow type (device_code, external, pkce)
- Status: logged_in / logged_out
- Token preview (last N chars)
- Expires at
- Has refresh token
- Disconnect command (for external providers: shows CLI command)

### Model Configuration Tab (Settings → Models)
Auto-populated from `CANONICAL_PROVIDERS`:
- Filter by provider slug
- Configure default model per provider
- Set model parameters (temperature, max_tokens, etc.)

### API Endpoints
```bash
# List OAuth providers with status
GET /api/providers/oauth?profile=default

# Add credential to pool
POST /api/credentials/pool
{ "provider": "gemini-oauth", "api_key": "ya29...", "label": "personal" }

# Remove credential
DELETE /api/credentials/pool/gemini-oauth/1

# Validate provider config
POST /api/providers/validate
{ "provider": "gemini-oauth", "base_url": "https://..." }
```

## Orchestration Patterns

### Pattern 1: Direct CLI Delegation (Terminal Tool)
```python
# One-shot with Codex
result = terminal(command="codex -p 'Review this PR for security issues'")

# One-shot with Antigravity
result = terminal(command="agy -p 'Review this PR' --model 'Gemini 3.1 Pro (High)'")

# Background long-running
session = terminal(
    command="agy -p 'Implement feature from TASK.md' --dangerously-skip-permissions",
    background=True,
    notify_on_complete=True
)
# Later: process(action="poll", session_id=session.session_id)
```

### Pattern 2: MCP Bridge Async Delegation (Antigravity)
```python
# 1. Delegate task
task = ag_delegate_task(
    task="Refactor auth module to use new credential pool",
    task_type="code",  # code, analysis, search, file_ops, system, research, general
    priority="high",   # low, normal, high, urgent
    context={
        "file_paths": ["hermes_cli/auth.py", "hermes_cli/auth_commands.py"],
        "project": "hermes-agent",
        "requirements": "Maintain backward compatibility"
    }
)
task_id = task["task_id"]

# 2. Poll for completion (with timeout)
for _ in range(30):  # 5 min with 10s intervals
    response = ag_poll_response(task_id=task_id, archive_on_read=True)
    if response["status"] == "COMPLETED":
        break
    elif response["status"] == "ARCHIVED":
        break
    await asyncio.sleep(10)

# 3. Read result
result = ag_read_response(task_id=task_id)
```

### Pattern 3: Multi-Provider Cross-Check
```python
# Get second opinion from different CLI family
codex_result = terminal(command="codex -p 'Review for security vulnerabilities'")
gemini_result = terminal(command="agy -p 'Review for security vulnerabilities' --model 'Gemini 3.1 Pro (High)'")

# Compare results programmatically
# Both return plain text - parse for findings
```

### Pattern 4: Worktree Fan-Out (Parallel)
```bash
# Create worktrees
git worktree add ../wt-auth feature/auth-refactor
git worktree add ../wt-api feature/api-refactor

# Launch parallel background tasks
# Terminal 1
terminal(command="cd ../wt-auth && agy -p 'Implement auth refactor per SPEC.md' --dangerously-skip-permissions", background=true, notify_on_complete=true)

# Terminal 2  
terminal(command="cd ../wt-api && codex -p 'Implement API refactor per SPEC.md' --dangerously-bypass-approvals-and-sandbox", background=true, notify_on_complete=true)

# Collect results via process(action="poll"/"wait", session_id=...)
```

### Pattern 5: Fallback Chain
```yaml
# In config.yaml
fallback_providers:
  - provider: gemini-oauth
    model: gemini-3.6-flash
  - provider: openai-codex
    model: gpt-4o
  - provider: openrouter
    model: google/gemini-3.6-flash
  - provider: nous
    model: tencent/hy3:free
```

## Verification Checklist

### Pre-Flight (Run Before Orchestration)
```bash
# 1. Verify all CLIs installed
command -v codex && codex --version
command -v agy && agy --version

# 2. Verify auth status
codex login status
# agy auth status  # may timeout
cat ~/.gemini/oauth_creds.json  # verify file exists
hermes auth list

# 3. Verify doctor
hermes doctor --fix

# 4. Verify MCP bridge
# In Hermes session: ag_get_status()

# 5. Verify model picker
hermes model  # should show gemini-oauth, openai-codex
```

### Integration Tests
```bash
# Test Codex direct
codex -p "echo hello"

# Test Antigravity direct
agy -p "echo hello"

# Test bridge delegation
ag_delegate_task(task="test", task_type="general")
ag_poll_response(task_id=...)

# Test credential pool
hermes auth add gemini-oauth --label "test"
hermes auth list
hermes auth remove gemini-oauth --target last
```

## Maintenance

### Updates
```bash
# Update Codex CLI
cd ~/.hermes/node && npm update @openai/codex

# Update Antigravity CLI
agy update

# Update MCP bridge
cd ~/.hermes/mcp-servers/custom/antigravity-bridge && pip install -e .
```

### Token Rotation
- **Codex**: `codex login --device-auth` → re-run `hermes auth add openai-codex`
- **Antigravity**: `agy auth login` → `hermes auth add gemini-oauth` (auto-reads fresh tokens)

### Backup
```bash
# Backup auth stores
cp ~/.hermes/auth.json ~/.hermes/auth.json.backup
cp ~/.codex/auth.json ~/.codex/auth.json.backup
cp ~/.gemini/oauth_creds.json ~/.gemini/oauth_creds.json.backup
```

## Key Files Summary

| File | Purpose |
|------|---------|
| `~/.hermes/auth.json` | Unified auth store + credential pool |
| `~/.codex/auth.json` | Codex CLI tokens |
| `~/.gemini/oauth_creds.json` | Antigravity CLI tokens |
| `hermes_cli/auth.py` | Provider registry, token reading, status functions |
| `hermes_cli/models.py` | `CANONICAL_PROVIDERS` model picker |
| `hermes_cli/web_server.py` | OAuth catalog, API endpoints |
| `hermes_cli/auth_commands.py` | `hermes auth add/remove/list` |
| `hermes_cli/doctor.py` | Health checks |
| `hermes_cli/credential_pool.py` | Pool logic, rotation, exhaustion |
| `config.yaml` | Profile/provider/model config |
| `~/.hermes/profiles/*/config.yaml` | Per-profile overrides |