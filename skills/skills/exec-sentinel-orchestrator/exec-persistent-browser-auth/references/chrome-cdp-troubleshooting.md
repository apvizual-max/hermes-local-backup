# Chrome CDP (Port 9222) Troubleshooting Reference

## Problem: Chrome Remote Debugging Port Not Opening

**Symptoms:**
- `netstat -an | findstr 9222` returns empty
- `curl http://localhost:9222/json/version` → Connection refused
- Chrome starts but immediately exits or connects to existing session

## Root Causes & Fixes

### 1. Existing Chrome Session Blocks New Instance
**Cause:** Chrome detects existing session and attaches to it instead of starting fresh with CDP.

**Fix:**
```bash
# Kill ALL Chrome processes
taskkill /F /IM chrome.exe

# Remove lock files
del "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\lockfile"
del "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\LOCK"
del "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\Singleton*"

# Start fresh with no-startup-window
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --no-startup-window ^
  --no-first-run ^
  --no-default-browser-check ^
  --disable-extensions ^
  --remote-allow-origins=*
```

### 2. Lock Files Prevent New Session
**Cause:** `LOCK` and `SingletonLock` files in User Data directory prevent new instance.

**Fix:** Delete all `LOCK` and `Singleton*` files in:
- `C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\`
- `C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\`

### 3. Chrome Attaches to Existing Session
**Cause:** Default behavior reuses existing Chrome window.

**Fix:** Use `--no-startup-window` flag AND ensure no other Chrome processes running.

### 4. Profile Locked by Another Process
**Cause:** Another Chrome instance holds the profile lock.

**Fix:**
```bash
# Nuclear option - kill all Chrome, clean locks, fresh start
taskkill /F /IM chrome.exe
timeout /t 2
powershell -Command "Get-ChildItem 'C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data' -Recurse -Filter 'LOCK' | Remove-Item -Force"
powershell -Command "Get-ChildItem 'C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data' -Recurse -Filter 'Singleton*' | Remove-Item -Force"
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --no-startup-window --no-first-run --no-default-browser-check
```

## Verification Commands

```bash
# Check port is listening
netstat -an | findstr 9222

# Test CDP endpoint
curl http://localhost:9222/json/version

# List available tabs
curl http://localhost:9222/json

# Expected output:
# {"Browser":"Chrome/120.0.0","Protocol-Version":"1.3","User-Agent":"Mozilla/5.0...","V8-Version":"12.0.0","WebKit-Version":"537.36","WebSocket-Debugger-URL":"ws://localhost:9222/devtools/browser/..."}
```

## Complete Fresh Start Script (Windows Batch)

```batch
@echo off
echo Killing all Chrome processes...
taskkill /F /IM chrome.exe 2>nul
timeout /t 2

echo Removing lock files...
del "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\lockfile" 2>nul
del "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\LOCK" 2>nul
del "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\SingletonLock" 2>nul
del "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\SingletonCookie" 2>nul
del "C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data\Default\SingletonSocket" 2>nul

echo Starting Chrome with remote debugging...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --no-startup-window ^
  --no-first-run ^
  --no-default-browser-check ^
  --disable-extensions ^
  --disable-background-networking ^
  --disable-sync ^
  --remote-allow-origins=*

timeout /t 5

echo Verifying CDP endpoint...
curl http://localhost:9222/json/version
```

## LinkedIn-Specific Notes

- The browser tool in this environment uses Browserbase (cloud), not local Chrome
- For local LinkedIn extraction, use `agent-browser` CLI which manages its own Chrome profile
- `li_at` cookie must be extracted from user's actual Chrome profile (DevTools → Application → Cookies)
- Inject into `agent-browser` session: `agent-browser cookies set --curl linkedin_cookies.txt --session linkedin-session`

## Related Files

- `exec-persistent-browser-auth` skill — Main workflow
- `sentinel-local-system-awareness` skill — System verification
- `linkedin-local-data-extraction` skill — LinkedIn-specific extraction