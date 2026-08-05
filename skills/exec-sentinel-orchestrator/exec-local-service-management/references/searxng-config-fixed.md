---
title: SearXNG Fixed Configuration (Session 2026-07-15)
description: Working SearXNG config after fixing 403 errors and container restart loops
---

# SearXNG Fixed Configuration

## Problem Summary

SearXNG container (`searxng/searxng:latest`) was returning 403 Forbidden and restarting continuously due to:
1. Missing Python dependencies (`msgspec`, `pyyaml`, `tomli`, `typing_extensions`, `httpx`, `granian`, `flask_babel`, `markdown-it-py`, `httpx_socks`, `valkey`, `lxml`, `typer`, `python-dateutil`, `isodate`, `h2`)
2. Missing `botdetection.trusted_proxies` config for Docker host IP
3. Missing `search.formats` including `json`
4. TOML syntax error in `limiter.toml` ("Cannot overwrite a value")

## Root Cause

The default SearXNG image expects config files at `/etc/searxng/settings.yml` and `/etc/searxng/limiter.toml` but these weren't properly configured for local Docker access.

## Working Configuration Files

### `/etc/searxng/settings.yml`

```yaml
# Read the documentation before extending the defaults:
# https://docs.searxng.org/admin/settings/

use_default_settings: true

server:
  secret_key: "h2q8yoY1RMArDr4hXuMMjOkTZfSi6v"
  image_proxy: true
  limiter: false
  trusted_proxies:
    - "127.0.0.0/8"
    - "::1"
    - "172.16.0.0/12"
    - "10.0.0.0/8"
    - "192.168.0.0/16"
    - "172.17.0.0/16"

botdetection:
  trusted_proxies:
    - "127.0.0.0/8"
    - "::1"
    - "172.16.0.0/12"
    - "10.0.0.0/8"
    - "192.168.0.0/16"
    - "172.17.0.0/16"

search:
  formats: [html, json, csv, rss]
```

### `/etc/searxng/limiter.toml`

```toml
[botdetection]
ipv4_prefix = 32
ipv6_prefix = 48

trusted_proxies = [
  '127.0.0.0/8',
  '::1',
  '172.16.0.0/12',
  '10.0.0.0/8',
  '192.168.0.0/16',
  '172.17.0.0/16'
]

[botdetection.ip_limit]
filter_link_local = false
link_token = false

[botdetection.ip_lists]
block_ip = []
pass_ip = ['172.17.0.1', '127.0.0.1', '::1']
pass_searxng_org = true
```

## Fix Procedure

1. **Install missing Python deps in container:**
   ```bash
   docker exec -it <container> python3 -m pip install msgspec pyyaml tomli typing_extensions httpx granian flask_babel markdown-it-py httpx_socks valkey lxml typer python-dateutil isodate h2
   ```

2. **Copy fixed config files:**
   ```bash
   docker cp settings.yml <container>:/etc/searxng/settings.yml
   docker cp limiter.toml <container>:/etc/searxng/limiter.toml
   ```

3. **Restart container:**
   ```bash
   docker restart <container>
   ```

4. **Verify:**
   ```bash
   curl "http://localhost:8081/search?q=test&format=json"
   # Should return JSON with results array
   ```

## Key Learnings

- **Docker host IP** from container perspective is typically `172.17.0.1` (on default bridge network)
- **Trusted proxies** must include Docker network ranges (`172.16.0.0/12`, `172.17.0.0/16`)
- **Formats** must explicitly include `json` for API access
- **Limiter TOML** must not have duplicate keys (use single `pass_ip` array)
- **Missing deps** cause worker crashes → container restart loop

## Test Commands

```bash
# Health check
curl -s "http://localhost:8081/search?q=test&format=json" | jq '.results | length'

# Full response
curl -s "http://localhost:8081/search?q=python&format=json" | head -c 2000
```

## Container Used for Fix

The working instance runs as `searxng-debug` on port 8082 (original `searxng` on 8081 was broken). All deps installed, configs applied.