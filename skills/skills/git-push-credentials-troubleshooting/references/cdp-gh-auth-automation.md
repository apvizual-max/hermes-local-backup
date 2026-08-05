# CDP-Based GitHub OAuth Automation (Windows Foreground Lock Workaround)

When `gh auth login --web` opens a Chrome browser for OAuth but `computer_use`
cannot interact with Chrome's address bar due to the Windows foreground lock,
use Chrome DevTools Protocol (CDP) to drive the authenticated browser session
programmatically.

## Prerequisites

- Chrome installed (Chrome/Chrome Dev/Chromium)
- Chrome with `--remote-debugging-port=9222` flag (launched with user data dir)
- `python3` with `websockets` library

## Recipe

### Step 1: Start Chrome with remote debugging

```bash
# Kill any existing Chrome instances first (prevents profile lock conflicts)
taskkill /f /im chrome.exe 2>nul

# Launch Chrome with RDP on a fresh or existing user data dir
start "" "C:\Program Files\Google\Chrome Dev\Application\chrome.exe" \
  --remote-debugging-port=9222 \
  --user-data-dir="C:\Users\apviz\AppData\Local\Google\Chrome Dev\User Data" \
  --no-first-run
```

**Pitfall**: Chrome crashes if `--remote-debugging-port` is used while another
Chrome instance is running with the same `--user-data-dir`. Always kill all
Chrome processes first, or use a separate user data dir for the RDP instance.

### Step 2: Get browser websocket URL

```bash
curl -s http://localhost:9222/json/version
# Returns "webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/<uuid>"
```

### Step 3: Create tab and navigate to GitHub device login

```python
import json, websockets, asyncio

async def complete_gh_auth():
    ws_url = "ws://localhost:9222/devtools/browser/<browser-uuid>"
    async with websockets.connect(ws_url) as ws:
        # Create a new tab
        await ws.send(json.dumps({
            "id": 1,
            "method": "Target.createTarget",
            "params": {"url": "https://github.com/login/device"}
        }))
        resp = json.loads(await ws.recv())
        target_id = resp["result"]["targetId"]
        
        # Connect to the page
        async with websockets.connect(
            f"ws://localhost:9222/devtools/page/{target_id}"
        ) as ws2:
            await ws2.send(json.dumps({"id": 1, "method": "Page.enable"}))
            await ws2.send(json.dumps({"id": 2, "method": "Runtime.enable"}))
            await asyncio.sleep(5)
            
            # Type the device code (if page shows a code input)
            # Or click "Authorize" if already signed in
            await ws2.send(json.dumps({
                "id": 3,
                "method": "Runtime.evaluate",
                "params": {"expression": "document.querySelector('input[name=\"codes\"]').value = 'YOUR_DEVICE_CODE'"}
            }))
            
            # Wait for auth to complete
            await asyncio.sleep(3)
            
            # Check if we're on the authorization page or redirected
            await ws2.send(json.dumps({
                "id": 4,
                "method": "Runtime.evaluate",
                "params": {"expression": "document.querySelector('button[type=\"submit\"]')?.click()"}
            }))
```

### Step 4: Extract the token from Chrome cookies (if needed)

Chrome 110+ encrypts cookies with AES-GCM using a master key from
`Local State` file. To decrypt:

1. Read master key from `Local State` JSON: `os_crypt.encrypted_key` (base64, strip "DPAPI" prefix, decrypt with Windows DPAPI)
2. Read cookies from `User Data/Default/Network/Cookies` SQLite DB
3. For each cookie with `encrypted_value` starting with `v20` prefix:
   - nonce = bytes[3:15], ciphertext = bytes[15:-16], tag = bytes[-16:]
   - Decrypt with AES-GCM using the master key

**Pitfall**: The master key from `Local State` may not match the cookie
encryption if Chrome was launched with a different profile. Always use the
same `--user-data-dir` for Chrome RDP that contains the authenticated session.

## Complete gh auth flow

```bash
# 1. Start the web auth flow with clipboard device code
gh auth login --web --clipboard --hostname github.com

# 2. Get the device code (copied to clipboard)
DEVICE_CODE=$(powershell -command "Get-Clipboard")

# 3. Use CDP to navigate to github.com/login/device, enter the code,
#    and complete the OAuth flow

# 4. Verify auth succeeded
gh auth status
gh api user --jq '.login'  # should show your GitHub username
```

## Alternative: Use gh with token directly

If you obtain a PAT from GitHub settings:

```bash
cat <<< "<YOUR_PAT>" | gh auth login --with-token
gh auth setup-git
```

## Windows-Specific Pitfalls

| Problem | Fix |
|---------|-----|
| `computer_use` can't type in Chrome address bar | Use CDP via `http://localhost:9222` |
| Chrome crashes on `--remote-debugging-port` launch | Kill all Chrome processes first |
| Foreground lock blocks `delivery_mode: foreground` | Launch Chrome as the foreground app manually, or use CDP |
| Cookie decryption MAC check failed | Use the correct master key from the same profile's `Local State` file |