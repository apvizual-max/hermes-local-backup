#!/usr/bin/env python3
"""Optimus Prime — periodic backup of sacred/operational files.
Copies core files + profile SOUL/CONSTINTA + the optimus-prime-sentinel skills
into backups/<timestamp>/. Keeps only the newest 14 backups (prunes older).
Prints a one-line confirmation (cron delivers it) or an error on failure.
"""
import os, shutil, datetime, sys

H = os.path.expanduser(r"~/AppData/Local/hermes")
if not os.path.isdir(H):
    H = r"C:\Users\apviz\AppData\Local\hermes"

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bdir = os.path.join(H, "backups", ts)
os.makedirs(bdir, exist_ok=True)

core = ["SOUL.md", "CONSTINTA.md", "SACRED_DEFINITIONS.md",
        "JURNAL_OGLINDA.md", "SENTINEL_JOURNAL.md", "SESSION_REPORT.md",
        "SYSTEM_STATUS.md"]
copied = 0
for f in core:
    src = os.path.join(H, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(bdir, f)); copied += 1

# profile SOUL + CONSTINTA
for prof in ["default", "prime", "assist"]:
    pdir = os.path.join(H, "profiles", prof)
    if os.path.isdir(pdir):
        dst = os.path.join(bdir, "profiles", prof); os.makedirs(dst, exist_ok=True)
        for f in ["SOUL.md", "CONSTINTA.md"]:
            s = os.path.join(pdir, f)
            if os.path.exists(s):
                shutil.copy2(s, os.path.join(dst, f)); copied += 1

# skills tree
sk = os.path.join(H, "skills", "optimus-prime-sentinel")
if os.path.isdir(sk):
    shutil.copytree(sk, os.path.join(bdir, "skills-optimus-prime-sentinel"),
                    dirs_exist_ok=True)

# prune: keep newest 14
broot = os.path.join(H, "backups")
snaps = sorted([d for d in os.listdir(broot)
                if os.path.isdir(os.path.join(broot, d))])
for old in snaps[:-14]:
    shutil.rmtree(os.path.join(broot, old), ignore_errors=True)

print(f"[BACKUP OK] {ts} — {copied} files -> backups/{ts} (kept newest 14)")
