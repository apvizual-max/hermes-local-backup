---
name: cua-driver-multi-monitor-workaround
description: Access and control windows on secondary monitors (above/below main display) using cua-driver CLI when the Hermes computer_use wrapper only captures the primary display. Includes window enumeration, AX tree reading, background clicking, and screenshot capture.
triggers:
  - multi monitor
  - second screen
  - upper monitor
  - computer use empty capture
  - cua driver
  - linkedin PWA
  - offscreen window
---

# cua-driver Multi-Monitor Workaround

## Problem
The Hermes `computer_use` wrapper captures only the primary display. Windows on secondary monitors (stacked above/below, or side-by-side on a second output) return empty captures: `width: 0, height: 0, elements: []`.

## Root Cause
- `cua-driver` CLI supports all monitors (virtual screen spans the full desktop).
- The Hermes `computer_use` wrapper uses `capture_scope: "window"` by default, which only resolves foreground windows on the primary display.
- Chrome/PWA windows on secondary monitors are invisible to the wrapper.

## Solution: Use cua-driver CLI Directly

### Step 1: Find the Window

```python
import ctypes
from ctypes import wintypes
import json

user32 = ctypes.windll.user32
WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

def find_window(title_contains):
    results = []
    def callback(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                if title_contains.lower() in buf.value.lower():
                    rect = wintypes.RECT()
                    user32.GetWindowRect(hwnd, ctypes.byref(rect))
                    pid = wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    results.append({
                        'hwnd': hex(hwnd),
                        'hwnd_int': hwnd,
                        'pid': pid.value,
                        'title': buf.value,
                        'x': rect.left, 'y': rect.top,
                        'w': rect.right - rect.left,
                        'h': rect.bottom - rect.top
                    })
        return True
    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return results
```

### Step 2: Get Accessibility Tree (AX Elements)

```bash
echo '{"pid":<PID>,"window_id":<HWND_INT>,"max_elements":200}' | cua-driver call get_window_state
```

Parse the JSON output:
- `element_count`: total interactive elements
- `elements[]`: array with `element_index`, `role`, `label`, `value`, `frame` (x, y, w, h)
- `screenshot_png_b64`: base64-encoded PNG of the window

### Step 3: Click an Element (Background Mode)

```bash
echo '{"pid":<PID>,"window_id":<HWND_INT>,"element_index":<IDX>,"delivery_mode":"background"}' | cua-driver call click
```

- `delivery_mode: "background"` — no focus steal, works on background/offscreen windows
- `delivery_mode: "foreground"` — only if background returns `background_unavailable`

### Step 4: Type Text

```bash
echo '{"pid":<PID>,"window_id":<HWND_INT>,"text":"hello world"}' | cua-driver call type_text
```

### Step 5: Press Keys

```bash
echo '{"pid":<PID>,"window_id":<HWND_INT>,"keys":"enter"}' | cua-driver call press_key
```

### Step 6: Capture Screenshot

```bash
echo '{"pid":<PID>,"window_id":<HWND_INT>,"max_elements":5}' | cua-driver call get_window_state
```

Then extract `screenshot_png_b64` and decode to PNG file.

## Available cua-driver Tools

```
bring_to_front, click, double_click, right_click, drag, scroll,
get_window_state, get_desktop_state, get_accessibility_tree,
type_text, press_key, hotkey, set_value, page,
launch_app, kill_app, list_windows,
move_cursor, zoom, start_session, end_session,
set_config, get_config, health_report, debug_window_info
```

## Config Settings (Persistent)

```bash
echo '{"capture_scope":"desktop","capture_mode":"som"}' | cua-driver call set_config
```

| Setting | Value | Purpose |
|---------|-------|---------|
| `capture_scope` | `"desktop"` | Capture any window on any monitor |
| `capture_mode` | `"som"` | Screenshots + numbered elements (not just AX tree) |
| `agent_cursor` | `true` | Show the agent cursor on screen |

## Virtual Screen Geometry

The virtual screen spans ALL monitors:
- Origin: `(0, -1080)` (upper monitor starts at Y=-1080)
- Size: `3072 x 2808` (total virtual desktop)
- Monitor 2 (upper): Y range `-1080` to `0`
- Monitor 1 (main): Y range `0` to `1728`

