#!/usr/bin/env python3
"""Fix MCP server configurations after Hermes update."""
from pathlib import Path

# Paths
HERMES_ROOT = Path(r"C:\Users\apviz\AppData\Local\hermes")
CONFIG = HERMES_ROOT / "config.yaml"
PROFILE_CONFIG = HERMES_ROOT / "profiles" / "default" / "config.yaml"

# System paths (working installations)
SYS_NPX = r'"C:\Program Files\nodejs\npx.cmd"'
PY_VENV = r'"C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"'

replacements = [
    # Fix npx commands to use system node
    ("command: npx", f"command: {SYS_NPX}"),
    # Fix uvx commands to use Python venv
    ("command: uvx", f"command: {PY_VENV}"),
    # Fix agent-browser path
    (r"command: C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd",
     r'command: "C:\Users\apviz\AppData\Roaming\npm\agent-browser.cmd"'),
    # Fix git server args (was using broken uvx --with mcp<2)
    ("args:\n      - --with\n      - mcp<2\n      - mcp-server-git",
     "args:\n      - -m\n      - mcp_server_git"),
    # Fix blender server args
    ("args:\n      - --with\n      - mcp<2\n      - blender-mcp==1.6.4",
     "args:\n      - -m\n      - blender_mcp.server"),
]

for config_path in [CONFIG, PROFILE_CONFIG]:
    if config_path.exists():
        content = config_path.read_text()
        original = content
        for old, new in replacements:
            content = content.replace(old, new)

        if content != original:
            config_path.write_text(content)
            print(f"✅ Fixed: {config_path}")
        else:
            print(f"⚠️  No changes needed: {config_path}")
    else:
        print(f"❌ Not found: {config_path}")

print("\n--- Verification ---")
# Verify
content = CONFIG.read_text()
npx_fixed = SYS_NPX.strip('"') in content
uvx_fixed = PY_VENV.strip('"') in content
print(f"npx fixed: {npx_fixed}")
print(f"uvx fixed: {uvx_fixed}")
