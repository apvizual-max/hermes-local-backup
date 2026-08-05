#!/usr/bin/env python3
"""Debug WhatsApp pairing - capture ALL output including Chrome logs."""
import subprocess
import json
import threading
import time
import sys
import os

def main():
    # Clear session
    session_path = r"C:\Users\apviz\.whatsapp-sessions"
    import shutil
    if os.path.exists(session_path):
        shutil.rmtree(session_path, ignore_errors=True)
    os.makedirs(session_path, exist_ok=True)

    env = os.environ.copy()
    env["WHATSAPP_PAIRING_PHONE_NUMBER"] = "40722121752"
    env["WHATSAPP_HEADLESS"] = "true"
    env["WHATSAPP_BROWSER"] = "chrome"
    env["WHATSAPP_SESSION_DIR"] = session_path

    proc = subprocess.Popen(
        [r"C:\Program Files\nodejs\node.exe",
         r"C:\Users\apviz\AppData\Roaming\npm\node_modules\mcp-whatsapp-web/dist/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )

    output_lines = []
    
    def reader(stream, prefix):
        for line in stream:
            output_lines.append(f"[{prefix}] {line.rstrip()}")
    
    t_stdout = threading.Thread(target=reader, args=(proc.stdout, "STDOUT"), daemon=True)
    t_stderr = threading.Thread(target=reader, args=(proc.stderr, "STDERR"), daemon=True)
    t_stdout.start()
    t_stderr.start()

    # Initialize MCP
    init_msg = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}
    proc.stdin.write(json.dumps(init_msg) + "\n")
    proc.stdin.flush()
    
    print("Waiting 30 seconds for WhatsApp client to initialize...")
    time.sleep(30)

    # Send initialized notification
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n")
    proc.stdin.flush()
    time.sleep(2)

    # Request pairing code
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "request_pairing_code", "arguments": {"phone_number": "40722121752"}}}) + "\n")
    proc.stdin.flush()
    
    print("Waiting 30 seconds for pairing code...")
    time.sleep(30)

    # Check auth status
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "check_auth_status", "arguments": {}}}) + "\n")
    proc.stdin.flush()
    time.sleep(10)

    proc.kill()
    
    print("\n=== ALL OUTPUT ===")
    for line in output_lines:
        print(line)

if __name__ == "__main__":
    main()
