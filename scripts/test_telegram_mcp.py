#!/usr/bin/env python3
"""Test the Telegram Bot MCP server."""
import subprocess, json, os, sys, time

# 🛡️ Sentinel: Read token from environment variable
api_token = os.environ.get("TELEGRAM_API_TOKEN")
if not api_token:
    print("❌ ERROR: TELEGRAM_API_TOKEN environment variable not set.", file=sys.stderr)
    print("Please set it to your bot token before running this script.", file=sys.stderr)
    sys.exit(1)

env = os.environ.copy()
env["TELEGRAM_API_TOKEN"] = api_token

# Start the server process
proc = subprocess.Popen(
    [r"C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe", "-m",
     "telegram_bot_mcp.server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env,
    cwd=r"C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\telegram-bot-mcp\src",
    text=True
)

# Send initialize
init = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "test", "version": "1.0"}}}) + "\n"
proc.stdin.write(init)
proc.stdin.flush()
time.sleep(2)

# Read response
init_resp = proc.stdout.readline()
print("Init response:", init_resp[:200] if init_resp else "no response")

# Send initialized notification
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "initialized"}) + "\n")
proc.stdin.flush()
time.sleep(0.5)

# Call tg_get_me
call = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "tg_get_me", "arguments": {}}}) + "\n"
proc.stdin.write(call)
proc.stdin.flush()
time.sleep(3)

# Read response
call_resp = proc.stdout.readline()
print("Call response:", call_resp[:200] if call_resp else "no response")

# Parse the result
if call_resp.strip().startswith('{'):
    resp = json.loads(call_resp.strip())
    if "result" in resp:
        content = resp.get("result", {}).get("content", [])
        if content:
            text = content[0].get("text", "")
            try:
                data = json.loads(text)
                bot = data.get("result", {}).get("username", "unknown")
                print(f"\n✅ Telegram bot verified: @{bot}")
                print(f"   Full data: {json.dumps(data, indent=2)}")
            except:
                print(f"Raw text: {text}")
    elif "error" in resp:
        print(f"❌ Error: {resp['error']}")

proc.kill()
