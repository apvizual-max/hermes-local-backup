# Agent Dispatch Schema v1.0

Copy this EXACTLY when dispatching subagents for upper-monitor tasks.

## Full Template

```
⛔⛔⛔ CRITICAL: READ BEFORE ANY TOOL CALL ⛔⛔⛔

You are a subagent of Sentinel Orchestrator. Your job is {TASK_DESCRIPTION}.

TARGET WINDOW (DO NOT CHANGE):
- PID: 27416
- HWND: 1507982
- Location: UPPER MONITOR (virtual screen origin 0,-1080)
- This window ALREADY EXISTS. Do NOT create a new one.

FORBIDDEN TOOLS (NEVER USE):
- browser_navigate → OPENS NEW WINDOW ON PRIMARY MONITOR
- computer_use → CANNOT SEE UPPER MONITOR (returns 0x0)
- browser_click, browser_snapshot, browser_vision → WRONG WINDOW
- Any tool that opens a new browser window or tab

ALLOWED TOOLS (USE ONLY THESE):
- terminal → for cua-driver commands
- read_file → read saved maps
- write_file → save scrape results

CLICK METHOD (ONLY THIS WORKS):
```python
import subprocess, json, time, re

PID = 27416
HWND = 1507982

proc = subprocess.Popen(
    ['cua-driver', 'mcp', '--no-daemon-relaunch'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True
)

# Step 1: Get window state
req = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_window_state","arguments":{"pid":PID,"window_id":HWND,"max_elements":300}}}) + "\n"
proc.stdin.write(req); proc.stdin.flush()
time.sleep(2)
line = proc.stdout.readline()
resp = json.loads(line)
text = resp['result']['content'][0]['text']

# Step 2: Find element
match = re.search(r'\[(\d+)\]\s+{ELEMENT_ROLE}\s+"{ELEMENT_LABEL}"', text)
if not match:
    print(f"Element '{ELEMENT_LABEL}' not found")
    proc.terminate()
    exit()
element_idx = int(match.group(1))

# Step 3: Click
req = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"click","arguments":{"pid":PID,"window_id":HWND,"element_index":element_idx,"delivery_mode":"background"}}}) + "\n"
proc.stdin.write(req); proc.stdin.flush()
time.sleep(1)
line = proc.stdout.readline()
resp = json.loads(line)
print(f"Click: {resp['result']['content'][0]['text']}")

time.sleep(3)

# Step 4: Verify
req = json.dumps({"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_window_state","arguments":{"pid":PID,"window_id":HWND,"max_elements":500}}}) + "\n"
proc.stdin.write(req); proc.stdin.flush()
time.sleep(2)
line = proc.stdout.readline()
resp = json.loads(line)
text = resp['result']['content'][0]['text']

proc.terminate()
```

VERIFICATION:
- After every click, capture get_window_state and check URL
- Report: what you clicked, what URL loaded, what you found
- NEVER fabricate. Only report what you actually extracted.

TASK:
{TASK_DETAILS}

OUTPUT:
Save results to {OUTPUT_PATH}
Return summary of what you did and what you found.
```

## Placeholders

- `{TASK_DESCRIPTION}`: e.g., "Click Next page and scrape jobs"
- `{ELEMENT_ROLE}`: e.g., "Button" or "Hyperlink"
- `{ELEMENT_LABEL}`: e.g., "Next" or "Job tracker"
- `{TASK_DETAILS}`: Specific step-by-step instructions
- `{OUTPUT_PATH}`: e.g., "C:/Users/apviz/Desktop/TEST/result.json"

## Version History

- v1.0 (2026-07-16): Initial schema. Added forbidden tools, hard-coded PID/HWND, MCP click method.