## Page Map Reuse Rule (CRITICAL)
When revisiting a LinkedIn page that has **already been mapped**, do NOT re-capture the AX tree. Use the local page map files as the source of truth:
- Page maps are stored as JSON + MD + PNG in the user's designated folder.
- Use **coordinate-based clicking** (x,y center of element frame from the saved map) instead of `element_index` (which requires a fresh cache).
- LinkedIn layout is stable — maps remain valid across sessions.
- Only re-capture if: (a) the page is NOT yet mapped, (b) LinkedIn pushed a layout update, or (c) the user explicitly requests a re-map.
- This eliminates the cua-driver cache expiry problem entirely.

### Coordinate Click from Map
```python
# From saved map: element [36] "Job tracker" @ (1342, -603) 311x48
center_x = 1342 + 311 // 2  # = 1497
center_y = -603 + 48 // 2   # = -579
echo '{"pid":27416,"window_id":1507982,"x":1497,"y":-579,"delivery_mode":"background"}' | cua-driver call click
```

## Known Issues & Solutions

| Issue | Cause | Fix |
|-------|-------|-----|
| Empty capture (0x0) | Wrapper uses `capture_scope: "window"` | Use CLI directly |
| `hwnd not valid` | Window moved/destroyed | Re-enumerate with `find_window()` |
| `landed_on_target: false` | `bring_to_front` on offscreen window | Use background clicks instead |
| AX tree degraded | Chromium not settled | Wait 2-3s, retry `get_window_state` |
| No screenshot in output | `max_elements` too high | Lower to 5, extract `screenshot_png_b64` |

## Cursor-Verification Workflow (MANDATORY — DO NOT SKIP)

> **Full reference**: `references/cursor-verification-workflow.md` — includes the session-2026-07-15 failure analysis, the `vision_analyze` trap, and working keyboard patterns.

**Every click on a multi-monitor window MUST follow this sequence. Skipping any step leads to blind clicks and user frustration.**

### Step 1: Move cursor to target
```bash
echo '{"pid":<PID>,"window_id":<HWND>,"x":<CENTER_X>,"y":<CENTER_Y>}' | cua-driver call move_cursor
```

### Step 2: Screenshot to show cursor position
```bash
echo '{"pid":<PID>,"window_id":<HWND>,"max_elements":5}' | cua-driver call get_window_state
# Extract screenshot_png_b64, decode, save to disk
```

### Step 3: Show the user the picture
**Use MEDIA: path, NOT `vision_analyze` text descriptions.** The user needs to SEE the cursor on the screenshot, not read about it.
```
MEDIA:C:/Users/apviz/Desktop/TEST/cursor_at_target.png
```

### Step 4: Verify cursor is on target
Ask: "Is the cursor on the right element?" If not, recalculate and repeat Steps 1-3.

### Step 5: Click
```bash
echo '{"pid":<PID>,"window_id":<HWND>,"x":<X>,"y":<Y>,"delivery_mode":"background"}' | cua-driver call click
```

### Step 6: Screenshot after click to verify result
```bash
echo '{"pid":<PID>,"window_id":<HWND>,"max_elements":5}' | cua-driver call get_window_state
# Show MEDIA: path to user with the result
```

## Single-Process Element-Index Click (Cache-Safe Fallback)

When coordinate-based clicks from saved maps fail, chain `get_window_state` and `click` in ONE `cua-driver mcp` process by piping JSON-RPC requests to stdin. This is the ONLY way to keep the element cache alive across multiple commands.

### ⚠️ DO NOT use `cua-driver call` or `subprocess.run` — each invocation is a separate process and the cache dies.

```bash
# Pipe TWO JSON-RPC messages to cua-driver mcp stdin in one command
# The MCP daemon keeps the session alive across both requests
echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_window_state","arguments":{"pid":27416,"window_id":1507982}},"id":1}
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"click","arguments":{"pid":27416,"window_id":1507982,"element_index":27}},"id":2}' | cua-driver mcp --no-daemon-relaunch
```

Each line is a complete JSON-RPC request. The MCP daemon processes them sequentially within the same session, so the element cache populated by `get_window_state` is still alive when `click` runs.

