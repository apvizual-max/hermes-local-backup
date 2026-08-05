# Hermes-Obsidian Integration Dependencies

## Python Packages
- `requests` — HTTP client for API calls
- `json` — JSON parsing (stdlib)
- `os` — Environment variables (stdlib)
- `time` — Pacing governor (stdlib)

## System Dependencies
- **Hermes Desktop** v0.18.0+ — Gateway and agent runtime
- **Obsidian** — Note-taking app with plugin support
- **Node.js** (for npx-based MCP servers)
- **Python** 3.11+ — For handler scripts and MCP servers

## Obsidian Plugins (Community Plugins)
1. **Hermes Agent** — Connects to Hermes gateway
2. **Hermes Console** — Terminal/debug console
3. **Hermes TTS** — Text-to-speech
4. **Obsidian Local REST API** — HTTP API for vault access
5. **Smart Connections** — Vector search

## MCP Servers (Hermes)
- `filesystem` — File access (D:\Alex - KV Obsidian, C:\Users\apviz, E:\CLAUDE)
- `obsidian` — Native Obsidian vault access
- `optimus-orchestrator` — Optimus Prime orchestration primitives
- `searxng` — Private web search
- `docker-mcp` — Docker container management
- `elasticsearch-mcp` — Elasticsearch cluster management
- `postgresql-mcp` — PostgreSQL database management
- `redis-mcp` — Redis cache management
- `prometheus-mcp` — Prometheus metrics
- `grafana-mcp` — Grafana dashboards
- `loki-mcp` — Log aggregation
- `tempo-mcp` — Distributed tracing
- `vault-mcp` — HashiCorp Vault secrets
- `minio-mcp` — S3-compatible storage
- `windows-system` — Windows administration
- `session-replay` — Session recording/replay
- `agent-browser` — Browser automation
- `chrome-devtools` — Chrome DevTools access
- `git` — Version control
- `memory` — Persistent knowledge graph
- `qwen` — Qwen CLI integration
- `sequential-thinking` — Structured reasoning
- `antigravity-bridge` — Antigravity AI bridge
- `notebooklm` — Google NotebookLM integration

## Docker Services
- **SearXNG** (port 8081) — Private search engine
- **Elasticsearch** (ports 9200, 9300) — Search and analytics
- **Grafana** (port 3000) — Dashboards
- **Loki** — Log aggregation
- **Prometheus** — Metrics
- **Tempo** — Tracing
- **MinIO** — S3-compatible storage
- **Redis** (port 6379) — Caching

## Environment Variables
- `API_SERVER_KEY` — Required for gateway API server
- `OPENROUTER_API_KEY` — OpenRouter model access
- `OPENAI_API_KEY` — OpenAI TTS
- `SEARXNG_URL` — http://localhost:8081/
- `AGENT_BROWSER_ENGINE` — auto

## File Paths
- `C:\Users\apviz\AppData\Local\hermes\.env` — Environment config
- `C:\Users\apviz\AppData\Local\hermes\config.yaml` — Hermes config
- `C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml` — Default profile config
- `C:\Users\apviz\AppData\Local\hermes\gateway_state.json` — Gateway status
- `/d/Alex_Knowlege_Vault/.obsidian/plugins/` — Obsidian plugin storage
- `/d/Alex_Knowlege_Vault/.obsidian/plugins/hermes-agent/data.json` — Agent plugin settings
- `/d/Alex_Knowlege_Vault/.obsidian/plugins/hermes-console/data.json` — Console plugin settings
- `/d/Alex_Knowlege_Vault/.obsidian/plugins/hermes-tts/data.json` — TTS plugin settings