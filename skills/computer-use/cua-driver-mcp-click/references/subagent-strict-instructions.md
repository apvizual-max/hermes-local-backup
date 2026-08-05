# Subagent Instructions — STRICT

When delegating to a subagent for clicking/scraping on the upper monitor, ALWAYS include these exact instructions:

```
⛔ CRITICAL: You are working on the EXISTING Chrome window on the UPPER MONITOR.
- PID: 27416
- HWND: 1507982
- Virtual screen origin: (0, -1080)

NEVER:
- Use browser_navigate (opens new window on primary monitor)
- Use computer_use (can't see upper monitor, returns 0x0)
- Open a new Chrome window or tab
- Use any tool other than cua-driver mcp for clicking

ALWAYS:
- Use cua-driver mcp --no-daemon-relaunch with JSON-RPC piping
- delivery_mode: "background" (no focus steal)
- Target the existing PID 27416, HWND 1507982
- Verify URL after every click
```

## Lesson Learned (2026-07-16)

Subagent `deleg_03f6dc77` was tasked with clicking "Next" on LinkedIn Job Tracker. It successfully scraped page 2 but opened a NEW window on the primary monitor, violating the user's setup.

Root cause: The subagent context didn't include strict enough instructions about NEVER opening new windows. The subagent defaulted to `browser_navigate` or `computer_use` which opened a new window.

Fix: All future subagent delegations for upper-monitor tasks MUST include the STRICT instructions above.