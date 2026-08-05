"""
Antigravity Bridge MCP Server
============================
Two-way communication bridge between Hermes Agent and Antigravity AI.

Architecture:
  - Uses a shared file-based IPC queue in HERMES_HOME/pairing/antigravity/
  - Hermes delegates tasks to Antigravity by writing task files
  - Antigravity reads pending tasks, executes them, writes response files
  - Hermes polls for responses or reads them directly

Tools exposed to Hermes:
  - ag_delegate_task      : Post a task to Antigravity's inbox
  - ag_poll_response      : Check if Antigravity has responded to a task
  - ag_list_pending       : List all pending tasks in the queue
  - ag_read_response      : Read a completed task response
  - ag_cancel_task        : Cancel a pending task
  - ag_send_message       : Send a freeform message to Antigravity
  - ag_get_status         : Get Antigravity bridge status and queue stats
  - ag_list_history       : List completed/cancelled tasks history
  - ag_clear_history      : Clear completed task history
"""

import asyncio
import json
import uuid
import time
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ─── Paths ─────────────────────────────────────────────────────────────────────

HERMES_HOME = Path(os.environ.get("HERMES_HOME", r"C:\Users\apviz\AppData\Local\hermes"))
BRIDGE_DIR = HERMES_HOME / "pairing" / "antigravity"
INBOX_DIR = BRIDGE_DIR / "inbox"       # Tasks Antigravity needs to process
OUTBOX_DIR = BRIDGE_DIR / "outbox"     # Responses from Antigravity
HISTORY_DIR = BRIDGE_DIR / "history"   # Archive of completed tasks
STATUS_FILE = BRIDGE_DIR / "status.json"

