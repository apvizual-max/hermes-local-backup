#!/usr/bin/env python3
"""
GitHub Backup Script for Hermes Agent
Run via cron weekly.

Creates a backup of essential Hermes config/state files to:
  apvizual-max/hermes-local-backup

This script backs up configuration, skills, profile settings, and 
important state files. Large binary data (node_modules, venv, 
sessions, caches, etc.) are excluded because:
1. GitHub has 5GB total repo limit, 100MB file limit
2. Binary data is not useful for recovery
3. Source code is already backed up on upstream GitHub

If you need a FULL disk backup including all binary data, use an
external drive instead of GitHub.
"""

import os
import sys
import shutil
import subprocess
import re
import json
import datetime
import stat

HERMES_HOME = os.environ.get('HERMES_HOME', 'C:/Users/apviz/AppData/Local/hermes')
STAGING_DIR = os.path.join(HERMES_HOME, 'hermes-backup-staging')
LOG_FILE = os.path.join(HERMES_HOME, 'scripts', 'backup.log')
REPO_URL = 'https://github.com/apvizual-max/hermes-local-backup.git'
GH_TOKEN = os.environ.get('GH_TOKEN', 'ghp_[REDACTED]')

# Directories that are EXCLUDED from backup (too large for GitHub)
EXCLUDE_DIRS = {
    # Source code (already on GitHub upstream)
    'hermes-agent',
    
    # Large data directories
    'OGLINDA-CASA',         # 210M - Obsidian vault
    '.obsidian',            # Obsidian config
    'OGLINDA-MINTE',        # Work vault
    'node',                 # 1.2G - Node.js runtime
    'backups',              # 639M - Old backups
    'state-snapshots',      # 354M - State data
    'cdp-profile',          # 232M - Chrome devtools data
    'cdp-default',          # 189M - Chrome devtools data
    'cdp-profile-prod',     # 69M - Chrome devtools data
    'cdp-profile2',         # 65M - Chrome devtools data
    'SESSION_ARCHIVES',     # 117M - Session archives
    'SESSION_ARCHIVES',
    
    # Staging/temp for this backup
    'hermes-backup-staging',
    'hermes-backup-temp',
    
    # Other large/caches
    'cache',                # 6.1M
    'sessions',             # 25M - Session data
    'logs',                 # 68M - Log files
    'image_cache',          # 
    'audio_cache',          # 
    'images',               # 6.7M
    'state-snapshots',      # 
    'state',                # Runtime state
    'checkpoints',          # Model checkpoints
    'pets',                 # Pet assets
    'lsp',                  # Language server data
    'OPTIMUS_GRAPH_VIEWER', # 15M
    'sandbox',              # Sandbox files
    'sandboxs',
    'sandboxes',            # 4.1M... wait that's pets
    'memories',             # Runtime memory
    'kanban',               # Kanban data
    'platforms',            # Platform runtime
    'shared',               # Shared data
    'pairing',              # Pairing codes
    'pastes',               # Paste buffer
    'pending_messages',     # Message queue
    'mcp-tokens',           # Token cache
    'bootstrap-cache',      # Bootstrap cache
    'gateway-service',      # Gateway data
    'desktop',              # Desktop runtime
    'desktop-plugins',      # Desktop plugins
    'Engine',               # Engine runtime
    'HISTORY',              # History data
    'hooks',                # Hook data
    'ollama-modelfiles',    # Model files
    'SYS_REPORTS',          # System reports
    'auth',                 # Auth data
    'plugins',              # Plugins (runtime, can be reinstalled)
    'bin',                  # 47M - Binary executables
    'venv',                 # Virtual env
}

# File patterns to exclude (secrets and caches)
EXCLUDE_FILE_PATTERNS = [
    r'\.env$',
    r'\.env\..*',
    r'\.lock$',
    r'\.tmp$',
    r'\.log$',
    r'auth\.json.*',
    r'auth\.lock',
    r'git-credentials',
    r'\.git-credentials',
    r'\.npmrc',
    r'\.skills_prompt_snapshot\.json',
    r'models_dev_cache\.json',
    r'provider_models_cache\.json',
    r'ollama_cloud_models_cache\.json',
    r'mcp_schema_cache\.json',
    r'model_catalog\.json$',
    r'nous_recommended_cache\.json',
    r'openrouter_model_metadata\.json',
    r'channel_directory\.json',
    r'gateway_state\.json',
    r'desktop-build-stamp\.json',
    r'context_length_cache\.yaml',
    r'profile\.yaml',
]

