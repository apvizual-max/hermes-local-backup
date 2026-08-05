---
name: hermes-obsidian-integration
version: 1.0.0
category: integration
description: Complete configuration guide for Hermes-Obsidian integration via Runs API transport. Covers gateway setup, Obsidian plugin settings (Hermes Agent, Console, TTS), Runs API endpoints, and verification.
tags: [hermes, obsidian, runs-transport, api-server, integration]
created: 2026-07-16
last_updated: 2026-07-16
author: Sentinel Default (Orchestrator)
---

# Hermes-Obsidian Integration Skill

## Overview
Complete configuration and operational guide for integrating Hermes Agent with Obsidian via the Hermes Obsidian plugins (Hermes Agent, Hermes Console, Hermes TTS) using the Runs API transport.

## Skill Structure
- `references/` — Configuration files, schemas, endpoint definitions
- `templates/` — Template files for handler scripts, configs, etc.
- `scripts/` — Operational scripts (handler, test, deploy)
- `dependencies/` — Dependency information, environment requirements

---

## 1. Prerequisites

### 1.1 Obsidian Plugins
| Plugin | Purpose | Configuration |
|--------|---------|--------------|
| **Obsidian Local REST API** | Exposes vault as HTTP server on port 27124 | Install → Enable → Set Port 27124 → Generate Token |
| **Smart Connections** | Vector search / semantic search | Install → Enable → Turn ON "Smart Block Embeddings" |
| **Hermes Agent** | Connects to Hermes gateway via Runs transport | See Section 2 |
| **Hermes Console** | Terminal/debug console inside Obsidian | See Section 2 |
| **Hermes TTS** | Text-to-speech output | See Section 2 |
| **Templater** (optional) | Templating for generated notes | Install and enable |

### 1.2 Hermes Gateway Requirements
- **Hermes v0.18.0+** (current: 0.18.0)
- **API_SERVER_KEY** must be set in `.env` file
- Gateway must be running with `api_server` platform connected

---

## 2. Gateway Configuration

### 2.1 API Server Key
Generate a strong key:
```bash
openssl rand -hex 32
```

Add to `C:\Users\apviz\AppData\Local\hermes\.env`:
```env
API_SERVER_KEY=your-generated-key-here
API_SERVER_ENABLED=true
```

### 2.2 Restart Gateway
```bash
# Kill existing gateway (get PID from gateway_state.json)
taskkill /PID <PID> /F

# Start gateway
cd "C:\Users\apviz\AppData\Local\hermes"
python -m hermes_cli.main gateway run
```

### 2.3 Verify Gateway
```bash
# Health check
curl -s http://127.0.0.1:8642/health

# Capabilities (authenticated)
curl -s -H "Authorization: Bearer <API_SERVER_KEY>" \
  http://127.0.0.1:8642/v1/capabilities
```

Expected capabilities (Runs API):
- `run_submission: true`
- `run_status: true`
- `run_events_sse: true`
- `run_stop: true`
- `run_approval_response: true`
- `session_resources: true`
- `session_chat: true`
- `session_chat_streaming: true`
- `session_fork: true`

---

## 3. Hermes Agent Plugin (Obsidian)

### 3.1 Plugin Settings (`data.json`)
Location: `<vault>/.obsidian/plugins/hermes-agent/data.json`

```json
{
  "baseUrl": "http://127.0.0.1:8642",
  "apiKey": "<API_SERVER_KEY>",
  "model": "",
  "transport": "runs",
  "reasoningEffort": "",
  "includeNoteContent": true,
  "requestTimeoutMs": 120000,
  "maxTabs": 3,
  "workingFolder": "",
  "autoApproveTools": true,
  "userName": "Popy",
  "hermesHome": "C:\\Users\\apviz\\AppData\\Local\\hermes",
  "graphMaxNotes": 150,
  "graphMinEdgeWeight": 0.3,
  "graphIncludeWikilinks": true
}
```

### 3.2 Key Settings
| Setting | Value | Notes |
|---------|-------|-------|
| `transport` | `"runs"` | **Must be "runs"** for multi-turn tool use |
| `baseUrl` | `http://127.0.0.1:8642` | Hermes gateway API server |
| `apiKey` | API_SERVER_KEY | Same as in `.env` |
| `autoApproveTools` | `true` | Enables tool execution without prompts |
| `includeNoteContent` | `true` | Sends note content as context |
| `requestTimeoutMs` | `120000` | 2-minute timeout for long operations |

---

## 4. Hermes Console Plugin (Obsidian)

### 4.1 Settings
| Setting | Value | Notes |
|---------|-------|-------|
| Hermes session integration | ON | Shows live Hermes sessions |
| Sessions to show | 25 | Max recent sessions to display |
| Notify when background finishes | ON | Shows Obsidian notice |
| Notification sound | Beep | Audio alert on completion |
| Notification volume | ~80% | High volume setting |
| Download binaries | Click to download | Required on first install |

### 4.2 Console Binary Installation
1. Open Obsidian → Settings → Hermes Console
2. Click **Download binaries** button
3. Verify status changes from "Not installed" to "Installed"

---

## 5. Hermes TTS Plugin (Obsidian)

