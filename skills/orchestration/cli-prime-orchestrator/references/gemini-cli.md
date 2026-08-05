---
title: Gemini CLI = Antigravity CLI Integration Spec
version: 1.0.0
---

# Gemini CLI (Google) = Antigravity CLI - Full Integration Specification

## Critical Architecture Note
**There is NO separate `gemini` binary.** The Google Gemini CLI **IS** the Antigravity CLI (`agy`). They are the same binary with different branding.

## Binary Details
- **Command**: `agy` (aliased as `gemini` in some contexts)
- **Install location**: `/c/Users/apviz/AppData/Local/agy/bin/agy`
- **Version**: 1.1.1+
- **On PATH**: Yes (via `~/.hermes/node` or system PATH)

## Authentication (Google OAuth)
```bash
# Authenticate
agy auth login
# Opens browser to Google sign-in
# Uses OS keyring + ~/.gemini/oauth_creds.json

# Tokens stored:
# ~/.gemini/oauth_creds.json (primary)
# ~/.gemini/antigravity-cli/oauth_creds.json (secondary, if exists)
```

## Token Format (Google OAuth)
```json
{
  "access_token": "[REDACTED_YA29]",
  "scope": "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid https://www.googleapis.com/auth/cloud-platform",
  "token_type": "Bearer",
  "id_token": "eyJhbG...",
  "expiry_date": 1785362656119,  // milliseconds since epoch
  "refresh_token": "[REDACTED_GOOGLE_TOKEN]"
}
```

## Key Difference from Codex
| Aspect | Codex CLI | Antigravity/Gemini CLI |
|--------|-----------|------------------------|
| **Auth flow** | Device code (OpenAI) | Google OAuth (browser) |
| **Token storage** | `~/.codex/auth.json` | `~/.gemini/oauth_creds.json` |
| **Token type** | OpenAI JWT | Google OAuth JWT |
| **Expiry** | Longer (~30 days?) | ~1 hour (3600s) |
| **Refresh** | Codex CLI handles | Must run `agy auth login` |
| **Hermes provider** | `openai-codex` | `gemini-oauth` (NEW) |
| **Auth type** | `oauth_external` | `oauth_external` |

## Hermes Integration (Same as Antigravity CLI)

Since they ARE the same CLI, all Hermes integration points are identical to the Antigravity CLI spec. See `references/antigravity-cli.md` for complete details.

### Provider Registry (`hermes_cli/auth.py`)
```python
"gemini-oauth": ProviderConfig(
    id="gemini-oauth",
    name="Google Gemini OAuth (via Antigravity CLI)",
    auth_type="oauth_external",
    inference_base_url="https://generativelanguage.googleapis.com/v1beta",
),
```

### Model Entry (`hermes_cli/models.py`)
```python
ProviderEntry("gemini-oauth", "Google Gemini OAuth", 
              "Google Gemini OAuth (via Antigravity CLI / Google account)"),
```

### Credential Pool Source
- **Source**: `manual:antigravity_cli`
- **Independent accounts**: Yes
- **Refresh**: Via `agy auth login` only (Hermes cannot refresh - needs Google OAuth client_id/secret)

## CLI Usage (Identical to Antigravity)
```bash
# Version
agy --version

# One-shot
agy -p "Summarize the repo in 3 bullets"

# With model
agy -p "Review this diff" --model "Gemini 3.1 Pro (High)"

# List models
agy models

# Background
terminal(command="agy -p 'Long task' --dangerously-skip-permissions", background=true, notify_on_complete=true)

# Interactive
agy  # then: /config, /permissions, /model, /skills, /mcp, /agents

# Plugins
agy plugin list
agy plugin install <target>
```

## MCP Bridge (Identical to Antigravity)
The Antigravity Bridge MCP works with `agy` since it IS the Antigravity CLI.

```python
# Delegate
ag_delegate_task(task="...", task_type="code")

# Poll
ag_poll_response(task_id="...")

# Status
ag_get_status()
```

## File Paths (Same as Antigravity)
| Path | Purpose |
|------|---------|
| `~/.gemini/oauth_creds.json` | Primary OAuth tokens |
| `~/.gemini/antigravity-cli/oauth_creds.json` | Secondary location |
| `~/.gemini/antigravity-cli/settings.json` | Settings |
| `~/.gemini/antigravity-cli/keybindings.json` | Keybindings |
| `~/.gemini/antigravity-cli/log/cli-*.log` | Logs |
| `~/.gemini/antigravity-cli/conversations/` | History |
| `~/.gemini/antigravity-cli/plugins/` | Plugins |

## Verification (Same as Antigravity)
```bash
# Check binary
which agy
agy --version

# Check tokens
cat ~/.gemini/oauth_creds.json

# Check Hermes
hermes auth list | grep gemini-oauth
hermes doctor --fix | grep "Gemini OAuth"
```

## Lessons Learned (Gemini-Specific)
1. **Single binary**: `agy` = `gemini` CLI - don't search for separate `gemini` command
2. **Google OAuth**: Uses standard Google OAuth flow (not device code)
3. **Short token life**: ~1 hour access tokens; refresh requires `agy auth login`
4. **No client_id/secret in Hermes**: Can't auto-refresh; user must re-auth via CLI
5. **Same integration as Antigravity**: All Hermes code paths are shared
6. **Model names**: Use `agy models` to see exact display strings (e.g., "Gemini 3.1 Pro (High)")

## Troubleshooting (Gemini-Specific)
| Problem | Solution |
|---------|----------|
| Looking for `gemini` command | Use `agy` instead |
| Token expires quickly | Normal - ~1 hour; run `agy auth login` |
| Can't refresh in Hermes | By design - must use `agy auth login` |
| Model name not recognized | Run `agy models` for exact strings |
| Auth status times out | Known issue - check `~/.gemini/oauth_creds.json` directly |

---

*This is a companion reference to `references/antigravity-cli.md` - they describe the same integration since Gemini CLI = Antigravity CLI.*