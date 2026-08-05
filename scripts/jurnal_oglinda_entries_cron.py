#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jurnal Oglinda entries cron job: adds a heartbeat entry to JURNAL_OGLINDA.md and generates a report.
"""

import os
import datetime
from pathlib import Path

try:
    from hermes_tools import read_file, write_file
except ImportError as e:
    print(f"Fatal: could not import hermes_tools: {e}")
    raise

def main():
    base_dir = Path("C:/Users/apviz/AppData/Local/hermes")
    journal_path = base_dir / "JURNAL_OGLINDA.md"
    reports_dir = base_dir / "SYS_REPORTS"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    
    if not journal_path.is_file():
        print(f"Jurnal Oglinda not found at {journal_path}")
        return
    
    try:
        journal_content = read_file(str(journal_path))["content"]
    except Exception as e:
        print(f"Failed to read Jurnal Oglinda: {e}")
        return
    
    # Determine next entry number (we'll use a simple counter based on existing lines that start with "- [[#" or look for a pattern)
    # We'll just count the number of lines that look like our entries: e.g., "- [[#..."
    import re
    # We'll look for lines that start with "- [[#" and then have some text and then "]]"
    # But to keep it simple, we'll just count the number of entries we've added via this script? 
    # Instead, we'll look for a pattern like "HEARTBEAT ENTRY" or just use a timestamp.
    # We'll not number them; we'll just add a timestamped entry.
    # However, the user might expect a numbering similar to AMINTIRE? 
    # Since JURNAL_OGLINDA.md might not have a numbering system, we'll just add a timestamped entry.
    
    # Create entry
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_lines = []
    entry_lines.append("---")
    entry_lines.append(f"JOURNAL OGLINDA HEARTBEAT — {now_str} — Scheduled heartbeat entry.")
    entry_lines.append("TAG-URI: #[H1]")
    entry_lines.append("SOURCES:")
    entry_lines.append("- Scheduled heartbeat cron job for Jurnal Oglinda")
    entry_lines.append("---")
    entry_block = "\n".join(entry_lines)
    
    if not journal_content.endswith("\n"):
        journal_content += "\n"
    new_journal_content = journal_content + entry_block + "\n"
    
    try:
        write_file(str(journal_path), new_journal_content)
        print(f"Jurnal Oglinda updated with heartbeat entry.")
    except Exception as e:
        print(f"Failed to write Jurnal Oglinda: {e}")
        return
    
    # Generate report
    report_lines = []
    report_lines.append(f"Jurnal Oglinda Entries Report - {date_str} {time_str}")
    report_lines.append("="*60)
    report_lines.append(f"Added heartbeat entry to JURNAL_OGLINDA.md")
    report_lines.append(f"Entry content:")
    report_lines.extend(entry_lines)
    report_lines.append("")
    report_lines.append("== End of Jurnal Oglinda Entries Report ==")
    
    report_path = reports_dir / f"joglinda_entries_{timestamp}.txt"
    write_file(str(report_path), "\n".join(report_lines))
    
    print(f"Jurnal Oglinda entries report saved to {report_path}")

if __name__ == "__main__":
    main()