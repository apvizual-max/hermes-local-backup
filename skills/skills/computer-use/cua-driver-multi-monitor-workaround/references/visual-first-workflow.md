# Visual-First Workflow — Computer Use Page Mapping

## Overview
When interacting with any desktop application via `cua-driver`, ALWAYS follow this workflow before attempting clicks. This eliminates the #1 source of failure: blind coordinate guessing.

## The 6-Step Visual-First Loop

### Step 1: Capture Screenshot + AX Tree
```python
import subprocess, json, base64, os

PID = 27416  # target process
HWND = 1507982  # target window handle
MAP_DIR = "C:/Users/apviz/Desktop/TEST"

r = subprocess.run(
    ['cua-driver', 'call', 'get_window_state'],
    input=json.dumps({"pid": PID, "window_id": HWND, "max_elements": 500}),
    capture_output=True, text=True, timeout=30
)

state = json.loads(r.stdout)
if 'output' in state:
    state = json.loads(state['output'])

# Extract screenshot
png_b64 = state.get('screenshot_png_b64', '')
img_data = base64.b64decode(png_b64)
w = state.get('screenshot_width', 0)
h = state.get('screenshot_height', 0)

print(f"Screenshot: {w}x{h}, {len(img_data)} bytes")
print(f"Elements: {state.get('element_count', 0)}")
```

### Step 2: Save Screenshot to Disk
```python
img_path = os.path.join(MAP_DIR, "page_XX_name.png")
with open(img_path, 'wb') as f:
    f.write(img_data)
```

### Step 3: Visual Analysis with vision_analyze
```python
# Use the Hermes vision_analyze tool on the saved screenshot:
# vision_analyze(image_url=img_path, question="Map the UI layout: identify all clickable elements, their positions relative to the image, and the page URL.")
```

**Key questions to ask**:
- "Where is the target element in this screenshot? Give me pixel coordinates relative to the {w}x{h} image."
- "What page am I on? What navigation elements are visible?"
- "List all clickable elements in the left sidebar with their approximate positions."

### Step 4: Extract Element Coordinates from AX Tree
```python
elements_map = []
for e in state.get('elements', []):
    frame = e.get('frame', {})
    if isinstance(frame, dict) and frame:
        elements_map.append({
            "index": e.get('index'),
            "role": e.get('role'),
            "label": str(e.get('label', ''))[:80],
            "frame": frame,
            "center_x": frame.get('x', 0) + frame.get('w', 0) // 2,
            "center_y": frame.get('y', 0) + frame.get('h', 0) // 2
        })

# Sort by position (top-to-bottom, left-to-right)
elements_map.sort(key=lambda e: (e['center_y'], e['center_x']))
```

### Step 5: Save Page Map (JSON + MD + PNG)
```python
# Save JSON map
map_data = {
    "url": url,
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "screenshot_dimensions": {"width": w, "height": h},
    "element_count": len(elements_map),
    "elements": elements_map
}

map_path = os.path.join(MAP_DIR, "page_XX_name_map.json")
with open(map_path, 'w') as f:
    json.dump(map_data, f, indent=2, ensure_ascii=False)

# Save human-readable MD map
md_lines = [f"# Page Map: {page_name}", f"**URL**: {url}", f"**Dimensions**: {w}x{h}", f"**Elements**: {len(elements_map)}", ""]
md_lines.append("| # | Role | Label | Frame | Center |")
md_lines.append("|---|------|-------|-------|--------|")
for e in elements_map:
    f = e['frame']
    md_lines.append(f"| {e['index']} | {e['role']} | {e['label'][:40]} | ({f.get('x')},{f.get('y')}) {f.get('w')}x{f.get('h')} | ({e['center_x']},{e['center_y']}) |")

md_path = os.path.join(MAP_DIR, "page_XX_name_map.md")
with open(md_path, 'w') as f:
    f.write('\n'.join(md_lines))
```

### Step 6: Click Using Saved Coordinates
```python
# From the saved map, find the target element's center coordinates
target_center_x = 1497
target_center_y = -579

r = subprocess.run(
    ['cua-driver', 'call', 'click'],
    input=json.dumps({
        "pid": PID,
        "window_id": HWND,
        "x": target_center_x,
        "y": target_center_y,
        "delivery_mode": "background"
    }),
    capture_output=True, text=True, timeout=15
)
```

## Page Naming Convention
- `page_01_landing.png` — first page captured
- `page_02_after_click_X.png` — page after clicking element X
- `page_03_navigation_result.png` — result of navigation
- Corresponding `_map.json` and `_map.md` files

## When to Re-Capture vs Use Saved Map

| Scenario | Action |
|----------|--------|
| Page already mapped, layout unchanged | Use saved coordinates directly |
| First visit to a page | Full 6-step workflow |
| After navigation (URL changed) | Re-capture (Step 1) |
| After clicking a link/button | Re-capture (Step 1) |
| LinkedIn pushed a UI update | Full re-map |
| Window was resized | Full re-map |

## Anti-Pattern: The Blind Click Loop (DO NOT DO THIS)
```python
# ❌ WRONG: Repeatedly trying different coordinates without visual confirmation
for attempt in range(10):
    click(x + random_offset, y + random_offset)
    time.sleep(1)
    # ... hope it worked
```

## Correct Pattern: Map → Verify → Click
```python
# ✅ RIGHT: Map first, verify visually, then click with confidence
capture_and_save("page_01_current")
analyze_with_vision("page_01_current.png")
extract_target_coordinates()
click(saved_x, saved_y)
verify_result()
```

## Coordinate System Reference

### Virtual Screen Layout (Dual Monitor)
```
Upper Monitor: Y = -1080 to 0
Main Monitor:  Y = 0 to 1728
Total Virtual: 3072 x 2808, origin at (0, -1080)
```

### AX Tree Frame → Virtual Coordinates
```python
# AX tree frame values ARE virtual coordinates (not relative to window)
# frame = {'x': 1342, 'y': -603, 'w': 311, 'h': 48}
# → This element is at virtual screen position (1342, -603)
# → Center for clicking: (1342 + 155, -603 + 24) = (1497, -579)
```

### Screenshot Coordinates → Virtual Coordinates
```python
# Screenshot is (width x height) of the window
# To convert screenshot pixel (sx, sy) to virtual coords:
# virtual_x = window_origin_x + sx
# virtual_y = window_origin_y + sy
# 
# Window origin can be estimated from frame elements near the top-left
```