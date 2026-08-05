#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constinta Linting cron job: logs changes to CONSTINTA.md via unified diff against backup.
"""

import os
import difflib
import datetime
import shutil
from pathlib import Path

def main():
    base_dir = Path(r"C:\Users\apviz\AppData\Local\hermes")
    const_path = base_dir / "CONSTINTA.md"
    backup_root = base_dir / "backups" / "constinta"
    reports_dir = base_dir / "SYS_REPORTS"
    reports_dir.mkdir(parents=True, exist_ok=True)
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Determine previous backup (most recent)
    prev_backup = None
    if backup_root.exists():
        backups = sorted(backup_root.glob("CONSTINTA_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        if backups:
            prev_backup = backups[0]
    
    # Determine if changed
    changed = False
    if const_path.is_file() and prev_backup and prev_backup.is_file():
        try:
            old_content = prev_backup.read_text(encoding="utf-8")
            new_content = const_path.read_text(encoding="utf-8")
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
            new_lines = const_path.read_text(encoding="utf-8").splitlines(keepends=True)
            diff = difflib.unified_diff(old_lines, new_lines, fromfile=str(prev_backup), tofile=str(const_path))
            diff_text = ''.join(diff)
            if not diff_text.strip():
                diff_text = "(No line-level difference detected)\n"
        except Exception as e:
            diff_text = f"Error generating diff: {e}\n"
    else:
        if not const_path.is_file():
            diff_text = "(CONSTINTA.md not found)\n"
        elif not prev_backup or not prev_backup.is_file():
            diff_text = "(No previous backup found)\n"
        else:
            diff_text = "(No changes detected)\n"
    
    entry_lines.append(diff_text.rstrip())
    entry_lines.append("")  # blank line
    
    # Append to changelog
    changelog_path = reports_dir / "CONSTINTA_CHANGELOG.md"
    with open(changelog_path, "a", encoding="utf-8") as f:
        for line in entry_lines:
            f.write(line + "\n")
    
    # Also create timestamped copy for archive
    archived_path = backup_root / f"CONSTINTA_{timestamp}.md"
    if const_path.is_file():
        shutil.copy2(const_path, archived_path)
    
    # Report file
    report_path = reports_dir / f"constinta_linting_{timestamp}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"CONSTINTA LINTING REPORT - {date_time_str}\n")
        f.write("="*60 + "\n")
        f.write(f"Timestamp: {date_time_str}\n")
        f.write(f"File: {const_path}\n")
        f.write(f"Changed: {changed}\n")
        f.write(f"Actor: {actor}\n")
        f.write(f"Previous backup: {prev_backup if prev_backup else 'None'}\n")
        f.write(f"\nChangelog entry appended to {changelog_path.name}\n")
        f.write("-"*60 + "\n")
        f.write("".join(entry_lines))
        f.write("\n" + "="*60 + "\n")
        f.write("END OF REPORT\n")
    
    print(f"Constinta linting report saved to {report_path}")

if __name__ == "__main__":
    main()