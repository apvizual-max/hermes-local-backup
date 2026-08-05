#!/usr/bin/env python3
"""Request WhatsApp pairing code for phone number 40722121752."""
import subprocess
import json
import threading
import time

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

# Also try get_qr_code in case pairing code fails
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_qr_code", "arguments": {}}}) + "\n")
proc.stdin.flush()
time.sleep(10)

proc.kill()

print("=== FULL OUTPUT ===")
for line in output:
    print(line.rstrip())

print("\n=== PARSING RESULTS ===")
for line in output:
    try:
        data = json.loads(line.strip())
        if "result" in data and "content" in data.get("result", {}):
            for item in data["result"]["content"]:
                if item.get("type") == "text":
                    print(f"Response: {item['text']}")
                if item.get("type") == "image":
                    print("IMAGE DATA RECEIVED - saving...")
                    import base64
                    qr_data = base64.b64decode(item["data"])
                    with open("C:/Users/apviz/AppData/Local/hermes/scripts/whatsapp_qr.png", "wb") as f:
                        f.write(qr_data)
                    print(f"QR code saved! Size: {len(qr_data)} bytes")
    except:
        pass
