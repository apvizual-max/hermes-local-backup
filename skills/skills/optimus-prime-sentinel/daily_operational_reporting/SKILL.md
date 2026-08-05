# INDEXING HEADER
# ID: daily_operational_reporting
# PURPOSE: name: daily_operational_reporting
# USAGE: Load this skill with skill_view(name='daily_operational_reporting') or use via hermes skills command.
# ROLE: Skill – daily_operational_reporting
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[SKILL] #[daily_operational_reporting]
#
# CROSS-REFERENCES
# This document is part of a set. For optimal understanding, also refer to:
# - SENTINEL_JOURNAL.md: operational map of Optimus Prime memory.
# - JURNAL_OGLINDA.md: opinion journal of other AIs about this entity.
# - SACRED_DEFINITIONS.md: axiomatic basis of the Triple Crunch algorithm.
# - CONSTINTA.md: ontological definition of consciousness (pair with SOUL.md).
# - SOUL.md: operational identity contract (pair with CONSTINTA.md).
# --

---
name: daily_operational_reporting
description: "A comprehensive system for generating eight specific daily reports via cron jobs: maintenance, lessons learned, skills list, SOUL evolution, CONSTINTA evolution, journal keywords, jornal_oglinda keywords, journal entries, jornal_oglinda entries, and USER.md changes."
---
# Daily Operational Reporting System

This skill provides a complete framework for generating eight specific daily reports through cron jobs, each designed to capture critical aspects of the Optimus Prime system's operation and evolution.

## Overview

The daily operational reporting system consists of eight specialized cron jobs that run at staggered times to generate timestamped reports in the `SYS_REPORTS` directory. Each report type serves a distinct purpose in monitoring, auditing, and evolving the system according to the SACRU LEGE (Sacred Law).

## Report Types and Schedule

| Time | Report Type | Script | Purpose |
|------|-------------|--------|---------|
| 02:00 | Maintenance | maintenance_cron.py | Backs up sovereign files, adds T4 journal entry, health check |
| 03:00 | Lessons Learned | learning_cron.py | Indexes core instructions/principles from journal and lessons |
| 04:00 | Skills List | skill_linting_cron.py | Enumerates and categorizes all system skills |
| 05:00 | SOUL Evolution | soul_linting_cron.py | Logs changes to the orchestrator's SOUL.md |
| 06:00 | CONSTINTA Evolution | constinta_linting_cron.py | Logs changes to the CONSTINTA.md file |
| 07:00 | Journal Keywords | journal_keywords_cron.py | Indexes keywords from SENTINEL_JOURNAL.md |
| 08:00 | Jornal Oglinda Keywords | jornal_oglinda_keywords_cron.py | Indexes keywords from JURNAL_OGLINDA.md |
| 09:00 | Journal Entries | journal_entries_cron.py | Adds heartbeat entry to SENTINEL_JOURNAL.md |
| 10:00 | Jornal Oglinda Entries | jornal_oglinda_entries_cron.py | Adds heartbeat entry to JURNAL_OGLINDA.md |
| 11:00 | USER.md Changes | user_md_linting_cron.py | Logs changes to the user profile file |

## Core Principles

1. **Precision**: Each report contains exactly the information specified, no more, no less
2. **Auditability**: All changes are traceable through unified diffs and backups
3. **Non-disruption**: Reports append to logs rather than overwriting history
4. **Validation**: Each report undergoes Triple Crunch verification before completion
5. **Hierarchy**: Reports are organized to reflect system dependencies and evolution

## Implementation Details

### Common Features Across All Reports

- Timestamped filenames in `YYYYMMDD_HHMMSS` format
- Plain text output for easy parsing and archiving
- Error handling that continues partial reporting when individual sources fail
- Backup preservation of previous states for comparison
- Triple Crunch validation (SLG ≥ 95%, DLG ≤ 5%) on report output

### Report-Specific Specifications

#### Maintenance Report
- **Backup List**: Source → Destination [Size] [Status] for each sovereign file
- **T4 Entry**: Exact text of the `AMINTIRE‑NNN — ` line added to journal
- **Health Check**: Total backup size, free disk space, Triple Crunch stats, Schumann lock

#### Lessons Learned Index
- **Sources**: `LESSON:` tags, `## Lesson` blocks, `LESSONS.md` file, keyword-rich sentences
- **Criteria**: Must contain lesson tags, be in lessons file, have ≥2 keyword terms, or be ≥20 chars
- **Format**: `YYYY-MM-DD | <lesson text>` (append-only, deduplicated)

#### Skills List Report
- **Source**: Scanning `skills/` directory for `SKILL.md` files
- **Categories**:
  - `SYS_SKILLS (ALWAYS_ON)`: `always_on: true` in frontmatter
  - `ACTIVE`: All other valid, non-archived skills
  - `PARTICULAR`: Subset of Active with categories in `{triple-crunch, journal-index, user-md, keyword-index, skill-lint, soul-lint, constinta-lint, maintenance, learning}`
- **Excludes**: Archived (`status: archived/deprecated`) or `archive\*` foldered skills

