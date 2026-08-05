# Messaging Platform MCP Setup Guide

## Overview
This document covers the setup and configuration of messaging platform MCP servers for Hermes Agent on Windows.

## Installed Packages
All messaging packages are installed globally via npm:
```bash
npm install -g mcp-whatsapp-web discord-mcp mcp-telegram gmail-mcp
```

## Package Details

### WhatsApp (mcp-whatsapp-web)
- **npm package:** mcp-whatsapp-web
- **Auth method:** QR code pairing via WebAuthn
- **First run:** Scanning the QR code with your WhatsApp mobile app
- **Config entry:**
  ```yaml
  whatsapp:
    args:
      - -y
      - mcp-whatsapp-web
    command: C:/Program Files/nodejs/npx.cmd
    timeout: 60
  ```
- **Note:** Do NOT use `mcp-whatsapp` (v0.0.1) — it is a stub ("coming-soon")

### Discord (discord-mcp)
- **npm package:** discord-mcp v2.4.0
- **Auth method:** Discord Bot Token (environment variable)
- **Required env var:** `DISCORD_BOT_TOKEN`
- **Config entry:**
  ```yaml
  discord:
    args:
      - -y
      - discord-mcp
    command: C:/Program Files/nodejs/npx.cmd
    timeout: 60
  ```
- **Bot setup:** https://discord.com/developers/applications
- **Bot permissions needed:** bot scope with Send Messages, Read Messages, Attach Files

### Telegram (mcp-telegram)
- **npm package:** mcp-telegram v3.0.0
- **Auth method:** Telegram API credentials
- **Required env vars:** `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_API_TOKEN`
- **Config entry:**
  ```yaml
  telegram:
    args:
      - -y
      - mcp-telegram
    command: C:/Program Files/nodejs/npx.cmd
    timeout: 60
  ```
- **API credentials:** https://my.telegram.org/apps
- **Bot token:** Get from @BotFather on Telegram

### Gmail (gmail-mcp)
- **npm package:** gmail-mcp v2.4.0
- **Auth method:** OAuth2 flow via Google Cloud Console
- **Config entry:**
  ```yaml
  gmail:
    args:
      - -y
      - gmail-mcp
    command: C:/Program Files/nodejs/npx.cmd
    timeout: 60
  ```
- **Google Cloud setup:**
  1. Go to https://console.cloud.google.com/
  2. Create/select a project
  3. Enable Gmail API
  4. Create OAuth 2.0 Client ID (Desktop application)
  5. Download credentials JSON
  6. First run will prompt for auth

## Google Workspace MCP Servers

### google-workspace-mcp (v2.3.6)
- **Comprehensive server:** Drive, Docs, Sheets, Calendar, Gmail, Slides, Forms
- **Auth method:** OAuth2
- **Credential directory:** `~/.google-mcp/`
- **Setup script:** `python3 C:\Users\apviz\AppData\Local\hermes\scripts\setup_google_workspace.py`
- **After running setup:** Download OAuth JSON from Google Cloud Console → save as `credentials.json`
- **Config entry:**
  ```yaml
  google-workspace:
    args:
      - -y
      - google-workspace-mcp
    command: C:/Program Files/nodejs/npx.cmd
    timeout: 60
  ```

### Individual Google MCP Servers
- **mcp-google-drive** (v1.6.2): Google Drive CRUD operations
- **google-calendar-mcp** (v1.0.9): Calendar event management

## Environment Variables Quick Reference

| Variable | Platform | Source |
|----------|----------|--------|
| `DISCORD_BOT_TOKEN` | Discord | discord.com/developers |
| `TELEGRAM_API_ID` | Telegram | my.telegram.org |
| `TELEGRAM_API_HASH` | Telegram | my.telegram.org |
| `TELEGRAM_API_TOKEN` | Telegram | @BotFather |
| `GOOGLE_CLIENT_ID` | Google Workspace | Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Google Workspace | Google Cloud Console |

## Verification
After providing credentials, verify each MCP server:
```bash
# Check if MCP servers load
hermes mcp list
# Test individual server
hermes mcp test whatsapp
hermes mcp test discord
hermes mcp test telegram
hermes mcp test gmail
```
