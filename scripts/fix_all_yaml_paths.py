#!/usr/bin/env python3
"""Fix all remaining backslash Windows paths and MCP config issues in Hermes YAML config files.

This is the PRIMARY recovery script to run after any Hermes update that breaks MCP servers.

Run: python3 C:/Users/apviz/AppData/Local/hermes/scripts/fix_all_yaml_paths.py
"""
from pathlib import Path
import yaml

# All config files that need fixing
CONFIG_FILES = [
    Path(r"C:\Users\apviz\AppData\Local\hermes\config.yaml"),
    Path(r"C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml"),
    Path(r"C:\Users\apviz\AppData\Local\hermes\profiles\cli-prime\config.yaml"),
]


def fix_config(content: str) -> str:
    """Apply all fixes to config content."""
    # Fix backslash paths in quoted strings -> forward slashes
    content = content.replace("C:\\\\Users", "C:/Users")
    content = content.replace("C:\\\\Program Files", "C:/Program Files")
    content = content.replace("D:\\\\Alex", "D:/Alex")
    content = content.replace("E:\\\\CLAUDE", "E:/CLAUDE")

    # Fix agent-browser: change args from invalid "mcp" to npx agent-browser-mcp-server
    content = content.replace(
        'agent-browser:\n    args:\n      - mcp\n    - --version\n    command: C:/Users/apviz/AppData/Roaming/npm/agent-browser.cmd\n    timeout: 60',
        'agent-browser:\n    args:\n      - -y\n      - agent-browser-mcp-server@latest\n    command: C:/Program Files/nodejs/npx.cmd\n    timeout: 60'
    )

    # Fix blender module name
    content = content.replace(
        "-m blender_mcp.server",
        "-m blender_mcp_server.server"
    )

    # Fix git server: change uvx/mcp-server-git to venv python module
    content = content.replace(
        'command: uvx\n    args:\n      - --with\n      - mcp<2\n      - mcp-server-git',
        'command: C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe\n    args:\n      - -m\n      - mcp_server_git'
    )
    content = content.replace(
        'command: uv\n    args:\n      - mcp-server-git',
        'command: C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe\n    args:\n      - -m\n      - mcp_server_git'
    )

    # Fix postgresql module name
    content = content.replace(
        "-m postgres_mcp.server",
        "-m postgresql_mcp.server"
    )
    content = content.replace(
        "-m postgresql-mcp",
        "-m postgresql_mcp.server"
    )
    # content = content.replace("-m docker_mcp.server", "-m docker_mcp.server")

    # Fix chrome-devtools version pin: v2.4.0 doesn't exist, use v1.6.0
    content = content.replace(
        "chrome-devtools-mcp@2.4.0",
        "chrome-devtools-mcp@1.6.0"
    )

    # Fix obsidian vault path (forward slash variant)
    content = content.replace(
        "D:/Alex - KV Obsidian\\\\Alex - KV Obsidian",
        "D:/Alex - KV Obsidian/Alex - KV Obsidian"
    )
    content = content.replace(
        'D:\\Alex - KV Obsidian\\Alex - KV Obsidian',
        "D:/Alex - KV Obsidian/Alex - KV Obsidian"
    )

    return content


def main():
    print("🔧 Hermes MCP Recovery Script")
    print("=" * 50)

    for config_file in CONFIG_FILES:
        if not config_file.exists():
            print(f"  ⚠️  Skipped (not found): {config_file}")
            continue

        original = config_file.read_text()
        fixed = fix_config(original)

        if fixed != original:
            config_file.write_text(fixed)
            print(f"  ✅ Fixed: {config_file}")

            # Verify YAML is still valid
            try:
                list(yaml.safe_load_all(fixed))
                print(f"    ✓ YAML valid")
            except yaml.YAMLError as e:
                print(f"    ❌ YAML ERROR: {e}")
        else:
            print(f"  ✓ Already clean: {config_file}")

    print()
    print("=" * 50)
    print("🔍 Post-fix verification...")
    print("Run: hermes doctor --fix")
    print("Then verify MCP servers:")
    print("  timeout 5 C:\\Program Files\\nodejs\\npx.cmd -y @modelcontextprotocol/server-filesystem")
    print("  timeout 5 C:\\Program Files\\nodejs\\npx.cmd -y @huangyihe/obsidian-mcp")
    print("  C:\\Users\\apviz\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe -m docker_mcp.server")
    print("  C:\\Users\\apviz\\AppData\\Local\\hermes\\hermes-agent\\venv\\Scripts\\python.exe -m mcp_server_git")


if __name__ == "__main__":
    main()
