#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lessons Learned Index cron job: extracts core instructions/principles from journal and lessons file,
stores them as dated lines in an index.
"""

import os
import re
import datetime
from pathlib import Path

def main():
    base_dir = Path(r"C:\Users\apviz\AppData\Local\hermes")
    journal_path = base_dir / "SENTINEL_JOURNAL.md"
    lessons_file = base_dir / "memories" / "LESSONS.md"
    reports_dir = base_dir / "SYS_REPORTS"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Stopword sets (basic)
    stopwords_en = set("""the and or of to in is it that this was for with as on at but from by about into over after also just not you we he she they i am are be been being have has had do does did can could should would may might must""".split())
    stopwords_ro = set("""si sau pentru cu la de este sa cat mai putin foarte dar ori de asemenea totusi insa chiar bine rau nu da nu""".split())
    stopwords = stopwords_en.union(stopwords_ro)
    
    def extract_lessons_from_text(text):
        lessons = []
        # Look for lines starting with LESSON:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.upper().startswith("LESSON:"):
                lesson = stripped[7:].strip()
                if lesson:
                    lessons.append(lesson)
        return lessons
    
    def extract_keyword_sentences(text):
            # Find sentences that contain at least two of the target words
            target = {"principle","rule","law","definition","instruction","protocol","axiom"}
            # Simple sentence split by . ? !
            sentences = re.split(r'[.!?]+', text)
            lessons = []
            for sent in sentences:
                sent_stripped = sent.strip()
                if not sent_stripped:
                    continue
                # Skip sentences that look like file paths or URLs (contain a colon and backslash, or http/https)
                if re.search(r'[A-Za-z]:\\\\', sent_stripped) or re.search(r'https?://', sent_stripped):
                    continue
                # Skip sentences that are primarily a code block or inline code (start and end with backticks)
                if sent_stripped.startswith('`') and sent_stripped.endswith('`'):
                    continue
                # Skip sentences that contain a backtick (to be safe)
                if '`' in sent_stripped:
                    continue
                sent_low = sent_stripped.lower()
                count = sum(1 for w in target if w in sent_low)
                if count >= 2 and len(sent_stripped) >= 20:
                    lessons.append(sent_stripped)
            return lessons
    
    lessons = []
    # From journal
    if journal_path.is_file():
        with open(journal_path, "r", encoding="utf-8") as f:
            journal_text = f.read()
        lessons.extend(extract_lessons_from_text(journal_text))
        lessons.extend(extract_keyword_sentences(journal_text))
    # From lessons file
    if lessons_file.is_file():
        with open(lessons_file, "r", encoding="utf-8") as f:
            lessons_text = f.read()
        # Each line is a lesson
        for line in lessons_text.splitlines():
            line = line.strip()
            if line:
                lessons.append(line)
    
    # Deduplicate while preserving order
    seen = set()
    unique_lessons = []
    for lesson in lessons:
        if lesson not in seen:
            seen.add(lesson)
            unique_lessons.append(lesson)
    
    # Write timestamped index file
    timestamped_path = reports_dir / f"LESSONS_INDEX_{timestamp}.txt"
    with open(timestamped_path, "w", encoding="utf-8") as f:
        for lesson in unique_lessons:
            f.write(f"{date_str} | {lesson}\n")
    
    # Update master index (append-only, avoid duplicates)
    master_path = reports_dir / "LESSONS_INDEX.txt"
    existing = set()
    if master_path.is_file():
        with open(master_path, "r", encoding="utf-8") as f:
            for line in f:
                existing.add(line.rstrip("\n"))
    to_append = []
    for lesson in unique_lessons:
        line = f"{date_str} | {lesson}"
        if line not in existing:
            to_append.append(line)
            existing.add(line)
    if to_append:
        with open(master_path, "a", encoding="utf-8") as f:
            for line in to_append:
                f.write(line + "\n")
    
    print(f"Lessons learned index updated. New lessons: {len(to_append)}")

if __name__ == "__main__":
    main()