# Ensure directories exist
for d in [INBOX_DIR, OUTBOX_DIR, HISTORY_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─── App ───────────────────────────────────────────────────────────────────────

app = Server("antigravity-bridge")


# ─── Helper functions ──────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _update_status() -> None:
    pending = list(INBOX_DIR.glob("*.json"))
    completed = list(OUTBOX_DIR.glob("*.json"))
    history = list(HISTORY_DIR.glob("*.json"))
    status = {
        "bridge": "active",
        "updated_at": _now_iso(),
        "queue": {
            "pending": len(pending),
            "completed": len(completed),
            "history": len(history),
        },
        "inbox_path": str(INBOX_DIR),
        "outbox_path": str(OUTBOX_DIR),
    }
    _write_json(STATUS_FILE, status)


def _create_task(task_type: str, content: str, priority: str = "normal", 
                  context: Optional[Dict] = None, caller: str = "hermes") -> dict:
    task_id = f"task_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"
    task = {
        "task_id": task_id,
        "task_type": task_type,
        "content": content,
        "priority": priority,
        "context": context or {},
        "caller": caller,
        "status": "pending",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    task_path = INBOX_DIR / f"{task_id}.json"
    _write_json(task_path, task)
    _update_status()
    return task


def _get_response(task_id: str) -> Optional[dict]:
    response_path = OUTBOX_DIR / f"{task_id}.json"
    if response_path.exists():
        return _read_json(response_path)
    return None


def _get_task(task_id: str) -> Optional[dict]:
    task_path = INBOX_DIR / f"{task_id}.json"
    if task_path.exists():
        return _read_json(task_path)
    # Check history
    hist_path = HISTORY_DIR / f"{task_id}.json"
    if hist_path.exists():
        return _read_json(hist_path)
    return None


def _list_pending() -> List[dict]:
    tasks = []
    for f in sorted(INBOX_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime):
        try:
            tasks.append(_read_json(f))
        except Exception:
            pass
    return tasks


def _list_completed() -> List[dict]:
    responses = []
    for f in sorted(OUTBOX_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            responses.append(_read_json(f))
        except Exception:
            pass
    return responses


def _list_history() -> List[dict]:
    items = []
    for f in sorted(HISTORY_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            items.append(_read_json(f))
        except Exception:
            pass
    return items


def _archive_task(task_id: str) -> None:
    """Move a completed response + its task to history."""
    resp_path = OUTBOX_DIR / f"{task_id}.json"
    task_path = INBOX_DIR / f"{task_id}.json"
    
    combined = {}
    if task_path.exists():
        combined.update(_read_json(task_path))
        task_path.unlink(missing_ok=True)
    if resp_path.exists():
        combined["response"] = _read_json(resp_path)
        resp_path.unlink(missing_ok=True)
    
    combined["archived_at"] = _now_iso()
    _write_json(HISTORY_DIR / f"{task_id}.json", combined)
    _update_status()


# ─── Tool definitions ──────────────────────────────────────────────────────────

@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="ag_delegate_task",
            description=(
                "Delegate a task to Antigravity AI for execution. "
                "Antigravity will pick it up, process it, and write a response to the outbox. "
                "Returns the task_id for polling. Use ag_poll_response to check for completion."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task description in natural language. Be detailed and specific."
                    },
                    "task_type": {
                        "type": "string",
                        "enum": ["code", "analysis", "search", "file_ops", "system", "research", "general"],
                        "default": "general",
                        "description": "Type of task to help Antigravity route it correctly"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "normal", "high", "urgent"],
                        "default": "normal",
                        "description": "Task priority"
                    },
                    "context": {
                        "type": "object",
                        "description": "Optional structured context (file paths, project info, etc.)"
                    }
                },
                "required": ["task"]
            }
        ),
        Tool(
            name="ag_poll_response",
            description=(
                "Poll for a response from Antigravity for a specific task_id. "
                "Returns the response if available, or a 'pending' status."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The task_id returned by ag_delegate_task"
                    },
                    "archive_on_read": {
                        "type": "boolean",
                        "default": False,
                        "description": "If true, move the completed task to history after reading"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="ag_list_pending",
            description="List all tasks currently waiting for Antigravity to process.",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_context": {
                        "type": "boolean",
                        "default": False,
                        "description": "Include full context in each task"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="ag_read_response",
            description=(
                "Read a completed response from Antigravity. "
                "Returns the full response including output, artifacts, and metadata."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The task_id to read response for"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="ag_cancel_task",
            description="Cancel a pending task that has not yet been picked up by Antigravity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The task_id to cancel"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for cancellation"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="ag_send_message",
            description=(
                "Send a freeform message or instruction to Antigravity. "
                "This is like sending Antigravity a chat message — ideal for short instructions, "
                "status updates, or coordination messages."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to send to Antigravity"
                    },
                    "from_agent": {
                        "type": "string",
                        "default": "hermes",
                        "description": "Sender identity (e.g. 'hermes', 'sentinel', 'prime')"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="ag_get_status",
            description="Get the current status of the Antigravity bridge: queue stats, paths, last activity.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="ag_list_history",
            description="List completed/archived task history with summaries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "default": 20,
                        "description": "Max number of history entries to return"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="ag_clear_history",
            description="Clear completed task history (does not affect pending or outbox items).",
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be true to confirm deletion"
                    }
                },
                "required": ["confirm"]
            }
        ),
    ]


# ─── Tool implementations ──────────────────────────────────────────────────────

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "ag_delegate_task":
            return await handle_delegate_task(arguments)
        elif name == "ag_poll_response":
            return await handle_poll_response(arguments)
        elif name == "ag_list_pending":
            return await handle_list_pending(arguments)
        elif name == "ag_read_response":
            return await handle_read_response(arguments)
        elif name == "ag_cancel_task":
            return await handle_cancel_task(arguments)
        elif name == "ag_send_message":
            return await handle_send_message(arguments)
        elif name == "ag_get_status":
            return await handle_get_status(arguments)
        elif name == "ag_list_history":
            return await handle_list_history(arguments)
        elif name == "ag_clear_history":
            return await handle_clear_history(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"[BRIDGE ERROR] {name} failed: {type(e).__name__}: {e}")]