# Secret patterns for redaction
SECRET_PATTERNS = [
    (r'ghp_[A-Za-z0-9]{36}', 'ghp_[REDACTED]'),
    (r'gho_[A-Za-z0-9]{36,}', 'gho_[REDACTED]'),
    (r'ghu_[A-Za-z0-9]{36,}', 'ghu_[REDACTED]'),
    (r'ghs_[A-Za-z0-9]{36,}', 'ghs_[REDACTED]'),
    (r'ghr_[A-Za-z0-9]{36,}', 'ghr_[REDACTED]'),
    (r'sk-or-[a-zA-Z0-9\-]+', 'sk-or-[REDACTED]'),
    (r'sk-ant-[a-zA-Z0-9\-]+', 'sk-ant-[REDACTED]'),
    (r'sk-[a-zA-Z0-9]{20,}', 'sk-[REDACTED]'),
    (r'AIza[A-Za-z0-9_\-]{35}', 'AIzaSy[REDACTED]'),
    (r'1//[A-Za-z0-9_\-]{40,}', '[REDACTED_GOOGLE_TOKEN]'),
    (r'ya29\.[A-Za-z0-9_\-\.]+', '[REDACTED_YA29]'),
]

# Files that MUST be backed up (core config)
ESSENTIAL_ROOT_FILES = [
    'SOUL.md',
    'SENTINEL_JOURNAL.md',
    'JURNAL_OGLINDA.md',
    'AGENTS.md',
    'config.yaml',
    '.env.example',
    '.gitignore',
    '.gitattributes',
    '.python-version',
    '.nvmrc',
    '.bytecode-fingerprint',
]

# Directories that contain config (always include)
ESSENTIAL_DIRS = {
    'skills',
    'profiles',
    'scripts',
    'mcp-servers',
    'cron',
    'cron_providers',
}

# Directories within profiles that should be skipped (runtime data)
PROFILE_EXCLUDE_SUBDIRS = {
    # Runtime data
    'sessions', 'state', 'state-snapshots', 'memories', 'kanban',
    'pets', 'platforms', 'shared', 'pairing', 'pending_messages',
    'pastes', 'logs', 'backups', '.archive', '.curator_backups',
    'checkpoints', 'gateway-service', 'desktop-plugins',
    'desktop', 'bin', 'node', 'node_modules', '__pycache__',
    'cache', 'audio_cache', 'image_cache', 'images',
    'bootstrap-cache', 'cdp-default', 'cdp-profile', 'cdp-profile2',
    'cdp-profile-prod', 'ollama-modelfiles', 'OPTIMUS_GRAPH_VIEWER',
    'ENGINE', 'HISTORY', 'SYS_REPORTS', 'auth', 'mcp-tokens',
    'lsp', 'hooks', 'sandbox', 'sandboxes',
    'SESSION_ARCHIVES', 'state-snapshots', 'workspace',
    'home', 'projects',
}

# File types that are safe to back up
SAFE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.json', '.yaml', '.yml',
    '.md', '.txt', '.env', '.cfg', '.ini', '.toml', '.sh', '.bat',
    '.ps1', '.xml', '.html', '.css', '.scss', '.sql', '.rb',
    '.go', '.rs', '.java', '.c', '.h', '.cpp', '.hpp',
    '.conf', '.properties', '.md', '.rst', '.in', '.example',
    '.svg', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf',
    '.crt', '.bst', '.sty', '.cls', '.tex',
    '.woff', '.woff2', '.ttf', '.eot',
}


