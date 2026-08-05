#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skills list cron job: enumerates skills, groups them by sys_/active/particular,
and writes a report to SYS_REPORTS/.
"""

import os
import datetime
from pathlib import Path

def main():
    base_dir = Path(r"C:\Users\apviz\AppData\Local\hermes")
    skills_dir = base_dir / "skills"
    reports_dir = base_dir / "SYS_REPORTS"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    date_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Define specialized categories for 'particular' skills
    particular_categories = {
        "triple-crunch", "journal-index", "user-md", "keyword-index",
        "skill-lint", "soul-lint", "constinta-lint", "maintenance", "learning"
    }

    sys_skills = []   # always_on: true
    active_skills = [] # active but not always_on
    particular_skills = [] # subset of active with specific category
    archived = []     # archived or status: archived/deprecated

    if skills_dir.is_dir():
        for skill_folder in skills_dir.iterdir():
            if not skill_folder.is_dir():
                continue
            skill_md = skill_folder / "SKILL.md"
            if not skill_md.is_file():
                continue
            try:
                content = skill_md.read_text(encoding="utf-8")
                # Parse frontmatter (simple: between --- lines)
                frontmatter = {}
                if content.startswith("--"):
                    end = content.find("\n--", 3)
                    if end != -1:
                        fm_text = content[3:end].strip()
                        for line in fm_text.splitlines():
                            if ':' in line:
                                key, val = line.split(':', 1)
                                frontmatter[key.strip()] = val.strip()
                # Determine status
                status = frontmatter.get('status', '').lower()
                if status in ('archived', 'deprecated'):
                    archived.append(skill_folder.name)
                    continue
                # Check always_on
                always_on = frontmatter.get('always_on', '').lower()
                if always_on == 'true':
                    sys_skills.append(skill_folder.name)
                else:
                    active_skills.append(skill_folder.name)
                    # Check category for particular
                    cat = frontmatter.get('category', '').lower()
                    if cat in particular_categories:
                        particular_skills.append(skill_folder.name)
            except Exception as e:
                # If we cannot parse, treat as active? but we'll skip for safety.
                pass

    # Sort lists for consistent output
    sys_skills.sort()
    active_skills.sort()
    particular_skills.sort()
    archived.sort()

    # Build report
    report_lines = []
    report_lines.append(f"SKILLS LIST REPORT - {date_time_str}")
    report_lines.append("=" * 60)
    report_lines.append("SYS_SKILLS (ALWAYS_ON)")
    report_lines.append("-" * 60)
    if sys_skills:
        for s in sys_skills:
            report_lines.append(s)
    else:
        report_lines.append("(none)")
    report_lines.append("")
    report_lines.append("ACTIVE")
    report_lines.append("-" * 60)
    if active_skills:
        for s in active_skills:
            report_lines.append(s)
    else:
        report_lines.append("(none)")
    report_lines.append("")
    report_lines.append("PARTICULAR")
    report_lines.append("-" * 60)
    if particular_skills:
        for s in particular_skills:
            report_lines.append(s)
    else:
        report_lines.append("(none)")
    report_lines.append("")
    report_lines.append("ARCHIVED / OUT OF USE")
    report_lines.append("-" * 60)
    if archived:
        for s in archived:
            report_lines.append(s)
    else:
        report_lines.append("(none)")
    report_lines.append("")
    report_lines.append("=" * 60)
    report_lines.append("END OF REPORT")

    report_path = reports_dir / f"skill_linting_{timestamp}.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"Skill linting report saved to {report_path}")

if __name__ == "__main__":
    main()