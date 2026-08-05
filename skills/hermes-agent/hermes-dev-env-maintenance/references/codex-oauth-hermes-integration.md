# Codex OAuth Integration with Hermes

**Session Date:** 2026-08-05

## Summary

This reference documents the complete Codex OAuth setup flow for Hermes, from Codex CLI installation to Hermes credential registration.

## Key Commands Used

```cmd
# 1. Install Codex CLI in Hermes isolated Node env
cd C:\Users\apviz\AppData\Local\hermes\node
npm install @openai/codex

# 2. Device authorization via Codex CLI
codex login --device-auth
# → Opens https://auth.openai.com/codex/device with code (e.g., A13Y-KZ0GO)

# 3. Verify Codex CLI auth
codex login status
# → "Logged in using ChatGPT"

# 4. Register with Hermes (auto-imports from ~/.codex/auth.json)
hermes auth
# → 1. Add credential
# → openai-codex
# → 2. OAuth login
# → Label: "codex-oauth"

# 5. Verify Hermes auth
hermes auth status openai-codex
# → "openai-codex: logged in"

hermes doctor --fix
# → Shows "✓ OpenAI Codex auth (logged in)"
```

## Files Involved

| File | Purpose |
|------|---------|
| `~/.codex/auth.json` | Codex CLI OAuth tokens (access_token, refresh_token, id_token) |
| `~/.hermes/auth.json` | Hermes credential pool (includes openai-codex provider) |
| `C:\Users\apviz\AppData\Local\hermes\node\package.json` | Hermes node env dependencies |

## Internal Hermes Functions

- `_import_codex_cli_tokens()` — reads tokens from `~/.codex/auth.json`
- `_recover_codex_tokens_from_cli(reason)` — imports valid CLI tokens into Hermes auth
- `_save_codex_tokens(tokens, last_refresh, label)` — writes to Hermes auth store
- `_sync_codex_pool_entries()` — syncs singleton tokens to credential pool

## Troubleshooting Notes

| Issue | Resolution |
|-------|------------|
| `codex` not found | Install in Hermes node env: `cd C:\Users\apviz\AppData\Local\hermes\node && npm install @openai/codex` |
| `stdin is not a terminal` | Run `codex login --device-auth` from interactive terminal, not piped |
| Device code expired (>15 min) | Re-run `codex login --device-auth` for fresh code |
| `hermes auth` hangs on OAuth | Use `--no-browser` flag or run from interactive shell |
| Codex CLI authed but Hermes not | Run `_recover_codex_tokens_from_cli("manual")` via Python |

## Verification Checklist

- [ ] `codex --version` works
- [ ] `codex login status` → "Logged in"
- [ ] `hermes auth status openai-codex` → "logged in"
- [ ] `hermes auth list` shows openai-codex credential
- [ ] `hermes doctor --fix` shows ✓ OpenAI Codex auth