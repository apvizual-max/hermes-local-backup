---
name: github-backup-automation
description: Autonomous GitHub backup of Hermes local files.
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
      - optimus-backup-restore
      - hermes-agent
      - hermes-system-verification
      - exec-local-service-management
---

# GitHub Backup Automation

## Overview

The **GitHub Backup Automation** skill provides the operational capability to
automatically and autonomously back up the local Hermes Agent installation
directory to a GitHub repository (`apvizular-max/hermes-local-backup`).

This skill makes GitHub backup a **transparent, automatic capability** — whenever
the system or a scheduled task needs to back up Hermes state, it uses this skill
rather than requiring manual intervention.

## When to Use

- **Weekly scheduled backup** — Runs every Sunday at 2:00 AM via cron
- **On-demand backup** — Run manually when config changes are significant
- **Pre-update snapshot** — Back up before major system changes
- **Disaster recovery** — Restore from a known-good backup state

## Prerequisites

### GitHub PAT Token

A GitHub Personal Access Token (PAT) with `repo` scope must be available
in the Hermes `.env` file as `GITHUB_TOKEN`.

### GitHub CLI (gh)

```bash
winget install --id GitHub.cli
gh auth login --with-token  # Using PAT from .env
```

## How to Run

```bash
python "C:\Users\apviz\AppData\Local\hermes\scripts\backup-hermes.py"
```

### Scheduled (Cron)

```
Cron Job ID: 534bbc34f2c6
Schedule: 0 2 * * 0 (Every Sunday at 2:00 AM)
Script: backup-hermes.sh
Delivery: origin
```

## Quick Reference

| Component | Path |
|-----------|------|
| Backup Script | `...\scripts\backup-hermes.py` |
| Shell Wrapper | `...\scripts\backup-hermes.sh` |
| GitHub Repo | `apvizular-max/hermes-local-backup` |
| Cron Job ID | `534bbc34f2c6` |

## Procedure

### 1. Backup Script Workflow (backup-hermes.py)

1. **Clean staging** — Remove old staging dir (handles locked files)
2. **Copy root config** — SOUL.md, config.yaml, AGENTS.md
3. **Copy directories** — skills/, profiles/, scripts/, mcp-servers/
4. **Redact secrets** — All files scanned for API keys/tokens
5. **Create README.md** — Auto-generated metadata
6. **Create system-snapshot.txt** — Git status, disk usage
7. **Git init + commit** — Fresh repo with .gitignore
8. **Force push** — `git push --force origin main:main`

### 2. Secret Patterns Redacted

| Pattern | Example |
|---------|---------|
| `ghp_[A-Za-z0-9]{36}` | GitHub PAT |
| `sk-or-[a-zA-Z0-9\-]+` | OpenRouter key |
| `sk-ant-[a-zA-Z0-9\-]+` | Anthropic key |
| `AIza[A-Za-z0-9_\-]{35}` | Google API key |
| `1//[A-Za-z0-9_\-]{40,}` | Google OAuth refresh token |

### 3. Excluded Directories

| Directory | Size | Reason |
|-----------|------|--------|
| `hermes-agent/` | 4.2G | Source on upstream GitHub |
| `node/` | 1.2G | Node.js runtime |
| `backups/` | 639M | Old archives |
| `state-snapshots/` | 354M | State data |
| `OGLINDA-CASA/` | 210M | Obsidian vault |

### 4. Profile Runtime Exclusion

Each profile has runtime subdirs (`cache/`, `sessions/`, `logs/`, `state/`, etc.)
that are excluded via `PROFILE_EXCLUDE` set — these are filtered at EVERY level
within `profiles/`, not just the top directory.

## Pitfalls

1. **GitHub push protection** blocks secrets even after redaction.
   If blocked, read the error for the exact file/pattern, add to
   `SECRET_PATTERNS`, and re-run. The `1//` Google OAuth prefix was
   initially missed from the patterns list.

2. **Git credential prompt** hangs in non-interactive contexts. Script sets
   `GIT_TERMINAL_PROMPT=0` and falls back to token-in-URL:
   `https://x-access-token:TOKEN@github.com/...`

3. **Stale info on push** — Fresh staging repo + remote with history causes
   "stale info" rejection. Use `--force` with `main:main` refspec.

4. **Locked files in staging** — `shutil.rmtree` fails on read-only files.
   Script uses `onerror=remove_readonly` handler that chmods and retries.

5. **Nested duplicate directories** (e.g., `skills/skills/`) — Auto-detected
   by checking if parent dir name == child dir name; walk is aborted.

6. **rsync not available** in WSL — Script uses Python `shutil.copy2`.

7. **Windows path length limit** — Mitigated with `git config core.longpaths true`.

8. **Token in .env** — PAT extracted from Hermes `.env`. Update extraction logic
   if format changes.

## Verification

```bash
# Check backup file count
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/apvizular-max/hermes-local-backup/git/trees/main?recursive=1" \
  | python3 -c "import sys,json; print(len([t for t in json.load(sys.stdin)['tree'] if t['type']=='blob']))"

# Check backup log
tail -20 ".../scripts/backup.log"

# Check cron job
hermes cron list
```

## Emergency Procedures

### Push Protection Blocked

1. Read error for file path + secret pattern
2. Add pattern to `SECRET_PATTERNS` in `backup-hermes.py`
3. Re-run script

### Token Expired

1. Get new PAT from `.env` or GitHub settings
2. Update `~/.git-credentials`

## Related

- **optimus-backup-restore** — Manual file backup/restore (bundled stub)
- **hermes-agent** — Source code management
- **hermes-system-verification** — Post-backup health checks

## Session History

Created during August 5, 2026 session for automated GitHub backup setup.
Commands reference: `references/exec-github-backup/references/backup-workflow-commands.md`
