#!/usr/bin/env python3
"""
Telegram MCP Server — Authentication Setup Helper

Run this script to complete Telegram authentication when ready.
The MCP server is currently DISABLED in config to prevent popup spam.

Usage:
    python telegram_auth_setup.py

This will start the mcp-telegram server and open a local sign-in page.
Complete the phone number verification in the browser, then re-enable
the server in config.yaml by setting `enabled: true` under the telegram
mcp_server entry.
"""
import subprocess
import os
import time

def main():
    env = os.environ.copy()
    env["TELEGRAM_API_ID"] = "35584659"
    env["TELEGRAM_API_HASH"] = "a64ced2efc33afbd0228a18686032fcf"
    env["TELEGRAM_AGENT_HOME"] = "/c/Users/apviz/.telegram-agent"
    env["LOG_LEVEL"] = "info"
    
    print("Starting Telegram MCP server for authentication...")
    print(f"Session dir: {env['TELEGRAM_AGENT_HOME']}")
    print("A browser window will open. Complete the sign-in in your browser.")
    print("Press Ctrl+C when done.")
    print()
    
    proc = subprocess.Popen(
        [r"C:\Program Files\nodejs\npx.cmd", "-y", "mcp-telegram"],
        env=env
    )
    
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        print("\nServer stopped.")
        print("\nTo re-enable Telegram MCP in Hermes:")
        print("  Edit profiles/default/config.yaml")
        print("  Find the telegram mcp_server entry")
        print("  Set 'enabled: true' and restart Hermes")

if __name__ == "__main__":
    main()
