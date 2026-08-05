#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive system reporting and logging script for Optimus Prime / Sentinel system.
Performs:
- Skill inventory report (active/archived/particular)
- Log changes to core files (SOUL.md, CONSTINTA.md, USER.md) with timestamps
- Index journal keywords for SENTINEL_JOURNAL.md and JURNAL_OGLINDA.md
- Update self via self-update-core (optional)
- Generate reports in C:\Users\apviz\AppData\Local\hermes\SYS_REPORTS
"""

import os
import re
import shutil
import datetime
from pathlib import Path

try:
    from hermes_tools import read_file, write_file, search_files
except ImportError as e:
    print(f"Fatal: could not import hermes_tools: {e}")
    raise

def main():
    base_dir = Path(r"C:\Users\apviz\AppData\Local\hermes")
    reports_dir = base_dir / "SYS_REPORTS"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    
    # 1. Skill inventory report
    skills_dir = base_dir / "skills"
    skill_report = []
    skill_report.append(f"Skill Inventory Report - {date_str} {time_str}")
    skill_report.append("="*60)
    if skills_dir.is_dir():
        for skill_cat in skills_dir.iterdir():
            if skill_cat.is_dir():
                skill_report.append(f"\nCategory: {skill_cat.name}")
                for skill in skill_cat.iterdir():
                    if skill.is_dir() and (skill / "SKILL.md").is_file():
                        # Determine if active, archived, particular
                        # For simplicity, we consider all as active; we could have an archived subdir.
                        skill_report.append(f"  - {skill.name}")
    else:
        skill_report.append("Skills directory not found.")
    skill_report_path = reports_dir / f"skill_inventory_{timestamp}.txt"
    write_file(str(skill_report_path), "\n".join(skill_report))
    
    # 2. Log changes to core files (we'll copy current version to a history folder with timestamp)
    history_dir = base_dir / "HISTORY"
    history_dir.mkdir(parents=True, exist_ok=True)
    core_files = [
        ("SOUL.md", base_dir / "SOUL.md"),
        ("CONSTINTA.md", base_dir / "CONSTINTA.md"),
        # USER.md: we need to locate it; assume in Hermes root or profiles? We'll search.
    ]
    # Find USER.md
    user_candidates = list(base_dir.rglob("user*.md")) + list((base_dir / "profiles").rglob("user*.md"))
    for name, path in core_files:
        if path.is_file():
            dest = history_dir / f"{name}_{timestamp}{path.suffix}"
            shutil.copy2(path, dest)
        else:
            print(f"Core file not found: {path}")
    # For USER.md, we'll search manually later.
    for path in user_candidates:
        if path.is_file():
            dest = history_dir / f"USER_{timestamp}{path.suffix}"
            shutil.copy2(path, dest)
        else:
            print(f"USER.md candidate not found: {path}")
    
    # 3. Index journal keywords
    def index_journal(journal_path, index_path):
        if not journal_path.is_file():
            return
        content = read_file(str(journal_path))["content"]
        # Extract words (simple: split on non-alphanumeric)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        # Get unique words, sort
        unique_words = sorted(set(words))
        # Write index
        index_content = f"Keyword Index for {journal_path.name} - {date_str} {time_str}\n"
        index_content += "="*60 + "\n"
        index_content += "\n".join(unique_words)
        write_file(str(index_path), index_content)
    
    journal_mirror = base_dir / "SENTINEL_JOURNAL.md"
    index_journal(journal_mirror, reports_dir / f"journal_keywords_{timestamp}.txt")
    
    jornal_oglinda = base_dir / "JURNAL_OGLINDA.md"
    index_journal(jornal_oglinda, reports_dir / f"jornal_oglinda_keywords_{timestamp}.txt")
    
    # 4. Log changes to SOUL.md and CONSTINTA.md (we already did history copy)
    # Also we could append a log entry with what changed? For simplicity, we rely on history.
    
    # 5. Update self via self-update-core (optional, we can call the skill)
    # We'll skip to avoid recursion; but we could run it if desired.
    # For now, we just note that we could run it.
    
    # 6. Generate a summary report
    summary = []
    summary.append(f"System Report - {date_str} {time_str}")
    summary.append("="*60)
    summary.append(f"Skill inventory saved to: {skill_report_path.name}")
    summary.append(f"Core files history stored in: {history_dir}")
    summary.append(f"Journal keyword index: {reports_dir / f'journal_keywords_{timestamp}.txt'}")
    summary.append(f"JORNAL_OGLINDA keyword index: {reports_dir / f'jornal_oglinda_keywords_{timestamp}.txt'}")
    summary.append("")
    summary.append("== End of Report ==")
    summary_path = reports_dir / f"system_report_{timestamp}.txt"
    write_file(str(summary_path), "\n".join(summary))
    
    print(f"System reporting completed. Reports saved to {reports_dir}")

if __name__ == "__main__":
    main()