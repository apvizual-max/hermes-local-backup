#!/usr/bin/env python3
"""
Telegram MCP Server (Bot API mode) - uses bot token, no phone auth needed.

This is a lightweight MCP server that wraps the Telegram Bot API.
It uses the bot token from TELEGRAM_API_TOKEN environment variable.

Usage:
  Set env vars:
    TELEGRAM_API_TOKEN=your_bot_token
    TELEGRAM_API_ID=(optional, for MTProto features)
    TELEGRAM_API_HASH=(optional, for MTProto features)

  Configure in Hermes config.yaml:
    telegram-bot:
      args:
        - -m
        - telegram_bot_mcp.server
      command: C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
      timeout: 60
"""
import os
import json
import aiohttp
from fastmcp import FastMCP

BOT_TOKEN = os.environ.get("TELEGRAM_API_TOKEN", "")
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

mcp = FastMCP("telegram-bot-mcp")

@mcp.tool()
async def tg_get_me() -> str:
    """Get information about the bot."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/getMe") as resp:
            data = await resp.json()
            return json.dumps(data, indent=2)

@mcp.tool()
async def tg_get_updates(offset: int = 0, limit: int = 100) -> str:
    """Get updates (messages, commands) for the bot. Use this to read incoming messages.
    
    Args:
        offset: Update offset (last_update_id + 1)
        limit: Max updates to return (default 100)
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/getUpdates", params={"offset": offset, "limit": limit}) as resp:
            data = await resp.json()
            return json.dumps(data, indent=2)

@mcp.tool()
async def tg_send_message(chat_id: str, text: str) -> str:
    """Send a message to a Telegram chat. chat_id can be a user ID, group ID, or @channelusername.
    
    Args:
        chat_id: Chat ID (user, group, or @channel)
        text: Message text
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE}/sendMessage", json={"chat_id": chat_id, "text": text}) as resp:
            data = await resp.json()
            return json.dumps(data, indent=2)

@mcp.tool()
async def tg_get_chat(chat_id: str) -> str:
    """Get information about a chat (group, channel, user).
    
    Args:
        chat_id: Chat ID
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/getChat", params={"chat_id": chat_id}) as resp:
            data = await resp.json()
            return json.dumps(data, indent=2)

@mcp.tool()
async def tg_get_webhook_info() -> str:
    """Get current webhook status."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/getWebhookInfo") as resp:
            data = await resp.json()
            return json.dumps(data, indent=2)

@mcp.tool()
async def tg_set_webhook(url: str) -> str:
    """Set webhook URL for receiving updates.
    
    Args:
        url: Webhook URL
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE}/setWebhook", json={"url": url}) as resp:
            data = await resp.json()
            return json.dumps(data, indent=2)

@mcp.tool()
async def tg_get_updates_alias(offset: int = 0, limit: int = 100) -> str:
    """Alias for tg_get_updates - get messages received by the bot."""
    return await tg_get_updates(offset=offset, limit=limit)

if __name__ == "__main__":
    if not BOT_TOKEN:
        import sys
        print("WARNING: TELEGRAM_API_TOKEN not set!", file=sys.stderr)
    mcp.run()
