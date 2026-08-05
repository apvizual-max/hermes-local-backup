#!/usr/bin/env python3
"""Test the Telegram Bot MCP server."""
import subprocess
import json
import os

env = os.environ.copy()
env["TELEGRAM_API_TOKEN"] = os.environ.get("TELEGRAM_API_TOKEN", "8677539910:AAGYKZHMI9GR98a4mcYBAuv6z-T0TIKNuSQ")

# Build all MCP messages
init = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "test", "version": "1.0"}}})
notif = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"})
call_me = json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "tg_get_me", "arguments": {}}})
call_updates = json.dumps({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "tg_get_updates", "arguments": {"limit": 1}}})

input_data = "\n".join([init, notif, call_me, call_updates]) + "\n"

# Start the server and communicate
proc = subprocess.Popen(
    ["C:\\Users\\apviz\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe", "-m", "telegram_bot_mcp.server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env,
    cwd=r"C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\telegram-bot-mcp\src",
    text=True
)

try:
    stdout, stderr = proc.communicate(input=input_data, timeout=15)
except subprocess.TimeoutExpired:
    proc.kill()
    stdout, stderr = proc.communicate()

print("=== Bot Info ===")
for line in (stdout or "").strip().split("\n"):
    line = line.strip()
    if line.startswith('{"id"'):
        try:
            resp = json.loads(line)
            if resp.get("id") == 3:
                content = resp.get("result", {}).get("content", [])
                if content:
                    text = content[0].get("text", "")
                    data = json.loads(text) if text else {}
                    bot = data.get("result", {})
                    print(f"Bot: @{bot.get('username')} (ID: {bot.get('id')})")
                    print(f"Name: {bot.get('first_name', '?')}")
                    print(f"Can join groups: {bot.get('can_join_groups')}")
        except Exception as e:
            print(f"  Error parsing: {e}")

print("\n=== Recent Messages ===")
for line in (stdout or "").strip().split("\n"):
    line = line.strip()
    if line.startswith('{"id"'):
        try:
            resp = json.loads(line)
            if resp.get("id") == 4:
                content = resp.get("result", {}).get("content", [])
                if content:
                    text = content[0].get("text", "")
                    data = json.loads(text) if text else {}
                    updates = data.get("result", [])
                    if updates:
                        print(f"Found {len(updates)} recent message(s):")
                        for u in updates[:3]:
                            msg = u.get("message", {})
                            from_info = msg.get("from", {})
                            print(f"  From: {from_info.get('first_name', '?')} (ID: {from_info.get('id')})")
                            print(f"  Text: {str(msg.get('text', ''))[:200]}")
                    else:
                        print("No messages received yet (bot has no conversations)")
        except Exception as e:
            print(f"  Error: {e}")

# Check for errors
if stderr and "ERROR" in stderr:
    print("\n=== Errors ===")
    for line in stderr.split("\n"):
        if "ERROR" in line or "Error" in line:
            print(line[:200])
