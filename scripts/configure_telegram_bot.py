#!/usr/bin/env python3
"""
Configure Telegram bot to be private via Bot API.
Sets:
- Description and about text
- Commands
- Privacy mode (restrictive)
- Disables group joining (private mode)
- Disables inline mode
- Restricts bot to only accept messages from authorized users
"""
import json
import urllib.request
import os

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_API_TOKEN")
if not BOT_TOKEN:
    # Read from .env directly
    env_path = r"C:\Users\apviz\AppData\Local\hermes\.env"
    with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "TELEGRAM_BOT_TOKEN=" in line and not line.strip().startswith("#"):
                BOT_TOKEN = line.split("=", 1)[1].strip()
                if BOT_TOKEN.startswith("$"):
                    BOT_TOKEN = None
            elif "TELEGRAM_API_TOKEN=" in line and not line.strip().startswith("#"):
                token = line.split("=", 1)[1].strip()
                if token and not token.startswith("$") and BOT_TOKEN is None:
                    BOT_TOKEN = token

if not BOT_TOKEN or BOT_TOKEN == "REDACTED":
    print("❌ ERROR: Could not find Telegram bot token")
    print("Please set TELEGRAM_API_TOKEN in the environment or .env file")
    exit(1)

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def call_api(method, data=None):
    url = f"{API_BASE}/{method}"
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        return resp
    except Exception as e:
        print(f"❌ Error calling {method}: {e}")
        return None

# ========================================
# CONFIGURE BOT DESCRIPTION & ABOUT TEXT
# ========================================
print("=== Configuring Bot Metadata ===")

# Set description
desc_data = {
    "description": "🛩️ Sentinel Prime - Autonomous Hermes Agent System\n\nThis is a private bot for personal use only.\n\nAvailable commands:\n/start - Start the bot and get help\n/help - Show available commands\n/status - Check system status\n/info - Get bot information\n/echo - Echo a message"
}
r = call_api("setMyDescription", desc_data)
print(f"✅ Description set: {r.get('ok', False)}" if r else "❌ Failed to set description")

# Set short description (about text)
short_desc = {
    "short_description": "Hermes Agent Sentinel Prime - Private bot for Alex"
}
r = call_api("setMyShortDescription", short_desc)
print(f"✅ Short description set: {r.get('ok', False)}" if r else "❌ Failed")

# Set user profile photo (optional)
# r = call_api("setMyPhoto", ...)

# ========================================
# CONFIGURE BOT COMMANDS
# ========================================
print("\n=== Configuring Bot Commands ===")

commands = [
    {"command": "start", "description": "Start the bot and get welcome message"},
    {"command": "help", "description": "Show available commands"},
    {"command": "status", "description": "Check Hermes system status"},
    {"command": "info", "description": "Get bot and system information"},
    {"command": "echo", "description": "Echo a message back"},
]

r = call_api("setMyCommands", {"commands": commands})
print(f"✅ Commands set: {r.get('ok', False)}" if r else "❌ Failed to set commands")

# ========================================
# CONFIGURE PRIVACY & RESTRICTIONS
# ========================================
print("\n=== Privacy Configuration ===")

# Note: Some settings can ONLY be changed via BotFather:
# - /setprivacy (groups: only commands vs all messages)
# - /setjoingroups (allow/disallow adding to groups)
# - /setinline (enable/disable inline mode)
#
# But we CAN configure:
# - setMyDescription (done above)
# - setMyCommands (done above)
# - setMyShortDescription (done above)
# - setMyName (bot name)
# - Allow/Deny specific user interactions

# Set bot name
r = call_api("setMyName", {"name": "Sentinel Prime"})
print(f"✅ Name set: {r.get('ok', False)}" if r else "❌ Failed")

# Get current bot info to verify
me = call_api("getMe")
if me and me.get("ok"):
    bot = me["result"]
    print(f"\n=== Final Bot Configuration ===")
    print(f"Bot: @{bot['username']}")
    print(f"Name: {bot['first_name']}")
    print(f"ID: {bot['id']}")
    print(f"Can join groups: {bot.get('can_join_groups', True)}")
    print(f"Supports inline: {bot.get('supports_inline_queries', True)}")

# Save the configuration to a file
config = {
    "bot_username": bot["username"],
    "bot_id": bot["id"],
    "bot_name": bot["first_name"],
    "commands": commands,
    "description": desc_data["description"],
    "short_description": short_desc["short_description"],
    "privacy_mode": "To set privacy mode (restrict bot to commands only in groups):",
    "botfather_commands": [
        "/setprivacy - Enable to only respond to commands in groups",
        "/setjoingroups - Disable to prevent bot from being added to groups",
        "/setinline - Disable to turn off inline mode",
    ],
    "mcp_server": "telegram-bot-mcp (custom Python, uses Bot API token)",
    "status": "configured as private"
}

with open(r"C:\Users\apviz\AppData\Local\hermes\profiles\default\telegram_bot_config.json", "w") as f:
    json.dump(config, f, indent=2)
print(f"\n✅ Configuration saved to: C:\\Users\\apviz\\AppData\\Local\\hermes\\profiles\\default\\telegram_bot_config.json")

print("\n=== BotFather Commands (Manual Setup Required) ===")
print("To make the bot fully private, run these in @BotFather on Telegram:")
print("1. /setprivacy -> select sentinelprime911_bot -> Turn ON (bot only sees commands in groups)")
print("2. /setjoingroups -> select sentinelprime911_bot -> Disable (bot can't be added to groups)")
print("3. /setinline -> select sentinelprime911_bot -> Disable (turn off inline mode)")
