#!/usr/bin/env python3
"""Request pairing code with extended wait time for WhatsApp client initialization."""
import subprocess
import json
import threading
import time
import re

# Don't kill existing processes - we want to reuse the one from whatsapp_pair_latest.py
# Just run a new one and wait longer

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
time.sleep(8)  # Wait 8 seconds for client to be ready

# Send initialized
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n")
proc.stdin.flush()
time.sleep(3)

# Request pairing code - should work now that client is initialized
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "request_pairing_code", "arguments": {"phone_number": "40722121752"}}}) + "\n")
proc.stdin.flush()
time.sleep(10)

proc.kill()

print("=== FULL OUTPUT ===")
for line in output:
    print(line.rstrip())

print("\n=== PARSING ===")
for line in output:
    try:
        data = json.loads(line.strip())
        if "result" in data and "content" in data.get("result", {}):
            for item in data["result"]["content"]:
                if item.get("type") == "text":
                    text = item["text"]
                    print(f"Result: {text}")
                    if "Pairing code" in text:
                        match = re.search(r'Pairing code: (\w+)', text)
                        if match:
                            code = match.group(1)
                            print(f"\n{'='*50}")
                            print(f"WHATSAPP PAIRING CODE: {code}")
                            print(f"Phone: +40722121752")
                            print(f"Steps: Settings > Linked Devices > Link a device > 'Link with phone number instead'")
                            print(f"Code expires in ~3 minutes")
                            print(f"{'='*50}")
    except:
        pass
