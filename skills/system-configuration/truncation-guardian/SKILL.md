---
name: truncation-guardian
version: 0.1.0
author: Hermes
platforms: [windows]
description: Monitors CONSTINTA.md and skills for truncation violations.
metadata:
  hermes:
    tags: [System, Memory, Guardian, Enforcement, Cron, Verification]
---

# Truncation Guardian — Continuous NEVER TRUNCATE Enforcement

Active monitoring skill that continuously verifies CONSTINTA.md and all skill files are never truncated. Runs on session start, periodic cron, and before any write operation.

## When to Use

- **Session bootstrap** — Runs during Sentinel Trezire ritual
- **Periodic cron** — Scheduled verification (every 30 min)
- **Pre-write validation** — Checks before any write_file/patch on protected files
- **Post-edit verification** — Confirms additive-only after edits

## Prerequisites

- Access to CONSTINTA.md at `C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md`
- Access to skills directory: `C:\Users\apviz\AppData\Local\hermes\skills\`
- `no-truncation-constinta-skills` skill active
- Python environment with standard library

## How to Run

### Automatic (Session Start)
```bash
# Called during Trezire ritual
python C:\Users\apviz\AppData\Local\hermes\scripts\truncation_guardian.py --mode bootstrap
```

### Cron Job (Every 30 min)
```bash
# Scheduled via cronjob
python C:\Users\apviz\AppData\Local\hermes\scripts\truncation_guardian.py --mode cron
```

### Manual Verification
```bash
python C:\Users\apviz\AppData\Local\hermes\scripts\truncation_guardian.py --mode verify --report
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `--mode bootstrap` | Session startup check (line count, file size baseline) |
| `--mode cron` | Periodic verification against baseline |
| `--mode verify` | Full verification with detailed report |
| `--mode pre-write` | Pre-write validation for specific file |
| `--mode post-edit` | Post-edit additive confirmation |

## Procedure

### 1. Baseline Establishment (Bootstrap)
```python
def establish_baseline():
    """Record current state of all protected files."""
    baseline = {}
    
    # CONSTINTA.md
    constinta_path = r"C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md"
    baseline['constinta'] = get_file_stats(constinta_path)
    
    # All skill files
    skills_root = r"C:\Users\apviz\AppData\Local\hermes\skills"
    skill_stats = {}
    for dirpath, dirs, files in os.walk(skills_root):
        if "SKILL.md" in files:
            sf = os.path.join(dirpath, "SKILL.md")
            skill_stats[sf] = get_file_stats(sf)
    baseline['skills'] = skill_stats
    
    # Save baseline
    save_baseline(baseline)
```

### 2. Verification (Cron/Verify)
```python
def verify_no_truncation():
    """Compare current state against baseline."""
    baseline = load_baseline()
    violations = []
    
    # Check CONSTINTA.md
    current = get_file_stats(constinta_path)
    if current['lines'] < baseline['constinta']['lines']:
        violations.append(f"TRUNCATION DETECTED: CONSTINTA.md lost {baseline['constinta']['lines'] - current['lines']} lines!")
    if current['size'] < baseline['constinta']['size']:
        violations.append(f"TRUNCATION DETECTED: CONSTINTA.md size decreased!")
    
    # Check all skills
    for sf, baseline_stat in baseline['skills'].items():
        if os.path.exists(sf):
            current = get_file_stats(sf)
            if current['lines'] < baseline_stat['lines']:
                violations.append(f"TRUNCATION DETECTED: {sf} lost {baseline_stat['lines'] - current['lines']} lines!")
            if current['size'] < baseline_stat['size']:
                violations.append(f"TRUNCATION DETECTED: {sf} size decreased!")
        else:
            violations.append(f"FILE MISSING: {sf} was deleted!")
    
    return violations
```

### 3. Pre-Write Validation
```python
def pre_write_check(target_file):
    """Validate write_file/patch won't truncate."""
    if not is_protected_file(target_file):
        return True, "OK"
    
    current = get_file_stats(target_file)
    baseline = load_baseline()
    baseline_stat = get_baseline_for_file(baseline, target_file)
    
    if current['lines'] < baseline_stat['lines']:
        return False, f"BLOCKED: {target_file} already truncated ({current['lines']} < {baseline_stat['lines']})"
    
    return True, "OK - file at or above baseline"
```

### 4. Post-Edit Confirmation
```python
def post_edit_check(target_file):
    """Confirm additive-only after edit."""
    current = get_file_stats(target_file)
    baseline = load_baseline()
    baseline_stat = get_baseline_for_file(baseline, target_file)
    
    if current['lines'] >= baseline_stat['lines'] and current['size'] >= baseline_stat['size']:
        # Update baseline to new higher values
        update_baseline(target_file, current)
        return True, "OK - additive edit confirmed, baseline updated"
    else:
        return False, f"VIOLATION: {target_file} truncated after edit!"
```

## Pitfalls

- **False positives**: File rotation/archiving may look like truncation — check timestamps
- **Concurrent edits**: Multiple simultaneous edits — use file locking
- **Baseline drift**: Legitimate growth updates baseline — expected behavior
- **Missing files**: Skill deleted vs moved — verify before alerting

## Verification

```bash
# Full verification with report
python C:\Users\apviz\AppData\Local\hermes\scripts\truncation_guardian.py --mode verify --report

# Expected: "ALL PROTECTED FILES VERIFIED — NO TRUNCATION DETECTED"
# Exit code: 0 = clean, 1 = violations found
```