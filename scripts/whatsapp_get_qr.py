#!/usr/bin/env python3
"""
Get WhatsApp QR code and auth status.
"""
import subprocess
import json
import os
import time
import threading
import sys

env = os.environ.copy()
env["WHATSAPP_SESSION_DIR"] = r"C:\Users\apviz\.whatsapp-sessions"
env["WHATSAPP_HEADLESS"] = "true"

proc = subprocess.Popen(
    ["C:\\Program Files\\nodejs\\npx.cmd", "-y", "mcp-whatsapp-web"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env,
    cwd=r"C:\Users\apviz"
)

print(f"WhatsApp MCP server started (PID: {proc.pid})")
print("Waiting 30s for server initialization...", flush=True)
time.sleep(30)

if proc.poll() is not None:
    print("❌ Server exited during startup")
    sys.exit(1)

# Build MCP messages
messages = [
    '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "hermes", "version": "1.0"}}}',
    '{"jsonrpc": "2.0", "method": "notifications/initialized"}',
    '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "check_auth_status", "arguments": {}}}',
    '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_qr_code", "arguments": {}}}',
]

for msg in messages:
    proc.stdin.write((msg + "\n").encode())
    proc.stdin.flush()
    time.sleep(2)

time.sleep(10)

# Read output
output_lines = []
def read_output():
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        output_lines.append(line.decode().rstrip())

t = threading.Thread(target=read_output, daemon=True)
t.start()
time.sleep(10)

for line in output_lines:
    if line.strip().startswith('{'):
        try:
            resp = json.loads(line.strip())
            if resp.get("id") == 3:
                content = resp.get("result", {}).get("content", [])
                if content:
                    text = content[0].get("text", "")
                    print(f"Auth Status: {text[:300]}")
            elif resp.get("id") == 4:
                content = resp.get("result", {}).get("content", [])
                if content:
                    text = content[0].get("text", "")
                    print(f"\nQR Code Response: {text[:500]}")
                    # Check if there's an image
                    if "qr" in text.lower() or "data" in text.lower() or "png" in text.lower():
                        print("QR code data received!")
        except:
            print(f"  Raw: {line[:200]}")
    elif line.strip():
        print(f"  {line[:200]}")

if proc.poll() is None:
    proc.terminate()
