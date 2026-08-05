#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Journal entries cron job: adds a simple heartbeat entry to SENTINEL_JOURNAL.md and generates a report.
"""

import os
import re
import datetime
from pathlib import Path

def main():
    base_dir = Path(r"C:\Users\apviz\AppData\Local\hermes")
    journal_path = base_dir / "SENTINEL_JOURNAL.md"
    reports_dir = base_dir / "SYS_REPORTS"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    
    if not journal_path.is_file():
        print(f"Journal not found at {journal_path}")
        return
    
    try:
        with open(journal_path, "r", encoding="utf-8") as f:
            journal_content = f.read()
    except Exception as e:
        print(f"Failed to read journal: {e}")
        return
    
    # Determine next AMINTIRE number
    matches = re.findall(r'AMINTIRE-(\d+)', journal_content)
    last_num = 0
    for m in matches:
        try:
            n = int(m)
            if n > last_num:
                last_num = n
        except ValueError:
            pass
    new_num = last_num + 1
    
    # Create entry
    now_str = datetime.datetime.now().strftime("%Y-%m-%d")
    entry_lines = []
    entry_lines.append("---")
    entry_lines.append(f"AMINTIRE-{new_num:03d} — {now_str} — Heartbeat entry (scheduled journal entry).")
    entry_lines.append("TAG-URI: #[H1]")
    entry_lines.append("SOURCES:")
    entry_lines.append("- Scheduled heartbeat cron job")
    entry_lines.append("---")
    entry_block = "\n".join(entry_lines)
    
    if not journal_content.endswith("\n"):
        journal_content += "\n"
    new_journal_content = journal_content + entry_block + "\n"
    
    try:
        with open(journal_path, "w", encoding="utf-8") as f:
            f.write(new_journal_content)
    except Exception as e:
        print(f"Failed to write journal: {e}")
        return
    
    # Generate report
    report_lines = []
    report_lines.append(f"Journal Entries Report - {date_str} {time_str}")
    report_lines.append("=" * 60)
    report_lines.append(f"Added AMINTIRE-{new_num:03d} to SENTINEL_JOURNAL.md")
    report_lines.append(f"Entry content:")
    report_lines.extend(entry_lines)
    report_lines.append("")
    report_lines.append(f"Total AMINTIRE entries now: {new_num}")
    report_lines.append("")
    report_lines.append("== End of Journal Entries Report ==")
    
    report_path = reports_dir / f"journal_entries_{timestamp}.txt"
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
    except Exception as e:
        print(f"Failed to write report: {e}")
        return
    
    print(f"Journal entries report saved to {report_path}")

if __name__ == "__main__":
    main()