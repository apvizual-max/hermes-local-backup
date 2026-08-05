# WhatsApp Web Pairing Code — Browser Automation Pattern

## Problem

mcp-whatsapp-web (whatsapp-web.js v1.34.7) pairing code authentication fails because the library's `requestPairingCode` method accesses `window.AuthStore.PairingCodeLinkUtils`, which no longer exists in the current WhatsApp Web version. The `require('WAWebAltDeviceLinkingApi')` call inside `ExposeAuthStore` throws "Requiring unknown module".

## The Working Approach: QR Code with Persistent Session

When pairing code fails, the reliable fallback is QR code authentication with a persistent Chrome user data directory that survives server restarts. The browser MUST stay open for the session to save to IndexedDB.

### Script Pattern

```javascript
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const SESSION_DIR = 'C:/Users/apviz/.whatsapp-sessions';

const browser = await puppeteer.launch({
    headless: false,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    userDataDir: path.join(SESSION_DIR, 'session'),
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    defaultViewport: { width: 1366, height: 768 },
});
const page = await browser.newPage();
await page.goto('https://web.whatsapp.com', { waitUntil: 'domcontentloaded' });

const authCheck = setInterval(async () => {
    const authStatus = await page.evaluate(() => {
        const chatList = document.querySelector('[data-testid="chat-list"]');
        return { hasChat: !!chatList };
    });
    if (authStatus.hasChat) {
        clearInterval(authCheck);
        // DO NOT close browser — session must save to IndexedDB
        fs.writeFileSync(path.join(SESSION_DIR, 'authenticated.txt'), 'true');
        await new Promise(() => {});  // Keep alive
    }
}, 3000);
```

### Running mcp-whatsapp-web HTTP Server with Existing Session

```bash
cd C:/Users/apviz/AppData/Roaming/npm/node_modules/mcp-whatsapp-web
WHATSAPP_HEADLESS=true WHATSAPP_BROWSER=chrome \
WHATSAPP_SESSION_DIR=C:\\Users\\apviz\\.whatsapp-sessions \
MCP_HTTP_PORT=3002 TRANSPORT=http node dist/index.js
```

### Session Persistence

- Session data: `C:\Users\apviz\.whatsapp-sessions\session`
- IndexedDB grows ~276KB (unauth) to ~6.2MB (auth)
- Never `rm -rf` session directory after successful pairing

## Verified Working (2026-08-05)

QR code scan with persistent session:
1. Chrome browser opened headless:false
2. User scanned QR code with phone
3. Browser stayed open (process NOT killed)
4. Session saved to IndexedDB in `.whatsapp-sessions/session`
5. mcp-whatsapp-web HTTP server loaded session successfully
6. Auth status: "You are currently authenticated"
7. 9 contacts retrieved successfully