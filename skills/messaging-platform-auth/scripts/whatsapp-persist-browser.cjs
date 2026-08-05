/**
 * whatsapp-persist-browser.cjs
 * Persistent Puppeteer browser for WhatsApp Web with QR code authentication.
 * 
 * This is the WORKING alternative to the broken requestPairingCode flow.
 * Since whatsapp-web.js v1.34.7's requestPairingCode crashes (AuthStore.PairingCodeLinkUtils
 * is not available in the current WhatsApp Web version), this script launches a real
 * Chrome browser that the user can manually scan the QR code for.
 * 
 * The browser session (including IndexedDB auth data) persists in userDataDir
 * across restarts.
 * 
 * USAGE:
 *   node whatsapp-persist-browser.cjs
 * 
 * After running, scan the QR code with your phone. The script will detect
 * authentication and write "authenticated" to authenticated.txt.
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SESSION_DIR = 'C:/Users/apviz/.whatsapp-sessions';

async function main() {
    console.log('[WHATSAPP_QR] Starting persistent Chrome session...');
    console.log('[WHATSAPP_QR] This will open a real WhatsApp Web browser window.');
    console.log('[WHATSAPP_QR] Please scan the QR code with your phone.');

    fs.mkdirSync(path.join(SESSION_DIR, 'session'), { recursive: true });

    const browser = await puppeteer.launch({
        headless: false,
        executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
        userDataDir: path.join(SESSION_DIR, 'session'),
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationDetected',
        ],
        defaultViewport: { width: 1366, height: 768 },
    });

    const page = await browser.newPage();
    page.on('console', msg => console.log('[PAGE]', msg.text()));
    page.on('pageerror', err => console.log('[PAGE ERROR]', err.message));

    console.log('[WHATSAPP_QR] Navigating to WhatsApp Web...');
    await page.goto('https://web.whatsapp.com', { waitUntil: 'domcontentloaded', timeout: 60000 });
    console.log('[WHATSAPP_QR] WhatsApp Web loaded! Waiting for QR scan...');

    // Poll authentication status
    const authCheck = setInterval(async () => {
        try {
            const authStatus = await page.evaluate(() => {
                const hasChat = document.querySelector('[data-testid="chat-list"]') !== null ||
                                document.querySelector('.app-2') !== null ||
                                document.querySelector('._3DNbb') !== null;
                const hasQR = document.querySelector('canvas') !== null ||
                             document.querySelector('img[src*="qr"]') !== null;
                const hasScanText = document.body.innerText.includes('Scan QR code') ||
                                   document.body.innerText.includes('Use your phone');
                return { hasChat, hasQR, hasScanText, title: document.title };
            });

            if (authStatus.hasChat) {
                console.log('[WHATSAPP_QR] AUTHENTICATED! Chats visible.');
                fs.writeFileSync(path.join(SESSION_DIR, 'authenticated.txt'), 'true');
                console.log('[WHATSAPP_QR] Auth confirmed. Session saved at:', path.join(SESSION_DIR, 'session'));
                console.log('[WHATSAPP_QR] Browser will stay open. You can now use WhatsApp Web.');
            } else {
                console.log('[WHATSAPP_QR] Waiting for QR scan...');
            }
        } catch(e) {
            console.log('[WHATSAPP_QR] Status check (page not ready)');
        }
    }, 3000);

    console.log('[WHATSAPP_QR] Browser is open. Scan the QR code with your phone.');
    console.log('[WHATSAPP_QR] DO NOT close this window.');

    await new Promise(() => {}); // Keep alive forever
}

main().catch(e => {
    console.error('[WHATSAPP_QR ERROR]', e);
    process.exit(1);
});
