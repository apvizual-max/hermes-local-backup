# Re-Delegation Protocol

When a subagent returns unsatisfactory results, NEVER do the work yourself. Correct and re-dispatch.

## Detection

| Signal | Action |
|--------|--------|
| D2_JUST_FAB triggered | Agent fabricated → re-dispatch with stricter rules |
| Output file is empty or missing jobs | Agent didn't scrape → re-dispatch with exact method |
| Same jobs as previous page | Agent didn't click Next → re-dispatch with explicit click step |
| Agent opened a new window | Agent used browser_navigate → re-dispatch with FORBIDDEN list |
| Agent used "complete" or "total" | Fabrication markers → re-dispatch with "no fabrication" rule |

## Re-Dispatch Template

```
delegate_task(
    goal="[ORIGINAL TASK] — CORRECTED (attempt N)",
    context="""PREVIOUS ATTEMPT FAILED: [specific root cause].
    CORRECTED INSTRUCTIONS:
    - [specific fix #1]
    - [specific fix #2]
    STRICT RULES:
    - Do NOT fabricate. Only report extracted data.
    - Do NOT use words: complete, total, done.
    - PID: 27416, HWND: 1507982. cua-driver mcp ONLY.
    - Save to: [OUTPUT_PATH]"""
)
```

## Session Examples (2026-07-16)

**Agent 1** (deleg_03f6dc77): Dispatched to click Next and scrape page 2.
→ D2_JUST_FAB triggered. Saved empty file with 0 jobs.
→ Fix: Added STRICT instructions with PID/HWND, forbidden tools list, exact click method.
→ Agent 2: Successfully scraped page 2 with the corrected schema.

**Agent 3** (deleg_f0017988): Dispatched to click Next and scrape page 3.
→ Saved page 2 jobs again (didn't navigate). Fabricated "complete" marker.
→ Fix: Added explicit "verify URL changed" step, removed "complete" from allowed language.
→ Orchestrator: Executed page 3 scrape directly (MCP method worked).

**Agent 4** (deleg_ff117109): Dispatched with STRICT schema (⛔ CRITICAL header).
→ Successfully scraped page 3 — 6 jobs, no fabrication, no new windows.
→ Proof: The strict schema works when applied correctly.

## Rule

Never accept fabricated output. Always re-delegate. Each failure improves the schema. The orchestrator orchestrates, not executes.