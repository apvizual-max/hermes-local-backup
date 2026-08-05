# Multi-Monitor & Computer Use Pitfalls (field-confirmed 2026-07-15)

## cua-driver Multi-Monitor Blind Spot
`computer_use` captures **per-window, per-monitor**. It CANNOT span multiple displays in a single capture.

### Symptom
- PWA or browser window opens on secondary monitor
- `computer_use(action='capture')` only shows main desktop (explorer.exe with icons)
- Window is completely invisible to captures despite being confirmed running

### Detection
```powershell
Get-Process chrome | Select-Object Id, MainWindowTitle | Where-Object { $_.MainWindowTitle -like '*LinkedIn*' }
```
If process exists but capture shows only desktop → window is on another monitor.

### Fix
1. `focus_app(raise_window=true)` — pull window to captured display
2. Ask user to drag the window to the main monitor
3. **Early detection rule**: 2 failed captures = check monitor placement immediately

---

## Browser Tool vs Computer Use Session Isolation
| Aspect | browser_navigate (Puppeteer) | computer_use (cua-driver) |
|--------|------------------------------|---------------------------|
| Browser instance | Fresh/separate | User's ACTUAL Chrome |
| Cookie sharing | None | Inherits all existing sessions |
| LinkedIn auth | Login wall every time | Uses existing PWA auth |

**Rule**: Never mix them expecting shared authentication state.

---

## User Preference: Visible Mouse Cursor
**Direct user quote (2026-07-15)**: "computer use means MOUSE CURSOR on screen"

When `computer_use` is available, ALWAYS prefer it over PowerShell Win32 API hacks or headless approaches. The user wants to SEE the cursor moving and interacting.
