---
name: cua-driver-mcp-click
description: "Click on any monitor using persistent MCP sessions."
version: 0.2.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags:
      - Computer-Use
      - cua-driver
      - MCP
      - Multi-Monitor
      - Click
---

# cua-driver MCP Click — Persistent Session Clicking

Use `cua-driver mcp --no-daemon-relaunch` with JSON-RPC piping to chain `get_window_state` + `click` in a **single persistent session**. This eliminates the element cache expiry problem.

## Why `cua-driver mcp` beats `cua-driver call`

| Method | Session | Cache | Cross-GPU |
|--------|---------|-------|-----------|
| `cua-driver call` | One-shot per invocation | ❌ Dies between calls | ❌ |
| `cua-driver mcp` | Persistent stdin/stdout | ✅ Survives across requests | ✅ |

## When to Use

- Any click on the upper/secondary monitor
- When `cua-driver call click` returns "Element N not in cache"
- Multi-monitor setups where `computer_use` wrapper returns 0x0 captures
- Cross-GPU clicking (different graphics cards)

## How to Run

### Quick: Use the bundled script

```bash
python scripts/click_mcp.py 27416 1507982 "Job tracker"
```

### Manual: Python inline

```python
import subprocess, json, time, re, base64

PID = 27416
HWND = 1507982

# Start persistent MCP session
proc = subprocess.Popen(
    ['cua-driver', 'mcp', '--no-daemon-relaunch'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True
)

# Step 1: Get window state (JSON-RPC)
req = json.dumps({
    "jsonrpc": "2.0", "id": 1, "method": "tools/call",
    "params": {"name": "get_window_state", "arguments": {"pid": PID, "window_id": HWND, "max_elements": 300}}
}) + "\n"
proc.stdin.write(req)
proc.stdin.flush()
time.sleep(2)
line = proc.stdout.readline()
resp = json.loads(line)

# Step 2: Parse TEXT response to find element index
# MCP returns text, not JSON! Parse with regex:
text = resp['result']['content'][0]['text']
# Format: [N] Role "Label"
match = re.search(r'\[(\d+)\]\s+\w+\s+"Job tracker"', text)
element_idx = int(match.group(1))

# Step 3: Click by element_index (same session — cache alive!)
req = json.dumps({
    "jsonrpc": "2.0", "id": 2, "method": "tools/call",
    "params": {"name": "click", "arguments": {"pid": PID, "window_id": HWND, "element_index": element_idx, "delivery_mode": "background"}}
}) + "\n"
proc.stdin.write(req)
proc.stdin.flush()
time.sleep(1)
line = proc.stdout.readline()
resp = json.loads(line)

# Step 4: Verify
req = json.dumps({
    "jsonrpc": "2.0", "id": 3, "method": "tools/call",
    "params": {"name": "get_window_state", "arguments": {"pid": PID, "window_id": HWND, "max_elements": 10}}
}) + "\n"
proc.stdin.write(req)
proc.stdin.flush()
time.sleep(1)
line = proc.stdout.readline()
resp = json.loads(line)
text = resp['result']['content'][0]['text']
url_match = re.search(r'value="([^"]+)"', text)
print(f"URL after click: {url_match.group(1) if url_match else 'unknown'}")

proc.terminate()
```

## Critical Details

### MCP Response Format
`get_window_state` via MCP returns **text**, not JSON:
```
window_id=1507982 pid=27416 elements=122

- Window "LinkedIn | Feed"
  - [0] Button [id=view_5 actions=[expand]]
  - [5] Edit "Address and search bar" [value="linkedin.com/jobs/"]
  - [35] Hyperlink "Job tracker"
```

Parse with regex: `r'\[(\d+)\]\s+\w+\s+"Label"'`

### URL Extraction
```python
url_match = re.search(r'value="([^"]+)"', text)
```

## Pitfalls

- MCP `get_window_state` returns TEXT, not JSON — use regex to parse
- Always `proc.terminate()` after use
- `delivery_mode: "background"` preferred — no focus steal
- Screenshot is in `content[1].data` as base64
- Element index is 0-based in text but 1-based in click command? Test both.

## Proven Results

- ✅ Clicked "Jobs" nav icon → navigated to `linkedin.com/jobs/`
- ✅ Clicked "Job tracker" → navigated to `linkedin.com/jobs-tracker/`
- ✅ Both on upper monitor (different GPU), background delivery, no focus steal

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

