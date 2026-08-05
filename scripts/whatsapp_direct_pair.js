const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SESSION_DIR = 'C:/Users/apviz/.whatsapp-sessions';
const PHONE = '40722121752';

async function main() {
    console.log('Starting WhatsApp direct pairing...');
    
    // Create session directory
    fs.mkdirSync(path.join(SESSION_DIR, 'session'), { recursive: true });
    
    const browser = await puppeteer.launch({
        headless: false, // Must be false for pairing to work
        userDataDir: path.join(SESSION_DIR, 'session'),
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
        ],
        defaultViewport: { width: 1366, height: 768 },
    });
    
    const page = await browser.newPage();
    
    // Listen for console messages
    page.on('console', msg => {
        if (msg.type() === 'log' || msg.type() === 'warn' || msg.type() === 'error') {
            console.log(`PAGE: ${msg.text()}`);
        }
    });
    
    // Listen for dialogs
    page.on('dialog', async dialog => {
        console.log('DIALOG:', dialog.message());
    });
    
    console.log('Navigating to web.whatsapp.com...');
    await page.goto('https://web.whatsapp.com', { waitUntil: 'networkidle2', timeout: 60000 });
    
    // Inject script to intercept the pairing code
    await page.evaluateOnNewDocument(() => {
        window.__PAIRING_CODE = null;
        window.__PAIRING_CODES = [];
        
        // Override the AuthStore to capture pairing codes
        const originalEvaluate = window.AuthStore;
        
        // Poll for AuthStore.PairingCodeLinkUtils
        const capturePairingCode = async () => {
            for (let i = 0; i < 120; i++) { // 2 minutes
                try {
                    if (window.AuthStore && window.AuthStore.PairingCodeLinkUtils) {
                        const utils = window.AuthStore.PairingCodeLinkUtils;
                        
                        // Check for existing code
                        if (utils.pairingCode && !window.__PAIRING_CODES.includes(utils.pairingCode)) {
                            window.__PAIRING_CODES.push(utils.pairingCode);
                            window.__PAIRING_CODE = utils.pairingCode;
                            console.log('PAIRING_CODE_DETECTED:', utils.pairingCode);
                        }
                        
                        // Start the flow
                        if (typeof utils.setPairingType === 'function') {
                            utils.setPairingType('ALT_DEVICE_LINKING');
                        }
                        if (typeof utils.initializeAltDeviceLinking === 'function') {
                            await utils.initializeAltDeviceLinking();
                        }
                        if (typeof utils.startAltLinkingFlow === 'function') {
                            const result = await utils.startAltLinkingFlow('40722121752', true);
                            if (result) {
                                window.__PAIRING_CODE = result;
                                window.__PAIRING_CODES.push(result);
                                console.log('PAIRING_CODE:', result);
                            }
                        }
                    }
                    
                    // Also check for SocketCodeLinking
                    if (window.AuthStore && window.AuthStore.SocketCodeLinking) {
                        const scl = window.AuthStore.SocketCodeLinking;
                        if (scl.pairingCode) {
                            window.__PAIRING_CODE = scl.pairingCode;
                            console.log('PAIRING_CODE (scl):', scl.pairingCode);
                        }
                    }
                } catch (e) {
                    // Ignore
                }
                
                await new Promise(r => setTimeout(r, 1000));
                
                // Check if we got a code
                if (window.__PAIRING_CODE) {
                    return;
                }
            }
        };
        
        capturePairingCode();
    });
    
    // Wait for the page to load
    await new Promise(r => setTimeout(r, 10000));
    
    // Try to get the pairing code from the page
    const result = await page.evaluate(() => {
        if (window.__PAIRING_CODE) return window.__PAIRING_CODE;
        return null;
    });
    
    if (result) {
        console.log('PAIRING_CODE:', result);
    } else {
        console.log('No pairing code detected - checking for SocketCodeLinking...');
        const fallback = await page.evaluate(() => {
            try {
                // Try to access the WhatsApp Web socket directly
                const socket = window.require('WAWebSocketModel').Socket;
                console.log('Socket state:', socket.state);
                
                // Try alternative API
                const auth = window.AuthStore;
                if (auth) {
                    const keys = Object.keys(auth);
                    return 'AuthStore keys: ' + keys.join(', ');
                }
                return 'No AuthStore found';
            } catch (e) {
                return 'Error: ' + e.message;
            }
        });
        console.log('Fallback:', fallback);
    }
    
    // Keep the browser open
    console.log('Browser session is active. Press Ctrl+C to exit.');
    await new Promise(() => {}); // Never resolve
}

main().catch(console.error);
