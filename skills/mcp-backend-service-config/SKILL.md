---
name: mcp-backend-service-config
description: "Docker backend services for MCP servers on Windows."
version: 1.0.0
author: Sentinel Prime
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [Docker, MCP, Backend, Services, Infrastructure, Windows]
---

# MCP Backend Service Configuration

## When to Use

When MCP servers need backend services (PostgreSQL, Redis, Vault, MinIO, Prometheus, Tempo, ElasticSearch, browser automation) to function. After any system restart or Docker cleanup.

See references/ for Tempo and compose templates.

## Quick Start: Start All Backends

```bash
docker run -d --name postgres-mcp -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16
docker run -d --name redis-mcp -p 6379:6379 redis:7-alpine
docker run -d --name vault-mcp -p 8200:8200 -e VAULT_DEV_ROOT_TOKEN_ID=root hashicorp/vault:1.15.0
docker run -d --name minio-mcp -p 9000:9000 -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin minio/minio server /data
docker run -d --name prometheus-mcp -p 9090:9090 prom/prometheus
docker run -d --name chrome-docker-cdp --shm-size=2gb -p 4446:4444 selenium/standalone-chrome:latest
```

**Tempo** requires S3 backend config (see references/tempo-config-troubleshooting.md).

## Service Registry

| Service | Container | Port | Image | Notes |
|---------|-----------|------|-------|-------|
| PostgreSQL | postgres-mcp | 5432 | postgres:16 | user: postgres, pass: postgres |
| Redis | redis-mcp | 6379 | redis:7-alpine | No auth |
| Vault | vault-mcp | 8200 | hashicorp/vault:1.15.0 | Dev mode, token: root |
| MinIO | minio-mcp | 9000/9199 | minio/minio | minioadmin/minioadmin |
| Prometheus | prometheus-mcp | 9090 | prom/prometheus | Default config |
| Tempo | tempo | 3200 | grafana/tempo:2.5.0 | Needs S3 backend |
| Elasticsearch | elasticsearch | 9200 | elasticsearch:8.12.2 | Pre-existing |
| SearXNG | searxng | 8081 | searxng/searxng | Pre-existing |
| Docker Chrome | chrome-docker-cdp | 4446->4444 | selenium/standalone-chrome | Use 4446 to avoid conflicts |\n| System Chrome | (host) | 9222 | chrome.exe | CDP debug port |\n\n## Messaging Platform MCP Servers\n\nMessaging MCP servers are npm packages installed globally via `npx -y`:\n\n```bash\nnpm install -g mcp-whatsapp-web discord-mcp mcp-telegram gmail-mcp google-workspace-mcp mcp-google-drive google-calendar-mcp\n```\n\n| Platform | Package | Env Vars | Notes |\n|----------|---------|----------|-------|\n| WhatsApp | `mcp-whatsapp-web` | None | QR code pairing on first run |\n| Discord | `discord-mcp` | `DISCORD_BOT_TOKEN` | Create bot at discord.com/developers |\n| Telegram | `mcp-telegram` | `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_API_TOKEN` | Get from my.telegram.org. PITFALL: set `TELEGRAM_AGENT_HOME` env var and `cwd` to user home to avoid path concatenation bug. Timeout 120s. |
| Telegram (Bot API) | Custom `telegram-bot-mcp` (Python/FastMCP) | `TELEGRAM_API_TOKEN` | Lightweight wrapper using bot token instead of MTProto. See `references/telegram_mcp_setup.md`. |\n| Gmail | `gmail-mcp` | OAuth2 flow | Google Cloud Console |\n| Google Drive | `mcp-google-drive` | OAuth2 flow | Google Cloud Console |\n| Google Calendar | `google-calendar-mcp` | OAuth2 flow | Google Cloud Console |\n| Google Workspace | `google-workspace-mcp` | OAuth2 flow | Comprehensive: Drive, Docs, Sheets, Calendar, Gmail, Slides, Forms |\n\n**Google Workspace credentials directory:** `~/.google-mcp/` (create with `python3 setup_google_workspace.py`)
**WhatsApp note:** `mcp-whatsapp` v0.0.1 is a stub — use `mcp-whatsapp-web` instead.
**Gmail note:** `mcp-gmail` is an alternative using refresh tokens (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`).

## Browser Automation

### System Chrome with CDP
```bash
"C:\Program Files\Google\Chrome Dev\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\Users\apviz\AppData\Local\Hermes\cdp-profile" ^
  --no-first-run --no-default-browser-check about:blank
```

### Docker Chrome (Selenium)
```bash
docker run -d --name chrome-docker-cdp --shm-size=2gb -p 4446:4444 selenium/standalone-chrome:latest
```

## Verification

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
curl -s http://localhost:8200/v1/sys/health  # Vault
curl -s http://localhost:9090/-/healthy       # Prometheus
curl -s http://localhost:9222/json/version    # System Chrome CDP
curl -s http://localhost:4446/status          # Docker Chrome WebDriver
```

## References\n\n- `references/tempo-config-troubleshooting.md`\n- `references/docker-compose-services.yaml`\n- `references/messaging-platforms-setup.md` — WhatsApp, Discord, Telegram, Gmail MCP server setup
