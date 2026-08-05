#!/usr/bin/env python3
"""
WhatsApp MCP Server - uses whatsapp-web.js for browser-based WhatsApp Web.

This MCP server wraps the whatsapp-web.js library to interact with WhatsApp Web.
The first run will generate a QR code for pairing with your phone's WhatsApp app.

Usage:
  Set env vars (optional):
    WHATSAPP_SESSION_FILE=path/to/session.json (to persist session)
    WHATSAPP_HEADLESS=true/false (default: true)

  Configure in Hermes config.yaml:
    whatsapp:
      args:
        - -m
        - whatsapp_mcp.server
      command: C:/Users/apviz/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
      timeout: 120
"""
import os
import json
import sys
import asyncio
from fastmcp import FastMCP

# Session data path
HOME_DIR = os.path.expanduser("~")
SESSION_DIR = os.path.join(HOME_DIR, ".whatsapp-mcp")
os.makedirs(SESSION_DIR, exist_ok=True)
SESSION_FILE = os.path.join(SESSION_DIR, "session.json")

mcp = FastMCP("whatsapp-mcp")

# Lazy-loaded whatsapp client
_client = None
_client_lock = asyncio.Lock()

def _get_client():
    """Get or create the WhatsApp Web client."""
    if _client is None:
        import whatsappWebClient
        _client = whatsappWebClient.Client({
            "session": json.load(open(SESSION_FILE)) if os.path.exists(SESSION_FILE) else None,
            "headless": True,
            "sessionData": None,
        })
    return _client

@mcp.tool()
async def wa_is_ready() -> str:
    """Check if the WhatsApp client is ready and connected."""
    try:
        from whatsapp_web import Client
    except ImportError:
        return json.dumps({"ok": False, "error": "whatsapp-web.js not installed"})

    client = Client({
        "session": json.load(open(SESSION_FILE)) if os.path.exists(SESSION_FILE) else None,
        "headless": True,
    })

    def on_ready():
        return True

    def on_qr(qr):
        print("🔐 WhatsApp QR Code generated. Scan with your phone's WhatsApp app.", file=sys.stderr)
        print(f"QR: {qr}", file=sys.stderr)

    client.on("ready", on_ready)
    client.on("qr", on_qr)

    try:
        await client.initialize()
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)})

    return json.dumps({"ok": True, "message": "WhatsApp client initialized"})

@mcp.tool()
async def wa_get_chats() -> str:
    """Get list of all WhatsApp chats."""
    from whatsapp_web import Client

    client = Client({"session": json.load(open(SESSION_FILE)) if os.path.exists(SESSION_FILE) else None})

    await client.initialize()
    chats = await client.get_chats()
    result = [{"id": chat.id, "name": chat.name} for chat in chats]
    await client.destroy()
    return json.dumps(result, indent=2)

@mcp.tool()
async def wa_send_message(chat_id: str, text: str) -> str:
    """Send a message to a WhatsApp chat.

    Args:
        chat_id: Chat ID (e.g., '1234567890-1234567890@g.us' or '1234567890@c.us')
        text: Message text to send
    """
    from whatsapp_web import Client

    client = Client({"session": json.load(open(SESSION_FILE)) if os.path.exists(SESSION_FILE) else None})
    await client.initialize()

    # Save session after init
    session = client.session
    with open(SESSION_FILE, "w") as f:
        json.dump(session, f)

    try:
        result = await client.send_message(chat_id, text)
        await client.destroy()
        return json.dumps({"ok": True, "message": "Message sent", "result": str(result)})
    except Exception as e:
        await client.destroy()
        return json.dumps({"ok": False, "error": str(e)})

@mcp.tool()
async def wa_get_messages(chat_id: str, limit: int = 10) -> str:
    """Get recent messages from a WhatsApp chat.

    Args:
        chat_id: Chat ID
        limit: Number of messages to retrieve (default 10)
    """
    from whatsapp_web import Client

    client = Client({"session": json.load(open(SESSION_FILE)) if os.path.exists(SESSION_FILE) else None})
    await client.initialize()

    try:
        chat = await client.get_chat(chat_id)
        messages = await chat.get_messages(limit)
        result = [{"id": m.id, "body": m.body, "from": m.from_me, "timestamp": m.timestamp} for m in messages]
        await client.destroy()
        return json.dumps(result, indent=2)
    except Exception as e:
        await client.destroy()
        return json.dumps({"ok": False, "error": str(e)})

@mcp.tool()
async def wa_get_qr_code() -> str:
    """Generate a QR code for initial WhatsApp Web pairing.

    First run: use this to generate QR code and scan with your phone.
    After: use existing session if available.
    """
    from whatsapp_web import Client

    qr_data = {"ok": False, "error": "No QR generated"}

    def qr_handler(qr):
        qr_data.update({"ok": True, "qr": qr})

    client = Client({
        "session": json.load(open(SESSION_FILE)) if os.path.exists(SESSION_FILE) else None,
    })

    client.on("qr", qr_handler)

    try:
        await asyncio.wait_for(client.initialize(), timeout=30)
    except asyncio.TimeoutError:
        if not qr_data.get("ok"):
            qr_data = {"ok": False, "error": "QR code not generated (no session file)"}
    except Exception as e:
        qr_data = {"ok": False, "error": str(e)}

    # Save session if we got one
    if hasattr(client, "session"):
        with open(SESSION_FILE, "w") as f:
            json.dump(client.session, f)

    await client.destroy()
    return json.dumps(qr_data, indent=2)

if __name__ == "__main__":
    mcp.run()
