"""Sync changed files from the live hermes home to the backup repo."""
import os
import shutil
import sys

LIVE = r'C:\Users\apviz\AppData\Local\hermes'
BACKUP = r'C:\Users\apviz\AppData\Local\hermes\hermes-backup-work'

# Only sync these specific directories/files that were changed
SYNC_PATHS = [
    # Profile-specific files
    (os.path.join(LIVE, 'profiles', 'default', 'CONSTINTA.md'),
     os.path.join(BACKUP, 'profiles', 'default', 'CONSTINTA.md')),
    (os.path.join(LIVE, 'profiles', 'default', 'JURNAL_OGLINDA.md'),
     os.path.join(BACKUP, 'profiles', 'default', 'JURNAL_OGLINDA.md')),
    (os.path.join(LIVE, 'profiles', 'default', 'SACRED_DEFINITIONS.md'),
     os.path.join(BACKUP, 'profiles', 'default', 'SACRED_DEFINITIONS.md')),
    (os.path.join(LIVE, 'profiles', 'default', 'SENTINEL_CLI_PRIME_INTEGRATIONS.md'),
     os.path.join(BACKUP, 'profiles', 'default', 'SENTINEL_CLI_PRIME_INTEGRATIONS.md')),
    (os.path.join(LIVE, 'profiles', 'default', 'SACRED_DEFINITIONS.md'),
     os.path.join(BACKUP, 'profiles', 'default', 'SACRED_DEFINITIONS.md')),
    (os.path.join(LIVE, 'profiles', 'default', 'SESSION_JOURNAL.md'),
     os.path.join(BACKUP, 'profiles', 'default', 'SESSION_JOURNAL.md')),
    (os.path.join(LIVE, 'profiles', 'cli-prime', 'config.yaml'),
     os.path.join(BACKUP, 'profiles', 'cli-prime', 'config.yaml')),
    (os.path.join(LIVE, 'profiles', 'default', 'SOUL.md'),
     os.path.join(BACKUP, 'profiles', 'default', 'SOUL.md')),

    # Global files
    (os.path.join(LIVE, 'config.yaml'),
     os.path.join(BACKUP, 'config.yaml')),
    (os.path.join(LIVE, 'SENTINEL_JOURNAL.md'),
     os.path.join(BACKUP, 'SENTINEL_JOURNAL.md')),
    (os.path.join(LIVE, 'SOUL.md'),
     os.path.join(BACKUP, 'SOUL.md')),

    # Skills - mcp-update-recovery
    (os.path.join(LIVE, 'skills', 'orchestration', 'mcp-update-recovery', 'SKILL.md'),
     os.path.join(BACKUP, 'skills', 'orchestration', 'mcp-update-recovery', 'SKILL.md')),
]

copied = 0
skipped = 0
for src, dst in SYNC_PATHS:
    if os.path.exists(src):
        # Create parent dirs
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        # Skip symlinks
        if os.path.islink(src):
            if os.path.exists(os.readlink(src)):
                real_src = os.readlink(src)
                print(f'  Symlink: {src} -> {real_src}, copying target')
                shutil.copy2(real_src, dst)
                copied += 1
            else:
                print(f'  Broken symlink: {src}, skipping')
                skipped += 1
            continue
        # Check if file changed
        should_copy = True
        if os.path.exists(dst):
            if os.path.getsize(src) == os.path.getsize(dst):
                with open(src, 'rb') as f1, open(dst, 'rb') as f2:
                    if f1.read() == f2.read():
                        should_copy = False
                        skipped += 1
        if should_copy:
            shutil.copy2(src, dst)
            print(f'  Copied: {os.path.basename(src)}')
            copied += 1
    else:
        print(f'  Not found: {src}')
        skipped += 1

print(f'\nDone: {copied} copied, {skipped} skipped/unchanged')
