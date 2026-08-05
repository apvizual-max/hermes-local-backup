#!/usr/bin/env python3
"""Update the SENTINEL_CLI_PRIME_INTEGRATIONS snapshot with agent-browser and blender fixes."""
from pathlib import Path

p = Path(r"C:\Users\apviz\AppData\Local\hermes\profiles\default\SENTINEL_CLI_PRIME_INTEGRATIONS.md")
content = p.read_text()

# Update agent-browser entry in MCP server table
old_ab = "| `agent-browser` | Direct cmd path | agent-browser CLI | `C:/Users/apviz/AppData/Roaming/npm/agent-browser.cmd` | Direct cmd |"
# Let me just search and replace more broadly
# Find the agent-browser MCP server table row
if "agent-browser" in content.lower():
    # Update the npm packages section
    content = content.replace(
        "agent-browser@0.27.0,",
        "agent-browser-mcp-server@0.14.2, agent-browser@0.27.0,"
    )

# Add the agent-browser and blender fixes to the recovery log
content = content.replace(
    "4. **Created recovery script**:",
    "4. **Installed agent-browser-mcp-server** (`@0.14.2`) - replaced broken `agent-browser mcp` command with correct MCP server package\n5. **Fixed blender module name** from `blender_mcp.server` to `blender_mcp_server.server`\n6. **Created recovery script**:"
)

p.write_text(content)
print("✅ Snapshot updated with agent-browser and blender fixes")
