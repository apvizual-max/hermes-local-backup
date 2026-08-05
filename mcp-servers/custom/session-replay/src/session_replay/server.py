"""
Session Replay MCP Server
Debugging and audit: full I/O capture, deterministic replay, behavioral regression detection.
"""

import asyncio
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

app = Server("session-replay")

# Database for session storage
REPLAY_DB = Path(r"C:\Users\apviz\AppData\Local\hermes\session_replay.db")


# ==================== MODELS ====================

class SessionStartRequest(BaseModel):
    session_id: Optional[str] = Field(default=None, description="Session ID (auto-generated if not provided)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")


class SessionRecordRequest(BaseModel):
    session_id: str = Field(description="Session ID")
    event_type: str = Field(description="Event type: input, output, tool_call, tool_result, error, state_change")
    data: Dict[str, Any] = Field(description="Event data")
    timestamp: Optional[str] = Field(default=None, description="ISO timestamp (auto-generated if not provided)")


class SessionStopRequest(BaseModel):
    session_id: str = Field(description="Session ID to stop")


class SessionReplayRequest(BaseModel):
    session_id: str = Field(description="Session ID to replay")
    speed: float = Field(default=1.0, description="Replay speed multiplier")
    event_types: Optional[List[str]] = Field(default=None, description="Filter by event types")
    start_from: Optional[int] = Field(default=None, description="Start from event index")


class SessionDiffRequest(BaseModel):
    session_a: str = Field(description="First session ID")
    session_b: str = Field(description="Second session ID")
    ignore_fields: List[str] = Field(default_factory=lambda: ["timestamp", "session_id"], description="Fields to ignore in diff")


class SessionListRequest(BaseModel):
    limit: int = Field(default=50, description="Maximum sessions to return")
    offset: int = Field(default=0, description="Offset for pagination")
    status: Optional[str] = Field(default=None, description="Filter by status: active, completed, failed")


class SessionExportRequest(BaseModel):
    session_id: str = Field(description="Session ID to export")
    format: str = Field(default="json", description="Export format: json, csv")


# ==================== DATABASE SETUP ====================

def init_db():
    """Initialize the replay database."""
    conn = sqlite3.connect(REPLAY_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            stopped_at TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            metadata TEXT,
            event_count INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            event_index INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)
    """)
    
    conn.commit()
    conn.close()


def get_db():
    conn = sqlite3.connect(REPLAY_DB)
    conn.row_factory = sqlite3.Row
    return conn


# ==================== TOOLS ====================

app = Server("session-replay")


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="session_start",
            description="Start a new recording session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "metadata": {"type": "object"}
                },
                "required": []
            },
        ),
        Tool(
            name="session_record",
            description="Record an event in a session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "event_type": {"type": "string", "enum": ["input", "output", "tool_call", "tool_result", "error", "state_change"]},
                    "data": {"type": "object"},
                    "timestamp": {"type": "string"}
                },
                "required": ["session_id", "event_type", "data"]
            },
        ),
        Tool(
            name="session_stop",
            description="Stop a recording session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"}
                },
                "required": ["session_id"]
            },
        ),
        Tool(
            name="session_replay",
            description="Replay a recorded session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "speed": {"type": "number", "default": 1.0},
                    "event_types": {"type": "array", "items": {"type": "string"}},
                    "start_from": {"type": "integer"}
                },
                "required": ["session_id"]
            },
        ),
        Tool(
            name="session_diff",
            description="Compare two sessions for behavioral regression detection",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_a": {"type": "string"},
                    "session_b": {"type": "string"},
                    "ignore_fields": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["session_a", "session_b"]
            },
        ),
        Tool(
            name="session_list",
            description="List recorded sessions",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 50},
                    "offset": {"type": "integer", "default": 0},
                    "status": {"type": "string", "enum": ["active", "completed", "failed"]}
                },
                "required": []
            },
        ),
        Tool(
            name="session_export",
            description="Export a session for analysis or archival",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "format": {"type": "string", "enum": ["json", "csv"], "default": "json"}
                },
                "required": ["session_id"]
            },
        ),
        Tool(
            name="session_get",
            description="Get session details and events",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "include_events": {"type": "boolean", "default": True}
                },
                "required": ["session_id"]
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "session_start":
            return await handle_session_start(arguments)
        elif name == "session_record":
            return await handle_session_record(arguments)
        elif name == "session_stop":
            return await handle_session_stop(arguments)
        elif name == "session_replay":
            return await handle_session_replay(arguments)
        elif name == "session_diff":
            return await handle_session_diff(arguments)
        elif name == "session_list":
            return await handle_session_list(arguments)
        elif name == "session_export":
            return await handle_session_export(arguments)
        elif name == "session_get":
            return await handle_session_get(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_session_start(args: Dict) -> List[TextContent]:
    session_id = arguments.get("session_id") or str(uuid.uuid4())[:8]
    metadata = arguments.get("metadata", {})
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO sessions (session_id, created_at, status, metadata, event_count)
            VALUES (?, ?, 'active', ?, 0)
        """, (session_id, datetime.utcnow().isoformat(), json.dumps(arguments.get("metadata", {}))))
        conn.commit()
    except sqlite3.IntegrityError:
        return [TextContent(type="text", text=f"Session {session_id} already exists")]
    finally:
        conn.close()
    
    return [TextContent(type="text", text=json.dumps({
        "status": "STARTED",
        "session_id": session_id,
        "created_at": datetime.utcnow().isoformat(),
        "metadata": metadata
    }, indent=2))]


