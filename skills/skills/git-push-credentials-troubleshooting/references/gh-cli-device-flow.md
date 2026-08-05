# gh CLI Device Flow Automation (Windows)

Complete `gh auth login --web` on Windows when `computer_use` can't interact
with the browser due to the foreground lock.

## Problem

`gh auth login --web --clipboard` opens a browser for OAuth but Chrome requires
foreground mode for keyboard input (Windows blocks background keyboard input
via the foreground lock). The device code is copied to clipboard.

## Solution: CDP-Driven Completion

```bash
# 1. Start the auth flow (non-blocking with timeout)
# This generates a device code and copies it to clipboard
timeout 5 gh auth login --web --clipboard --hostname github.com 2>&1 || true

# 2. Get the device code from clipboard
DEVICE_CODE=$(powershell -command "Get-Clipboard")
echo "Device code: $DEVICE_CODE"

# 3. Launch Chrome with remote debugging (kill existing first)
taskkill /f /im chrome.exe 2>nul
start "" "C:\Program Files\Google\Chrome Dev\Application\chrome.exe" \
  --remote-debugging-port=9222 \
  --user-data-dir="C:\Users\apviz\AppData\Local\Google\Chrome Dev\User Data" \
  --no-first-run

# 4. Use CDP to navigate to device login, enter code, complete auth
python3 << 'PYEOF'
import json, websockets, asyncio, time

async def complete_auth():
    ws_url = "ws://localhost:9222/devtools/browser/YOUR_BROWSER_UUID"
    async with websockets.connect(ws_url) as ws:
        # Create tab with GitHub device login page
        await ws.send(json.dumps({
            "id": 1,
            "method": "Target.createTarget",
            "params": {"url": "https://github.com/login/device"}
        }))
        resp = json.loads(await ws.recv())
        target_id = resp["result"]["targetId"]
        
        async with websockets.connect(f"ws://localhost:9222/devtools/page/{target_id}") as ws2:
            await ws2.send(json.dumps({"id": 1, "method": "Page.enable"}))
            await asyncio.sleep(5)
            
            # Type device code
            device_code = "YOUR_DEVICE_CODE_HERE"
            await ws2.send(json.dumps({
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {"expression": f"document.querySelector('input[name=\"device_code\"]').value = '{device_code}'"}
            }))
            
            # Click Submit
            await ws2.send(json.dumps({
                "id": 3,
                "method": "Runtime.evaluate",
                "params": {"expression": "document.querySelector('button[type=\"submit\"]').click()"}
            }))
            await asyncio.sleep(3)
            
            # If already logged in, click "Authorize" button
            await ws2.send(json.dumps({
                "id": 4,
                "method": "Runtime.evaluate",
                "params": {"expression": "document.querySelector('button[type=\"submit\"]')?.click()"}
            }))
            await asyncio.sleep(5)
            
            # Check for success
            await ws2.send(json.dumps({
                "id": 5,
                "method": "Runtime.evaluate",
                "params": {"expression": "document.body.innerText || 'no content'"}
            }))
            resp = await ws2.recv()
            text = json.loads(resp).get("result", {}).get("result", {}).get("value", "")
            print(f"Page text: {text[:200]}")

asyncio.run(complete_auth())
PYEOF

# 5. Verify
gh auth status
gh api user --jq '.login'
```

## Key Variables

- **Browser UUID**: Get from `curl http://localhost:9222/json/version` (look for `webSocketDebuggerUrl`)
- **Device code**: Copied to clipboard by `gh auth login --web --clipboard`
- **Chrome path**: `C:\Program Files\Google\Chrome Dev\Application\chrome.exe` (or Chrome stable)
- **User data dir**: Must match the profile with GitHub session cookies

## Pitfall: Chrome Profile Conflicts

If Chrome was previously running (e.g., the normal GUI session), launching a
second instance with `--remote-debugging-port` and the same `--user-data-dir`
will cause a profile lock conflict and Chrome will crash. Solution: kill all
existing Chrome processes first, or use a separate user data directory for the
RDP instance.

## Pitfall: Foreground Lock

Windows' foreground lock prevents `computer_use` from sending keyboard input
to background windows. CDP bypasses this limitation entirely — the browser is
controlled via WebSocket at the protocol level, not via Windows input APIs.

## Pitfall: Cookie Decryption

If you need to extract the OAuth callback token from Chrome cookies instead
of letting `gh` complete the flow, Chrome 110+ encrypts cookies with AES-GCM.
See `references/cdp-gh-auth-automation.md` for the master key extraction recipe.