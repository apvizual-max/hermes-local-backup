#!/usr/bin/env python3
"""Test the WhatsApp MCP server (mcp-whatsapp-web)."""
import subprocess, json, os, time, sys

env = os.environ.copy()
env["WHATSAPP_SESSION_DIR"] = os.path.expanduser("~/.whatsapp-sessions")
env["WHATSAPP_HEADLESS"] = "true"
env["WHATSAPP_BROWSER"] = "chrome"

# We'll pipe a simple initialize + tools/list to see if the server starts
mcp_messages = [
    json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "clientInfo": {"name": "test", "version": "1.0"}}}),
    json.dumps({"jsonrpc": "2.0", "id": 2, "method": "notifications/initialized"}),
    json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/list"}),
]
input_data = "\n".join(mcp_messages) + "\n"

proc = subprocess.Popen(
    ["C:\\Program Files\\nodejs\\npx.cmd", "-y", "mcp-whatsapp-web"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env,
    text=True,
    cwd=r"C:\Users\apviz\AppData\Local\hermes"
)

try:
    stdout, stderr = proc.communicate(input=input_data, timeout=60)
    print("=== STDOUT ===")
    for line in stdout.strip().split('\n'):
        line = line.strip()
        if line.startswith('{'):
            resp = json.loads(line)
            if resp.get("id") == 3:
                tools = resp.get("result", {}).get("tools", [])
                print(f"\n✅ WhatsApp MCP server is responding!")
                print(f"   Available tools ({len(tools)}):")
                for t in tools:
                    print(f"     - {t.get('name')}: {t.get('description', '')[:60]}")
            elif resp.get("id") == 1:
                server_info = resp.get("result", {}).get("serverInfo", {})
                print(f"Server: {server_info.get('name', 'unknown')} v{server_info.get('version', 'unknown')}")
    
    if stderr:
        print("\n=== STDERR (first 300 chars) ===")
        print(stderr[:300])
except subprocess.TimeoutExpired:
    proc.kill()
    stdout, stderr = proc.communicate()
    print("⚠️ Server timed out (60s) - this may be normal for first run (QR code generation)")
    print("\n=== STDOUT ===")
    for line in (stdout or "").strip().split('\n'):
        line = line.strip()
        if line.startswith('{'):
            resp = json.loads(line)
            if resp.get("id") == 3:
                tools = resp.get("result", {}).get("tools", [])
                print(f"\n✅ WhatsApp MCP server is responding!")
                print(f"   Available tools ({len(tools)}):")
                for t in tools:
                    print(f"     - {t.get('name')}")
            elif resp.get("id") == 1:
                server_info = resp.get("result", {}).get("serverInfo", {})
                print(f"Server: {server_info.get('name', '?')} v{server_info.get('version', '?')}")
    
    if stderr:
        print("\n=== STDERR (first 500 chars) ===")
        print(stderr[:500])
