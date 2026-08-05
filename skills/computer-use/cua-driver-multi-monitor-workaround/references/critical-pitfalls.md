# Critical Pitfalls — Computer Use on Multi-Monitor (Windows + Chrome)

## 1. Element Cache Expiry — THE #1 FAILURE MODE

**Problem**: The AX element cache dies between separate `cua-driver call` invocations. Each call is a new daemon connection.

**Symptom**: 
```
Element 36 not in cache for hwnd=1507982. Call get_window_state first.
```

**Solution**: Use **coordinate-based clicking** (x,y) instead of `element_index`. Coordinates don't require a fresh cache.

**Rule**: NEVER chain `get_window_state` → `click by element_index` across separate `cua-driver call` invocations. Each `cua-driver call` spawns a new process; the cache is per-process.

**Cache-safe alternative**: Pipe JSON-RPC requests to `cua-driver mcp --no-daemon-relaunch` via stdin. The MCP daemon keeps the session alive across all requests in the pipe, so the cache from `get_window_state` is valid when `click` runs next. See SKILL.md "Single-Process Element-Index Click" section for the exact command.

---

## 2. Browser Chrome is NOT in the AX Tree

**Problem**: Browser UI elements (back button, forward, address bar, window controls) are **not** exposed via the accessibility tree.

**Symptom**: Agent searches for "back button" in elements but finds nothing.

**Solution**: Use coordinate estimation based on window frame position.

**Example**: 
```python
# If window top-left is at virtual (960, -1080):
back_button_x = 960 + 15  # 15px right of window edge
back_button_y = -1080 + 5  # 5px down from top
# → (975, -1075)
```

---

## 3. Chrome Keyboard Input Requires Foreground Delivery

**Problem**: Background `PostMessage` doesn't work for keystrokes on Chrome_WidgetWin_1 windows.

**Symptom**: `type_text` and `press_key` return exit code 1 with empty output.

**Error message**:
```
Background delivery is not available for target window class 'Chrome_WidgetWin_1' 
on this event kind (keystroke). Either call bring_to_front then retry with 
delivery_mode:"foreground", or accept the foreground requirement.
```

**Solution**: Use `delivery_mode: "foreground"` for ALL keyboard operations on Chrome.

**Example**:
```bash
echo '{"pid":27416,"window_id":1507982,"text":"https://linkedin.com/jobs-tracker/","delivery_mode":"foreground"}' | cua-driver call type_text
```

---

## 4. Visual-First Workflow (MANDATORY)

**Problem**: Agent tries to work from AX trees alone, guessing at coordinates.

**Solution**: ALWAYS follow this sequence:
1. **Capture screenshot** via `get_window_state` (extract `screenshot_png_b64`)
2. **Save screenshot** to disk immediately
3. **Analyze screenshot** with `vision_analyze` to map UI layout visually
4. **Extract element coordinates** from AX tree + screenshot overlay
5. **Save page map** (JSON + MD + PNG) before attempting any clicks
6. **Click using saved coordinates** from the map

**Rule**: No click attempts until you have a saved visual map. Map first, click second.

---

## 5. Click Target Selection Guide

### When to Use Coordinates (x,y)
- ✅ Browser chrome elements (back button, address bar) — not in AX tree
- ✅ Elements from saved page maps — no cache dependency
- ✅ Multi-monitor windows where cache expires between calls
- ✅ Any click that failed with `element_index`

### When to Use element_index
- ✅ MCP stdin piping: `get_window_state` and `click` in the same `cua-driver mcp --no-daemon-relaunch` stdin pipe (see SKILL.md)
- ✅ Fresh captures where you just populated the cache in the same MCP session
- ❌ NEVER via `cua-driver call` CLI — each invocation is a separate process, cache dies
- ❌ NEVER via `subprocess.run(['cua-driver', 'call', ...])` — same problem, separate processes

### Coordinate Calculation Formula
```python
# From AX tree element:
frame = {'x': 1342, 'y': -603, 'w': 311, 'h': 48}
center_x = frame['x'] + frame['w'] // 2  # 1497
center_y = frame['y'] + frame['h'] // 2  # -579

# For browser chrome (not in AX tree):
window_origin = (960, -1080)  # from window frame elements
back_button = (window_origin[0] + 15, window_origin[1] + 5)  # (975, -1075)
```

---

## 6. Direct URL Navigation Pattern

When clicks fail or you need to navigate to a known URL:

```bash
# Step 1: Select address bar (foreground required)
echo '{"pid":27416,"window_id":1507982,"keys":"ctrl+l","delivery_mode":"foreground"}' | cua-driver call press_key

# Step 2: Wait for selection
sleep 0.5

# Step 3: Type URL (foreground required)
echo '{"pid":27416,"window_id":1507982,"text":"https://linkedin.com/jobs-tracker/","delivery_mode":"foreground"}' | cua-driver call type_text

# Step 4: Wait for typing
sleep 0.5

# Step 5: Press Enter (foreground required)
echo '{"pid":27416,"window_id":1507982,"keys":"enter","delivery_mode":"foreground"}' | cua-driver call press_key
```

**Pitfall**: Even with foreground delivery, the window must be **activated** (not just brought to front). If keyboard commands fail:
1. Click anywhere in the window first (to activate it)
2. Then send keyboard commands

---

## 7. Window Origin Detection

To find browser chrome coordinates, locate window frame elements:

```python
# From AX tree, find window control buttons:
# [None] Button "Minimize" frame={'h': 33, 'w': 45, 'x': 2727, 'y': -1078}
# [None] Button "Maximize" frame={'h': 33, 'w': 46, 'x': 2772, 'y': -1078}
# [None] Button "Close" frame={'h': 33, 'w': 46, 'x': 2818, 'y': -1078}

# Window top-right corner: x = 2818 + 46 = 2864, y = -1078
# If window width from capture is 1568px:
# Window top-left: x = 2864 - 1568 = 1296, y = -1078

# Back button position (15px right, 5px down from top-left):
back_button_x = 1296 + 15  # = 1311
back_button_y = -1078 + 5  # = -1073
```

---

## Session Log: 2026-07-15

### Problem Encountered
Agent spent 20+ iterations trying to click the "Job tracker" link on LinkedIn Jobs page, repeatedly failing due to:
1. Element cache expiry between `get_window_state` and `click` calls
2. Attempting to find "back button" in AX tree (not present)
3. Using background delivery for Chrome keyboard input (not supported)
4. Not following visual-first workflow (screenshot → analyze → map → click)

### Root Cause
Lack of documented pitfalls led to repeated trial-and-error instead of systematic approach.

### Solution Applied
- Created this pitfall reference file
- Documented coordinate-based clicking as the primary method
- Established visual-first workflow as mandatory
- Documented Chrome keyboard foreground requirement

### Time Saved for Future Sessions
Estimated 15-20 minutes of debugging per multi-monitor click task.