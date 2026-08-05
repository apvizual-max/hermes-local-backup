# MCP_JSONRPC_PROTOCOL.md
# JSON-RPC 2.0 test protocol reference for MCP servers

# MCP JSON-RPC Protocol Reference

## Protocol Version

**Supported**: `2024-11-05`

All MCP servers use JSON-RPC 2.0 over stdio (stdin/stdout).
Each message is a single JSON object terminated by `\n`.

## Handshake Sequence (MANDATORY)

```
1. Client → Server:  initialize request
2. Server → Client:  initialize response
3. Client → Server:  notifications/initialized  (no response expected)
4. Client → Server:  tools/list request
5. Server → Client:  tools/list response
```

## Message Format

### Request
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "method_name",
  "params": {}
}
```

### Notification (no response)
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized",
  "params": {}
}
```

### Response (success)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { ... }
}
```

### Response (error)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": "..."
  }
}
```

## initialize Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "hermes-verify",
      "version": "1.0.0"
    }
  }
}
```

## initialize Response (expected)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": { "tools": {} },
    "serverInfo": {
      "name": "server-name",
      "version": "1.0.0"
    }
  }
}
```

## tools/list Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "tool_name",
        "description": "What this tool does",
        "inputSchema": {
          "type": "object",
          "properties": {
            "param": { "type": "string", "description": "..." }
          },
          "required": ["param"]
        }
      }
    ]
  }
}
```

## tools/call Request

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {
      "param": "value"
    }
  }
}
```

## tools/call Response

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "result text or JSON string"
      }
    ]
  }
}
```

## Known Server Tool Counts

| Server | Command | Min Tools |
|--------|---------|-----------|
| agent-browser | agent-browser.cmd mcp --tools all | 64 |
| antigravity-bridge | python -m antigravity_bridge.server | 9 |
| optimus-orchestrator | python -m optimus_orchestrator.server | varies |
| session-replay | python -m session_replay.server | varies |
| windows-system | python -m windows_system.server | varies |

## Common Error Codes

| Code | Meaning |
|------|---------|
| -32700 | Parse error — invalid JSON received |
| -32600 | Invalid Request — missing required fields |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
