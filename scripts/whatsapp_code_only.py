#!/usr/bin/env python3
"""
Clean single-instance WhatsApp pairing for phone +407****1752.
Captures the auto-emitted pairing code from stderr (WHATSAPP_PAIRING_PHONE_NUMBER env var).
"""
import subprocess
import json
import threading
import time
import sys
import os
import re
import shutil

def main():
    session_path = r"C:\Users\apviz\.whatsapp-sessions"
    
    # Clear old session
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
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    pairing_code = None
    qr_data = None
    output_lines = []

    def reader(stream, prefix):
        for line in stream:
            output_lines.append(line)

    t_out = threading.Thread(target=reader, args=(proc.stdout, "STDOUT"), daemon=True)
    t_err = threading.Thread(target=reader, args=(proc.stderr, "STDERR"), daemon=True)
    t_out.start()
    t_err.start()

    # MCP handshake
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}) + "\n")
    proc.stdin.flush()
    time.sleep(3)

    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n")
    proc.stdin.flush()
    time.sleep(3)

    # Wait for the pairing code to be auto-emitted (up to 30s)
    for i in range(30):
        if pairing_code:
            break
        time.sleep(1)
        # Check output for pairing code
        for line in output_lines:
            if "pairing code:" in line.lower():
                match = re.search(r'pairing code: (\w+)', line, re.IGNORECASE)
                if match:
                    pairing_code = match.group(1)
                    break

    proc.kill()

    if pairing_code:
        print(f"\n{'='*55}")
        print(f"  ✅ WHATSAPP PAIRING CODE: {pairing_code}")
        print(f"  Phone: +40722121752")
        print(f"  Enter on phone: Settings > Linked Devices")
        print(f"  > Link a device > 'Link with phone number instead'")
        print(f"  Code expires in ~3 minutes")
        print(f"{'='*55}")
        print(f"\n  Pairing code saved to pairing code for phone: +40722121752")
        
        # Save to file
        with open(r"C:\Users\apviz\AppData\Local\hermes\scripts\whatsapp_pairing_code.txt", "w") as f:
            f.write(pairing_code)
        print(f"\n  Saved to: C:\\Users\\apviz\\AppData\\Local\\hermes\\scripts\\whatsapp_pairing_code.txt")
    else:
        print("❌ Pairing code not found in output")
        print("\n=== ALL STDERR ===")
        for line in output_lines:
            print(line.rstrip())

if __name__ == "__main__":
    main()
