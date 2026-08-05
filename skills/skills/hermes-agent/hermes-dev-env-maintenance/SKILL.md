---
name: hermes-dev-env-maintenance
description: "Fix npm vulns and install Codex CLI in Hermes node env."
version: 1.1.0
author: Hermes Agent
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [Hermes, Development, NPM, Security, Codex, OAuth, NodeJS, Gemini, Antigravity]
    related_skills: [hermes-agent, hermes-mcp-integration, codex, antigravity-cli]
---

# Hermes Development Environment Maintenance

Class-level skill for keeping the Hermes Agent development environment healthy, secure, and properly configured for autonomous coding agents.

## When to Use

- `hermes doctor --fix` reports npm vulnerabilities in workspaces (root, web, ui-tui)
- Need to install CLI tools (Codex, Gemini/Antigravity, Claude Code, etc.) in Hermes' isolated Node.js environment
- Setting up OAuth device authorization for coding agents
- Verifying development toolchain after Hermes updates

---

## 1. NPM Vulnerability Remediation in Monorepo Workspaces

### Symptom
`hermes doctor --fix` reports:
```
⚠ Browser tools (agent-browser) deps (N high vulnerabilities)
⚠ web workspace deps (N high vulnerabilities)
⚠ ui-tui workspace deps (N high vulnerabilities)
```

### Root Cause
Transitive dependency `brace-expansion@5.0.8` (DoS vulnerability GHSA-rgw5-rvv9-x895) pinned in root `package.json` overrides, blocking `npm audit fix` in workspaces.

### Fix Procedure

1. **Locate the override** in root `package.json`:
   ```json
   "overrides": {
     "brace-expansion": "5.0.8"  // VULNERABLE VERSION
   }
   ```

2. **Update to safe version** (allows `^5.0.9` which patches the DoS):
   ```json
   "overrides": {
     "brace-expansion": "^5.0.9"
   }
   ```

3. **Reinstall root dependencies** (propagates to workspaces):
   ```cmd
   cd C:\Users\apviz\AppData\Local\hermes\hermes-agent
   npm install --workspaces=false
   ```

4. **Verify all workspaces clean**:
   ```cmd
   npm audit --workspaces=false
   cd web && npm audit
   cd ../ui-tui && npm audit
   ```
   All should report `found 0 vulnerabilities`.

### Key Insight
Monorepo workspaces inherit root `overrides`. A single vulnerable override in root `package.json` blocks `npm audit fix` in ALL workspaces. Fix at root, then reinstall.

---

## 2. Codex CLI Installation in Hermes Node Environment

### Prerequisite
Hermes maintains an isolated Node.js installation at:
```
C:\Users\apviz\AppData\Local\hermes\node\
```
This has its own `package.json`, `node_modules`, and bin shims (`codex.cmd`, `codex.ps1`).

### Installation
```cmd
cd C:\Users\apviz\AppData\Local\hermes\node
npm install @openai/codex
```

This installs Codex CLI and creates `codex`/`codex.cmd`/`codex.ps1` in the Hermes node bin directory, making `codex` available on PATH when Hermes runs.

### Verification
```cmd
codex --version
# Should output: codex-cli 0.146.0 (or newer)
```

---

## 3. Codex OAuth Device Authorization Flow

When no `OPENAI_API_KEY` is available, use Codex's built-in device authorization.

### Initiate Login
```cmd
codex login --device-auth
```

### Output Example
```
Welcome to Codex [v0.146.0]
OpenAI's command-line coding agent

Follow these steps to sign in with ChatGPT using device code authorization:

*** Open this link in your browser and sign in to your account
   https://auth.openai.com/codex/device

2. Enter this one-time code (expires in 15 minutes)
   A13Y-KZ0GO

Continue only if you started this login in Codex.
```

### Complete Authorization
1. Open `https://auth.openai.com/codex/device` in browser
2. Sign in to OpenAI/ChatGPT account
3. Enter the one-time code (e.g., `A13Y-KZ0GO`)
4. Click "Authorize"

### Verify
```cmd
codex login status
# Should show: "Logged in"
```

Credential stored in `~/.codex/auth.json`.

---

## 4. Register Codex OAuth with Hermes

For Hermes to use `model.provider: openai-codex`:

```cmd
hermes auth
# → 1. Add credential
# → openai-codex
# → 2. OAuth login
# → (optional label, e.g., "codex-oauth")
```

