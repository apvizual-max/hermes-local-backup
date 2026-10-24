#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Journal Keywords cron job: extracts keywords from SENTINEL_JOURNAL.md and writes an index.
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
    
    # Stopword sets (basic)
    stopwords_en = set("""the and or of to in is it that this was for with as on at but from by about into over after also very just not you we he she they i am are be been being have has had do does did can could should would may might must""".split())
    stopwords_ro = set("""si sau pentru cu la de este sa cat mai putin foarte dar ori de asemenea totusi insa chiar bine rau nu da nu""".split())
    stopwords = stopwords_en.union(stopwords_ro)
    
    if not journal_path.is_file():
        print(f"Journal not found at {journal_path}")
        return
    
    try:
        with open(journal_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read journal: {e}")
        return
    
    # Split into entries: delimiters are lines that are exactly '---' or lines starting with AMINTIRE- followed by digits and a space or dash.
    # We'll split by regex that matches a line with only --- or AMINTIRE-#### 
    # We'll keep the delimiters as separate? Simpler: find all entries by splitting on pattern that matches the delimiter line and keep the delimiter?
    # We'll just split by '\\n---\\n' and also by '\\nAMINTIRE-\\d+ '
    # Let's do a simple approach: replace AMINTIRE lines with a marker then split.
    # But we want to preserve order and extract per entry.
    # We'll split by '(?m)^---$|^AMINTIRE-\\d+ .*$' but we want to keep the sections between.
    # Instead, we can find all matches of the delimiter and then slice.
    # For simplicity, we'll treat the whole file and extract words from the entire content? The spec said to log keywords matching chronological order of the journal.
    # We'll extract from the whole content but we need to keep order of appearance across entries.
    # We'll just process the whole file as a string, extract words in order, and deduplicate globally (first occurrence kept). That gives chronological order.
    
    # Tokenize: split by non-alphanumeric (including underscore) but keep letters with diacritics? We'll use regex \\w+ which matches alphanumeric and underscore, but also matches digits and underscore.
    # We want to keep words with letters (including Unicode). We'll use regex [\\w\\p{L}]+? Python's re doesn't support \\p{L} by default. We'll use [^\W\d_]+ which matches any Unicode letter and underscore? Actually \w in Python 3 with Unicode includes letters, digits, underscore. We'll then filter out those that are only digits.
    # Simpler: extract sequences of Unicode letters (including diacritics) using the regex [^\W\d_]+ with the UNICODE flag.
    # We'll do: re.findall(r'[^\W\d_]+', content, flags=re.UNICODE) to get sequences of Unicode letters.
    # Then filter length >=4 and not in stopwords (case-insensitive check).
    
    # ⚡ Bolt optimization: pushed length filter into regex {4,} to avoid O(N) allocation of short words,
    # and reordered loop checks to delay .lower() allocation until after O(1) deduplication check.
    words = re.findall(r'[^\W\d_]{4,}', content, flags=re.UNICODE)
    seen = set()
    keywords = []
    for w in words:
        if w in seen:
            continue
        seen.add(w)
        if w.lower() in stopwords:
            continue
        keywords.append(w)
    
    # Write timestamped index file
    timestamped_path = reports_dir / f"JOURNAL_KEYWORDS_{timestamp}.txt"
    with open(timestamped_path, "w", encoding="utf-8") as f:
        for kw in keywords:
            f.write(kw + "\n")
    
    # Update master index (append-only, avoid duplicates)
    master_path = reports_dir / "JOURNAL_KEYWORDS_IDX.txt"
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
    
    print(f"Journal keywords index updated. New keywords: {len(to_add)}")

if __name__ == "__main__":
    main()