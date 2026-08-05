# SearXNG Local Instance Configuration Reference

## Problem: SearXNG Returns 403 Forbidden from Local Docker

**Symptoms:**
- `curl http://localhost:8081/search?q=test&format=json` → 403 Forbidden
- Container runs but denies all requests from Docker host IP

## Root Cause

SearXNG's bot detection/limiter blocks requests from untrusted IPs. The Docker host appears as `172.17.0.1` (bridge gateway) from inside the container, which is not in the default `trusted_proxies` or `pass_ip` lists.

## Required Configuration Files

### 1. `/etc/searxng/settings.yml` (or `/usr/local/searxng/searx/settings.yml`)

```yaml
use_default_settings: true

server:
  secret_key: "your-secret-key-here"
  image_proxy: true
  limiter: false                    # CRITICAL: Disable rate limiting for local use
  public_instance: false
  trusted_proxies:                  # CRITICAL: Add Docker networks
    - '127.0.0.0/8'
    - '::1'
    - '172.16.0.0/12'               # Docker bridge networks
    - '10.0.0.0/8'                  # Docker default bridge
    - '192.168.0.0/16'              # Common local networks
  default_http_headers:
    X-Content-Type-Options: nosniff
    X-Download-Options: noopen
    X-Robots-Tag: noindex, nofollow
    Referrer-Policy: no-referrer

search:
  formats:
    - html
    - json                          # CRITICAL: Enable JSON output
    - csv
    - rss

botdetection:
  trusted_proxies:                  # CRITICAL: Mirror server.trusted_proxies
    - '127.0.0.0/8'
    - '::1'
    - '172.16.0.0/12'
    - '10.0.0.0/8'
    - '192.168.0.0/16'
```

### 2. `/etc/searxng/limiter.toml` (or `/usr/local/searxng/searx/limiter.toml`)

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
pass_ip = [
  '127.0.0.1',
  '::1',
  '172.17.0.1',      # Docker host from container perspective
  '172.16.0.0/12',
  '10.0.0.0/8',
  '192.168.0.0/16'
]
pass_searxng_org = true
```

## Docker Compose Example

```yaml
version: '3.8'
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8081:8080"
    volumes:
      - ./settings.yml:/etc/searxng/settings.yml:ro
      - ./limiter.toml:/etc/searxng/limiter.toml:ro
    environment:
      - SEARXNG_BASE_URL=http://localhost:8081
      - SEARXNG_SECRET_KEY=your-secret-key
    restart: unless-stopped
```

## Python Dependencies (if building custom image)

```dockerfile
RUN pip install --no-cache-dir \
    msgspec \
    pyyaml \
    tomli \
    typing_extensions \
    httpx \
    pygments \
    granian \
    flask \
    blinker \
    whitenoise \
    flask_babel \
    markdown-it-py \
    httpx_socks \
    valkey \
    lxml \
    typer \
    python-dateutil \
    isodate \
    h2
```

## Verification

```bash
# Test JSON endpoint
curl "http://localhost:8081/search?q=test&format=json"

# Expected: 200 OK with JSON results array
# {"query": "test", "results": [...], "corrections": [], "infoboxes": [], ...}

# Test HTML endpoint
curl "http://localhost:8081/search?q=test"

# Expected: 200 OK with HTML
```

## Quick Fix for Existing Container

```bash
# 1. Copy fixed configs into container
docker cp settings.yml searxng:/etc/searxng/settings.yml
docker cp limiter.toml searxng:/etc/searxng/limiter.toml

# 2. Restart
docker restart searxng

# 3. Test
curl "http://localhost:8081/search?q=test&format=json"
```

## Related Skills

- `sentinel-local-system-awareness` — System verification protocol
- `exec-local-service-management` — Local service management
- `linkedin-local-data-extraction` — Uses SearXNG as fallback search