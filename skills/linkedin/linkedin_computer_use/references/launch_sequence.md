# Reference: Launch Sequence & Window Management

DEEP DIVE into Phase 1 (Launch) and Phase 2 (Window Management) of the LinkedIn Computer Use skill.
Based on the verified 2026-07-15 session.

---

## PHASE 1 — LAUNCH VIA COMPUTER_USE (Exact Steps)

### Step 1: Capture desktop
```
computer_use(action="capture", app="screen", mode="som")
```
**Observed return (truncated):**
```json
{
  "mode": "som", "width": 1568, "height": 1323, "app": "explorer.exe",
  "elements": [
    {"index": 0, "role": "ListItem", "label": "Recycle Bin", "bounds": [95,127,94,87]},
    {"index": 5, "role": "ListItem", "label": "LinkedIn   Feed", "bounds": [285,127,94,107]},
    ...
  ]
}
```
- Shortcut "LinkedIn   Feed" at **index 5** (top-left, below Recycle Bin at index 0).
- Label has **3 spaces** between "LinkedIn" and "Feed".

### Step 2: Double-click (NOT single click)
```
computer_use(action="double_click", element=5)
```
**Observed return:**
```json
{"action": "double_click", "ok": true, "message": "✅ Posted double-click to [5] at screen-point (332, 180)."}
```
**What single click does instead (WRONG):**
```json
{"action": "click", "ok": true, "message": "✅ Performed UIA Toggle on [5] (screen (332,180))."}
```
→ "Toggle" = just selects the icon. App does NOT open. **Use double_click.**

### Step 3: Wait & verify
```
computer_use(action="wait", seconds=5)
computer_use(action="capture", app="screen", mode="som")
```
- App opens as separate window (left ~60% split in user's view).
- User confirmed via screenshot: LinkedIn dark-mode feed visible with nav, profile sidebar, posts.

---

## PHASE 2 — WINDOW MANAGEMENT QUIRKS

### The problem
After launch, agent tried to focus the app window:
```
computer_use(action="list_apps")
```
**Returned:**
```json
{"apps": [{"name": "- Google Chrome", "pid": 66884}, ...]}
```
→ Process IS running as "Google Chrome" pid 66884.

Then:
```
computer_use(action="focus_app", app="Google Chrome")
```
**Returned ERROR:**
```json
{"ok": false, "message": "No on-screen window found for app 'Google Chrome'."}
```

And:
```
computer_use(action="capture", app="Google Chrome", mode="som")
```
**Returned:**
```json
{"mode":"som","width":0,"height":0,"window_title":"<no on-screen window matched app='Google Chrome'...>","elements":[],"total_elements":0}
```

### Root cause
Chrome App windows (launched via `--app=` or "Open as window" shortcut) are not matched by
cua-driver's app-name filter the same way as a normal Chrome browser window. The process shows as
"Google Chrome" in list_apps but cannot be focused/captured by name.

### The fix (USE THIS)
```
computer_use(action="capture", app="screen", mode="som")
```
Always capture the full screen. The app window appears within the desktop capture. Identify its
UI elements by SOM index or screen coordinates and interact via `computer_use(action="click", element=N)`
or `computer_use(action="type", ...)`.

### Summary table
| Attempt | Result | Verdict |
|---------|--------|---------|
| `focus_app("Google Chrome")` | "No on-screen window found" | ❌ Don't use |
| `capture("Google Chrome")` | 0x0 empty | ❌ Don't use |
| `capture("LinkedIn")` | no match | ❌ Don't use |
| `capture("screen", mode="som")` | Shows full desktop + app | ✅ USE THIS |
| `list_apps()` | Shows pid 66884 | ℹ️ Confirms running, but can't focus |

---

## TROUBLESHOOTING LAUNCH

| Symptom | Cause | Fix |
|---------|-------|-----|
| Nothing opens after click | Used `click` not `double_click` | Use `double_click` on the shortcut |
| App opens but can't be focused | Chrome App window quirk | Use `capture("screen")` to observe |
| Desktop capture shows only icons | App may be behind / on other monitor | `capture("screen")` still captures it; or user confirms |
| Shortcut not found at index 5 | Desktop layout differs | Read `capture("screen")` output, find "LinkedIn   Feed" index |