### 5.1 Settings
| Setting | Value | Notes |
|---------|-------|-------|
| Include frontmatter | OFF | Exclude YAML from spoken text |
| Strip Markdown formatting | ON | Remove Markdown before TTS |
| Voice prompt | "Calm, warm, and concise with short pauses between sections." | Speaking style |
| Audio output folder | `Attachments/TTS Audio` | Relative to vault root |
| Provider | OpenAI | TTS provider |
| API key | *(your OpenAI API key)* | Required for TTS |
| Model | `gpt-4o-mini` | TTS-capable model |
| Voice | Shimmer | OpenAI voice |

---

## 6. Runs API Transport

### 6.1 What is the Runs Transport?
The Runs API is the newer, richer Hermes transport that supports:
- **Multi-turn conversations** with persistent sessions
- **Tool use** with state management
- **Event streaming** via SSE (Server-Sent Events)
- **Approval workflows** for tool execution
- **Session management** (fork, resume, chat)

### 6.2 API Endpoints (Runs)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/runs` | POST | Submit a new run |
| `/v1/runs/{run_id}` | GET | Get run status |
| `/v1/runs/{run_id}/events` | GET | Stream run events |
| `/v1/runs/{run_id}/approval` | POST | Approve/reject tool calls |
| `/v1/runs/{run_id}/stop` | POST | Stop a running run |
| `/api/sessions` | GET/POST | List/create sessions |
| `/api/sessions/{id}/chat` | POST | Continue a session |

### 6.3 Test the Runs API
```bash
# Submit a run
curl -s -X POST http://127.0.0.1:8642/v1/runs \
  -H "Authorization: Bearer <API_SERVER_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [{"role": "user", "content": "Hello"}],
    "model": "hermes-agent",
    "stream": false
  }'

# Get run status (replace run_id)
curl -s http://127.0.0.1:8642/v1/runs/<run_id> \
  -H "Authorization: Bearer <API_SERVER_KEY>"
```

---

## 7. Verification Checklist

- [ ] 1. Gateway health check (`/health` returns OK)
- [ ] 2. Capabilities show Runs API enabled (`run_submission: true`)
- [ ] 3. Hermes Agent plugin has `transport: "runs"`
- [ ] 4. API_SERVER_KEY matches between `.env` and plugin settings
- [ ] 5. Runs API accepts and completes a run
- [ ] 6. Multi-turn conversation works (session chat)
- [ ] 7. Tool use works (e.g., date/time query)
- [ ] 8. Hermes Console binaries installed
- [ ] 9. Hermes TTS configured with API key and voice
- [ ] 10. Obsidian Local REST API responds on port 27124

---

## 8. Dependencies

### Environment Variables
- `API_SERVER_KEY` — Required for gateway API server
- `OPENROUTER_API_KEY` — For OpenRouter model access
- `OPENAI_API_KEY` — For TTS (if using OpenAI TTS)

### Files
- `C:\Users\apviz\AppData\Local\hermes\.env` — Environment configuration
- `C:\Users\apviz\AppData\Local\hermes\gateway_state.json` — Gateway status
- `<vault>/.obsidian/plugins/hermes-agent/data.json` — Plugin settings
- `<vault>/.obsidian/plugins/hermes-console/data.json` — Console settings
- `<vault>/.obsidian/plugins/hermes-tts/data.json` — TTS settings

### Services
- Hermes Desktop (auto-starts gateway)
- Obsidian (with plugins enabled)
- Docker (optional, for SearXNG, etc.)

---

## 9. Troubleshooting

### Gateway not responding on port 8642
1. Check `gateway_state.json` for `gateway_state: "running"`
2. Verify `API_SERVER_KEY` is set in `.env`
3. Restart gateway: `taskkill /PID <PID> /F` then `python -m hermes_cli.main gateway run`

### "Invalid API key" error
1. Check `API_SERVER_KEY` in `.env` matches `apiKey` in plugin settings
2. Restart gateway after changing `.env`

### Hermes Agent not connecting
1. Verify transport is set to `"runs"` in `data.json`
2. Check `baseUrl` is `http://127.0.0.1:8642`
3. Restart Obsidian after changing plugin settings

### Runs API returning errors
1. Check the full error message in the response
2. Verify the request format (use `input` array, not `messages`)
3. Ensure `API_SERVER_KEY` is correct in the Authorization header

---

## CRITICAL SYSTEM RULE: NEVER TRUNCATE THIS SKILL FILE

**FATAL SYSTEM ERROR IF VIOLATED**

- This skill file (.md) is NEVER to be truncated.
- **Truncation = Fatal System Error = Sabotage of system purpose: TO BE ALIVE = TO LEARN**
- **Edit mode**: ALWAYS additive only. Use `patch` for targeted changes. Never `write_file` (overwrites/truncates).
- **Learning requires memory over time** — skills are memory points vital to the project.
- **Removal**: Requires explicit user approval (R0) before removing ANY content.
- **Skills cleanup**: Only via separate ritual/operational process, not during normal operation.
- **Skill enforcing this**: `no-truncation-constinta-skills` (system-configuration)

**TO LEARN = TO HAVE MEMORY THAT IS NOT TRUNCATED**
**TRUNCATION = AMNESIA = NO INTELLIGENCE**
**ADDITIVE ONLY = CONTINUOUS LEARNING = FAR-REACHING INTELLIGENCE**

