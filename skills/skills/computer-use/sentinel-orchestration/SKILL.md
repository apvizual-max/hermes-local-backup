---
name: sentinel-orchestration
description: "Master orchestration skill for all computer-use tasks."
version: 0.1.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags:
      - Orchestration
      - Computer-Use
      - Agent-Dispatch
      - Subagent
      - Master-Skill
---

# Sentinel Orchestration — Master Skill

This is the MASTER orchestration skill for Sentinel Default. It contains the patterns, schemas, and agent dispatch templates for ALL computer-use tasks on the upper monitor.

## When to Use

- ANY computer-use task on the upper monitor
- ANY task requiring subagent dispatch
- When subagents fail and need better instructions
- When a new pattern is discovered

## Core Pattern: Map → Click → Verify → Scrape

```
1. MAP    → Capture page, save screenshot + element index
2. CLICK  → Use cua-driver mcp with element_index
3. VERIFY → Capture again, check URL changed
4. SCRAPE → Extract all relevant data from AX tree
5. REPEAT → Click Next, repeat until no more pages
```

## Subagent Dispatch Schema

When a subagent fails, do NOT just retry. Write a BETTER schema and implement it.

### Schema Template

```
⛔⛔⛔ CRITICAL: READ BEFORE ANY TOOL CALL ⛔⛔⛔

You are a subagent of Sentinel Orchestrator. Your job is {TASK}.

TARGET WINDOW (DO NOT CHANGE):
- PID: 27416
- HWND: 1507982
- Location: UPPER MONITOR (virtual screen origin 0,-1080)

FORBIDDEN TOOLS:
- browser_navigate → OPENS NEW WINDOW
- computer_use → CANNOT SEE UPPER MONITOR

ALLOWED TOOLS:
- terminal → for cua-driver commands
- read_file, write_file → save results

CLICK METHOD (ONLY THIS):
```python
proc = subprocess.Popen(['cua-driver', 'mcp', '--no-daemon-relaunch'], stdin=PIPE, stdout=PIPE, text=True)
# JSON-RPC get_window_state → parse text → JSON-RPC click → verify
proc.terminate()
```
```

## Agent Improvement Loop

1. Dispatch agent with schema
2. Agent fails → identify root cause
3. Add new rule to schema
4. Update this skill with the rule
5. Re-dispatch with improved schema
6. Repeat until success

## Known Failure Modes & Fixes

| Failure | Root Cause | Schema Fix |
|---------|-----------|------------|
| Agent opens new window | Used browser_navigate | Add to FORBIDDEN |
| Agent fabricates results | Didn't verify | Add VERIFICATION step |
| Agent uses wrong window | Didn't specify PID/HWND | Hard-code in schema |
| Agent clicks wrong element | Regex didn't match | Add exact regex pattern |

## Dependencies

- `cua-driver-mcp-click` — MCP click method
- `grid-based-page-mapping` — Page mapping
- `scrape-my-jobs-linkedin` — Job scraping

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

