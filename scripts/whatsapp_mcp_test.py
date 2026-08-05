#!/usr/bin/env python3
"""
Communicate with the WhatsApp MCP server.
Sends MCP initialize, notifications/initialized, then tools/list and get_qr_code.
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

# Start a fresh server process
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
    '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}',
]

# Send all messages
for msg in messages:
    proc.stdin.write((msg + "\n").encode())
    proc.stdin.flush()
    time.sleep(2)

time.sleep(5)

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

print("\n=== Server Output ===")
for line in output_lines:
    if line.strip().startswith('{'):
        try:
            resp = json.loads(line.strip())
            if resp.get("id") == 1:
                server_info = resp.get("result", {}).get("serverInfo", {})
                print(f"Initialize: {server_info.get('name', '?')} v{server_info.get('version', '?')}")
            elif resp.get("id") == 2:
                tools = resp.get("result", {}).get("tools", [])
                print(f"\n✅ WhatsApp MCP server responding!")
                print(f"Tools available ({len(tools)}):")
                for tool in tools:
                    print(f"  - {tool.get('name', '?')}")
        except:
            print(f"  JSON: {line[:200]}")
    elif line.strip():
        print(f"  {line[:200]}")

# Check auth status
auth_check = json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "check_auth_status", "arguments": {}}}) + "\n"
proc.stdin.write(auth_check.encode())
proc.stdin.flush()
time.sleep(5)

# Read more output
for line in output_lines:
    if line.strip().startswith('{"id":3'):
        try:
            resp = json.loads(line.strip())
            content = resp.get("result", {}).get("content", [])
            if content:
                text = content[0].get("text", "")
                print(f"\nAuth status: {text[:200]}")
        except:
            pass

if proc.poll() is None:
    print("\n✅ Server still running - ready for QR code generation")
else:
    print(f"\n❌ Server exited: {proc.returncode}")
