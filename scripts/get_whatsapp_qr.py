#!/usr/bin/env python3
"""Extract and save the WhatsApp QR code image from MCP server output."""
import subprocess
import json
import time
import threading
import base64
import re

proc = subprocess.Popen(
    ["C:\\Program Files\\nodejs\\node.exe", "C:\\Users\\apviz\\AppData\\Roaming\\npm\\node_modules\\mcp-whatsapp-web/dist/index.js"],
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

# Initialize and get QR
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}) + "\n")
proc.stdin.flush()
time.sleep(3)

proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n")
proc.stdin.flush()
time.sleep(1)

# Keep trying to get QR code
for attempt in range(5):
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "get_qr_code", "arguments": {}}}) + "\n")
    proc.stdin.flush()
    time.sleep(8)
    
    # Check if we got the QR code
    for line in output:
        try:
            data = json.loads(line.strip())
            if data.get("id") == 2 and "result" in data:
                content = data["result"].get("content", [])
                for item in content:
                    if item.get("type") == "image":
                        base64_data = item.get("data")
                        if base64_data:
                            # Save the QR code image
                            qr_bytes = base64.b64decode(base64_data)
                            qr_path = "C:/Users/apviz/AppData/Local/hermes/scripts/whatsapp_qr.png"
                            with open(qr_path, "wb") as f:
                                f.write(qr_bytes)
                            print(f"✅ QR code saved to: {qr_path}")
                            print(f"   Image size: {len(qr_bytes)} bytes")
                            proc.kill()
                            exit(0)
        except:
            pass

proc.kill()
print("❌ QR code not available after multiple attempts")
print("All output lines:")
for line in output:
    print(line[:200])
