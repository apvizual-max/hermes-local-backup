# GitHub Backup Workflow Command Reference

## One-Time Setup

### 1. Configure GitHub Authentication
```bash
# Ensure you're authenticated
gh auth status

# If not, authenticate with token:
# 1. Get token from Hermes .env file
# 2. Use gh auth login --with-token
```

### 2. Create Backup Repository (one-time)
```bash
gh repo create apvizual-max/hermes-local-backup --private --confirm
git remote add origin https://github.com/apvizual-max/hermes-local-backup.git
```

### 3. Configure Git
```bash
git config --global user.name "Sentinel Prime"
git config --global user.email "sentinel.prime@optimus.local"
git config --global credential.helper store
```

## Backup Script Location

```bash
C:\Users\apviz\AppData\Local\hermes\scripts\backup-hermes.py
```

## Running Backup Manually

```bash
# Run the backup script
python "C:\Users\apviz\AppData\Local\hermes\scripts\backup-hermes.py"

# Or via Hermes cronjob (run immediately)
hermes cron run 534bbc34f2c6
```

## Cron Job Configuration

**Cron Job ID:** `534bbc34f2c6`

**Schedule:** `0 2 * * 0` (Every Sunday at 2:00 AM)

**Script:** `backup-hermes.py` (no_agent mode)

**Delivery:** origin (current chat session)

### Manage Cron Job
```bash
# List all cron jobs
hermes cron list

# Update cron job
hermes cron update 534bbc34f2c6 --script "backup-hermes.py" --schedule "0 2 * * 0"

# Run immediately
hermes cron run 534bbc34f2c6

# Pause
hermes cron pause 534bbc34f2c6

# Resume
hermes cron resume 534bbc34f2c6
```

## GitHub Repository Info

- **Owner:** apvizual-max
- **Repo Name:** hermes-local-backup
- **URL:** https://github.com/apvizual-max/hermes-local-backup
- **Visibility:** Private

## Backup Contents

The backup includes:

1. **Root config files:**
   - SOUL.md
   - SENTINEL_JOURNAL.md
   - JURNAL_OGLINDA.md
   - config.yaml
   - AGENTS.md
   - .env.example
   - .gitignore
   - CLAUDE.md

2. **skills/** directory (all Hermes skills)

3. **profiles/** directory (all profile configs):
   - profiles/default/ (CONSTINTA.md, SOUL.md, etc.)
   - profiles/prime/
   - profiles/assist/
   - profiles/coder/
   - ... (all profiles)

4. **scripts/** directory

5. **mcp-servers/** directory

6. **README.md** (auto-generated with backup metadata)

7. **system-snapshot.txt** (git status, disk usage)

## Excluded Directories

These are NOT backed up (too large or redundant):

| Directory | Reason |
|-----------|--------|
| hermes-agent/ | Source code (on upstream GitHub) |
| OGLINDA-CASA/ | Large Obsidian vault (210M) |
| node/ | Node.js runtime (1.2G) |
| backups/ | Old backup archives (639M) |
| state-snapshots/ | State data (354M) |
| cdp-*/ | Chrome DevTools data |
| SESSION_ARCHIVES/ | Session transcripts |
| cache/ | Cache files |
| sessions/ | Session data |
| logs/ | Log files |

## Secret Redaction

The backup script automatically redacts these patterns:

| Pattern | Replacement |
|---------|-------------|
| `ghp_[A-Za-z0-9]{36}` | `ghp_[REDACTED]` |
| `gho_[A-Za-z0-9]{36,}` | `gho_[REDACTED]` |
| `sk-or-[a-zA-Z0-9\-]+` | `sk-or-[REDACTED]` |
| `sk-ant-[a-zA-Z0-9\-]+` | `sk-ant-[REDACTED]` |
| `AIza[A-Za-z0-9_\-]{35}` | `AIzaSy[REDACTED]` |
| `1//[A-Za-z0-9_\-]{40,}` | `[REDACTED_GOOGLE_TOKEN]` |

## Verification Commands

```bash
# Check backup repo on GitHub
gh repo view apvizual-max/hermes-local-backup

# List recent commits
gh repo view apvizual-max/hermes-local-backup --json commits

# Clone for restore
git clone https://github.com/apvizual-max/hermes-local-backup.git

# Check file count
curl -s -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/repos/apvizual-max/hermes-local-backup/commits/main \
  | python -c "import sys,json; print(json.load(sys.stdin)['stats'])"

# View backup log
type "C:\Users\apviz\appdata\Local\hermes\scripts\backup.log" | tail -20
```

## Error Recovery

### Push Protection Error
If GitHub blocks the push due to detected secrets:

1. Check the error message for the file/path
2. Identify the secret pattern
3. Add the pattern to SECRET_PATTERNS in backup-hermes.py
4. Re-run the script

### Locked Files
If staging directory can't be cleaned:

```bash
# Find locking process
handle.exe hermes-backup-staging

# Or just kill and retry
del /S /Q "C:\Users\apviz\AppData\Local\hermes\hermes-backup-staging"
```

### GitHub API Unblock (if needed)
```bash
curl -X POST -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/repos/apvizular-max/hermes-local-backup/security/secret-scanning/unblock-secret/<BLOCK_ID>
```