async def handle_delegate_task(args: Dict) -> List[TextContent]:
    task_str = args.get("task", "").strip()
    if not task_str:
        return [TextContent(type="text", text="ERROR: 'task' is required and cannot be empty")]
    
    task = _create_task(
        task_type=args.get("task_type", "general"),
        content=task_str,
        priority=args.get("priority", "normal"),
        context=args.get("context"),
        caller=args.get("from_agent", "hermes"),
    )
    
    return [TextContent(type="text", text=json.dumps({
        "status": "DELEGATED",
        "task_id": task["task_id"],
        "message": (
            f"Task delegated to Antigravity successfully.\n"
            f"Task ID: {task['task_id']}\n"
            f"Poll for response using: ag_poll_response(task_id='{task['task_id']}')\n"
            f"Antigravity will process this when it next checks the inbox."
        ),
        "task": {
            "task_id": task["task_id"],
            "task_type": task["task_type"],
            "priority": task["priority"],
            "created_at": task["created_at"],
            "inbox_file": str(INBOX_DIR / f"{task['task_id']}.json"),
        }
    }, indent=2))]


async def handle_poll_response(args: Dict) -> List[TextContent]:
    task_id = args.get("task_id", "").strip()
    if not task_id:
        return [TextContent(type="text", text="ERROR: 'task_id' is required")]
    
    archive = args.get("archive_on_read", False)
    
    # Check outbox
    response = _get_response(task_id)
    if response:
        result = {
            "status": "COMPLETED",
            "task_id": task_id,
            "response": response,
        }
        if archive:
            _archive_task(task_id)
            result["archived"] = True
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    # Check if still in inbox
    task = _get_task(task_id)
    if task:
        return [TextContent(type="text", text=json.dumps({
            "status": "PENDING",
            "task_id": task_id,
            "task_type": task.get("task_type"),
            "priority": task.get("priority"),
            "created_at": task.get("created_at"),
            "message": "Task is still in Antigravity's inbox. Check again later.",
        }, indent=2))]
    
    # Check history
    hist_path = HISTORY_DIR / f"{task_id}.json"
    if hist_path.exists():
        hist = _read_json(hist_path)
        return [TextContent(type="text", text=json.dumps({
            "status": "ARCHIVED",
            "task_id": task_id,
            "data": hist,
            "message": "Task has been archived. Use ag_list_history to see all archived tasks.",
        }, indent=2))]
    
    return [TextContent(type="text", text=json.dumps({
        "status": "NOT_FOUND",
        "task_id": task_id,
        "message": "No task found with this ID in inbox, outbox, or history.",
    }, indent=2))]


async def handle_list_pending(args: Dict) -> List[TextContent]:
    include_context = args.get("include_context", False)
    tasks = _list_pending()
    
    result = []
    for t in tasks:
        entry = {
            "task_id": t.get("task_id"),
            "task_type": t.get("task_type"),
            "priority": t.get("priority"),
            "content_preview": t.get("content", "")[:120] + ("..." if len(t.get("content", "")) > 120 else ""),
            "created_at": t.get("created_at"),
            "caller": t.get("caller"),
        }
        if include_context:
            entry["context"] = t.get("context")
        result.append(entry)
    
    return [TextContent(type="text", text=json.dumps({
        "total_pending": len(result),
        "tasks": result,
    }, indent=2))]


async def handle_read_response(args: Dict) -> List[TextContent]:
    task_id = args.get("task_id", "").strip()
    if not task_id:
        return [TextContent(type="text", text="ERROR: 'task_id' is required")]
    
    response = _get_response(task_id)
    if response:
        return [TextContent(type="text", text=json.dumps({
            "status": "FOUND",
            "task_id": task_id,
            "response": response,
        }, indent=2))]
    
    return [TextContent(type="text", text=json.dumps({
        "status": "NOT_FOUND",
        "task_id": task_id,
        "message": "No response found in outbox. Task may still be pending or has been archived.",
    }, indent=2))]


