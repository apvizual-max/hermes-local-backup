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

## Verification Steps

```bash
# 1. Check port is listening
netstat -an | findstr 9222
# Should show: TCP    127.0.0.1:9222    0.0.0.0:0    LISTENING

# 2. Test CDP endpoint
curl http://localhost:9222/json/version
# Should return JSON with Browser, Protocol-Version, etc.

# 3. List available tabs
curl http://localhost:9222/json
# Should return array of tab objects
```

## Common Flags for Stable CDP

| Flag | Purpose |
|------|---------|
| `--remote-debugging-port=9222` | Enable CDP on port 9222 |
| `--no-startup-window` | Don't open visible window |
| `--no-first-run` | Skip first-run experience |
| `--no-default-browser-check` | Skip default browser prompt |
| `--disable-extensions` | Disable extensions (cleaner fingerprint) |
| `--disable-background-networking` | Reduce background noise |
| `--disable-sync` | Disable sync |
| `--disable-default-apps` | Disable default apps |
| `--remote-allow-origins=*` | Allow all origins for CDP |

## Integration with agent-browser + chrome-devtools-mcp

The two browser MCP servers complement each other:

1. **chrome-devtools-mcp** (port 9222): Uses Chrome's native CDP. Requires Chrome started with `--remote-debugging-port=9222`
2. **agent-browser** (Docker Chrome): Selenium WebDriver on port 4446. Uses npx-based installation:
   ```bash
   npx -y agent-browser-mcp-server@latest  # Latest package
   ```

**If `agent-browser` CLI times out on `open`:**
- The old binary path `agent-browser-win32-x64.exe` is no longer used
- Use Docker Chrome with CDP port 9223 instead:
  ```bash
  docker run -d --name chrome-docker-cdp --shm-size=2gb -p 4446:4444 -p 9223:9222 selenium/standalone-chrome:latest --remote-debugging-port=9223
  ```
- Or use system Chrome Dev on port 9222 with `--user-data-dir` for persistent sessions

## SearXNG Integration

When Chrome CDP works, SearXNG can use it for JavaScript-heavy engines:
- Add Chrome CDP URL to SearXNG engine config
- Use `--remote-debugging-port` with Selenium/Playwright if needed

## Related Skills

- `exec-local-service-management` — Local service management (SearXNG, Docker)
- `exec-persistent-browser-auth` — Persistent browser auth patterns
- `linkedin-local-data-extraction` — LinkedIn extraction workflows