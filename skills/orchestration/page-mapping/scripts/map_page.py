"""
Page Mapping Script — generates the 3-file map package for subagents.

Usage: python map_page.py <page_name>

Output (in C:/Users/apviz/Desktop/TEST/):
  {page_name}.png         — screenshot
  {page_name}_MAP.json    — clickable elements with coordinates
  {page_name}_INDEX.md    — human-readable grid index
"""

import subprocess, json, base64, os, sys, time

PID = 27416
HWND = 1507982
MAP_DIR = "C:/Users/apviz/Desktop/TEST"
GRID_COLS = 16
GRID_ROWS = 9
CLICKABLE_ROLES = {'Hyperlink', 'Button', 'ComboBox', 'MenuItem', 'Tab', 'CheckBox', 'RadioButton'}

def map_page(page_name):
    # 1. Capture
    r = subprocess.run(
        ['cua-driver', 'call', 'get_window_state'],
        input=json.dumps({"pid": PID, "window_id": HWND, "max_elements": 500}),
        capture_output=True, text=True, timeout=30
    )
    state = json.loads(r.stdout)
    if 'output' in state:
        state = json.loads(state['output'])
    
    w = state.get('screenshot_width', 1568)
    h = state.get('screenshot_height', 842)
    cell_w = w / GRID_COLS
    cell_h = h / GRID_ROWS
    
    # 2. Screenshot
    png = state.get('screenshot_png_b64', '')
    img_path = os.path.join(MAP_DIR, f"{page_name}.png")
    with open(img_path, 'wb') as f:
        f.write(base64.b64decode(png))
    print(f"✅ Screenshot: {img_path}")
    
    # 3. URL
    url = "unknown"
    for e in state.get('elements', []):
        if 'Address' in str(e.get('label', '')):
            url = str(e.get('value', ''))
            break
    
    # 4. Extract clickable elements
    window_origin_x = 960
    window_origin_y = -1080
    
    elements = []
    for e in state.get('elements', []):
        role = str(e.get('role', ''))
        label = str(e.get('label', '')).strip()
        frame = e.get('frame', {})
        if role not in CLICKABLE_ROLES or not label or len(label) < 2:
            continue
        if not isinstance(frame, dict) or not frame:
            continue
        
        fx, fy, fw, fh = frame.get('x', 0), frame.get('y', 0), frame.get('w', 0), frame.get('h', 0)
        cx, cy = fx + fw // 2, fy + fh // 2
        
        sx = fx - window_origin_x
        sy = fy - window_origin_y
        grid_col = max(0, min(int(sx / cell_w), GRID_COLS - 1))
        grid_row = max(0, min(int(sy / cell_h), GRID_ROWS - 1))
        
        elements.append({
            "index": e.get('element_index'),
            "label": label[:80],
            "role": role,
            "center_vx": cx, "center_vy": cy,
            "frame": {"x": fx, "y": fy, "w": fw, "h": fh},
            "grid_id": f"G{grid_row:02d}{grid_col:02d}"
        })
    
    elements.sort(key=lambda e: (e['grid_id'], e['center_vy']))
    
    # 5. Save JSON
    map_data = {
        "page_name": page_name,
        "url": url,
        "screenshot": f"{page_name}.png",
        "grid": {"cols": GRID_COLS, "rows": GRID_ROWS, "cell": f"{cell_w:.0f}x{cell_h:.0f}px"},
        "window": {"pid": PID, "hwnd": HWND},
        "element_count": len(elements),
        "elements": elements
    }
    
    json_path = os.path.join(MAP_DIR, f"{page_name}_MAP.json")
    with open(json_path, 'w') as f:
        json.dump(map_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Map: {json_path} ({len(elements)} elements)")
    
    # 6. Save MD index
    md_path = os.path.join(MAP_DIR, f"{page_name}_INDEX.md")
    with open(md_path, 'w') as f:
        f.write(f"# {page_name}\n\n**URL**: `{url}`\n\n")
        f.write(f"| Grid | # | Label | Role | Center (vx,vy) |\n")
        f.write(f"|------|---|-------|------|----------------|\n")
        for e in elements:
            f.write(f"| {e['grid_id']} | {e['index']} | {e['label'][:40]} | {e['role']} | ({e['center_vx']},{e['center_vy']}) |\n")
    print(f"✅ Index: {md_path}")
    
    return map_data

if __name__ == "__main__":
    page_name = sys.argv[1] if len(sys.argv) > 1 else "PAGE"
    map_page(page_name)