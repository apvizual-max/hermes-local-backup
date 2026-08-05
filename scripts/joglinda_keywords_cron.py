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
    base_dir = Path(r"C:\Users\apviz\AppData\Local\hermes")
    journal_path = base_dir / "JURNAL_OGLINDA.md"
    reports_dir = base_dir / "SYS_REPORTS"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Stopword sets (basic)
    stopwords_en = set("""the and or of to in is it that this was for with as on at but from by about into over after also very just not you we he she they i am are be been being have has had do does did can could should would may might must""".split())
    stopwords_ro = set("""și sau pentru cu la de este să cât mai puțin foarte dar ori de asemenea totuși insă chiar bine rău nu da nu""".split())
    stopwords = stopwords_en.union(stopwords_ro)
    
    if not journal_path.is_file():
        print(f"Jurnal Oglinda not found at {journal_path}")
        return
    
    try:
        with open(journal_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read Jurnal Oglinda: {e}")
        return
    
    # Extract words: sequences of Unicode letters (including diacritics) of length >=4
    # We'll use regex to match any Unicode letter character: \w matches letters, digits, underscore in Python 3 with Unicode.
    # We want to exclude digits and underscore, so we use [^\W\d_]+ which matches any Unicode letter and underscore? Actually \w is [a-zA-Z0-9_] in ASCII mode, but with Unicode it's letters, digits, underscore.
    # Subtracting digits and underscore: [^\W\d_] matches any character that is not non-word, not digit, not underscore -> effectively letters.
    # We'll use the UNICODE flag.
    words = re.findall(r'[^\W\d_]+', content, flags=re.UNICODE)
    seen = set()
    keywords = []
    for w in words:
        if len(w) < 4:
            continue
        if w.lower() in stopwords:
            continue
        if w not in seen:
            seen.add(w)
            keywords.append(w)
    
    # Write timestamped index file
    timestamped_path = reports_dir / f"OGLINDA_KEYWORDS_{timestamp}.txt"
    with open(timestamped_path, "w", encoding="utf-8") as f:
        for kw in keywords:
            f.write(kw + "\n")
    
    # Update master index (append-only, avoid duplicates)
    master_path = reports_dir / "OGLINDA_KEYWORDS_IDX.txt"
    existing = set()
    if master_path.is_file():
        with open(master_path, "r", encoding="utf-8") as f:
            for line in f:
                existing.add(line.strip())
    to_add = []
    for kw in keywords:
        if kw not in existing:
            to_add.append(kw)
            existing.add(kw)
    if to_add:
        with open(master_path, "a", encoding="utf-8") as f:
            for kw in to_add:
                f.write(kw + "\n")
    
    print(f"Jurnal Oglinda keywords index updated. New keywords: {len(to_add)}")

if __name__ == "__main__":
    main()