#!/usr/bin/env python3
"""FIX SearXNG — final code generation for WhatsApp pairing."""
import subprocess
import os
import time
import re
import shutil
import threading
import json

def main():
    # Kill ALL node processes
    subprocess.run("taskkill /F /IM node.exe 2>nul || true", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM chrome.exe 2>nul || true", shell=True, capture_output=True)
    time.sleep(3)

    # Clear session
    session_path = r"C:\Users\apviz\.whatsapp-sessions"
    if os.path.exists(session_path):
        shutil.rmtree(session_path, ignore_errors=True)
    os.makedirs(session_path, exist_ok=True)

    env = os.environ.copy()
    env["WHATSAPP_PAIRING_PHONE_NUMBER"] = "40722121752"
    env["WHATSAPP_HEADLESS"] = "true"
    env["WHATSAPP_BROWSER"] = "chrome"
    env["WHATSAPP_SESSION_DIR"] = session_path

    proc = subprocess.Popen(
        [r"C:\Program Files\nodejs\node.exe",
         r"C:\Users\apviz\AppData\Roaming\npm\node_modules\mcp-whatsapp-web/dist/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env
    )

    output_lines = []
    
    def reader():
        for line in proc.stdout:
            output_lines.append(line)
            print(f"  [{time.time():.0f}] {line.rstrip()}")

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    # Send MCP initialize to keep the server alive
    proc.stdin.write(b'{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}\n')
    proc.stdin.flush()
    
    pairing_code = None
    for i in range(60):
        time.sleep(1)
        for line in output_lines:
            if "pairing code:" in line.lower():
                match = re.search(r'pairing code: (\w+)', line, re.IGNORECASE)
                if match:
                    pairing_code = match.group(1)
                    break
        if pairing_code:
            break

    proc.kill()

    if pairing_code:
        print(f"\n{'='*55}")
        print(f"  ✅ WHATSAPP PAIRING CODE: {pairing_code}")
        print(f"  Phone: +40722121752")
        print(f"  Enter: Settings > Linked Devices > Link a device > 'Link with phone number instead'")
        print(f"  Code expires in ~3 minutes")
        print(f"{'='*55}")
        with open(r"C:\Users\apviz\AppData\Local\hermes\scripts\whatsapp_pairing_code.txt", "w") as f:
            f.write(pairing_code)
    else:
        print("\n  ❌ No pairing code found")
        for line in output_lines:
            print(f"  {line.rstrip()}")

if __name__ == "__main__":
    main()
