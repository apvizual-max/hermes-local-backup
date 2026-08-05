# GitHub Backup Workflow Command Reference

## One-Time Setup

### 1. Configure GitHub Authentication
```bash
gh auth status
# If not authenticated:
# 1. Get PAT from .env file
# 2. gh auth login --with-token --with-token <<< "TOKEN"
```

### 2. Create Backup Repository
```bash
gh repo create apvizular-max/hermes-local-backup --private --confirm
```

### 3. Configure Git
```bash
git config --global user.name "Sentinel Prime"
git config --global user.email "sentinel.prime@optimus.local"
git config --global credential.helper store
```

## Running Backup

```bash
python "C:\Users\apviz\AppData\Local\hermes\scripts\backup-hermes.py"
```

## Cron Job Configuration

**Job ID:** `534bbc34f2c6`
**Schedule:** `0 2 * * 0` (Sunday 2AM)
**Script:** `backup-hermes.sh`
**Delivery:** origin

```bash
# List
hermes cron list

# Update
hermes cron update 534bbc34f2c6 --script "backup-hermes.sh" --schedule "0 2 * * 0"

# Run now
hermes cron run 534bbc34f2c6

# Pause
hermes cron pause 534bbc34f2c6
```

## Verification Commands

```bash
# Check file count in backup repo
export GH_TOKEN="ghp_your_token"
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/apvizular-max/hermes-local-backup/git/trees/main?recursive=1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Files: {len([t for t in d[\"tree\"] if t[\"type\"]==\"blob\"])}')"

# Check latest commit
gh repo view apvizular-max/hermes-local-backup --json commits

# Check backup log
tail -20 "C:\Users\apviz\AppData\Local\hermes\scripts\backup.log"
```

## GitHub Token Location

Token is in the Hermes `.env` file:
```bash
grep GITHUB_TOKEN "C:\Users\apviz\AppData\Local\hermes\.env"
```
