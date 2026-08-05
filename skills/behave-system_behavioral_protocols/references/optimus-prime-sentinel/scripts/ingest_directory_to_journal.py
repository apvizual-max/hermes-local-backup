#!/usr/bin/env python3
"""
Ingest all text files from a directory into SENTINEL_JOURNAL.md as AMINTIRE entries.
Usage: python ingest_directory_to_journal.py <directory> [file_pattern]
Defaults: file_pattern = *
"""

import os
import re
import sys
from pathlib import Path

JOURNAL_PATH = r"C:\Users\apviz\AppData\Local\hermes\SENTINEL_JOURNAL.md"

def get_last_antimire_number(journal_path):
    try:
        with open(journal_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-20000:]  # last 20000 lines
            for line in reversed(lines):
                if line.startswith('AMINTIRE-'):
                    match = re.search(r'AMINTIRE-(\d+)', line)
                    if match:
                        return int(match.group(1))
    except Exception:
        pass
    return 0

def is_text_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            sample = f.read(1024)
            sample.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False
    except Exception:
        return False

def process_file(filepath, start_num):
    entries = []
    next_num = start_num
    try:
        if os.path.getsize(filepath) > 1 * 1024 * 1024:  # skip >1MB
            print(f"Skipping large file: {filepath}")
            return [], start_num
        with open(filepath, 'r', encoding='utf-8', errors='strict') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        return [], start_num
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return [], start_num

    rel_path = os.path.relpath(filepath, '/c')
    for i, line in enumerate(lines, start=1):
        line_content = line.rstrip('\n')
        entry = f"""AMINTIRE-{next_num:07d} — 2026-07-05 — Line {i} from {rel_path}: {line_content}
TAG-URI: #[LN{i}]
SOURCES:
- `{filepath}`
---
"""
        entries.append(entry)
        next_num += 1
    return entries, next_num

def main():
    if len(sys.argv) < 2:
        print("Usage: python ingest_directory_to_journal.py <directory> [file_pattern]")
        sys.exit(1)
    directory = sys.argv[1]
    pattern = sys.argv[2] if len(sys.argv) > 2 else "*"
    # Normalize path
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    last_num = get_last_antimire_number(JOURNAL_PATH)
    next_num = last_num + 1
    all_entries = []

    for root, dirs, files in os.walk(directory):
        for f in files:
            if not fnmatch.fnmatch(f, pattern):
                continue
            filepath = os.path.join(root, f)
            if not os.path.isfile(filepath):
                continue
            entries, next_num = process_file(filepath, next_num)
            all_entries.extend(entries)

    if not all_entries:
        print("No files processed.")
        return

    try:
        with open(JOURNAL_PATH, 'a', encoding='utf-8') as f:
            f.write(''.join(all_entries))
        print(f"Successfully appended {len(all_entries)} lines to {JOURNAL_PATH}")
    except Exception as e:
        print(f"Error writing to journal: {e}")
        sys.exit(1)

if __name__ == '__main__':
    import fnmatch
    main()