def log(msg):
    """Log message to console and log file."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except Exception:
        pass


def should_exclude_dir(dirname):
    """Check if directory should be excluded."""
    if dirname in EXCLUDE_DIRS:
        return True
    if dirname in PROFILE_EXCLUDE_SUBDIRS:
        return True
    # Skip hidden directories
    if dirname.startswith('.') and dirname not in {'.env.example'}:
        return True
    return False


def should_exclude_file(filename):
    """Check if file should be excluded."""
    # Check patterns
    for pattern in EXCLUDE_FILE_PATTERNS:
        if re.search(pattern, filename):
            return True
    
    # Skip backup artifacts
    if filename in {'backup.log', 'backup-hermes.py', 'redact-secrets.py', 
                     'weekly-backup.bat'}:
        return True
    
    return False


def safe_copy2(src, dst):
    """Copy file with error handling."""
    try:
        shutil.copy2(src, dst)
        return True
    except Exception:
        return False


def copy_files():
    """Copy essential Hermes files to staging directory."""
    log("Copying files from Hermes home directory...")
    
    file_count = 0
    
    # Clean staging
    if os.path.exists(STAGING_DIR):
        def remove_readonly(func, path, excinfo):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception:
                pass
        shutil.rmtree(STAGING_DIR, onerror=remove_readonly)
    
    os.makedirs(STAGING_DIR, exist_ok=True)
    
    # Copy essential root-level files
    for filename in ESSENTIAL_ROOT_FILES:
        src = os.path.join(HERMES_HOME, filename)
        if os.path.isfile(src):
            dst = os.path.join(STAGING_DIR, filename)
            if safe_copy2(src, dst):
                file_count += 1
    log(f"  Copied {len(ESSENTIAL_ROOT_FILES)} root config files")
    
    # Copy essential directories
    for dirname in os.listdir(HERMES_HOME):
        src_dir = os.path.join(HERMES_HOME, dirname)
        if not os.path.isdir(src_dir):
            continue
        
        # Only copy essential dirs
        if dirname not in ESSENTIAL_DIRS:
            log(f"  Skipping: {dirname}")
            continue
        
        dst_dir = os.path.join(STAGING_DIR, dirname)
        
        for root, dirs, files in os.walk(src_dir):
            # Filter excluded directories
            dirs[:] = [d for d in dirs if not should_exclude_dir(d)]
            
            # Skip nested duplicate directories (e.g., skills/skills/)
            rel_to_src = os.path.relpath(root, src_dir)
            if rel_to_src != '.':
                parts = rel_to_src.split(os.sep)
                if len(parts) > 1 and parts[-2] == parts[-1]:
                    dirs[:] = []
                    continue
            
            # Calculate relative path
            rel_root = os.path.relpath(root, src_dir)
            dest_root = os.path.join(dst_dir, rel_root) if rel_root != '.' else dst_dir
            os.makedirs(dest_root, exist_ok=True)
            
            for filename in files:
                if should_exclude_file(filename):
                    continue
                
                src_file = os.path.join(root, filename)
                dst_file = os.path.join(dest_root, filename)
                
                # Skip if inside staging dir
                if os.path.abspath(src_file).startswith(os.path.abspath(STAGING_DIR)):
                    continue
                
                if safe_copy2(src_file, dst_file):
                    file_count += 1
    
    log(f"Total files copied: {file_count}")
    return file_count


def redact_secrets_in_staging():
    """Redact secrets in staging directory."""
    log("Running secret redaction...")
    redacted = 0
    
    for root, dirs, files in os.walk(STAGING_DIR):
        dirs[:] = [d for d in dirs if d != '.git']
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                original = content
                for pattern, replacement in SECRET_PATTERNS:
                    content = re.sub(pattern, replacement, content)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(content)
                    redacted += 1
            except Exception:
                pass
    
    log(f"  Redacted secrets in {redacted} files")


def create_readme_and_snapshot(file_count):
    """Create README.md and system-snapshot.txt."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # README.md
    readme_path = os.path.join(STAGING_DIR, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(f"""# Hermes Agent - Weekly Backup

Automated backup of local Hermes Agent files from:
`{HERMES_HOME}`

## Backup Details

- **Timestamp**: {timestamp}
- **Total files**: {file_count}
- **Source path**: `{HERMES_HOME}`

## What's Backed Up

- `config.yaml` - Hermes configuration
- `SOUL.md` - Operational identity contract
- `SENTINEL_JOURNAL.md` - System journal
- `JURNAL_OGLINDA.md` - Journal of opinions from other AIs
- `AGENTS.md` - Development guide
- `scripts/` - Utility scripts including backup automation
- `skills/` - All Hermes skills
- `profiles/` - Profile configurations (CONSTINTA.md, config.yaml, etc.)
- `mcp-servers/` - Custom MCP servers
- `cron/` - Cron job configurations

## What's Excluded

Large directories excluded because GitHub has a 5GB repo limit:
- `hermes-agent/` - Source code (backed up on upstream GitHub)
- `node/` - Node.js runtime (1.2GB)
- `OGLINDA-CASA/` - Obsidian knowledge vault
- `backups/` - Old backup archives
- `state-snapshots/` - State data snapshots
- `cdp-*/` - Chrome DevTools data
- `SESSION_ARCHIVES/` - Session transcript archives
- Session/cache/runtime data directories

**For a full disk backup including binary data, use an external drive.**

## Recovery

```bash
git clone https://github.com/apvizual-max/hermes-local-backup.git
cp -r hermes-local-backup/* "{HERMES_HOME}/"
```
""")
    
    # System snapshot
    snapshot_path = os.path.join(STAGING_DIR, 'system-snapshot.txt')
    with open(snapshot_path, 'w') as f:
        f.write(f"=== Hermes Agent System Snapshot ===\n")
        f.write(f"Date: {timestamp}\n\n")
        
        # Git status of hermes-agent repo
        f.write("--- Hermes-Agent Repo ---\n")
        agent_dir = os.path.join(HERMES_HOME, 'hermes-agent')
        if os.path.isdir(os.path.join(agent_dir, '.git')):
            try:
                branch = subprocess.check_output(
                    ['git', 'branch', '--show-current'],
                    cwd=agent_dir, text=True, errors='ignore'
                ).strip()
                f.write(f"Branch: {branch}\n")
                last_commit = subprocess.check_output(
                    ['git', 'log', '--oneline', '-1'],
                    cwd=agent_dir, text=True, errors='ignore'
                ).strip()
                f.write(f"Last commit: {last_commit}\n")
            except Exception:
                f.write("Git status unavailable\n")
        else:
            f.write("No hermes-agent repo found\n")
        f.write("\n")


def git_commit_and_push(timestamp):
    """Initialize git in staging dir, commit, and push."""
    log("Setting up git...")
    
    # Initialize git if needed
    subprocess.run(['git', 'init'], cwd=STAGING_DIR, capture_output=True)
    subprocess.run(['git', 'config', 'core.longpaths', 'true'], cwd=STAGING_DIR, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Sentinel Prime'], cwd=STAGING_DIR, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'sentinel.prime@optimus.local'], cwd=STAGING_DIR, capture_output=True)
    subprocess.run(['git', 'config', 'credential.helper', 'store'], cwd=STAGING_DIR, capture_output=True)
    
    # Set up environment for git operations
    push_env = os.environ.copy()
    push_env['GH_TOKEN'] = GH_TOKEN
    push_env['GIT_TERMINAL_PROMPT'] = '0'
    
    # Write credentials for git to use
    cred_file = os.path.expanduser('~/.git-credentials')
    with open(cred_file, 'w') as f:
        f.write(f"https://apvizual-max:{GH_TOKEN}@github.com\n")
    
    # Set remote
    try:
        subprocess.run(['git', 'remote', 'add', 'origin', REPO_URL],
                       cwd=STAGING_DIR, capture_output=True)
    except Exception:
        subprocess.run(['git', 'remote', 'set-url', 'origin', REPO_URL],
                       cwd=STAGING_DIR, capture_output=True)
    
    # Rename to main
    subprocess.run(['git', 'branch', '-M', 'main'], cwd=STAGING_DIR, capture_output=True)
    
    # Create .gitignore
    gitignore_path = os.path.join(STAGING_DIR, '.gitignore')
    with open(gitignore_path, 'w') as f:
        f.write("""# Secrets
.env
.env.*
*.key
*.pem
.git-credentials
**/auth.json*

# Cache/temp
*.log
cache/
hermes-backup-staging/

# Runtime
sessions/
state/
state-snapshots/
memories/
checkpoints/

# Binaries
*.pyc
__pycache__/
""")
    
    # Stage and commit
    log("Staging files...")
    subprocess.run(['git', 'add', '-A'], cwd=STAGING_DIR, capture_output=True)
    
    result = subprocess.run(
        ['git', 'commit', '-m', f"Weekly backup - {timestamp}"],
        cwd=STAGING_DIR, capture_output=True, text=True
    )
    if 'nothing to commit' not in (result.stderr + result.stdout):
        log(f"  Committed: {result.stdout.strip()}")
    else:
        log("  Nothing to commit (no changes)")
    
    # Push
    log("Pushing to GitHub...")
    
    result = subprocess.run(
        ['git', 'push', '-u', 'origin', 'main'],
        cwd=STAGING_DIR, capture_output=True, text=True,
        env=push_env, timeout=120
    )
    
    if result.returncode != 0:
        # Retry with explicit token in URL and force
        log("  Retrying with token in URL and force...")
        result2 = subprocess.run(
            ['git', 'push', '-u', '--force', f'https://x-access-token:{GH_TOKEN}@github.com/apvizual-max/hermes-local-backup.git', 'main:main'],
            cwd=STAGING_DIR, capture_output=True, text=True,
            env=push_env, timeout=120
        )
        if result2.returncode == 0:
            log("  Push successful!")
            return True
        else:
            log(f"  Push failed: {result2.stderr[:200]}")
            return False


def main():
    log("=" * 60)
    log("Starting Hermes Agent Weekly Backup")
    log(f"Source: {HERMES_HOME}")
    log(f"Staging: {STAGING_DIR}")
    log(f"Target: {REPO_URL}")
    log("=" * 60)
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # Step 1: Copy files
        file_count = copy_files()
        
        # Step 2: Redact secrets
        redact_secrets_in_staging()
        
        # Step 3: Create README.md and system snapshot
        create_readme_and_snapshot(file_count)
        
        # Step 4: Commit and push
        success = git_commit_and_push(timestamp)
        
        if success:
            log(f"Backup complete! {file_count} files backed up.")
            print(json.dumps({
                "status": "success",
                "files_backed_up": file_count,
                "timestamp": timestamp,
                "repo": REPO_URL,
            }, indent=2))
        else:
            log("Backup FAILED during push")
            return 1
            
    except Exception as e:
        log(f"ERROR: {e}")
        import traceback
        log(traceback.format_exc())
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
