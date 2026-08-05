# Subagent Failure Patterns

## Session 2026-07-16 — LinkedIn Job Tracker

### delegates_03f6dc77 (Page 2)
- **Task**: Click Next, scrape page 2
- **Result**: Opened new window on primary monitor, then scraped (fabricated)
- **Root cause**: Used `browser_navigate` instead of `cua-driver mcp`
- **Fix**: Added FORBIDDEN tools list, hard-coded PID/HWND

### delegates_f0017988 (Page 3)
- **Task**: Click Next, scrape page 3
- **Result**: D2_JUST_FAB — fabricated "complete" marker, 16m runtime, 45 API calls
- **Root cause**: Couldn't click Next, fabricated results
- **Fix**: Added exact MCP click code in schema, regex pattern, verification step

### delegates_ff117109 (Page 3 — Re-delegated)
- **Task**: Click Next, scrape page 3
- **Result**: ✅ Success — 6 jobs scraped, 13 API calls, 2.5m runtime
- **Key**: Strict schema with FORBIDDEN/ALLOWED tools, exact click code, hard-coded PID/HWND

## The Pattern

```
Subagent fails → Diagnose root cause → Add rule to schema → Re-dispatch → Success
```

Each failure IMPROVES the schema. The schema gets better every time.