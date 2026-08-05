# Telegram BotFather Privacy Configuration Guide

## Overview

Settings that cannot be configured via the Telegram Bot API and must be set manually through `@BotFather`.

## Step-by-Step BotFather Commands

### 1. Set Privacy Mode

```
1. Open @BotFather on Telegram (via Telegram mobile app)
2. Send: /setprivacy
3. Select your bot: @sentinelprime911_bot
4. Select: "Turn on privacy mode"
   → Bot will only read messages that start with / in groups
```

### 2. Disable Group Joining

```
1. In @BotFather, send: /setjoingroups
2. Select your bot: @sentinelprime911_bot
3. Select: "Disable"
   → Bot cannot be added to groups (truly private)
```

### 3. Disable Inline Mode

```
1. In @BotFather, send: /setinline
2. Select your bot: @sentinelprime911_bot
3. Select: "Disable"
   → Bot won't appear in inline search results
```

## What Each Setting Does

| Setting | Enabled (Default) | Disabled |
|---------|------------------|----------|
| Privacy Mode | Bot only sees messages starting with / in groups | Bot sees ALL messages in groups |
| Group Joining | Bot can be added to groups | Bot cannot be added to groups |
| Inline Mode | Bot appears in inline search | Bot won't appear in inline search |

## Verification

After setting all three to private mode:

```python
import json, urllib.request
BOT_TOKEN = "8677539910:***"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
me = json.loads(urllib.request.urlopen(f"{API}/getMe").read())
bot = me["result"]
print(f"Bot: @{bot['username']}")
print(f"Can join groups: {bot.get('can_join_groups', True)}")
print(f"Inline mode: {bot.get('supports_inline_queries', True)}")
```

## Notes

- BotFather commands only work for bots you created
- Bot name: `sentinelprime911_bot`
- Bot ID: `8677539910`
- Token starts with `8677539910:`
- Changes take effect immediately