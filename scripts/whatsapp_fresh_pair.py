#!/usr/bin/env python3
"""
FRESH WhatsApp pairing - SINGLE instance approach.

Key insight from source code analysis:
- mcp-whatsapp-web automatically emits pairing codes when WHATSAPP_PAIRING_PHONE_NUMBER env var is set
- The code is printed to STDERR (not stdout), bypassing MCP protocol
- The QR code is stored in latestQrCode, which is required before requestPairingCode() can work
- Running multiple instances corrupts session state

This script:
1. Kills ALL existing node processes running mcp-whatsapp-web
2. Clears the session cache completely
3. Starts ONE single MCP server instance WITH the phone number env var
4. Captures the pairing code from stderr
5. Waits for the pairing code to appear
"""
import subprocess
import os
import shutil
import time
import sys
import signal

# Step 1: Kill ALL existing node processes
print("1. Killing all existing node processes...")
subprocess.run("taskkill /F /FI \"IMAGENAME eq node.exe\" 2>nul || true", shell=True, capture_output=True)
subprocess.run("taskkill /F /FI \"IMAGENAME eq npm.cmd\" 2>nul || true", shell=True, capture_output=True)
# Also kill any puppeteer/chrome processes
subprocess.run("taskkill /F /FI \"IMAGENAME eq chrome.exe\" 2>nul || true", shell=True, capture_output=True)
subprocess.run("taskkill /F /FI \"IMAGENAME eq puppeteer*\" 2>nul || true", shell=True, capture_output=True)
time.sleep(3)

# Step 2: Clear session cache completely
print("2. Clearing session cache...")
session_path = r"C:\Users\apviz\.whatsapp-sessions"
if os.path.exists(session_path):
    shutil.rmtree(session_path, ignore_errors=True)
    print(f"   Cleared: {session_path}")
os.makedirs(session_path, exist_ok=True)

# Step 3: Start ONE single MCP server instance with the phone number
print("3. Starting WhatsApp MCP server with phone number...")

env = os.environ.copy()
env["WHATSAPP_PAIRING_PHONE_NUMBER"] = "40722121752"
env["WHATSAPP_HEADLESS"] = "true"
env["WHATSAPP_BROWSER"] = "chrome"
env["WHATSAPP_SESSION_DIR"] = session_path

# Start the process - capture both stdout and stderr separately
proc = subprocess.Popen(
    ["C:\\Program Files\\nodejs\\node.exe",
     "C:\\Users\\apviz\\AppData\\Roaming\\npm\\node_modules\\mcp-whatsapp-web/dist/index.js"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    env=env,
    bufsize=1,
    universal_newlines=True
)

# Send MCP initialize
proc.stdin.write(json_str := '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}\n')
proc.stdin.flush()

print("4. Waiting for pairing code (checking stderr)...")
print("   (This may take 10-20 seconds for the WhatsApp Web client to initialize)")

# Wait for pairing code in stderr
pairing_code = None
import threading
stdout_lines = []
stderr_lines = []

def read_stdout():
    for line in proc.stdout:
        stdout_lines.append(line)

def read_stderr():
    global pairing_code
    for line in proc.stderr:
        stderr_lines.append(line)
        # Look for the pairing code in stderr
        if "WhatsApp pairing code:" in line:
            # Extract the 8-character code
            import re
            match = re.search(r'pairing code: (\w+)', line)
            if match:
                pairing_code = match.group(1)
                # Signal that we found it
                proc.terminate()

# Start reader threads
stdout_thread = threading.Thread(target=read_stdout, daemon=True)
stderr_thread = threading.Thread(target=read_stderr, daemon=True)
stdout_thread.start()
stderr_thread.start()

# Wait up to 40 seconds for the pairing code
for i in range(40):
    if pairing_code:
        break
    time.sleep(1)
    if i % 10 == 0 and i > 0:
        print(f"   Still waiting... ({i}s elapsed)")

# Kill the process
proc.kill()

print("\n=== RESULTS ===")
if pairing_code:
    print(f"\n{'='*50}")
    print(f"  ✅ WHATSAPP PAIRING CODE: {pairing_code}")
    print(f"  Phone: +40722121752")
    print(f"  Enter this code on WhatsApp: Settings > Linked Devices")
    print(f"  > Link a device > 'Link with phone number instead'")
    print(f"  Code expires in ~3 minutes")
    print(f"{'='*50}")
else:
    print("\n  ❌ Pairing code not received within 40 seconds")
    print("  stderr output:")
    for line in stderr_lines:
        print(f"  {line.rstrip()}")
    print("\n  stdout output:")
    for line in stdout_lines:
        print(f"  {line.rstrip()}")

# Save the pairing code to a file for reference
if pairing_code:
    with open(r"C:\Users\apviz\AppData\Local\hermes\scripts\whatsapp_pairing_code.txt", "w") as f:
        f.write(pairing_code)
    print(f"\n  Pairing code saved to: C:\\Users\\apviz\\AppData\\Local\\hermes\\scripts\\whatsapp_pairing_code.txt")
