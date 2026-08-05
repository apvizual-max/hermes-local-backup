---
title: Codex CLI Integration Spec
version: 1.0.0
---

# Codex CLI (OpenAI) - Full Integration Specification

## Overview
- **Binary**: `codex` (installed via npm `@openai/codex`)
- **Version**: 0.146.0+
- **Auth**: Device-code OAuth via ChatGPT subscription
- **Hermes Provider**: `openai-codex`
- **Auth Type**: `oauth_external` (Hermes reads tokens, doesn't drive flow)

## Installation
```bash
cd ~/.hermes/node
npm install @openai/codex
# Binary at: ~/.hermes/node/codex
```

## Authentication Flow
```bash
# 1. Device code auth
codex login --device-auth
# Output: URL + one-time code (e.g., A13Y-KZ0GO)

# 2. Browser: https://auth.openai.com/codex/device
# 3. Enter code, authorize

# 3. Verify
codex login status  # "Logged in using ChatGPT"
```

## Token Storage
- **Codex CLI**: `~/.codex/auth.json`
  ```json
  {
    "auth_mode": "chatgpt",
    "tokens": {
      "id_token": "eyJhbG...",
      "access_token": "eyJhbG...",
      "refresh_token": "rt.1...",
      "account_id": "dc04d23b-..."
    },
    "last_refresh": "2026-08-05T03:26:09.873331400Z"
  }
  ```

- **Hermes Auth Store**: `~/.hermes/auth.json` (provider: `openai-codex`)
- **Credential Pool**: `manual:device_code` source entries

## Hermes Integration Points

### Provider Registry (`hermes_cli/auth.py`)
```python
"openai-codex": ProviderConfig(
    id="openai-codex",
    name="OpenAI Codex",
    auth_type="oauth_external",
    inference_base_url=DEFAULT_CODEX_BASE_URL,  # "https://chatgpt.com/backend-api/codex"
),
CODEX_OAUTH_CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
CODEX_OAUTH_TOKEN_URL = "https://auth.openai.com/oauth/token"
```

### Model Entry (`hermes_cli/models.py`)
```python
ProviderEntry("openai-codex", "OpenAI Codex", 
              "OpenAI Codex (Codex CLI via ChatGPT subscription or API key)"),
```

### OAuth Catalog (`hermes_cli/web_server.py`)
```python
{
    "id": "openai-codex",
    "name": "OpenAI OAuth (ChatGPT)",
    "flow": "device_code",
    "cli_command": "hermes auth add openai-codex",
    "docs_url": "https://platform.openai.com/docs",
    "status_fn": None,  # dispatched via get_codex_auth_status
},
```

### Auth Commands (`hermes_cli/auth_commands.py` lines 310-346)
```python
if provider == "openai-codex":
    creds = auth_mod._codex_device_code_login()
    label = label or label_from_token(creds["tokens"]["access_token"], _oauth_default_label(...))
    entry = PooledCredential(
        provider=provider,
        id=uuid.uuid4().hex[:6],
        label=label,
        auth_type=AUTH_TYPE_OAUTH,
        priority=0,
        source=SOURCE_MANUAL_DEVICE_CODE,  # "manual:device_code"
        access_token=creds["tokens"]["access_token"],
        refresh_token=creds["tokens"].get("refresh_token"),
        base_url=creds.get("base_url"),
        last_refresh=creds.get("last_refresh"),
    )
    pool.add_entry(entry)
```

### Status Function (`hermes_cli/auth.py` `get_codex_auth_status()`)
- Checks credential pool first (`load_pool("openai-codex")`)
- Falls back to legacy provider state (`resolve_codex_runtime_credentials()`)
- Returns: `logged_in`, `auth_store`, `last_refresh`, `auth_mode`, `source`, `api_key`, `rate_limited`, `reset_at`

### Doctor Check (`hermes_cli/doctor.py`)
```python
codex_status = get_codex_auth_status()
if codex_status.get("logged_in"):
    check_ok("OpenAI Codex auth", "(logged in)")
else:
    check_warn("OpenAI Codex auth", "(not logged in)")
    if not _safe_which("codex"):
        check_info("codex CLI not installed (optional)")
```

## Credential Pool Behavior
- **Source types**: `device_code` (singleton from Hermes device-code flow), `manual:device_code` (independent accounts from `hermes auth add`)
- **Rotation**: Multiple accounts supported with independent token pairs
- **Refresh**: Handled by Codex CLI; Hermes re-reads on next `load_pool()`
- **Exhaustion**: 401/403 → 5 min cooldown (1 min if sole credential)

## CLI Usage Patterns
```bash
# One-shot
codex -p "Review this PR"

# With model
codex -p "Fix bug" --model "gpt-4o"

# Interactive
codex  # or codex -i

# Resume session
codex resume --last

# Background long-running
codex -p "Implement feature" --dangerously-bypass-approvals-and-sandbox &
```

## Key Files & Paths
| File | Purpose |
|------|---------|
| `~/.codex/auth.json` | Codex CLI OAuth tokens |
| `~/.hermes/auth.json` | Hermes auth store + credential pool |
| `hermes_cli/auth.py` | Provider config, token reading, status |
| `hermes_cli/models.py` | Model picker entry |
| `hermes_cli/web_server.py` | OAuth catalog, API endpoints |
| `hermes_cli/auth_commands.py` | `hermes auth add` command handler |
| `hermes_cli/doctor.py` | Health check |

## Lessons Learned
1. **Device code flow** works best for headless/remote environments
2. **Credential pool** enables true multi-account with rotation/failover
3. **Singleton vs manual entries**: `manual:device_code` are independent; singleton sync (`_save_codex_tokens`) only updates `device_code` source entries
4. **Token refresh**: Codex CLI handles refresh; Hermes reads refreshed tokens on next `load_pool()`
5. **External auth type**: `oauth_external` = Hermes reads tokens, doesn't drive OAuth flow

## Troubleshooting
| Problem | Solution |
|---------|----------|
| `codex` not found | `cd ~/.hermes/node && npm install @openai/codex` |
| Auth failed | `codex login --device-auth` + browser |
| Tokens not in Hermes | `hermes auth add openai-codex --type oauth` |
| Rate limited | Wait for `reset_at` or re-auth |