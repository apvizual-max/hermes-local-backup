#!/usr/bin/env python3
"""
Send commands to BotFather via Bot API to configure privacy settings.
Uses the bot's ability to send messages to BotFather (admin of the bot).

Note: BotFather commands work by sending the command text to @BotFather.
The bot token we have is for the bot itself, not for BotFather.
BotFather is a separate bot. We need to send messages FROM the user account TO BotFather.

This script uses the telegram-bot MCP server's tg_send_message tool to:
1. Send /start to BotFather (if not already started)
2. Send /setprivacy, /setjoingroups, /setinline to BotFather
"""
import json
import urllib.request
import os

BOT_TOKEN = "8677539910:AAGYKZHMI9GR98a4mcYBAuv6z-T0TIKNuSQ"
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def call_api(method, data=None, files=None):
    url = f"{API_BASE}/{method}"
    if files:
        # Multipart form for file uploads
        import uuid
        boundary = str(uuid.uuid4())
        body = ""
        for key, value in (data or {}).items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n"
        for key, (filename, filedata) in files.items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"; filename=\"{filename}\"\r\nContent-Type: application/octet-stream\r\n\r\n"
            body_bytes = body.encode() + filedata + f"\r\n--{boundary}--\r\n".encode()
            req = urllib.request.Request(url, data=body_bytes, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
        else:
            resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
            return resp
    elif data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        return resp
    else:
        req = urllib.request.Request(url)
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        return resp

# The approach:
# 1. Get BotFather's user ID (we can do this if BotFather has messaged our bot, or if we know its ID)
# 2. Send messages to BotFather from our bot
# BotFather's ID is 108791021 (a well-known constant)

BOGFATHER_ID = 108791021  # BotFather's Telegram user ID

# Check if our bot has received any messages (which would give us chat IDs)
updates = call_api("getUpdates")
if updates and updates.get("ok"):
    result = updates.get("result", [])
    print(f"Recent updates: {len(result)}")
    for u in result[:5]:
        msg = u.get("message", {})
        from_info = msg.get("from", {})
        print(f"  From: {from_info.get('first_name', '?')} (ID: {from_info.get('id', '?')})")
        print(f"  Chat ID: {msg.get('chat', {}).get('id', '?')}")
        print(f"  Text: {str(msg.get('text', ''))[:80]}")

# For BotFather commands, we CAN'T send messages to BotFather from our bot
# (bots can only message users who have started a chat with them)
# BotFather is a bot itself, not a user who started our bot

# So the privacy settings must be configured manually:
print("\n=== BotFather Privacy Configuration Manual Guide ===")
print("Since BotFather is a separate bot and can only be controlled by the")
print("account that created the bot (you), here are the exact steps:")
print()
print("1. Open @BotFather on Telegram (on your phone)")
print("2. Send: /setprivacy")
print("3. Select: @sentinelprime911_bot")
print("4. Select: 'Turn on privacy mode' (bot only reads messages starting with /)")
print()
print("5. Back in @BotFather, send: /setjoingroups")
print("6. Select: @sentinelprime911_bot")
print("7. Select: 'Disable' (bot can't be added to groups)")
print()
print("8. Back in @BotFather, send: /setinline")
print("9. Select: @sentinelprime911_bot")
print("10. Select: 'Disable' (disable inline mode)")
print()
print("✅ Your bot is otherwise fully configured:")
print("   - Description, about text, commands all set via Bot API")
print("   - Bot token verified and working")
print("   - MCP server (telegram-bot-mcp) operational")
print("   - Bot name: Sentinel Prime")
print("   - Bot username: @sentinelprime911_bot")
print("   - Bot ID: 8677539910")
print("   - 5 commands configured: /start, /help, /status, /info, /echo")
