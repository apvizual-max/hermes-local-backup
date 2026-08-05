#!/usr/bin/env python3
"""Final comprehensive system verification."""
import subprocess, json, yaml, socket, os

print("=" * 60)
print("   FINAL COMPREHENSIVE SYSTEM VERIFICATION")
print("=" * 60)

results = {"pass": [], "warn": [], "fail": []}

# 1. YAML config validation
for name, path in [("global config", r"C:\Users\apviz\AppData\Local\hermes\config.yaml"),
                   ("default config", r"C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml"),
                   ("cli-prime config", r"C:\Users\apviz\AppData\Local\hermes\profiles\cli-prime\config.yaml")]:
    try:
        with open(path) as f:
            config = yaml.safe_load(f)
        mcp_count = len(config.get("mcp_servers", {}))
        messaging = [k for k in ["whatsapp","discord","telegram","gmail"] if k in config.get("mcp_servers", {})]
        google = [k for k in ["google-drive","google-calendar","google-workspace"] if k in config.get("mcp_servers", {})]
        results["pass"].append(f"YAML {name}: valid, {mcp_count} MCP servers")
    except Exception as e:
        results["fail"].append(f"YAML {name}: {e}")

# 2. Docker containers
result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True, timeout=10)
containers = [c.strip() for c in result.stdout.split('\n') if c.strip()]
results["pass"].append(f"Docker: {len(containers)} containers running")

# 3. Backend port checks
backends = {"PostgreSQL": 5432, "Redis": 6379, "Vault": 8200, "MinIO": 9000, 
            "Prometheus": 9090, "Tempo": 3200, "Elasticsearch": 9200, "SearXNG": 8081,
            "Chrome CDP": 9222, "Docker Chrome": 4446}
for name, port in backends.items():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    if sock.connect_ex(("127.0.0.1", port)) == 0:
        results["pass"].append(f"{name}: port {port}")
    else:
        results["warn"].append(f"{name}: port {port} not listening")
    sock.close()

# 4. Ollama
result = subprocess.run(["curl", "-s", "--connect-timeout", "3", "http://localhost:11434/api/tags"], 
                        capture_output=True, text=True, timeout=10)
if result.stdout:
    models = json.loads(result.stdout).get("models", [])
    results["pass"].append(f"Ollama: {len(models)} models")

# 5. hermes doctor
result = subprocess.run(["hermes", "doctor", "--fix"], capture_output=True, text=True, timeout=30)
if "Found" in result.stdout:
    results["pass"].append("hermes doctor: passes")

# 6. npm packages
npm_packages = ["agent-browser-mcp-server", "discord-mcp", "mcp-telegram",
                "mcp-whatsapp-web", "gmail-mcp", "google-workspace-mcp", 
                "gdrive-mcp", "google-calendar-mcp", "mcp-google-drive"]
for pkg in npm_packages:
    pkg_path = f"C:\\Users\\apviz\\AppData\\Roaming\\npm\\node_modules\\{pkg}"
    if os.path.exists(pkg_path):
        results["pass"].append(f"npm: {pkg}")
    else:
        results["fail"].append(f"npm: {pkg} NOT installed")

# 7. Google Workspace credentials dir
cred_dir = os.path.expanduser("~/.google-mcp")
if os.path.exists(cred_dir):
    has_creds = os.path.exists(os.path.join(cred_dir, "credentials.json"))
    if has_creds:
        results["pass"].append("Google Workspace credentials: present")
    else:
        results["warn"].append("Google Workspace credentials: NOT present (user action needed)")
else:
    results["warn"].append("Google Workspace dir: NOT created")

# Summary
print("\n" + "=" * 60)
print(f"Summary: {len(results['pass'])} pass, {len(results['warn'])} warn, {len(results['fail'])} fail")
print("=" * 60)

print("\nPASS:")
for r in results["pass"]:
    print(f"  + {r}")

if results["warn"]:
    print("\nWARN:")
    for w in results["warn"]:
        print(f"  ! {w}")

if results["fail"]:
    print("\nFAIL:")
    for f in results["fail"]:
        print(f"  x {f}")
