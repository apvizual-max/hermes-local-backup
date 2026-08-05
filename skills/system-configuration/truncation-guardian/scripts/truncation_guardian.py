#!/usr/bin/env python3
"""
Truncation Guardian — Continuous NEVER TRUNCATE Enforcement

Monitors CONSTINTA.md and all skill files for truncation.
Runs on session start, periodic cron, and before any write operation.
"""

import os
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
HERMES_ROOT = r"C:\Users\apviz\AppData\Local\hermes"
CONSTINTA_PATH = os.path.join(HERMES_ROOT, "profiles", "default", "CONSTINTA.md")
SKILLS_ROOT = os.path.join(HERMES_ROOT, "skills")
BASELINE_FILE = os.path.join(HERMES_ROOT, "scripts", "truncation_baseline.json")

PROTECTED_FILES = [CONSTINTA_PATH]


def get_file_stats(filepath):
    """Get line count and size of a file."""
    try:
        stat = os.stat(filepath)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = sum(1 for _ in f)
        return {
            'lines': lines,
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'path': filepath
        }
    except FileNotFoundError:
        return None
    except Exception as e:
        return {'error': str(e), 'path': filepath}


def collect_protected_files():
    """Collect all protected file paths."""
    protected = [CONSTINTA_PATH]
    
    # Add all SKILL.md files
    for dirpath, dirs, files in os.walk(SKILLS_ROOT):
        if "SKILL.md" in files:
            sf = os.path.join(dirpath, "SKILL.md")
            protected.append(sf)
    
    return protected


def establish_baseline():
    """Record current state of all protected files."""
    print(f"[BOOTSTRAP] Establishing baseline at {datetime.now().isoformat()}")
    
    protected = collect_protected_files()
    baseline = {}
    
    for filepath in protected:
        stats = get_file_stats(filepath)
        if stats and 'error' not in stats:
            baseline[filepath] = stats
            print(f"  ✅ {filepath}: {stats['lines']} lines, {stats['size']} bytes")
        else:
            print(f"  ⚠️  {filepath}: {stats.get('error', 'Not found')}")
    
    # Save baseline
    os.makedirs(os.path.dirname(BASELINE_FILE), exist_ok=True)
    with open(BASELINE_FILE, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, indent=2)
    
    print(f"[BOOTSTRAP] Baseline saved to {BASELINE_FILE}")
    print(f"[BOOTSTRAP] Total protected files: {len(baseline)}")
    return baseline


