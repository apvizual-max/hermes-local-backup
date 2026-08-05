# Multi-Monitor & Computer Use Pitfalls (field-confirmed 2026-07-15)

## cua-driver Multi-Monitor Blind Spot
`computer_use` captures **per-window, per-monitor**. It CANNOT span multiple displays in a single capture.

### Symptom
- LinkedIn PWA launched via desktop shortcut opens on secondary monitor
- `computer_use(action='capture')` only shows main desktop (explorer.exe with icons)
- PWA window is completely invisible to captures
- Repeated captures with different `app=` values all return desktop icons only

### Detection
```powershell
# Confirm PWA IS running (will show MainWindowTitle like "LinkedIn | Feed - Feed | LinkedIn")
Get-Process chrome | Select-Object Id, MainWindowTitle | Where-Object { $_.MainWindowTitle -like '*LinkedIn*' }
```
If process exists but capture shows only desktop → window is on another monitor.

### Fix (priority order)
1. **`focus_app(raise_window=true)`** — pull window to captured display
2. **Ask user** to drag the PWA window to the main monitor
3. **Early detection rule**: 2 failed captures with different app names = check monitor placement immediately, do NOT retry blindly

### Anti-pattern (DO NOT)
- Do NOT waste 10+ captures trying different `app=` parameter values
- Do NOT assume the PWA didn't launch just because capture can't see it
- Do NOT fall back to PowerShell Win32 API hacks (ShowWindow, SetForegroundWindow via Add-Type/DllImport) — these fail with compilation errors in the shell environment and the user explicitly said "computer use means MOUSE CURSOR on screen"

---

## Browser Tool vs Computer Use Session Isolation
The `browser_navigate` tool (Puppeteer/Browserbase) runs a **SEPARATE browser instance** from the user's real Chrome.

| Aspect | browser_navigate (Puppeteer) | computer_use (cua-driver) |
|--------|------------------------------|---------------------------|
| Browser instance | Fresh/separate | User's ACTUAL Chrome |
| Cookie sharing | None | Inherits all existing sessions |
| LinkedIn auth | Login wall every time | Uses existing PWA auth |
| CAPTCHA | Must solve fresh | Bypassed (already authenticated) |
| Visible to user | Sometimes | Always (real mouse cursor) |

### Rule
- Use `browser_navigate` ONLY for Path B (Puppeteer + user solves CAPTCHA manually in visible browser)
- Use `computer_use` for Path C (drive user's ACTUAL authenticated browser/PWA)
- NEVER mix them expecting shared authentication state

---

## User Preference: Visible Mouse Cursor
**Direct user quote (2026-07-15)**: "spin up a cursor mouse and follow my visual instructions...computer use means MOUSE CURSOR on screen...you can do it"

### Implication
When `computer_use` is available, ALWAYS prefer it over:
- PowerShell Win32 API window management
- Headless browser approaches
- Terminal-based URL launching

The user wants to SEE the cursor moving and interacting on screen. This is not just a technical preference — it's a trust/visibility requirement.

---

## Working Pattern: Desktop PWA Shortcut → computer_use
1. `computer_use(action='capture', mode='som')` — find the desktop shortcut (e.g., "LinkedIn Feed")
2. `computer_use(action='double_click', element=N)` — launch the PWA
3. `computer_use(action='wait', seconds=5)` — wait for PWA to load
4. `computer_use(action='focus_app', app='Chrome', raise_window=true)` — bring to captured display
5. `computer_use(action='capture', mode='som')` — verify PWA content is visible
6. If step 5 shows desktop icons only → multi-monitor issue, apply fix above
7. Once PWA is visible → drive navigation with `click`, `type`, `key`, `scroll`
