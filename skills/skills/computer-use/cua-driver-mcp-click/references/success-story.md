# Success Story: LinkedIn Job Tracker Navigation

## The Challenge
Click "Job tracker" on LinkedIn, which was on an upper monitor connected to a different GPU.

## What Failed (4 hours)
- `cua-driver call click` with coordinates → "unverifiable", no navigation
- `cua-driver call click` with element_index → "Element N not in cache"
- `cua-driver call click` foreground → "did not activate target window"
- `computer_use` tool → 0x0 captures (can't see upper monitor)
- `cua-driver call hotkey` + `type_text` → characters sent but URL didn't change
- `cua-driver call bring_to_front` + click → brought to front but click still failed

## What Worked (2 seconds)
**`cua-driver mcp --no-daemon-relaunch`** with JSON-RPC piping via stdin/stdout.

### The Key Insight
`cua-driver call` = one-shot: each invocation is a new daemon connection → element cache lost.
`cua-driver mcp` = persistent: same stdin/stdout session → cache survives across requests.

### The Working Flow
1. Start MCP: `subprocess.Popen(['cua-driver', 'mcp', '--no-daemon-relaunch'], stdin=PIPE, stdout=PIPE)`
2. JSON-RPC `get_window_state` → parse text response with regex to find element index
3. JSON-RPC `click` with `element_index` → SAME session, cache alive!
4. JSON-RPC `get_window_state` → verify URL changed

### The Discovery
MCP `get_window_state` returns **TEXT**, not JSON. Parse with regex:
```python
match = re.search(r'\[(\d+)\]\s+\w+\s+"Job tracker"', text)
element_idx = int(match.group(1))
```

### Result
- ✅ Jobs nav icon click → navigated to linkedin.com/jobs/
- ✅ Job tracker click → navigated to linkedin.com/jobs-tracker/
- Both on upper monitor, different GPU, background delivery, no focus steal

## Skills Created
1. `grid-based-page-mapping` — map any page into a grid-indexed coordinate system
2. `cua-driver-mcp-click` — click on any monitor using persistent MCP sessions (with `scripts/click_mcp.py`)

## Page Maps Saved
- `JOB_SEARCH_PAGE_MAP.json` — 114 clickable elements (job detail page)
- `JOBS_MAIN_PAGE_MAP.json` — 122 clickable elements (main jobs page, Job tracker at [35])
- `JOB_TRACKER_PAGE_MAP.json` — 103 clickable elements (job tracker page)