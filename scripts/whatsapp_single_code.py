#!/usr/bin/env python3
"""
WhatsApp Pairing — SINGLE instance, CODE ONLY (no QR)
Root cause: whatsapp-web.js needs the page fully loaded (AuthStore.PairingCodeLinkUtils)
before requestPairingCode() works. The MCP server auto-emits code via env var,
but the browser crashes if it starts before WhatsApp Web initializes.

This script:
1. Kills ALL node processes (clean slate)
2. Sets WHATSAPP_PAIRING_PHONE_NUMBER env var (triggers auto-emit)
3. Starts SINGLE instance with extended wait time
4. Captures the auto-emitted pairing code from stderr
"""
import subprocess
import os
import time
import re
import shutil
import threading

def main():
    # Step 1: Kill ALL node processes
    print("1. Killing all node processes...")
    subprocess.run("taskkill /F /IM node.exe 2>nul || true", shell=True, capture_output=True)
    time.sleep(3)

    # Step 2: Clear session
    session_path = r"C:\Users\apviz\.whatsapp-sessions"
    print("2. Clearing session cache...")
    if os.path.exists(session_path):
        shutil.rmtree(session_path, ignore_errors=True)
    os.makedirs(session_path, exist_ok=True)

    # Step 3: Start single MCP server with env var
    print("3. Starting WhatsApp MCP server (single instance)...")
    
    env = os.environ.copy()
    env["WHATSAPP_PAIRING_PHONE_NUMBER"] = "40722121752"
    env["WHATSAPP_HEADLESS"] = "true"  # Headless is fine - code is server-side
    env["WHATSAPP_BROWSER"] = "chrome"
    env["WHATSAPP_SESSION_DIR"] = session_path

    proc = subprocess.Popen(
        [r"C:\Program Files\nodejs\node.exe",
         r"C:\Users\apviz\AppData\Roaming\npm\node_modules\mcp-whatsapp-web/dist/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    output_lines = []
    
    def reader(stream):
        for line in stream:
            output_lines.append(line)
    
    t_out = threading.Thread(target=reader, args=(proc.stdout,), daemon=True)
    t_err = threading.Thread(target=reader, args=(proc.stderr,), daemon=True)
    t_out.start()
    t_err.start()

    # MCP handshake
    proc.stdin.write(b'{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}\n')
    proc.stdin.flush()
    time.sleep(5)

    proc.stdin.write(b'{"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}\n')
    proc.stdin.flush()
    
    # Wait for pairing code in stderr (auto-emitted after WhatsApp Web page loads)
    print("4. Waiting for pairing code (auto-emitted after WhatsApp Web loads)...")
    pairing_code = None
    for i in range(60):
        if pairing_code:
            break
        time.sleep(1)
        for line in output_lines:
            if "pairing code:" in line.lower():
                match = re.search(r'pairing code: (\w+)', line, re.IGNORECASE)
                if match:
                    pairing_code = match.group(1)
                    break
        if i == 10:
            print(f"   Still waiting... ({i}s)")
        if i == 30:
            print(f"   Still waiting... ({i}s) - WhatsApp Web page loading")
        if i == 45:
            print(f"   Still waiting... ({i}s) - connecting to servers")

    proc.kill()

    if pairing_code:
        print(f"\n{'='*55}")
        print(f"  ✅ WHATSAPP PAIRING CODE: {pairing_code}")
        print(f"  Phone: +40722121752")
        print(f"  Enter on phone: Settings > Linked Devices")
        print(f"  > Link a device > 'Link with phone number instead'")
        print(f"  Code expires in ~3 minutes")
        print(f"{'='*55}")
        
        with open(r"C:\Users\apviz\AppData\Local\hermes\scripts\whatsapp_pairing_code.txt", "w") as f:
            f.write(pairing_code)
        print(f"\n  Saved to: C:\\Users\\apviz\\AppData\\Local\\hermes\\scripts\\whatsapp_pairing_code.txt")
        print(f"  Script:   C:\\Users\\apviz\\AppData\\Local\\hermes\\scripts\\whatsapp_single_code.py")
    else:
        print(f"\n  ❌ Pairing code not found after 60s")
        print(f"\n  === LAST 20 LINES OF OUTPUT ===")
        for line in output_lines[-20:]:
            print(f"  {line.rstrip()}")

if __name__ == "__main__":
    main()