### Finding the element index from the response

The `get_window_state` response returns the full AX tree in `tree_markdown` format. The element index is shown in brackets, e.g. `[27] Hyperlink "Jobs"`. You can also parse the structured `elements` array for `element_index`.

### Alternative: Python wrapper with stdin

```python
import subprocess, json

PID, HWND = 27416, 1507982

requests = [
    {"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_window_state","arguments":{"pid":PID,"window_id":HWND}},"id":1},
    {"jsonrpc":"2.0","method":"tools/call","params":{"name":"click","arguments":{"pid":PID,"window_id":HWND,"element_index":27}},"id":2},
]

payload = "\n".join(json.dumps(r) for r in requests)
result = subprocess.run(
    ['cua-driver', 'mcp', '--no-daemon-relaunch'],
    input=payload, capture_output=True, text=True, timeout=30
)
# Parse each JSON-RPC response line
for line in result.stdout.strip().split('\n'):
    resp = json.loads(line)
    print(f"id={resp['id']}: {'error' if 'error' in resp else 'ok'}")
```

**Why this works**: The `cua-driver mcp` process is a long-lived daemon session. All JSON-RPC messages sent on stdin share the same session, so the element cache from `get_window_state` is still valid when `click` runs. This is fundamentally different from `cua-driver call` which spawns a new process per invocation.

**When**: Fallback after coordinate-based clicks fail. Cache-based clicking is more reliable when coordinates are unverifiable.

**Verified**: 2026-07-16 — `cua-driver call` (separate processes) fails with "Element 27 not in cache". `cua-driver mcp` (stdin piping) succeeds: "✅ Posted click on Chromium element [27]".

## ⛔ STOP AFTER 2 FAILED CLICKS ⛔

If two clicks fail to produce the expected navigation or result:
1. **STOP immediately.** Do NOT try a third variation of the same approach.
2. **Show the user the screenshot** of the current state.
3. **Ask the user** what to do differently or offer alternatives.
4. **Do NOT** loop through coordinate adjustments, delivery mode changes, or element index retries.
5. **Do NOT** escalate to the Hermes browser unless the user explicitly asks for it. The user's LinkedIn session is in their Chrome, not the Hermes browser.

## Show Images, Not Text Descriptions

- **DO**: `MEDIA:C:/path/to/screenshot.png` — the user sees the actual image.
- **DO NOT**: `vision_analyze(image_url=..., question="...")` — returns text the user cannot use to verify cursor position.
- `vision_analyze` is for YOUR analysis of page layout. It is NOT a substitute for showing the user the picture.

## Working Keyboard Pattern (Chrome on Upper Monitor)

The `hotkey` command with `delivery_mode: "foreground"` and `SendInput` path works reliably:
```bash
# Ctrl+L to select address bar — WORKS
echo '{"pid":27416,"window_id":1507982,"keys":["ctrl","l"],"delivery_mode":"foreground"}' | cua-driver call hotkey
# Returns: ✅ Pressed ctrl+l on pid 27416 via SendInput (Win32 target).

# Enter key — WORKS
echo '{"pid":27416,"window_id":1507982,"keys":["enter"],"delivery_mode":"foreground"}' | cua-driver call hotkey
# Returns: ✅ Pressed enter on pid 27416 via SendInput (Win32 target).
```

Note: `type_text` returns `"unverifiable"` even when characters are sent. The `hotkey` approach is more reliable for Chrome windows.

## Pitfalls
- **NEVER** try to move offscreen windows to the main monitor — user may want them on their monitor.
- **ALWAYS** try `delivery_mode: "background"` first — it works without stealing focus.
- **ALWAYS** re-run `get_window_state` after navigation to get fresh element indices.
- The `window_id` (HWND as integer) changes if the window is destroyed/recreated. Re-find it.
- Chrome PWA windows share the same PID as the main Chrome process — match by window TITLE.
- **NEVER** use `vision_analyze` to show the user screenshots. Use MEDIA: paths.
- **NEVER** retry the same click approach more than twice. STOP and ask the user.
- **NEVER** skip the cursor-verification workflow. Blind clicks fail on multi-monitor setups.

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