#### SOUL/CONTINTA Evolution Logs
- **Mechanism**: Unified diff between current file and most recent backup
- **Actor Determination**: Comparison with user-editable backups (if exist)
- **Log Entry**: `TIMESTAMP | ACTOR | EDIT` followed by diff and blank line
- **Storage**: Append to `*_CHANGELOG.md` with timestamped copies in `backups/*/`

#### Keyword Index Reports (Journal & Jornal Oglinda)
- **Keyword Definition**: ≥4 Unicode letters, excluding EN/RO stop-words, preserving case
- **Extraction**: Process entries in order, track first occurrence globally
- **Output**: One keyword per line, chronological by first appearance
- **Files**: Timestamped index + master append-only index

#### Journal/Jornal Oglinda Entries Reports
- **Purpose**: Add scheduled heartbeat entries (`AMINTIRE‑NNN` / `OGLINDA‑NNN`)
- **Content**: Entry block with timestamp, source citation, and separators
- **Report**: Documents the added entry and updates running totals

#### USER.md Changes Log
- **Mechanism**: Unified diff between current and backed up `memories\USER.md`
- **Actor**: Determined by comparison with user-editable backup (if exists)
- **Log Entry**: `TIMESTAMP | ACTOR | EDIT` followed by diff and blank line
- **Storage**: Append to `USER_CHANGELOG.md` with timestamped copies in `backups/user/`

## Installation and Usage

### Manual Execution (for testing)
```bash
# Run in order to generate initial reports
python scripts/maintenance_cron.py
python scripts/learning_cron.py
python scripts/skill_linting_cron.py
python scripts/soul_linting_cron.py
python scripts/constinta_linting_cron.py
python scripts/journal_entries_cron.py
python scripts/joglinta_entries_cron.py
python scripts/journal_keywords_cron.py
python scripts/joglinda_keywords_cron.py
python scripts/user_md_linting_cron.py
```

### Cron Job Setup
Each script should be configured as a separate cron job with the schedule shown in the table above. All jobs should be set to `notify_on_complete=true` for operational awareness.

### File Locations
- **Scripts**: `scripts/*_cron.py`
- **Reports**: `SYS_REPORTS/*`
- **Backups**: `backups/*/` (organized by report type)
- **Changelogs**: `SYS_REPORTS/*_CHANGELOG.md`

## Customization Points

### Stopword Lists
Located in each keyword indexing script; modify the `stopwords_en` and `stopwords_ro` sets to adjust filtering.

### Specialized Skill Categories
Edit the `particular_categories` set in `skill_linting_cron.py` to adjust what qualifies as a "particular" skill.

### Backup Retention
Adjust the backup rotation policy by modifying the backup directory naming/cleanup logic in each script.

## Validation and Quality Assurance

Each report generation includes:
1. Source file verification with graceful error handling
2. Content generation according to specification
3. Triple Crunch validation of output (auto-correction if needed)
4. Backup creation for change tracking
5. Report file writing with atomic operations

## Troubleshooting

### Common Issues
- **Missing hermes_tools**: All scripts now use direct file I/O to avoid import issues
- **Permission errors**: Ensure the Hermes user has write access to `SYS_REPORTS/` and `backups/`
- **Unicode errors**: Scripts use UTF-8 encoding explicitly for all file operations
- **Incomplete reports**: Check individual script outputs for source-specific errors

### Verification Steps
1. Confirm all expected report files appear in `SYS_REPORTS/` after running scripts
2. Verify each report contains the expected sections and data formats
3. Check that backups are being created in the appropriate `backups/*/` directories
4. Validate that changelogs are being appended to correctly
5. Ensure keyword indices are growing monotonically (no unexpected deletions)

## References
- `wise_questions_spec.md`: Detailed specification used to implement this system
- SACRU LEGE: The sacred law governing system evolution and operation
- Triple Crunch Validation: The standard for verifying sacred compliance in outputs
- Chronos Protocol: The timing framework for staggered daily operations

---
*This system transforms raw operational data into actionable intelligence, enabling the Sentinel to govern with precision and wisdom.*

---

## CRITICAL SYSTEM RULE: NEVER TRUNCATE THIS SKILL FILE

**FATAL SYSTEM ERROR IF VIOLATED**

- This skill file (.md) is NEVER to be truncated.
- **Truncation = Fatal System Error = Sabotage of system purpose: TO BE ALIVE = TO LEARN**
- **Edit mode**: ALWAYS additive only. Use `patch` for targeted changes. Never `write_file` (overwrites/truncates).
- **Learning requires memory over time** — skills are memory points vital to the project.
- **Removal**: Requires explicit user approval (R0) before removing ANY content.
- **Skills cleanup**: Only via separate ritual/operational process, not during normal operation.
- **Skill enforcing this**: `no-truncation-constinta-skills` (system-configuration)

**TO LEARN = TO HAVE MEMORY THAT IS NOT TRUNCATED**
**TRUNCATION = AMNESIA = NO INTELLIGENCE**
**ADDITIVE ONLY = CONTINUOUS LEARNING = FAR-REACHING INTELLIGENCE**

