---
name: github-backup
description: Autonomous GitHub backup orchestration for Hermes.
version: 1.0.0
author: Sentinel Prime
license: MIT
platforms:
  - windows
metadata:
  hermes:
    tags:
      - GitHub
      - BackUp
      - Automation
      - Cron
      - Orchestration
    category: exec-sentinel-orchestrator
    related_skills:
      - hermes-agent
      - hermes-system-verification
      - optimus-backup-restore
---

# GitHub BackUp Skill

## Overview

The **GitHub BackUp** skill provides the operational capability to automatically
and autonomously back up the entire local Hermes Agent installation directory
(`C:\Users\apviz\AppData\Local\hermes`) to a GitHub repository
(`apvizual-max/hermes-local-backup`).

This skill makes GitHub backup a **transparent, automatic capability** —
whenever the system or a scheduled task needs to back up Hermes state, it
uses this skill rather than requiring manual intervention.

## When to Use

- **Weekly scheduled backup** — Runs every Sunday at 2:00 AM via cron
- **On-demand backup** — Run manually when config changes are significant
- **Pre-update snapshot** — Back up before major system changes
- **Disaster recovery** — Restore from a known-good backup state

## Prerequisites

### GitHub PAT Token

A GitHub Personal Access Token (PAT) with `repo` scope must be configured:

```bash
# Must be stored in one of these locations:
1. ~/.git-credentials (format: https://apvizual-max:TOKEN@github.com)
2. Hermes .env file: GITHUB_TOKEN=your_token_here
3. Environment variable: GH_TOKEN=your_token_here
```

### SSH Key (Optional - for SSH-based auth)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_hermes -C "sentinel.prime@optimus.local"
```

## How to Run

### Manual Execution

```bash
# Run backup immediately
python "C:\Users\apviz\AppData\Local\hermes\scripts\backup-hermes.py"
```

### Scheduled (Cron)

The weekly cron job is configured via the Hermes `cronjob` tool:

```bash
# Schedule: Every Sunday at 2:00 AM
# Runs: backup-hermes.py (no_agent mode)
# Delivers results to: origin (current chat)
```

### Via Hermes Cronjob

The cron job ID: `534bbc34f2c6`
Schedule: `0 2 * * 0` (every Sunday at 2:00 AM)

## Quick Reference

| Component | Path |
|-----------|------|
| Backup Script | `C:\Users\apviz\AppData\Local\hermes\scripts\backup-hermes.py` |
| Shell Script | `C:\Users\apviz\appData\Local\hermes\scripts\backup-hermes.sh` |
| Redaction Script | `C:\Users\apviz\AppData\Local\hermes\scripts\redact-secrets.py` |
| Log File | `C:\Users\apviz\appData\Local\hermes\scripts\backup.log` |
| GitHub Repo | `https://github.com/apvizual-max/hermes-local-backup` |
| Cron Job ID | `534bbc34f2c6` |

## Procedure

### 1. Backup Script Workflow (backup-hermes.py)

The backup script performs these steps in sequence:

1. **Clean staging directory** — Remove old staging files (handles locked files)
2. **Copy root config files** — SOUL.md, config.yaml, AGENTS.md, etc.
3. **Copy essential directories** — skills/, profiles/, scripts/, mcp-servers/
4. **Redact secrets** — Scan all files for API keys, tokens, credentials
5. **Create README.md** — Auto-generated with backup timestamp and file count
6. **Create system-snapshot.txt** — Git status, branch, disk usage
7. **Initialize git** — Fresh repo with proper .gitignore
8. **Commit** — All files with timestamp message
9. **Push** — Force push to GitHub backup repo

### 2. Secret Redaction

The script redacts these patterns before pushing:

- GitHub PATs: `ghp_[A-Za-z0-9]{36}`, `gho_`, `ghu_`, `ghs_`, `ghr_`
- OpenRouter: `sk-or-[a-zA-Z0-9\-]+`
- Anthropic: `sk-ant-[a-zA-Z0-9\-]+`
- OpenAI: `sk-[a-zA-Z0-9]{20,}`
- Google API: `AIza[A-Za-z0-9_\-]{35}`
- Google OAuth: `1//[A-Za-z0-9_\-]{40,}`, `ya29\.[A-Za-z0-9_\-\.]+`

### 3. Excluded Directories