async def handle_cancel_task(args: Dict) -> List[TextContent]:
    task_id = args.get("task_id", "").strip()
    reason = args.get("reason", "Cancelled by Hermes")
    
    task_path = INBOX_DIR / f"{task_id}.json"
    if not task_path.exists():
        return [TextContent(type="text", text=json.dumps({
            "status": "NOT_FOUND",
            "task_id": task_id,
            "message": "Task not found in inbox (may already be processing or completed).",
        }, indent=2))]
    
    task = _read_json(task_path)
    task["status"] = "cancelled"
    task["cancel_reason"] = reason
    task["cancelled_at"] = _now_iso()
    
    # Move to history
    _write_json(HISTORY_DIR / f"{task_id}.json", task)
    task_path.unlink(missing_ok=True)
    _update_status()
    
    return [TextContent(type="text", text=json.dumps({
        "status": "CANCELLED",
        "task_id": task_id,
        "reason": reason,
    }, indent=2))]


async def handle_send_message(args: Dict) -> List[TextContent]:
    message = args.get("message", "").strip()
    from_agent = args.get("from_agent", "hermes")
    
    if not message:
        return [TextContent(type="text", text="ERROR: 'message' is required")]
    
    # Messages are just tasks of type 'general' with a message wrapper
    task = _create_task(
        task_type="message",
        content=message,
        priority="normal",
        context={"from_agent": from_agent, "message_type": "freeform"},
        caller=from_agent,
    )
    
    return [TextContent(type="text", text=json.dumps({
        "status": "SENT",
        "task_id": task["task_id"],
        "message": f"Message sent to Antigravity from '{from_agent}'.",
        "poll_response": f"ag_poll_response(task_id='{task['task_id']}')",
    }, indent=2))]


async def handle_get_status(args: Dict) -> List[TextContent]:
    _update_status()
    status = _read_json(STATUS_FILE)
    
    completed = _list_completed()
    latest_response = completed[0] if completed else None
    
    status["latest_response"] = {
        "task_id": latest_response.get("task_id") if latest_response else None,
        "completed_at": latest_response.get("completed_at") if latest_response else None,
    }
    status["bridge_paths"] = {
        "inbox": str(INBOX_DIR),
        "outbox": str(OUTBOX_DIR),
        "history": str(HISTORY_DIR),
        "status_file": str(STATUS_FILE),
    }
    
    return [TextContent(type="text", text=json.dumps(status, indent=2))]


async def handle_list_history(args: Dict) -> List[TextContent]:
    limit = min(args.get("limit", 20), 100)
    history = _list_history()[:limit]
    
    summaries = []
    for item in history:
        resp = item.get("response", {})
        summaries.append({
            "task_id": item.get("task_id"),
            "task_type": item.get("task_type"),
            "content_preview": item.get("content", "")[:80] + "...",
            "status": item.get("status", "unknown"),
            "created_at": item.get("created_at"),
            "archived_at": item.get("archived_at"),
            "response_summary": resp.get("summary", str(resp)[:100]) if resp else None,
        })
    
    return [TextContent(type="text", text=json.dumps({
        "total_history": len(_list_history()),
        "returned": len(summaries),
        "history": summaries,
    }, indent=2))]


async def handle_clear_history(args: Dict) -> List[TextContent]:
    if not args.get("confirm"):
        return [TextContent(type="text", text="ERROR: 'confirm' must be true to clear history")]
    
    count = 0
    for f in HISTORY_DIR.glob("*.json"):
        try:
            f.unlink()
            count += 1
        except Exception:
            pass
    
    _update_status()
    return [TextContent(type="text", text=json.dumps({
        "status": "CLEARED",
        "items_deleted": count,
    }, indent=2))]


# ─── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
