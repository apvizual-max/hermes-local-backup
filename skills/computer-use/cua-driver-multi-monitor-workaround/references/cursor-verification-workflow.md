# Cursor-Verification Workflow — Detailed Reference

## Why This Exists

On 2026-07-15, the agent spent 3+ hours trying to click "Job tracker" on LinkedIn. Every click failed. The root cause: **the agent never verified cursor position before clicking.** The user repeatedly demanded to see the cursor on screen but the agent kept describing screenshots with `vision_analyze` text instead of showing actual images.

This reference file documents the correct workflow so future sessions don't repeat the same failure.

## The 6-Step Cursor-Verification Loop

### Step 1: Move Cursor to Target
```
cua-driver call move_cursor → {"pid": PID, "window_id": HWND, "x": X, "y": Y}
```
Use the center coordinates from the saved page map. Do NOT guess.

### Step 2: Capture Screenshot with Cursor
```
cua-driver call get_window_state → {"pid": PID, "window_id": HWND, "max_elements": 5}
```
Keep max_elements low (5) to minimize payload. We only need the screenshot.

### Step 3: Decode and Save Screenshot
```python
import base64
png_b64 = result['screenshot_png_b64']
with open('C:/Users/apviz/Desktop/TEST/cursor_verify.png', 'wb') as f:
    f.write(base64.b64decode(png_b64))
```

### Step 4: Show the User
```
MEDIA:C:/Users/apviz/Desktop/TEST/cursor_verify.png
```
**CRITICAL**: Use MEDIA: path syntax. Do NOT use `vision_analyze` — it returns text, not an image.

### Step 5: Wait for User Confirmation
Ask: "Is the cursor on the correct element?" If the user says no, recalculate coordinates and repeat from Step 1.

### Step 6: Click and Verify
```bash
echo '{"pid":PID,"window_id":HWND,"x":X,"y":Y,"delivery_mode":"background"}' | cua-driver call click
# Then capture again and show the result
```

## Why This Matters

**Without cursor verification:**
- The agent clicks blindly at calculated coordinates
- The user cannot see where the click is going
- A miscalculation means clicking the wrong element
- The user gets frustrated because they can't see what's happening

**With cursor verification:**
- The user sees exactly where the cursor is
- The user can confirm or correct the position
- Clicks are precise and intentional
- The user trusts the process

## The vision_analyze Trap

`vision_analyze` returns a TEXT DESCRIPTION of an image. It does NOT show the image to the user. This is useful for the agent's own analysis but useless for user verification.

**Session 2026-07-15 failure**: The agent called `vision_analyze` 5+ times to "show" the cursor to the user. Each time, the user saw only text and responded "I DO NOT SEE ANY CURSOR." The agent interpreted this as "the cursor isn't on screen" rather than "you're showing me text, not an image."

**Rule**: `vision_analyze` = for agent's eyes only. `MEDIA:` = for the user.

## The STOP-After-2 Rule

From the session: the agent tried 20+ variations of the same click approach:
- Background click → failed
- Foreground click → failed
- Double-click → failed
- Right-click → failed
- Coordinate adjustments → failed
- Element index → failed
- Keyboard navigation → failed

After 2 failures, the correct action is to STOP and show the user the current state. The user knows their setup better than the agent and can provide guidance.

## Working Keyboard Commands (Lessons Learned)

The ONLY keyboard command that worked reliably on the upper monitor Chrome window:
```bash
# hotkey with delivery_mode: "foreground" — WORKS
echo '{"pid":27416,"window_id":1507982,"keys":["ctrl","l"],"delivery_mode":"foreground"}' | cua-driver call hotkey
# → ✅ Pressed ctrl+l on pid 27416 via SendInput (Win32 target).
```

What did NOT work:
- `press_key` with `delivery_mode: "foreground"` → exit 1
- `type_text` with `delivery_mode: "foreground"` → "unverifiable"
- `type_text` with `delivery_mode: "background"` → exit 1 (Chrome_WidgetWin_1 class rejected)

The `hotkey` command uses `SendInput` which is more reliable than `key_events` path for Chrome windows.