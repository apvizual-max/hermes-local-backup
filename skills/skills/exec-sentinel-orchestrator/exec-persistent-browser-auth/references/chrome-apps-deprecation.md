# Chrome Apps Deprecation — Impact on Desktop Shortcuts

## Summary

**Google deprecated Chrome Apps in 2022** (phased out from 2020–2022). The `.lnk` shortcuts created by Chrome Apps in:

```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Chrome Apps\
```

**No longer work** on modern Chrome versions (100+).

## What Breaks

| Shortcut Location | Status | Behavior |
|-------------------|--------|----------|
| `AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Chrome Apps\*.lnk` | ❌ Broken | Opens nothing or shows "App not installed" |
| `C:\Users\Public\Desktop\*.lnk` (Chrome App shortcuts) | ❌ Broken | Same |
| `chrome://apps` page | ❌ Removed | No longer accessible |

## What Still Works

| Method | Description |
|--------|-------------|
| `agent-browser open --url <url> --session <name> --restore auto` | Persistent local session with cookies |
| Launch real Chrome via desktop shortcut | Uses actual Chrome profile with all logins |
| Modern PWA (Progressive Web App) shortcuts | Created via Chrome menu → More tools → Create shortcut → "Open as window" |

## Migration Path for LinkedIn Feed

### Old (Broken)
```
C:\Users\apviz\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Chrome Apps\LinkedIn   Feed.lnk
```

### New Options

#### Option 1: agent-browser persistent session (for automation)
```bash
agent-browser open --url https://www.linkedin.com/feed --session linkedin-session --restore auto --restore-save auto
```

#### Option 2: Launch real Chrome (for manual use)
```bash
# Via terminal
start "" "C:\Users\Public\Desktop\Google Chrome.lnk" https://www.linkedin.com/feed

# Via computer_use (clicks actual shortcut on desktop)
computer_use(action="double_click", app="explorer.exe", element=<chrome_shortcut_index>)
```

#### Option 3: Create modern PWA shortcut (one-time manual)
1. Open Chrome → `https://www.linkedin.com/feed`
2. Click ⋮ menu → More tools → Create shortcut...
3. Name: "LinkedIn Feed"
4. Check ✅ "Open as window"
5. Click Create
6. New shortcut appears in Start Menu → Chrome Apps (works on Chrome 100+)

## Verification

Test if a shortcut is a legacy Chrome App vs modern PWA:
- Right-click shortcut → Properties → Target
- **Legacy**: `chrome.exe --app-id=... --profile-directory=...` (contains `--app-id`)
- **Modern PWA**: `chrome.exe --app=https://www.linkedin.com/feed/ ...` (contains `--app=` with URL)

## Related

- `exec-persistent-browser-auth` skill — local browser automation pattern
- `linkedin-user-login` skill — manual login workflow
- `references/linkedin-session-guide.md` — session management details