#!/usr/bin/env python3
"""
Telegram MCP Server — Authentication Setup (if needed later).

The mcp-telegram server is currently DISABLED in config.yaml:
  - platforms.telegram.enabled: false
  - mcp_servers.telegram.enabled: false

The browser auto-login is also DISABLED in the npm package source code:
  (commented out in node_modules/mcp-telegram/dist/index.js)

To re-enable Telegram later:
1. Uncomment the runBrowserLogin block in node_modules/mcp-telegram/dist/index.js
2. Set enabled: true in config.yaml for both telegram sections
3. Restart Hermes Desktop
"""
print("Telegram MCP is disabled. See comments in this file for re-enable instructions.")
