#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jurnal Oglinda keywords indexing cron job: extracts keywords from JURNAL_OGLINDA.md and saves an index.
"""

import os
import re
import datetime
from pathlib import Path

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
        with open(journal_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read Jurnal Oglinda: {e}")
        return
    
    # Extract words (sequences of letters, at least 4 letters) and make lowercase
    words = re.findall(r'\b[a-zA-Z]{4,}\b', content)
    # Get unique words, sort
    unique_words = sorted(set(w.lower() for w in words))
    
    # Build report
    lines = []
    lines.append(f"Jurnal Oglinda Keywords Index - {date_str} {time_str}")
    lines.append("="*60)
    lines.append(f"Source: {journal_path}")
    lines.append(f"Total words found: {len(words)}")
    lines.append(f"Unique keywords: {len(unique_words)}")
    lines.append("")
    lines.append("Keywords (alphabetical):")
    for w in unique_words:
        lines.append(f"  {w}")
    lines.append("")
    lines.append("== End of Jurnal Oglinda Keywords Index ==")
    
    report_path = reports_dir / f"jurnal_oglinda_keywords_{timestamp}.txt"
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
    except Exception as e:
        print(f"Failed to write report: {e}")
        return
    
    print(f"Jurnal Oglinda keywords index saved to {report_path}")

if __name__ == "__main__":
    main()