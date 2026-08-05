---
title: Maintenance, Updates & Troubleshooting
version: 1.0.0
---

# Maintenance, Updates & Troubleshooting

---

## 1. Regular Maintenance Tasks

### Daily/Weekly
```bash
# 1. Verify all CLIs working
codex --version
agy --version

# 2. Check auth status
hermes auth list
hermes doctor --fix

# 3. Check MCP bridge
# In Hermes: ag_get_status()

# 4. Review credential pool for exhausted entries
hermes auth list | grep -i exhausted
```

### Monthly
```bash
# 1. Update CLIs
cd ~/.hermes/node && npm update @openai/codex
agy update

# 2. Update MCP bridge
cd ~/.hermes/mcp-servers/custom/antigravity-bridge && pip install -e .

# 3. Update Python dependencies
pip install --upgrade -r ~/.hermes/hermes-agent/requirements.txt

# 3. Rotate tokens if needed
# Codex: codex login --device-auth
# Antigravity: agy auth login

# 4. Backup auth stores
cp ~/.hermes/auth.json ~/.hermes/auth.json.backup.$(date +%Y%m%d)
cp ~/.codex/auth.json ~/.codex/auth.json.backup.$(date +%Y%m%d)
cp ~/.gemini/oauth_creds.json ~/.gemini/oauth_creds.json.backup.$(date +%Y%m%d)
```

---

## 2. Update Procedures

### Codex CLI Update
```bash
# Check current version
codex --version

# Update
cd ~/.hermes/node
npm update @openai/codex

# Verify
codex --version

# Re-authenticate if needed
codex login --device-auth
hermes auth add openai-codex --type oauth --label "updated-$(date +%Y%m%d)"
```

### Antigravity CLI Update
```bash
# Check current version
agy --version

# Update
agy update

# Verify
agy --version

# Re-authenticate if needed
agy auth login
hermes auth add gemini-oauth --label "updated-$(date +%Y%m%d)"
```

### MCP Bridge Update
```bash
cd ~/.hermes/mcp-servers/custom/antigravity-bridge
git pull  # if cloned from repo
pip install -e .

# Restart Hermes to reload MCP
```

### Hermes Agent Update
```bash
cd ~/.hermes/hermes-agent
git pull
pip install -e .

# Run doctor to verify
hermes doctor --fix
```

---

## 3. Token Rotation Procedures

### Codex CLI Token Rotation
```bash
# 1. Run device code auth again
codex login --device-auth
# Follow browser flow

# 2. Verify
codex login status

# 3. Import to Hermes (creates new manual:device_code entry)
hermes auth add openai-codex --type oauth --label "codex-$(date +%Y%m%d)"

# 4. Optionally remove old credential
hermes auth list
hermes auth remove openai-codex --target <old-index>
```

### Antigravity CLI Token Rotation
```bash
# 1. Run Google OAuth again
agy auth login
# Follow browser flow

# 2. Verify tokens updated
cat ~/.gemini/oauth_creds.json

# 3. Import to Hermes (reads fresh tokens automatically)
hermes auth add gemini-oauth --label "antigravity-$(date +%Y%m%d)"

# 4. Optionally remove old credential
hermes auth list
hermes auth remove gemini-oauth --target <old-index>
```

---

## 4. Troubleshooting Guide

### 4.1 Codex CLI Issues

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| `codex: command not found` | Not on PATH | `export PATH="$PATH:~/.hermes/node"` or reinstall |
| `codex login --device-auth` fails | Network/auth issue | Check internet, try again |
| `codex login status` → "Not logged in" | Tokens expired | Run `codex login --device-auth` again |
| Hermes shows "logged out" for openai-codex | Tokens not imported | `hermes auth add openai-codex --type oauth` |
| Rate limited (429) | Quota exhausted | Wait for reset_at or re-auth |
| "Missing Authentication header" | Credential pool empty | Check `hermes auth list`, re-add if needed |

### 4.2 Antigravity/Gemini CLI Issues

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| `agy: command not found` | Not on PATH | Check `/c/Users/apviz/AppData/Local/agy/bin/agy` in PATH |
| `agy auth login` hangs | Browser issue | Use `agy auth login --no-browser` if available |
| `agy auth status` times out | Known issue | Check `~/.gemini/oauth_creds.json` directly |
| Tokens expired quickly (~1hr) | Normal Google OAuth | Run `agy auth login` to refresh |
| Hermes shows "logged out" for gemini-oauth | Tokens not imported | `hermes auth add gemini-oauth` |
| "Token refresh failed" | No client_id/secret in Hermes | Must run `agy auth login` manually |

