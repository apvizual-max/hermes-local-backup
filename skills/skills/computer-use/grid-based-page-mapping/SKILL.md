---
name: grid-based-page-mapping
description: "Map any page into a grid-indexed coordinate system."
version: 0.1.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags:
      - Page-Mapping
      - Grid-Index
      - Visual-Mapping
      - Coordinate-System
---

# Grid-Based Page Mapping

Capture any page, divide it into a grid, and index every clickable element with grid coordinates. Produces a reusable map (JSON + Index + PNG) that survives element cache expiry.

## When to Use

- "map the page"
- "index the page"
- "create a coordinate map"
- "grid the page"
- When you need reusable click coordinates for a page

## How to Run

1. Capture with `get_window_state` (max_elements=500)
2. Extract screenshot_png_b64 and save to PNG
3. Choose grid: 16×9 for 16:9-ish pages, adjust for other ratios
4. Extract all clickable elements (Hyperlink, Button, ComboBox, etc.)
5. Convert virtual coordinates to screenshot coordinates
6. Assign each element to a grid cell
7. Save JSON map + MD index + PNG screenshot

## Grid Formula

```
GRID_COLS = 16
GRID_ROWS = 9
cell_w = screenshot_width / GRID_COLS
cell_h = screenshot_height / GRID_ROWS
grid_id = f"G{row:02d}{col:02d}"
```

## Coordinate Conversion

Virtual screen coords → Screenshot coords:
```
sx = virtual_x - window_origin_x
sy = virtual_y - window_origin_y
```

Window origin found from AX tree frame elements near top-left.

## Output Files

- `{PAGE_NAME}.png` — screenshot
- `{PAGE_NAME}_MAP.json` — full clickable element index with coordinates
- `{PAGE_NAME}_INDEX.md` — human-readable grid table

## Click from Map

```bash
echo '{"pid":<PID>,"window_id":<HWND>,"x":<center_vx>,"y":<center_vy>,"delivery_mode":"background"}' | cua-driver call click
```

## Pitfalls

- Grid is fixed — if page design changes, remap
- Window origin must be recalculated if window moves
- Only clickable roles are indexed (Hyperlink, Button, ComboBox, etc.)
- **Multi-monitor GPU boundary**: If the upper monitor is on a different GPU, clicks may fail even with correct coordinates. Use the single-process element-index fallback from `cua-driver-multi-monitor-workaround`.
- **Map first, click second**: Never attempt clicks without a saved page map. Load `cua-driver-multi-monitor-workaround` for the full cursor-verification workflow.
- **Coordinate reuse**: Once mapped, the same coordinates work across sessions until LinkedIn changes the layout. Do not re-map the same page.

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

