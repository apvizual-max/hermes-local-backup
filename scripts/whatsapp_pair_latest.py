#!/usr/bin/env python3
"""Request fresh WhatsApp pairing code for phone number 40722121752."""
import subprocess
import json
import threading
import time
import base64

# Kill any existing whatsapp sessions (Windows equivalent)
subprocess.run("taskkill /F /IM node.exe /FI \"WINDOWTITLE=*whatsapp*\" 2>nul || true", shell=True, capture_output=True)
time.sleep(2)

# Clear old session to force fresh auth
import os
import shutil
session_path = r"C:\Users\apviz\.whatsapp-sessions"
if os.path.exists(session_path):
    shutil.rmtree(session_path, ignore_errors=True)
os.makedirs(session_path, exist_ok=True)

proc = subprocess.Popen(
    ["C:\\Program Files\\nodejs\\node.exe",
     "C:\\Users\\apviz\\AppData\\Roaming\\npm\\node_modules\\mcp-whatsapp-web/dist/index.js"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

output = []
def reader():
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        output.append(line)

t = threading.Thread(target=reader, daemon=True)
t.start()

# Initialize
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}) + "\n")
proc.stdin.flush()
time.sleep(5)

proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n")
proc.stdin.flush()
time.sleep(2)

# Request pairing code
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "request_pairing_code", "arguments": {"phone_number": "40722121752"}}}) + "\n")
proc.stdin.flush()
time.sleep(10)

# Get QR code as fallback
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_qr_code", "arguments": {}}}) + "\n")
proc.stdin.flush()
time.sleep(10)

proc.kill()

print("=== FULL OUTPUT ===")
for line in output:
    print(line.rstrip())

print("\n=== PARSING RESULTS ===")
pairing_code = None
qr_data = None
for line in output:
    try:
        data = json.loads(line.strip())
        if "result" in data and "content" in data.get("result", {}):
            for item in data["result"]["content"]:
                if item.get("type") == "text":
                    text = item["text"]
                    print(f"Response: {text[:300]}")
                    # Extract pairing code
                    if "Pairing code:" in text:
                        import re
                        match = re.search(r'Pairing code: (\w+)', text)
                        if match:
                            pairing_code = match.group(1)
                    # Extract QR data
                if item.get("type") == "image":
                    qr_data = item.get("data")
                    print("IMAGE DATA RECEIVED")
    except:
        pass

if pairing_code:
    print(f"\n=== PAIRING CODE: {pairing_code} ===")
    print(f"Enter this code on WhatsApp: Settings > Linked Devices > Link a device > 'Link with phone number instead'")
    print(f"Pairing code expires in ~3 minutes.")

if qr_data:
    qr_bytes = base64.b64decode(qr_data)
    with open(r"C:\Users\apviz\AppData\Local\hermes\scripts\whatsapp_qr.png", "wb") as f:
        f.write(qr_bytes)
    print(f"\n=== QR CODE SAVED ===")
    print(f"Path: C:\\Users\\apviz\\AppData\\Local\\hermes\\scripts\\whatsapp_qr.png")
    print(f"Size: {len(qr_bytes)} bytes")
