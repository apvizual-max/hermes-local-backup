# Sub-Skill: exec-antigravity-delegation

* **Description:** How to delegate tasks and communicate with Antigravity AI via the  antigravity-bridge MCP server. Use when you need Antigravity to execute a task, when a task requires Antigravity's specific capabilities (web research, code  generation, complex analysis), or when coordinating with Antigravity as part  of a larger orchestration workflow.

---

# Antigravity Delegation Skill

## When to Delegate to Antigravity

Delegate to Antigravity when:
- Complex code generation or debugging is required
- Deep web research with multi-step synthesis needed
- File system analysis across many files/directories
- Tasks requiring Antigravity's specialized skills or knowledge base
- You want a second opinion or parallel execution
- The task is too complex for a single Hermes response

## Quick Start

### 1. Delegate a Task
```
ag_delegate_task(
  task="<detailed task description>",
  task_type="code|analysis|search|file_ops|system|research|general",
  priority="normal|high|urgent|low",
  context={"key": "value"}  # optional
)
→ Returns: { "task_id": "task_...", "status": "DELEGATED" }
```

### 2. Poll for Response
```
ag_poll_response(task_id="task_...", archive_on_read=false)
→ Returns: { "status": "PENDING|COMPLETED|ARCHIVED", "response": {...} }
```

### 3. Read Full Response
```
ag_read_response(task_id="task_...")
→ Returns: { "result": "...", "summary": "...", "artifacts": [...] }
```

## Communication Patterns

### Fire-and-Wait Pattern
```
1. task_id = ag_delegate_task(task="...", priority="high")
2. Wait (tell user you're delegating)
3. Periodically: ag_poll_response(task_id)
4. When COMPLETED: ag_read_response(task_id)
5. Archive: ag_poll_response(task_id, archive_on_read=true)
```

### Send-and-Forget Pattern
```
1. ag_send_message(message="...", from_agent="hermes")
2. Continue with other work
3. Later check: ag_list_pending()
```

### Check Queue Status
```
ag_get_status()
→ Shows: pending count, completed count, last activity
```

## Task Type Guide

| Type | When to use | Example |
|------|-------------|---------|
| `code` | Write/fix code | "Write a Python script to parse logs" |
| `analysis` | Deep analysis | "Analyze all log files and find error patterns" |
| `search` | Web research | "Research latest AI agent frameworks" |
| `file_ops` | File management | "Reorganize the skills folder" |
| `system` | System commands | "Check disk space on all drives" |
| `research` | Report generation | "Create a report on..." |
| `general` | Anything else | General questions/tasks |
| `message` | Coordination | "FYI: I'm starting task X, please be ready" |

## Priority Guide
- `urgent` → Antigravity processes ASAP (use sparingly)
- `high` → Important, process before normal queue
- `normal` → Default — standard queue order  
- `low` → Background/nice-to-have tasks

## Context Best Practices

Always include relevant context:
```json
{
  "project_path": "C:\\Users\\apviz\\...",
  "file_types": [".py", ".yaml"],
  "constraints": ["no external APIs", "Python 3.11"],
  "output_format": "markdown report",
  "related_task_id": "task_previous_..."
}
```

## Bridge Infrastructure

```
Queue location: C:\Users\apviz\AppData\Local\hermes\pairing\antigravity\
├── inbox\      ← Your tasks go here
├── outbox\     ← Antigravity's responses appear here
├── history\    ← Archive of completed tasks
└── status.json ← Current queue health
```

## Error Handling

If `ag_poll_response` returns `NOT_FOUND`:
- Task may have been archived — check `ag_list_history()`
- Task may have been cancelled

If response never arrives:
- Check `ag_get_status()` for queue health
- Verify Antigravity is active and checking inbox
- Cancel and retry: `ag_cancel_task(task_id, reason="timeout")`

## Example Full Workflow

```
You: "Hermes, research the latest MCP protocol updates"

Hermes:
1. ag_delegate_task(
     task="Research the latest Model Context Protocol (MCP) updates, 
           focusing on new features in 2025-2026. Summarize in a report.",
     task_type="research",
     priority="normal"
   )
   → task_id = "task_1783870000000_abc12345"

2. "I've delegated the research task to Antigravity (task_1783870000000_abc12345).
    They'll conduct the research and I'll have results shortly."

3. [After Antigravity completes]:
   ag_read_response(task_id="task_1783870000000_abc12345")
   → result = "# MCP Protocol Updates 2025-2026\n\n..."

4. Present results to user
```