async def handle_session_record(args: Dict) -> List[TextContent]:
    req = SessionRecordRequest(**arguments)
    timestamp = req.timestamp or datetime.utcnow().isoformat()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get next event index
    cursor.execute("SELECT COALESCE(MAX(event_index), -1) + 1 FROM events WHERE session_id = ?", (req.session_id,))
    event_index = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        INSERT INTO events (session_id, event_index, timestamp, event_type, data)
        VALUES (?, ?, ?, ?, ?)
    """, (req.session_id, event_index, timestamp, req.event_type, json.dumps(req.data)))
    
    # Update session event count
    cursor.execute("UPDATE sessions SET event_count = event_count + 1 WHERE session_id = ?", (req.session_id,))
    
    conn.commit()
    conn.close()
    
    return [TextContent(type="text", text=json.dumps({
        "status": "RECORDED",
        "session_id": req.session_id,
        "event_index": event_index,
        "event_type": req.event_type,
        "timestamp": timestamp
    }, indent=2))]


async def handle_session_stop(args: Dict) -> List[TextContent]:
    req = SessionStopRequest(**arguments)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE sessions SET status = 'completed', stopped_at = ? WHERE session_id = ?", 
                   (datetime.utcnow().isoformat(), req.session_id))
    conn.commit()
    
    # Get final stats
    cursor.execute("SELECT event_count, created_at FROM sessions WHERE session_id = ?", (req.session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return [TextContent(type="text", text=json.dumps({
            "status": "STOPPED",
            "session_id": req.session_id,
            "duration_seconds": (datetime.utcnow() - datetime.fromisoformat(row["created_at"])).total_seconds(),
            "total_events": row["event_count"]
        }, indent=2))]
    else:
        return [TextContent(type="text", text=f"Session {req.session_id} not found")]


async def handle_session_replay(args: Dict) -> List[TextContent]:
    req = SessionReplayRequest(**arguments)
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM events WHERE session_id = ?"
    params = [req.session_id]
    
    if req.event_types:
        placeholders = ",".join("?" * len(req.event_types))
        query += f" AND event_type IN ({','.join(['?'] * len(req.event_types))})"
        params.extend(req.event_types)
    
    if req.start_from is not None:
        query += " AND event_index >= ?"
        params.append(req.start_from)
    
    query += " ORDER BY event_index"
    
    cursor.execute(query, params)
    events = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Parse JSON data
    for event in events:
        event["data"] = json.loads(event["data"])
    
    return [TextContent(type="text", text=json.dumps({
        "session_id": req.session_id,
        "total_events": len(events),
        "replay_speed": req.speed,
        "events": events
    }, indent=2))]


async def handle_session_diff(args: Dict) -> List[TextContent]:
    req = SessionDiffRequest(**arguments)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get events for both sessions
    events_a = {}
    cursor.execute("SELECT event_index, event_type, data FROM events WHERE session_id = ? ORDER BY event_index", (req.session_a,))
    for row in cursor.fetchall():
        events_a[row["event_index"]] = {"type": row["event_type"], "data": json.loads(row["data"])}
    
    events_b = {}
    cursor.execute("SELECT event_index, event_type, data FROM events WHERE session_id = ? ORDER BY event_index", (req.session_b,))
    for row in cursor.fetchall():
        events_b[row["event_index"]] = {"type": row["event_type"], "data": json.loads(row["data"])}
    
    conn.close()
    
    # Compute diff
    all_indices = set(events_a.keys()) | set(events_b.keys())
    diff = {
        "session_a": req.session_a,
        "session_b": req.session_b,
        "total_a": len(events_a),
        "total_b": len(events_b),
        "differences": [],
        "only_in_a": [],
        "only_in_b": [],
        "identical": []
    }
    
    for idx in sorted(all_indices):
        event_a = events_a.get(idx)
        event_b = events_b.get(idx)
        
        if event_a and event_b:
            # Compare events ignoring specified fields
            data_a = {k: v for k, v in event_a["data"].items() if k not in req.ignore_fields}
            data_b = {k: v for k, v in event_b["data"].items() if k not in req.ignore_fields}
            
            if event_a["type"] != event_b["type"] or data_a != data_b:
                diff["differences"].append({
                    "index": idx,
                    "a": event_a,
                    "b": event_b
                })
            else:
                diff["identical"].append(idx)
        elif event_a:
            diff["only_in_a"].append({"index": idx, "event": event_a})
        else:
            diff["only_in_b"].append({"index": idx, "event": event_b})
    
    return [TextContent(type="text", text=json.dumps(diff, indent=2))]


async def handle_session_list(args: Dict) -> List[TextContent]:
    req = SessionListRequest(**arguments)
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM sessions"
    params = []
    
    if req.status:
        query += " WHERE status = ?"
        params.append(req.status)
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([req.limit, req.offset])
    
    cursor.execute(query, params)
    sessions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Parse metadata
    for session in sessions:
        session["metadata"] = json.loads(session["metadata"]) if session["metadata"] else {}
    
    return [TextContent(type="text", text=json.dumps({
        "total_returned": len(sessions),
        "sessions": sessions
    }, indent=2))]


async def handle_session_export(args: Dict) -> List[TextContent]:
    req = SessionExportRequest(**arguments)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (req.session_id,))
    session = cursor.fetchone()
    
    if not session:
        return [TextContent(type="text", text=f"Session {req.session_id} not found")]
    
    cursor.execute("SELECT * FROM events WHERE session_id = ? ORDER BY event_index", (req.session_id,))
    events = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Parse events
    for event in events:
        event["data"] = json.loads(event["data"])
    
    export = {
        "session": dict(session),
        "events": events
    }
    export["session"]["metadata"] = json.loads(export["session"]["metadata"]) if export["session"]["metadata"] else {}
    
    if req.format == "csv":
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["event_index", "timestamp", "event_type", "data"])
        for event in events:
            writer.writerow([event["event_index"], event["timestamp"], event["event_type"], json.dumps(event["data"])])
        return [TextContent(type="text", text=output.getvalue())]
    else:
        return [TextContent(type="text", text=json.dumps(export, indent=2))]


async def handle_session_get(args: Dict) -> List[TextContent]:
    session_id = args.get("session_id", "")
    include_events = args.get("include_events", True)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
    session = cursor.fetchone()
    
    if not session:
        return [TextContent(type="text", text=f"Session {session_id} not found")]
    
    result = dict(session)
    result["metadata"] = json.loads(result["metadata"]) if result["metadata"] else {}
    
    if include_events:
        cursor.execute("SELECT * FROM events WHERE session_id = ? ORDER BY event_index", (session_id,))
        events = [dict(row) for row in cursor.fetchall()]
        for event in events:
            event["data"] = json.loads(event["data"])
        result["events"] = events
    
    conn.close()
    
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    # Initialize database on startup
    init_db()
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