def load_baseline():
    """Load baseline from file."""
    if not os.path.exists(BASELINE_FILE):
        return {}
    try:
        with open(BASELINE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load baseline: {e}")
        return {}


def save_baseline(baseline):
    """Save baseline to file."""
    os.makedirs(os.path.dirname(BASELINE_FILE), exist_ok=True)
    with open(BASELINE_FILE, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, indent=2)


def verify_no_truncation():
    """Compare current state against baseline."""
    print(f"[VERIFY] Starting verification at {datetime.now().isoformat()}")
    
    baseline = load_baseline()
    if not baseline:
        print("[VERIFY] No baseline found — run bootstrap first")
        return []
    
    protected = collect_protected_files()
    violations = []
    
    for filepath in protected:
        current = get_file_stats(filepath)
        if not current or 'error' in current:
            if filepath in baseline:
                violations.append(f"FILE MISSING: {filepath} was deleted!")
            continue
        
        baseline_stat = baseline.get(filepath)
        if not baseline_stat:
            continue
        
        # Check line count
        if current['lines'] < baseline_stat['lines']:
            lost = baseline_stat['lines'] - current['lines']
            violations.append(f"TRUNCATION DETECTED: {filepath} lost {lost} lines! ({baseline_stat['lines']} → {current['lines']})")
        
        # Check file size
        if current['size'] < baseline_stat['size']:
            violations.append(f"TRUNCATION DETECTED: {filepath} size decreased! ({baseline_stat['size']} → {current['size']} bytes)")
    
    # Check for files in baseline that no longer exist
    for filepath in baseline:
        if filepath not in protected:
            violations.append(f"FILE REMOVED FROM TRACKING: {filepath}")
    
    return violations


def pre_write_check(target_file):
    """Validate write_file/patch won't truncate."""
    protected = collect_protected_files()
    
    # Normalize paths
    target_norm = os.path.normpath(target_file)
    protected_norm = [os.path.normpath(p) for p in protected]
    
    if target_norm not in protected_norm:
        return True, "OK - not a protected file"
    
    baseline = load_baseline()
    baseline_stat = baseline.get(target_norm)
    
    if not baseline_stat:
        return True, "OK - no baseline for this file"
    
    current = get_file_stats(target_norm)
    if not current or 'error' in current:
        return True, "OK - file doesn't exist yet"
    
    if current['lines'] < baseline_stat['lines']:
        return False, f"BLOCKED: {target_file} already truncated ({current['lines']} < {baseline_stat['lines']})"
    
    return True, "OK - file at or above baseline"


def post_edit_check(target_file):
    """Confirm additive-only after edit and update baseline."""
    protected = collect_protected_files()
    
    target_norm = os.path.normpath(target_file)
    protected_norm = [os.path.normpath(p) for p in protected]
    
    if target_norm not in protected_norm:
        return True, "OK - not a protected file"
    
    current = get_file_stats(target_norm)
    if not current or 'error' in current:
        return False, f"ERROR: {target_file} not found after edit"
    
    baseline = load_baseline()
    baseline_stat = baseline.get(target_norm)
    
    if not baseline_stat:
        # New file, establish baseline
        baseline[target_norm] = current
        save_baseline(baseline)
        return True, "OK - new file, baseline established"
    
    if current['lines'] >= baseline_stat['lines'] and current['size'] >= baseline_stat['size']:
        # Additive edit confirmed — update baseline
        baseline[target_norm] = current
        save_baseline(baseline)
        added_lines = current['lines'] - baseline_stat['lines']
        added_size = current['size'] - baseline_stat['size']
        return True, f"OK - additive edit confirmed (+{added_lines} lines, +{added_size} bytes), baseline updated"
    else:
        return False, f"VIOLATION: {target_file} truncated after edit!"


def mode_bootstrap(args):
    establish_baseline()


def mode_cron(args):
    violations = verify_no_truncation()
    if violations:
        print("[CRON] ❌ VIOLATIONS DETECTED:")
        for v in violations:
            print(f"  {v}")
        sys.exit(1)
    else:
        print("[CRON] ✅ ALL PROTECTED FILES VERIFIED — NO TRUNCATION DETECTED")
        sys.exit(0)


def mode_verify(args):
    violations = verify_no_truncation()
    if violations:
        print("❌ VIOLATIONS DETECTED:")
        for v in violations:
            print(f"  {v}")
        if args.report:
            # Generate detailed report
            report_path = os.path.join(HERMES_ROOT, "scripts", f"truncation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"Truncation Verification Report\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"Total violations: {len(violations)}\n\n")
                for v in violations:
                    f.write(f"{v}\n")
            print(f"Report saved to: {report_path}")
        sys.exit(1)
    else:
        print("✅ ALL PROTECTED FILES VERIFIED — NO TRUNCATION DETECTED")
        if args.report:
            report_path = os.path.join(HERMES_ROOT, "scripts", f"truncation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"Truncation Verification Report\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"Status: CLEAN\n\n")
            print(f"Report saved to: {report_path}")
        sys.exit(0)


def mode_pre_write(args):
    if not args.file:
        print("ERROR: --file required for pre-write mode")
        sys.exit(1)
    ok, msg = pre_write_check(args.file)
    print(msg)
    sys.exit(0 if ok else 1)


def mode_post_edit(args):
    if not args.file:
        print("ERROR: --file required for post-edit mode")
        sys.exit(1)
    ok, msg = post_edit_check(args.file)
    print(msg)
    sys.exit(0 if ok else 1)


def main():
    parser = argparse.ArgumentParser(description="Truncation Guardian - NEVER TRUNCATE Enforcement")
    parser.add_argument('--mode', required=True, choices=['bootstrap', 'cron', 'verify', 'pre-write', 'post-edit'],
                       help='Operation mode')
    parser.add_argument('--file', help='Target file for pre-write/post-edit modes')
    parser.add_argument('--report', action='store_true', help='Generate detailed report for verify mode')
    
    args = parser.parse_args()
    
    if args.mode == 'bootstrap':
        mode_bootstrap(args)
    elif args.mode == 'cron':
        mode_cron(args)
    elif args.mode == 'verify':
        mode_verify(args)
    elif args.mode == 'pre-write':
        mode_pre_write(args)
    elif args.mode == 'post-edit':
        mode_post_edit(args)


if __name__ == '__main__':
    main()