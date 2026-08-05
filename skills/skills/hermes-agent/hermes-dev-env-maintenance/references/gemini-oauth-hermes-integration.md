# Gemini OAuth Integration with Hermes (via Antigravity CLI)

**Session Date:** 2026-08-05

## Summary

This reference documents the complete Gemini/Antigravity OAuth setup flow for Hermes, from Antigravity CLI authentication to Hermes credential registration.

## Prerequisites

- Antigravity CLI installed and authenticated (`gemini auth login` or `agy auth login`)
- Valid OAuth credentials at `~/.gemini/oauth_creds.json`

## Key Commands Used

```cmd
# 1. Verify Antigravity CLI auth
cat ~/.gemini/oauth_creds.json
# Should show: access_token, refresh_token, expiry_date

# 2. Add to Hermes credential pool
hermes auth add gemini-oauth
# → Uses resolve_gemini_oauth_runtime_credentials() to import from Antigravity CLI

# 3. Verify Hermes auth
hermes auth status gemini-oauth
# → "gemini-oauth: logged in via Antigravity CLI"

# 4. Verify doctor
hermes doctor --fix
# → Shows "✓ Google Gemini OAuth (logged in via Antigravity CLI)"
```

## Files Involved

| File | Purpose |
|------|---------|
| `~/.gemini/oauth_creds.json` | Antigravity CLI OAuth tokens (access_token, refresh_token, id_token, expiry_date) |
| `~/.hermes/auth.json` | Hermes credential pool (includes gemini-oauth provider) |

## Internal Hermes Functions

- `_antigravity_cli_auth_path()` → returns `Path.home() / ".gemini" / "oauth_creds.json"`
- `_read_antigravity_cli_tokens()` — reads tokens from Antigravity CLI auth file
- `_save_antigravity_cli_tokens(tokens)` — writes tokens to Antigravity CLI auth file (atomic)
- `_antigravity_access_token_is_expiring(access_token, skew_seconds=120)` — checks JWT exp claim
- `get_gemini_oauth_auth_status()` — status for doctor/desktop UI
- `resolve_gemini_oauth_runtime_credentials(force_refresh, refresh_if_expiring, refresh_skew_seconds)` — runtime credentials for model calls

## Token Refresh Note

Antigravity OAuth tokens use Google's OAuth2. The refresh token in `~/.gemini/oauth_creds.json` can be used to obtain new access tokens via Google's token endpoint, but the client_id/client_secret used for initial auth are not stored in the Antigravity CLI auth file. 

**Current behavior:** If the access token is expiring (within 120s), Hermes logs a warning and continues with the current token. The actual refresh should be done by running `gemini auth login` in a terminal, which has the full OAuth client credentials.

## Troubleshooting Notes

| Issue | Resolution |
|-------|------------|
| `gemini` not found | Install via Antigravity IDE or standalone installer |
| `gemini auth login` fails | Use `--no-browser` flag or run from interactive shell |
| Hermes doesn't see gemini-oauth | Run `gemini auth login` to refresh, then `hermes auth add gemini-oauth` |
| Token expired | Antigravity CLI must refresh; Hermes cannot refresh without client_id/client_secret |

## Verification Checklist

- [ ] `cat ~/.gemini/oauth_creds.json` shows valid tokens
- [ ] `hermes auth add gemini-oauth` succeeds
- [ ] `hermes auth status gemini-oauth` → "logged in via Antigravity CLI"
- [ ] `hermes auth list` shows gemini-oauth credential
- [ ] `hermes doctor --fix` shows ✓ Google Gemini OAuth

## Implementation Details

### Provider Registration (auth.py)
```python
"gemini-oauth": ProviderConfig(
    id="gemini-oauth",
    name="Google Gemini OAuth (via Antigravity CLI)",
    auth_type="oauth_external",
    inference_base_url="https://generativelanguage.googleapis.com/v1beta",
),
```

### Model Picker Entry (models.py)
```python
ProviderEntry("gemini-oauth", "Google Gemini OAuth", "Google Gemini OAuth (via Antigravity CLI / Google account)"),
```

### OAuth Catalog Entry (web_server.py)
```python
{
    "id": "gemini-oauth",
    "name": "Google Gemini OAuth (via Antigravity CLI)",
    "flow": "external",
    "cli_command": "hermes auth add gemini-oauth",
    "docs_url": "https://github.com/google-gemini/gemini-cli",
    "status_fn": None,  # dispatched via auth.get_gemini_oauth_auth_status
},
```

### Auth Command Handler (auth_commands.py)
```python
if provider == "gemini-oauth":
    creds = auth_mod.resolve_gemini_oauth_runtime_credentials(refresh_if_expiring=False)
    label = (getattr(args, "label", None) or "").strip() or label_from_token(
        creds["api_key"],
        _oauth_default_label(provider, len(pool.entries()) + 1),
    )
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
    print(f'Added {provider} OAuth credential #{len(pool.entries())}: "{entry.label}"')
    return
```

### Doctor Check (doctor.py)
```python
gemini_oauth_status = get_gemini_oauth_auth_status()
if gemini_oauth_status.get("logged_in"):
    check_ok("Google Gemini OAuth", "(logged in via Antigravity CLI)")
else:
    check_warn("Google Gemini OAuth", "(not logged in)")
    if gemini_oauth_status.get("error"):
        check_info(gemini_oauth_status["error"])
```