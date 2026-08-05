#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
USER.md linting cron job: logs changes to USER.md (in memories) via unified diff against backup.
"""

import os
import difflib
import datetime
import shutil
from pathlib import Path

def main():
    base_dir = Path(r"C:\Users\apviz\AppData\Local\hermes")
    user_path = base_dir / "memories" / "USER.md"
    backup_root = base_dir / "backups" / "user"
    reports_dir = base_dir / "SYS_REPORTS"
    reports_dir.mkdir(parents=True, exist_ok=True)
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine previous backup (most recent)
    prev_backup = None
    if backup_root.exists():
        backups = sorted(backup_root.glob("USER_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        if backups:
            prev_backup = backups[0]
    
    # Determine if changed
    changed = False
    if user_path.is_file() and prev_backup and prev_backup.is_file():
        try:
            old_content = prev_backup.read_text(encoding="utf-8")
            new_content = user_path.read_text(encoding="utf-8")
            if old_content != new_content:
                changed = True
        except Exception:
            changed = False  # assume not changed on error
    else:
        changed = False  # if no previous backup or file missing, treat as no change for reporting
    
    # Determine actor (simplified: if we have a user-editable backup? We'll assume ASSISTANT)
    actor = "ASSISTANT"
    
    # Prepare changelog entry
    entry_lines = []
    entry_lines.append(f"{date_time_str} | {actor} | EDIT")
    if changed and prev_backup and prev_backup.is_file():
        try:
            old_lines = prev_backup.read_text(encoding="utf-8").splitlines(keepends=True)
            new_lines = user_path.read_text(encoding="utf-8").splitlines(keepends=True)
            diff = difflib.unified_diff(old_lines, new_lines, fromfile=str(prev_backup), tofile=str(user_path))
            diff_text = ''.join(diff)
            if not diff_text.strip():
                diff_text = "(No line-level difference detected)\n"
        except Exception as e:
            diff_text = f"Error generating diff: {e}\n"
    else:
        if not user_path.is_file():
            diff_text = "(USER.md not found)\n"
        elif not prev_backup or not prev_backup.is_file():
            diff_text = "(No previous backup found)\n"
        else:
            diff_text = "(No changes detected)\n"
    
    entry_lines.append(diff_text.rstrip())
    entry_lines.append("")  # blank line
    
    # Append to changelog
    changelog_path = reports_dir / "USER_CHANGELOG.md"
    with open(changelog_path, "a", encoding="utf-8") as f:
        for line in entry_lines:
            f.write(line + "\n")
    
    # Also create timestamped copy for archive
    archived_path = backup_root / f"USER_{timestamp}.md"
    if user_path.is_file():
        shutil.copy2(user_path, archived_path)
    
    # Report file
    report_path = reports_dir / f"user_md_linting_{timestamp}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"USER.MD LINTING REPORT – {date_time_str}\n")
        f.write("="*60 + "\n")
        f.write(f"Timestamp: {date_time_str}\n")
        f.write(f"File: {user_path}\n")
        f.write(f"Changed: {changed}\n")
        f.write(f"Actor: {actor}\n")
        f.write(f"Previous backup: {prev_backup if prev_backup else 'None'}\n")
        f.write(f"\nChangelog entry appended to {changelog_path.name}\n")
        f.write("-"*60 + "\n")
        f.write("".join(entry_lines))
        f.write("\n" + "="*60 + "\n")
        f.write("END OF REPORT\n")
    
    print(f"USER.md linting report saved to {report_path}")

if __name__ == "__main__":
    main()