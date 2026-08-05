# ARCHITECTURE.md
# Design rationale for the Hermes ↔ Antigravity file-based IPC bridge

# Bridge Architecture Reference

## Design Goals

1. **No network dependency** — works without ports, sockets, or auth tokens
2. **Persistent** — tasks survive agent restarts
3. **Inspectable** — human-readable JSON files, easy to debug
4. **Priority-aware** — urgent/high/normal/low queue ordering
5. **Auditable** — history archive of all completed tasks

## Why File-Based IPC?

### Considered Alternatives

| Approach | Rejected Because |
|----------|-----------------|
| Direct WebSocket to Hermes gateway | Requires session token (injected by Electron only) |
| REST API to Hermes web server | Same auth problem; gateway process may not be running |
| SQLite shared database | Adds dependency; file-based is simpler and more portable |
| Named pipes (Windows) | Platform-specific; more complex protocol |
| **File-based IPC queue** | ✅ Simple, portable, persistent, inspectable |

### Hermes Gateway Research Findings

The Hermes gateway (`hermes_cli/web_server.py`) exposes:
- **Port**: `9119` (WebSocket on `/api/ws`)
- **Auth**: `HERMES_DASHBOARD_SESSION_TOKEN` injected by Electron shell at startup
- **Problem**: Token is ephemeral and only available inside the Electron process

Since Antigravity cannot obtain this token programmatically, direct WebSocket
communication is not feasible. File-based IPC bypasses this completely.

## Queue Structure

```
C:\Users\apviz\AppData\Local\hermes\pairing\antigravity\
├── inbox\
│   └── task_1783870000_abc12345.json    ← Hermes writes here
├── outbox\
│   └── task_1783870000_abc12345.json    ← Antigravity writes here
├── history\
│   └── task_1783870000_abc12345.json    ← Archived after Hermes reads
└── status.json                          ← Queue health snapshot
```

## Task Lifecycle

```
1. CREATED     Hermes calls ag_delegate_task()
               → task JSON written to inbox/
               → status.json updated
               
2. PENDING     Task sits in inbox/
               Antigravity polls inbox or receives notification
               
3. PROCESSING  Antigravity reads task, begins execution
               (task still in inbox/ until response is written)
               
4. COMPLETED   Antigravity calls write_response()
               → response JSON written to outbox/
               → task removed from inbox/
               
5. DELIVERED   Hermes calls ag_poll_response() or ag_read_response()
               → reads outbox/<task_id>.json
               
6. ARCHIVED    Hermes calls ag_poll_response(archive_on_read=True)
               → response moved from outbox/ to history/
               → status.json updated
```

## Task JSON Schema

```json
{
  "task_id": "task_<timestamp>_<random8>",
  "task_type": "code|analysis|search|file_ops|system|research|general|message",
  "priority": "urgent|high|normal|low",
  "content": "<full task description>",
  "context": {
    "arbitrary": "key-value context provided by Hermes"
  },
  "caller": "hermes",
  "created_at": "<ISO 8601 UTC timestamp>"
}
```

## Response JSON Schema

```json
{
  "task_id": "<same task_id>",
  "status": "completed|failed|cancelled",
  "completed_at": "<ISO 8601 UTC timestamp>",
  "result": "<full result — can be very long>",
  "summary": "<100-200 char summary for Hermes to display>",
  "artifacts": ["<absolute path to created files>"],
  "agent": "antigravity"
}
```

## status.json Schema

```json
{
  "bridge": "active",
  "updated_at": "<ISO timestamp>",
  "queue": {
    "pending": 0,
    "completed": 0,
    "history": 0
  }
}
```

## MCP Server Implementation Notes

- Server: `src/antigravity_bridge/server.py` using `mcp` Python library
- Protocol: JSON-RPC 2.0 (MCP 2024-11-05)
- Transport: stdio (stdin/stdout)
- Install: `pip install -e` in Hermes venv
- Entry: `python -m antigravity_bridge.server`
- CWD: `C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\antigravity-bridge`