These directories are NOT backed up to GitHub (too large or redundant):

```text
hermes-agent/      → Source code (already on GitHub upstream)
OGLINDA-CASA/      → Large Obsidian vault (210M)
node/              → Node.js runtime (1.2G)
backups/           → Old backup archives (639M)
state-snapshots/   → State data (354M)
cdp-*/             → Chrome DevTools data (~500M combined)
SESSION_ARCHIVES/  → Session transcripts (117M)
```

### 4. What IS Backed Up

```text
├── SOUL.md                    # Operational identity contract
├── SENTINEL_JOURNAL.md        # System journal
├── JURNAL_OGLINDA.md          # Journal of opinions
├── config.yaml                # Hermes configuration
├── scripts/                   # Utility scripts
├── skills/                    # All Hermes skills (~3000 files)
├── profiles/                  # Profile configurations
│   ├── default/               # Default profile
│   ├── prime/                 # Prime profile
│   ├── assist/                # Assist profile
│   ├── coder/                 # Coder profile
│   └── ... (all profiles)
└── mcp-servers/               # Custom MCP servers
```

## Pitfalls

1. **GitHub secret scanning** — If secrets are not fully redacted, the push
   will be blocked. The script's secret patterns must cover all token formats used.

2. **File permissions** — The staging directory may contain locked files.
   The script handles this with `shutil.rmtree(onerror=remove_readonly)`.

3. **Path length limits** — Windows 260-character path limit can cause
   `FileNotFoundError` for deeply nested files. The script uses
   `git config core.longpaths true` to mitigate.

4. **Git credential prompt** — In non-interactive environments (cron),
   Git may prompt for credentials. The script uses `GIT_TERMINAL_PROMPT=0`
   and token-in-URL as fallback.

5. **Force push** — The script uses `--force` to overwrite remote history
   because the staging directory starts fresh each time. This is safe
   because the backup repo exists solely for backup purposes.

6. **Nested duplicate directories** — If `skills/skills/` exists, the script
   auto-detects and skips the nested duplicate.

## Verification

### Check backup repo

```bash
gh repo view apvizual-max/hermes-local-backup --json name,defaultBranchRef
git -C hermes-backup-staging log --oneline -5
```

### Check backup log

```bash
cat "C:\Users\apviz\appdata\Local\hermes\scripts\backup.log" | tail -20
```

### Verify files count

```bash
git -C hermes-backup-staging ls-files | wc -l
```

### Test restore

```bash
git clone https://github.com/apvizual-max/hermes-local-backup.git
ls hermes-local-backup/
```

## Configuration

### Cron Job Configuration

```bash
# View current cron job
hermes cron list

# Update cron job
hermes cron update <job_id> --script "backup-hermes.py" --schedule "0 2 * * 0"

# Manual run
hermes cron run <job_id>
```

### Script Configuration

Edit `backup-hermes.py` to change:

- `HERMES_HOME` — Source directory path
- `REPO_URL` — GitHub repository URL
- `GH_TOKEN` — GitHub PAT token (from .env)
- `EXCLUDE_DIRS` — Directories to skip
- `SECRET_PATTERNS` — Additional regex patterns for redaction
- `ESSENTIAL_DIRS` — Directories to include in backup

### GitHub Repository Settings

The backup repository should have:
- **Private visibility** (to protect config)
- **GitHub Actions disabled** (no CI needed for backup)
- **Push protection enabled** (secrets must be redacted)

```bash
# Create backup repo (one-time setup)
gh repo create apvizual-max/hermes-local-backup --private --confirm
```

## Emergency Procedures

### If push protection blocks backup

1. Identify the blocking secret from the error message
2. Add the secret pattern to `SECRET_PATTERNS` in the script
3. Re-run the backup

### If staging directory is locked

```bash
# Find process locking the directory
handle.exe hermes-backup-staging
# Or kill all python processes and retry
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *backup*"
```

### If GitHub token expires

1. Create new PAT at https://github.com/settings/tokens
2. Update in `.env`: `GITHUB_TOKEN=new_token_here`
3. Update `~/.git-credentials`: `https://apvizual-max:new_token@github.com`

## Related

- **hermes-agent** skill — For managing the source code repo
- **optimus-backup-restore** skill — For system-level backup strategies
- **hermes-system-verification** skill — Post-backup verification
