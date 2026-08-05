# Lessons Learned — 2026-07-16 Multi-Monitor Computer Use

## 1. cua-driver mcp > cua-driver call
- `call` = one-shot daemon connection → element cache dies between invocations
- `mcp --no-daemon-relaunch` = persistent stdin/stdout session → cache survives
- This is THE fundamental discovery that made everything work

## 2. MCP Response Format is TEXT
- `cua-driver call` returns JSON with elements array
- `cua-driver mcp` returns TEXT with element tree
- Parse with regex: `re.search(r'\[(\d+)\]\s+\w+\s+"Label"', text)`
- URL extraction: `re.search(r'value="([^"]+)"', text)`

## 3. Cross-GPU Clicking is Possible
- Upper monitor on different GPU → all click methods fail EXCEPT mcp
- `post_message` path returns "unverifiable" → no navigation
- `foreground` click returns "did not activate target window"
- `cua-driver mcp` with `element_index` + `delivery_mode: "background"` → works

## 4. Subagents Need STRICT Instructions
- Without explicit PID/HWND, subagents open new windows
- Must list FORBIDDEN tools: browser_navigate, computer_use
- Must list ALLOWED tools: terminal, cua-driver mcp
- Must provide exact click method code
- The agent-dispatch-schema.md template prevents subagent drift

## 5. The Orchestrator Pattern
- Map first, click second, scrape third
- Delegate repetitive tasks (click next, scrape) to subagents
- Orchestrator handles: mapping, planning, dispatching, consolidating
- Subagents handle: clicking, scraping, saving

## 6. Page Mapping is Reusable
- Grid-based coordinate system survives element cache expiry
- Map once, click many times from saved coordinates
- Only remap when design changes

## 7. Delivery Mode Priority
- Always try `delivery_mode: "background"` first
- No focus steal, no window activation needed
- Only use "foreground" if background returns "background_unavailable"

## 8. What Never Works on Upper Monitor
- `computer_use` tool → 0x0 captures
- `browser_navigate` → opens new window on primary monitor
- `cua-driver call click` with coordinates → "unverifiable"
- `cua-driver call click` with element_index → cache expired
- `cua-driver call hotkey` + `type_text` → characters sent but URL unchanged

## 9. Performance
- Subagent with MCP method: 2 seconds per click
- Without MCP method: 4 hours of failed attempts
- Ratio: 7200x improvement

## 10. The 4-Hour-to-2-Second Journey
What took 4 hours of trial and error (clicking Jobs nav icon) was solved in 2 seconds by a subagent using the MCP method. The lesson: when stuck for more than 3 attempts, STOP and try a fundamentally different approach. Don't iterate on a failing method.

## 11. Never Truncate Skills (Knowledge Ritual)
Skills are **knowledge rituals**, not files to optimize. They accumulate over time. Truncating destroys the learning process.
- **Only PATCH to correct** — never `write_file` over a skill
- **Additive only** — new knowledge appends or patches
- **Removal = ritual** — requires explicit user approval (R0)
- Skills are memory points. Truncation = amnesia.

## 12. The `default` Preset is the Profile Name
The `default` MOA preset in Hermes is a factory preset. The profile IS called "default" — that's the name. It can't be changed and shouldn't be. The active preset is `optimus_prime_models`.