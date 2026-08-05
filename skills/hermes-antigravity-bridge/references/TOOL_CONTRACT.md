# TOOL_CONTRACT.md
# Full JSON schema and behavioral contract for all 9 antigravity-bridge MCP tools

# Antigravity Bridge Tool Contract

## Tool Inventory

| Tool | Input | Output |
|------|-------|--------|
| `ag_delegate_task` | task, task_type, priority, context | task_id, status |
| `ag_poll_response` | task_id, archive_on_read | status, response (if ready) |
| `ag_list_pending` | include_context | list of pending tasks |
| `ag_read_response` | task_id | full response object |
| `ag_cancel_task` | task_id, reason | status, message |
| `ag_send_message` | message, from_agent | task_id |
| `ag_get_status` | — | bridge health + queue counts |
| `ag_list_history` | limit | list of archived tasks |
| `ag_clear_history` | confirm | count cleared |

---

## ag_delegate_task

**Purpose**: Post a task to Antigravity's inbox for execution.

**Input Schema**:
```json
{
  "task": "string (required) — full task description",
  "task_type": "string (optional) — one of: code, analysis, search, file_ops, system, research, general, message",
  "priority": "string (optional) — one of: urgent, high, normal, low (default: normal)",
  "context": "object (optional) — arbitrary key-value context"
}
```

**Output**:
```json
{
  "status": "DELEGATED",
  "task_id": "task_<timestamp>_<random8>",
  "message": "Task delegated to Antigravity",
  "task_type": "general",
  "priority": "normal"
}
```

---

## ag_poll_response

**Purpose**: Check if Antigravity has completed a task and retrieve the response.

**Input Schema**:
```json
{
  "task_id": "string (required)",
  "archive_on_read": "boolean (optional, default: false)"
}
```

**Output (pending)**:
```json
{ "status": "PENDING", "task_id": "...", "message": "Task is still pending" }
```

**Output (completed)**:
```json
{
  "status": "COMPLETED",
  "task_id": "...",
  "response": {
    "task_id": "...",
    "status": "completed",
    "completed_at": "2026-07-12T16:00:00+00:00",
    "result": "full result text...",
    "summary": "brief summary...",
    "artifacts": [],
    "agent": "antigravity"
  }
}
```

---

## ag_get_status

**Purpose**: Get bridge health and queue statistics.

**Input**: none

**Output**:
```json
{
  "bridge": "active",
  "updated_at": "2026-07-12T16:00:00+00:00",
  "queue": {
    "pending": 0,
    "completed": 0,
    "history": 0
  }
}
```

---

## ag_cancel_task

**Purpose**: Cancel a pending task and remove from inbox.

**Input**:
```json
{
  "task_id": "string (required)",
  "reason": "string (optional)"
}
```

**Output**:
```json
{
  "status": "CANCELLED",
  "task_id": "...",
  "reason": "cancelled by caller"
}
```

---

## ag_send_message

**Purpose**: Send a freeform message to Antigravity (creates a `message` type task).

**Input**:
```json
{
  "message": "string (required)",
  "from_agent": "string (optional, default: hermes)"
}
```

**Output**: Same as `ag_delegate_task` output (returns task_id).

---

## Task Type Behavioral Contract

| task_type | Antigravity behavior |
|-----------|---------------------|
| `code` | Writes code to file, runs it, returns output + file path |
| `analysis` | Reads files/logs, returns structured analysis report |
| `search` | Searches web, returns synthesized summary with sources |
| `file_ops` | Performs file management, returns list of actions taken |
| `system` | Runs PowerShell/cmd commands, returns stdout/stderr |
| `research` | Deep multi-source research, creates artifact report |
| `general` | Answers with LLM reasoning, returns text response |
| `message` | Acknowledges and logs the message, returns confirmation |

---

## Priority Behavioral Contract

| Priority | Antigravity behavior |
|----------|---------------------|
| `urgent` | Process immediately, interrupt current work |
| `high` | Process before any normal/low tasks in queue |
| `normal` | Process in FIFO order within normal priority |
| `low` | Process only when no urgent/high/normal tasks remain |

---

## Error Responses

```json
{
  "status": "ERROR",
  "error": "description of what went wrong",
  "task_id": "..."
}
```

**NOT_FOUND** (task_id doesn't exist in inbox/outbox):
```json
{
  "status": "NOT_FOUND",
  "task_id": "...",
  "message": "Task not found. May be in history — try ag_list_history()"
}
```