### 4.3 Antigravity Bridge MCP Issues

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Bridge not in `mcp list` | Not in config.yaml | Add `antigravity-bridge` to `mcp_servers` |
| `ag_get_status()` fails | Server not running | Check `config.yaml` cwd path, restart Hermes |
| Tasks stuck "PENDING" | Antigravity not processing | Start Antigravity CLI to process inbox |
| "Connection refused" | Wrong cwd/command | Verify `cwd` and `command` in config.yaml |
| Tasks not appearing in inbox | Path mismatch | Check `HERMES_HOME` env var, inbox path |

### 4.4 Credential Pool Issues

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| "No available credentials" | Pool empty/exhausted | `hermes auth list`, add new creds |
| Credentials not rotating | Wrong strategy | Check `credential_pool.strategy` in config |
| Exhausted credentials not recovering | Cooldown not elapsed | Wait or `hermes auth reset <provider>` |
| DEAD credentials persisting | Terminal auth errors | Re-auth and add fresh credentials |

### 4.5 Profile Issues

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Provider not available in profile | Not in fallback_providers | Add to profile's config.yaml |
| MCP server not loading in profile | Not in profile's mcp_servers | Add to profile's config.yaml |
| Model not found | Not in provider's model list | Check `hermes model` for available models |

---

## 5. Diagnostic Commands

### Full System Diagnostic
```bash
#!/bin/bash
# Save as ~/diagnose.sh and run

echo "=== HERMES DOCTOR ==="
hermes doctor --fix

echo -e "\n=== CLI VERSIONS ==="
codex --version 2>/dev/null || echo "codex: NOT FOUND"
agy --version 2>/dev/null || echo "agy: NOT FOUND"

echo -e "\n=== AUTH STATUS ==="
hermes auth list

echo -e "\n=== TOKEN FILES ==="
ls -la ~/.codex/auth.json 2>/dev/null || echo "codex auth: MISSING"
ls -la ~/.gemini/oauth_creds.json 2>/dev/null || echo "gemini auth: MISSING"

echo -e "\n=== MCP SERVERS ==="
hermes mcp list 2>/dev/null || echo "MCP not available"

echo -e "\n=== CREDENTIAL POOL ==="
cat ~/.hermes/auth.json | python -m json.tool | grep -A5 "credential_pool"

echo -e "\n=== DISK SPACE ==="
df -h ~/.hermes
```

### Quick Health Check
```bash
# One-liner health check
hermes doctor --fix && hermes auth list && codex --version && agy --version
```

---

## 6. Emergency Recovery

### If All Auth Breaks
```bash
# 1. Backup current state
cp ~/.hermes/auth.json ~/.hermes/auth.json.emergency.bak

# 2. Clear credential pool (keep providers)
# Edit ~/.hermes/auth.json, set "credential_pool": {}

# 3. Re-authenticate each
codex login --device-auth
agy auth login

# 4. Re-import
hermes auth add openai-codex --type oauth --label "recovery-codex"
hermes auth add gemini-oauth --label "recovery-antigravity"

# 5. Verify
hermes doctor --fix
```

### If MCP Bridge Corrupted
```bash
# 1. Clear bridge state
rm -rf ~/.hermes/pairing/antigravity/inbox/*
rm -rf ~/.hermes/pairing/antigravity/outbox/*
rm -rf ~/.hermes/pairing/antigravity/history/*

# 2. Restart Hermes
# 3. Verify
ag_get_status()
```

### If Config Corrupted
```bash
# 1. Backup
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak
cp ~/.hermes/profiles/default/config.yaml ~/.hermes/profiles/default/config.yaml.bak

# 2. Restore from known good
# Copy from backup or recreate minimal config

# 3. Run doctor
hermes doctor --fix
```

---

## 7. Log Locations for Debugging

| Component | Log Location |
|-----------|--------------|
| Hermes Agent | `~/.hermes/logs/` |
| Codex CLI | `~/.codex/log/` |
| Antigravity CLI | `~/.gemini/antigravity-cli/log/cli-*.log` |
| Antigravity Bridge | `~/.hermes/pairing/antigravity/status.json` |
| MCP Servers | `~/.hermes/logs/mcp-*.log` |
| Hermes Doctor | Console output (run with `--verbose`) |

---

## 8. Support & Escalation

### Self-Service Resources
- `hermes doctor --fix` - Primary diagnostic
- `hermes auth list` - Credential status
- `hermes model` - Provider/model availability
- Skill references in `~/.hermes/skills/orchestration/cli-prime-orchestrator/references/`

### When to Escalate
- Persistent auth failures after re-auth
- MCP bridge completely unresponsive
- Credential pool corruption
- Profile config conflicts

### Information to Provide
```bash
# Collect for bug report
hermes doctor --fix > doctor-output.txt 2>&1
hermes auth list >> doctor-output.txt
cat ~/.hermes/auth.json >> doctor-output.txt
codex --version >> doctor-output.txt
agy --version >> doctor-output.txt
```

---

*This maintenance guide ensures long-term health of the CLI integration ecosystem.*