Stores credential in `~/.hermes/auth.json` for Hermes-managed Codex provider.

---

## 5. Gemini CLI (Antigravity) OAuth Integration

The Antigravity CLI (`gemini`/`agy`) uses Google OAuth stored at `~/.gemini/oauth_creds.json`. Hermes can integrate this as `gemini-oauth` provider.

### Prerequisites
- Antigravity CLI installed and authenticated (run `gemini auth login` or `agy auth login`)
- Valid OAuth credentials at `~/.gemini/oauth_creds.json`

### Hermes Integration (Auto-detected)
Hermes now includes `gemini-oauth` provider with `auth_type: oauth_external` that reads tokens from `~/.gemini/oauth_creds.json`:

```cmd
# Verify Antigravity auth
cat ~/.gemini/oauth_creds.json
# Should show: access_token, refresh_token, expiry_date

# Add to Hermes credential pool
hermes auth add gemini-oauth
# → Uses resolve_gemini_oauth_runtime_credentials() to import from Antigravity CLI

# Verify
hermes auth status gemini-oauth
# → "gemini-oauth: logged in via Antigravity CLI"
```

### Internal Hermes Functions
- `_antigravity_cli_auth_path()` → `~/.gemini/oauth_creds.json`
- `_read_antigravity_cli_tokens()` — reads Antigravity OAuth tokens
- `_antigravity_access_token_is_expiring()` — checks token expiry (120s skew)
- `get_gemini_oauth_auth_status()` — status for doctor/desktop UI
- `resolve_gemini_oauth_runtime_credentials()` — runtime credentials for model calls

### Doctor Check
```cmd
hermes doctor --fix
# Shows: "✓ Google Gemini OAuth (logged in via Antigravity CLI)"
```

### Token Refresh Note
Antigravity OAuth tokens use Google's OAuth2. The refresh token in `~/.gemini/oauth_creds.json` can be used to obtain new access tokens, but the client_id/client_secret used for initial auth are not stored. Token refresh must be done via `gemini auth login` in a terminal. Hermes will warn if the access token is expiring and continue with the current token (which may still work due to Google's grace period).

---

## 6. Troubleshooting Quick Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| `codex` not found | Hermes node bin not on PATH | Use full path or ensure `C:\Users\apviz\AppData\Local\hermes\node` in PATH |
| `stdin is not a terminal` | Running in piped/scripted context | Run `codex login --device-auth` from interactive terminal (PowerShell, cmd.exe) |
| Device code expired | >15 minutes elapsed | Re-run `codex login --device-auth` for fresh code |
| `codex exec` hangs | Missing PTY | Always use `pty=true` in terminal calls |
| `npm audit fix` does nothing | Vulnerable override in root `package.json` | Update root `overrides.brace-expansion` to `^5.0.9` and reinstall |
| `gemini` not found | Antigravity CLI not installed | Install via Antigravity IDE or standalone installer |
| `gemini auth login` fails | Browser/port issues | Use `--no-browser` flag or run from interactive shell |
| Hermes doesn't see gemini-oauth | Antigravity tokens expired | Run `gemini auth login` to refresh, then `hermes auth add gemini-oauth` |

---

## Verification Checklist

After any environment maintenance:
- [ ] `hermes doctor --fix` shows no npm vulnerabilities
- [ ] `codex --version` works
- [ ] `codex login status` shows "Logged in"
- [ ] `hermes auth` lists `openai-codex` credential
- [ ] `gemini auth status` or `cat ~/.gemini/oauth_creds.json` shows valid tokens
- [ ] `hermes auth` lists `gemini-oauth` credential
- [ ] `hermes doctor --fix` shows ✓ OpenAI Codex auth + ✓ Google Gemini OAuth
- [ ] `hermes mcp list` shows all expected servers enabled

---

## References

- [npm audit documentation](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [Codex CLI GitHub](https://github.com/openai/codex)
- [Codex Authentication Docs](https://github.com/openai/codex/blob/main/docs/auth.md)
- Hermes `package.json` override pattern (this skill's Section 1)
- `references/codex-oauth-hermes-integration.md` — complete Codex OAuth + Hermes integration guide
- `references/gemini-oauth-hermes-integration.md` — complete Gemini/Antigravity OAuth + Hermes integration guide

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