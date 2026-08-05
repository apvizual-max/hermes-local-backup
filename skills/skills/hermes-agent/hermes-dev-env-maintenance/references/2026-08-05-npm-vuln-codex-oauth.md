# Session Notes: npm Vulnerability Fix + Codex OAuth Setup

**Date:** 2026-08-05
**Trigger:** `hermes doctor --fix` reported 4 issues including npm vulnerabilities in 3 workspaces

---

## npm Vulnerability Remediation

### Doctor Output (Before Fix)
```
⚠ Browser tools (agent-browser) deps (2 high vulnerabilities)
⚠ web workspace deps (3 high vulnerabilities)
⚠ ui-tui workspace deps (1 high vulnerability)
```

### Root Cause Identified
Root `package.json` had:
```json
"overrides": {
  "brace-expansion": "5.0.8"
}
```

This pinned the vulnerable version (DoS via GHSA-rgw5-rvv9-x895), blocking `npm audit fix` in all workspaces.

### Fix Applied
```json
"overrides": {
  "brace-expansion": "^5.0.9"
}
```

Then:
```cmd
cd C:\Users\apviz\AppData\Local\hermes\hermes-agent
npm install --workspaces=false
```

### Verification (After Fix)
```
npm audit --workspaces=false        → found 0 vulnerabilities
cd web && npm audit                 → found 0 vulnerabilities
cd ../ui-tui && npm audit           → found 0 vulnerabilities
hermes doctor --fix                 → "no known vulnerabilities" on all three
```

### Key Learning
Monorepo workspaces inherit root `overrides`. A single vulnerable override blocks `npm audit fix` everywhere. Fix at root, then reinstall.

---

## Codex CLI Installation

### Hermes Isolated Node Environment
```
C:\Users\apviz\AppData\Local\hermes\node\
```
Has its own `package.json` (no `@openai/codex` initially).

### Installation
```cmd
cd C:\Users\apviz\AppData\Local\hermes\node
npm install @openai/codex
```

Created `codex.cmd`, `codex.ps1` in bin directory.

### Verification
```cmd
codex --version
# codex-cli 0.146.0
```

---

## Codex OAuth Device Authorization

### Flow Initiated
```cmd
codex login --device-auth
```

### Output
```
Welcome to Codex [v0.146.0]
OpenAI's command-line coding agent

Follow these steps to sign in with ChatGPT using device code authorization:

*** Open this link in your browser and sign in to your account
   https://auth.openai.com/codex/device

2. Enter this one-time code (expires in 15 minutes)
   A13Y-KZ0GO
```

### User Action Required
1. Open https://auth.openai.com/codex/device
2. Sign in to OpenAI/ChatGPT
3. Enter code: `A13Y-KZ0GO`
4. Authorize

### Post-Authorization Verification
```cmd
codex login status
# Should show: "Logged in"
```

Credential stored in `~/.codex/auth.json`.

---

## Register with Hermes

```cmd
hermes auth
# → 1. Add credential
# → openai-codex
# → 2. OAuth login
# → Label: "codex-oauth"
```

Stores in `~/.hermes/auth.json` for `model.provider: openai-codex`.

---

## Troubleshooting Encountered

| Issue | Resolution |
|-------|------------|
| `codex` not found initially | Missing from Hermes node env — installed via npm |
| `codex login --device-auth` timeout | Must run from interactive terminal (not piped) |
| `npm audit fix` no-op | Vulnerable override in root package.json |
| `hermes auth` prompts for label | Optional but recommended for identification |

---

## Files Modified
- `C:\Users\apviz\AppData\Local\hermes\hermes-agent\package.json` (line 53: `brace-expansion` override)