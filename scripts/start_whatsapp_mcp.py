#!/usr/bin/env python3
"""Start WhatsApp MCP server with proper initialization."""
import subprocess
import json
import os
import time
import threading
import sys

env = os.environ.copy()
env["WHATSAPP_SESSION_DIR"] = r"C:\Users\apviz\.whatsapp-sessions"
env["WHATSAPP_HEADLESS"] = "true"
env["WHATSAPP_BROWSER"] = "chrome"

proc = subprocess.Popen(
    ["C:\\Program Files\\nodejs\\npx.cmd", "-y", "mcp-whatsapp-web"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env,
    cwd=r"C:\Users\apviz"
)

print(f"WhatsApp MCP server started (PID: {proc.pid})")
print("Waiting 30s for full initialization...", flush=True)
time.sleep(30)

# Send MCP initialize
init = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "hermes", "version": "1.0"}}}) + "\n"

proc.stdin.write(init.encode())
proc.stdin.flush()
time.sleep(5)

# Read any output
output = ""
try:
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        output += line.decode().rstrip()
        print(f"OUTPUT: {line.decode().rstrip()[:300]}")
except:
    pass

if output:
    print(f"\nTotal output: {len(output)} chars")
else:
    print("\nNo output received")

# Check if still running
if proc.poll() is None:
    print("✅ Server is running")
    # Keep it running and try to get tools list
    notif = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"
    tools = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}) + "\n"
    proc.stdin.write(notif.encode())
    proc.stdin.flush()
    time.sleep(1)
    proc.stdin.write(tools.encode())
    proc.stdin.flush()
    time.sleep(5)
    
    # Read
    try:
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(f"TOOL LIST: {line.decode().rstrip()[:300]}")
    except:
        pass
else:
    print(f"❌ Server exited with code {proc.returncode}")
    err = proc.stderr.read().decode()
    print(f"stderr: {err[:500]}")
