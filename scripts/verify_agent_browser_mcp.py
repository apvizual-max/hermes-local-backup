import os
import subprocess
import json
import yaml

configs = [
    r"C:\Users\apviz\AppData\Local\hermes\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\prime\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\assist\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\cli-prime\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\coder\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\cowork\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\designer\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\trader\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\profiles\translator\config.yaml",
    r"C:\Users\apviz\AppData\Local\hermes\state-snapshots\20260711-095000-optimal-config\config.yaml",
]

all_passed = True
print("=== VERIFYING CONFIGURATIONS ===")
for config_path in configs:
    if not os.path.exists(config_path):
        print(f"[FAIL] Config missing: {config_path}")
        all_passed = False
        continue
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        mcp_servers = data.get("mcp_servers", {})
        agent_browser_cfg = mcp_servers.get("agent-browser", {})
        
        cmd = agent_browser_cfg.get("command", "")
        args = agent_browser_cfg.get("args", [])
        
        if cmd == r"C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd" and args == ["mcp", "--tools", "all"]:
            print(f"[OK] Configuration matched: {config_path}")
        else:
            print(f"[FAIL] Configuration mismatch in {config_path}: cmd='{cmd}', args={args}")
            all_passed = False
    except Exception as e:
        print(f"[FAIL] Error reading {config_path}: {e}")
        all_passed = False

print("\n=== VERIFYING NATIVE BINARY & VERSION ===")
cmd_path = r"C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd"
if not os.path.exists(cmd_path):
    print(f"[FAIL] agent-browser.cmd missing at: {cmd_path}")
    all_passed = False
else:
    try:
        res = subprocess.run([cmd_path, "--version"], capture_output=True, text=True)
        version_out = res.stdout.strip() or res.stderr.strip()
        print(f"[OK] version checked: {version_out}")
        if "0.31.1" not in version_out:
            print(f"[FAIL] version is not 0.31.1 (found '{version_out}')")
            all_passed = False
    except Exception as e:
        print(f"[FAIL] Error checking version: {e}")
        all_passed = False

print("\n=== VERIFYING JSON-RPC INITIALIZATION & TOOLS LIST ===")
if os.path.exists(cmd_path):
    try:
        proc = subprocess.Popen(
            [cmd_path, "mcp", "--tools", "all"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # 1. Send initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-verify", "version": "1.0.0"}
            }
        }
        proc.stdin.write(json.dumps(init_req) + "\n")
        proc.stdin.flush()
        
        init_res_line = proc.stdout.readline()
        init_res = json.loads(init_res_line)
        
        # 2. Send tools/list
        list_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        proc.stdin.write(json.dumps(list_req) + "\n")
        proc.stdin.flush()
        
        list_res_line = proc.stdout.readline()
        list_res = json.loads(list_res_line)
        
        # Shutdown
        shutdown_req = {"jsonrpc": "2.0", "id": 3, "method": "shutdown"}
        proc.stdin.write(json.dumps(shutdown_req) + "\n")
        proc.stdin.flush()
        
        import time
        time.sleep(0.5)
        if proc.poll() is None:
            proc.terminate()
            
        server_name = init_res.get("result", {}).get("serverInfo", {}).get("name", "")
        server_ver = init_res.get("result", {}).get("serverInfo", {}).get("version", "")
        tools_list = list_res.get("result", {}).get("tools", [])
        
        if server_name == "agent-browser" and server_ver == "0.31.1" and len(tools_list) == 64:
            print(f"[OK] JSON-RPC test successful: server='{server_name}', version='{server_ver}', total_tools={len(tools_list)}")
        else:
            print(f"[FAIL] JSON-RPC verification mismatch: name='{server_name}', version='{server_ver}', total_tools={len(tools_list)}")
            all_passed = False
            
    except Exception as e:
        print(f"[FAIL] JSON-RPC communication failed: {e}")
        all_passed = False

if all_passed:
    print("\n=== SYSTEM VERIFICATION SUCCESSFUL: ALL CHECKS PASSED ===")
else:
    print("\n=== SYSTEM VERIFICATION FAILED ===")
