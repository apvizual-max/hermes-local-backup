const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SESSION_DIR = 'C:/Users/apviz/.whatsapp-sessions';
const PHONE = '40722121752';

async function main() {
    console.log('[DIRECT] Starting WhatsApp direct pairing...');
    
    fs.mkdirSync(path.join(SESSION_DIR, 'session'), { recursive: true });
    
    const browser = await puppeteer.launch({
        headless: false,
        userDataDir: path.join(SESSION_DIR, 'session'),
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
        ],
        defaultViewport: { width: 1366, height: 768 },
    });
    
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('[PAGE]', msg.text()));
    page.on('error', err => console.log('[PAGE ERROR]', err.message));
    page.on('pageerror', err => console.log('[PAGE ERROR]', err.message));
    
    // Expose a function that the browser can call with the pairing code
    await page.exposeFunction('__onPairingCode', (code) => {
        console.log('[PAIRING_CODE]', code);
        fs.writeFileSync(path.join(SESSION_DIR, 'pairing_code.txt'), code);
    });
    
    console.log('[DIRECT] Navigating to web.whatsapp.com...');
    await page.goto('https://web.whatsapp.com', { waitUntil: 'networkidle2', timeout: 60000 });
    
    // Wait for the page to fully load
    await new Promise(r => setTimeout(r, 10000));
    
    // Try to request the pairing code by directly manipulating the page
    console.log('[DIRECT] Attempting to request pairing code...');
    
    try {
        await page.evaluate(async (phoneNumber) => {
            // Wait for AuthStore to be available
            for (let i = 0; i < 30; i++) {
                if (window.AuthStore) {
                    console.log('[DIRECT] AuthStore found');
                    
                    // Check for PairingCodeLinkUtils
                    if (window.AuthStore.PairingCodeLinkUtils) {
                        console.log('[DIRECT] PairingCodeLinkUtils found');
                        const utils = window.AuthStore.PairingCodeLinkUtils;
                        
                        if (utils.setPairingType) utils.setPairingType('ALT_DEVICE_LINKING');
                        if (utils.initializeAltDeviceLinking) await utils.initializeAltDeviceLinking();
                        
                        if (utils.startAltLinkingFlow) {
                            const code = await utils.startAltLinkingFlow(phoneNumber, true);
                            console.log('[DIRECT] Code from startAltLinkingFlow:', code);
                            if (window.__onPairingCode) window.__onPairingCode(code);
                        }
                        return;
                    }
                    
                    // Check for SocketCodeLinking
                    if (window.AuthStore.SocketCodeLinking) {
                        console.log('[DIRECT] SocketCodeLinking found');
                        const scl = window.AuthStore.SocketCodeLinking;
                        if (scl.startAltLinkingFlow) {
                            const code = await scl.startAltLinkingFlow(phoneNumber, true);
                            console.log('[DIRECT] Code from SocketCodeLinking:', code);
                            if (window.__onPairingCode) window.__onPairingCode(code);
                        }
                        return;
                    }
                    
                    // Check for any other pairing-related objects
                    const keys = Object.keys(window.AuthStore).filter(k => k.toLowerCase().includes('pair') || k.toLowerCase().includes('link') || k.toLowerCase().includes('code'));
                    console.log('[DIRECT] Pairing-related keys:', keys);
                }
                await new Promise(r => setTimeout(r, 500));
            }
            console.log('[DIRECT] AuthStore not found after 15 seconds');
        }, PHONE);
    } catch (e) {
        console.log('[DIRECT] Evaluate error:', e.message);
    }
    
    // Wait for pairing code file
    console.log('[DIRECT] Waiting for pairing code to be detected...');
    for (let i = 0; i < 120; i++) {
        const codeFile = path.join(SESSION_DIR, 'pairing_code.txt');
        if (fs.existsSync(codeFile)) {
            const code = fs.readFileSync(codeFile, 'utf8').trim();
            console.log('[DIRECT] PAIRING CODE DETECTED:', code);
            break;
        }
        await new Promise(r => setTimeout(r, 1000));
    }
    
    // Check if the pairing code file exists
    const codeFile = path.join(SESSION_DIR, 'pairing_code.txt');
    if (!fs.existsSync(codeFile)) {
        console.log('[DIRECT] No pairing code detected. Trying alternative method...');
        
        // Try scanning the DOM for a code element
        const domCode = await page.evaluate(() => {
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                const text = (el.innerText || '').trim();
                if (/^[a-zA-Z0-9]{8}$/.test(text) && text.length === 8) {
                    return text;
                }
            }
            return null;
        });
        
        if (domCode) {
            console.log('[DIRECT] DOM CODE:', domCode);
            fs.writeFileSync(codeFile, domCode);
        } else {
            console.log('[DIRECT] No code found in DOM either.');
        }
    }
    
    console.log('[DIRECT] Browser is running. User should enter code on phone.');
    console.log('[DIRECT] Keeping browser open...');
    
    // Keep the browser open
    await new Promise(() => {});
}

main().catch(e => {
    console.error('[DIRECT ERROR]', e);
    process.exit(1);
});
