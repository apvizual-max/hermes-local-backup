#!/usr/bin/env python3
"""Test SearXNG MCP server end-to-end."""
import subprocess, json, threading, time

proc = subprocess.Popen(
    [r"C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe", "-m", "searxng_mcp.server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

output = []
def reader(stream):
    for line in stream:
        output.append(line)

t = threading.Thread(target=reader, args=(proc.stdout,), daemon=True)
t.start()

# Initialize
proc.stdin.write(json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}) + "\n")
proc.stdin.flush()
time.sleep(3)

proc.stdin.write(json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"}) + "\n")
proc.stdin.flush()
time.sleep(2)

# Search
proc.stdin.write(json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search","arguments":{"query":"test"}}}) + "\n")
proc.stdin.flush()
time.sleep(15)

proc.kill()

print("=== OUTPUT ===")
for line in output:
    print(line.rstrip())
