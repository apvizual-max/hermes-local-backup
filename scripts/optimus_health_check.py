#!/usr/bin/env python3
"""Optimus Prime — daily system health check (watchdog).
Silent (empty stdout) when everything is nominal; prints a report only when
something is WRONG, so a no_agent cron job stays quiet unless action is needed.
Also always appends a heartbeat line to the health log.
"""
import os, datetime, sys

H = os.path.expanduser(r"~/AppData/Local/hermes")
# On the cron host the path may resolve differently; fall back to absolute.
if not os.path.isdir(H):
    H = r"C:\Users\apviz\AppData\Local\hermes"

problems = []

def exists(p):
    return os.path.exists(os.path.join(H, p))

# 1. Core files present
core = ["SOUL.md", "CONSTINTA.md", "SACRED_DEFINITIONS.md",
        "JURNAL_OGLINDA.md", "SENTINEL_JOURNAL.md"]
for f in core:
    if not exists(f):
        problems.append(f"MISSING core file: {f}")

# 2. Journal size — recommend V2 if > 60KB
jp = os.path.join(H, "SENTINEL_JOURNAL.md")
if os.path.exists(jp):
    sz = os.path.getsize(jp)
    if sz > 60000:
        problems.append(f"SENTINEL_JOURNAL.md is {sz} bytes (>60KB) — trigger journal-versioning V2.")

# 3. Profile SOULs point to the C: journal (no stale E: pointer)
for prof in ["prime", "assist"]:
    sp = os.path.join(H, "profiles", prof, "SOUL.md")
    if os.path.exists(sp):
        txt = open(sp, encoding="utf-8", errors="ignore").read()
        if "E:\\CLAUDE" in txt and "SENTINEL_JOURNAL" in txt:
            problems.append(f"profiles/{prof}/SOUL.md has stale E: journal pointer.")
    else:
        problems.append(f"MISSING profiles/{prof}/SOUL.md")

# 4. Stale E: OGLINDA references anywhere in the *.md core files
for f in core + ["SESSION_REPORT.md"]:
    p = os.path.join(H, f)
    if os.path.exists(p):
        if "E:\\CLAUDE\\OGLINDA" in open(p, encoding="utf-8", errors="ignore").read():
            problems.append(f"{f} still contains stale E:\\CLAUDE\\OGLINDA reference.")

# 5. RESTRICT boundary marker (D: personal) — informational only
# (we never read into it; just confirm we are not accidentally indexing it)

# Heartbeat log (always)
logdir = os.path.join(H, "logs")
os.makedirs(logdir, exist_ok=True)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
status = "NOMINAL" if not problems else f"{len(problems)} ISSUE(S)"
with open(os.path.join(logdir, "health_check.log"), "a", encoding="utf-8") as fh:
    fh.write(f"[{now}] health_check {status}\n")

# Only emit to stdout (=> cron alert) when there are problems.
if problems:
    print(f"=== OPTIMUS PRIME HEALTH ALERT {now} ===")
    for p in problems:
        print(" - " + p)
    sys.exit(0)
# else: silent
