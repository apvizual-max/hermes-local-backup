---
name: page-mapping
description: "Map a page to a grid-indexed coordinate system for agents."
version: 0.1.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags:
      - Page-Mapping
      - Grid-Index
      - Subagent
      - Click-Coordinates
---

# Page Mapping — Subagent's Visual Map

Deliver a screenshot + grid index + clickable coordinates to a subagent so it can click any element on the upper monitor in under 1 minute. No thinking required — just follow the map.

## What This Skill Delivers

A 3-file package: **screenshot (PNG)** + **coordinate map (JSON)** + **human index (MD)**. The subagent uses the JSON to find element centers and clicks via `cua-driver mcp`.

## What This Skill RESTRICTS

The subagent is FORBIDDEN from:
- Opening new windows (no `browser_navigate`)
- Using `computer_use` (returns 0x0 on upper monitor)
- Thinking about alternative approaches
- Mapping the page itself (map is provided)
- Any thought process beyond: find index → click → verify

## The Map Package

### 1. Screenshot (PNG)
Full window capture at 1568x842. Visual reference only — not used for clicking.

### 2. Coordinate Map (JSON)
```json
{
  "page_name": "JOBS_MAIN_PAGE",
  "url": "linkedin.com/jobs/",
  "grid": {"cols": 16, "rows": 9, "cell": "98x94px"},
  "window": {"pid": 27416, "hwnd": 1507982},
  "elements": [
    {
      "index": 35,
      "label": "Job tracker",
      "role": "Hyperlink",
      "center_vx": 1497, "center_vy": -570,
      "grid_id": "G0205"
    }
  ]
}
```

### 3. Human Index (MD)
Grid table for quick reference:
```
| Grid | Label | Center (vx,vy) |
|------|-------|-----------------|
| G0205 | Job tracker | (1497, -570) |
| G0011 | Jobs | (2106, -967) |
```

## How the Subagent Uses It

### Step 1: Receive the map
The orchestrator provides: page name, target element label, map file path.

### Step 2: Look up coordinates
```python
import json
with open("JOBS_MAIN_PAGE_MAP.json") as f:
    map_data = json.load(f)
for e in map_data["elements"]:
    if e["label"] == "Job tracker":
        target = e  # {"index": 35, "center_vx": 1497, "center_vy": -570}
```

### Step 3: Click via MCP (single command)
```python
proc = subprocess.Popen(['cua-driver', 'mcp', '--no-daemon-relaunch'], stdin=PIPE, stdout=PIPE, text=True)
# get_window_state → find element index → click by index
# OR: use saved center_vx/center_vy for coordinate click
req = json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call",
    "params":{"name":"click","arguments":{"pid":27416,"window_id":1507982,
    "element_index":35,"delivery_mode":"background"}}}) + "\n"
proc.stdin.write(req); proc.stdin.flush()
```

### Step 4: Verify
```python
req = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{"name":"get_window_state","arguments":{"pid":27416,"window_id":1507982,"max_elements":5}}}) + "\n"
# Check URL in response text
```

## The Mapping Process (Orchestrator Only)

### 1. Screenshot
```bash
echo '{"pid":27416,"window_id":1507982,"max_elements":500}' | cua-driver call get_window_state
```
Extract `screenshot_png_b64` → save as PNG.

### 2. Scrape AX Tree
Same call returns elements array with: `element_index`, `role`, `label`, `frame {x,y,w,h}`.

### 3. Text Compress
Filter to clickable roles only: `Hyperlink`, `Button`, `ComboBox`, `Tab`, `MenuItem`, `CheckBox`. Discard empty labels.

### 4. Image → Grid → Coordinates
```
GRID = 16 cols × 9 rows
cell_w = 1568/16 = 98px, cell_h = 842/9 = 94px
grid_id = f"G{row:02d}{col:02d}"
center_vx = frame.x + frame.w/2
center_vy = frame.y + frame.h/2
```

### 5. Label Non-Clickable Blocks
For text regions (headings, descriptions), label as "BLOCK: {text}" with frame coordinates. These guide the agent's page understanding but aren't clickable.

### 6. Deliver Package
3 files to `C:/Users/apviz/Desktop/TEST/`:
- `{PAGE}_MAP.json` — clickable elements
- `{PAGE}_INDEX.md` — human reference
- `{PAGE}.png` — visual reference

## Subagent Restriction Schema

```
⛔ YOU ARE A HANDS AGENT. DO NOT THINK. DO NOT EXPLORE. EXECUTE.

MAP: {MAP_PATH}
TARGET: {ELEMENT_LABEL}
CLICK: cua-driver mcp → element_index={N} → delivery_mode=background
VERIFY: get_window_state → check URL
OUTPUT: Report new URL. Nothing else.

FORBIDDEN: browser_navigate, computer_use, opening windows, asking questions
```

## Quick Reference

| Step | Command |
|------|---------|
| Map page | `cua-driver call get_window_state` (max_elements=500) |
| Find element | Parse JSON: `elements[].label` match |
| Click | `cua-driver mcp` + JSON-RPC `click` (element_index) |
| Verify | `cua-driver mcp` + JSON-RPC `get_window_state` |

## Pitfalls

- Map is STATIC — if page design changes, re-map
- Subagent gets the MAP, not the mapping process
- Subagent is FORBIDDEN from thinking — just execute
- Coordinates are in VIRTUAL screen space (origin 0,-1080)
- Always use `delivery_mode: "background"`

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

