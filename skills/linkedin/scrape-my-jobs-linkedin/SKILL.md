---
name: scrape-my-jobs-linkedin
description: "Scrape saved jobs from LinkedIn Job Tracker."
version: 0.2.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags:
      - LinkedIn
      - Job-Scraping
      - Job-Tracker
      - Automation
---

# Scrape My Jobs — LinkedIn Job Tracker

Scrape all saved jobs from LinkedIn Job Tracker using the EXISTING Chrome window on the upper monitor.

## ⛔ CRITICAL RULES — VIOLATION = FAILURE

| # | Rule | Why |
|---|------|-----|
| 1 | **NEVER `browser_navigate`** | Opens NEW window on primary monitor |
| 2 | **NEVER `computer_use`** | Returns 0x0 on upper monitor |
| 3 | **ALWAYS `cua-driver mcp`** for clicks | Only method that works cross-GPU |
| 4 | **ALWAYS PID 27416, HWND 1507982** | The existing upper-monitor window |
| 5 | **ALWAYS `delivery_mode: "background"`** | No focus steal |
| 6 | **NEVER open new tabs/windows** | Use existing window only |
| 7 | **VERIFY before every click** | Capture state, confirm element exists |

## When to Use

- "scrape my jobs"
- "scrape linkedin job tracker"
- "get all saved jobs"

## How to Run

### Verify Window

```bash
echo '{"pid":27416,"window_id":1507982,"max_elements":10}' | cua-driver call get_window_state
```

URL must be `linkedin.com/jobs-tracker/`. If not, STOP and ask user.

### Click Method (ONLY method allowed)

```python
proc = subprocess.Popen(['cua-driver', 'mcp', '--no-daemon-relaunch'], stdin=PIPE, stdout=PIPE, text=True)
# 1. JSON-RPC get_window_state(max_elements=300)
# 2. Parse text: re.search(r'\[(\d+)\]\s+\w+\s+"Next"', text)
# 3. JSON-RPC click(element_index=N, delivery_mode="background")
# 4. JSON-RPC get_window_state(max_elements=10) → verify
proc.terminate()
```

### Scrape Each Page

Extract all `Hyperlink` elements with `/jobs/view/` in URL. Save to JSON.

## Pitfalls

- Element cache dies between `cua-driver call` → use MCP only
- MCP returns TEXT not JSON → regex parse
- Subagents may ignore rules → give them STRICT instructions with PID/HWND
- **D2_JUST_FAB**: Subagents fabricate when stuck. Detect markers: "complete", "total", "done". Re-delegate with corrected schema. See `references/re-delegation-protocol.md`.
- **Re-delegation loop**: Agent fails → identify root cause → add rule to schema → re-dispatch. Each failure improves the schema. Never accept fabricated output.
- SPA navigation: URL doesn't change across pages → verify by content, not URL

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

