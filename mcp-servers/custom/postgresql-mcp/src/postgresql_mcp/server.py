"""
PostgreSQL MCP Server
PostgreSQL database management, queries, and administration.
"""

import asyncio
import json
import asyncpg
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

app = Server("postgresql-mcp")

# Database configuration
PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "postgres"
PG_PASSWORD = "postgres"
PG_DATABASE = "postgres"


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="query",
            description="Execute a SELECT query",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                    "params": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["sql"]
            },
        ),
        Tool(
            name="execute",
            description="Execute a non-SELECT query (INSERT, UPDATE, DELETE, DDL)",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                    "params": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["sql"]
            },
        ),
        Tool(
            name="tables_list",
            description="List all tables in database",
            inputSchema={
                "type": "object",
                "properties": {
                    "schema": {"type": "string", "default": "public"}
                },
                "required": []
            },
        ),
        Tool(
            name="table_schema",
            description="Get table schema",
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {"type": "string"},
                    "schema": {"type": "string", "default": "public"}
                },
                "required": ["table"]
            },
        ),
        Tool(
            name="indexes_list",
            description="List indexes on a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {"type": "string"},
                    "schema": {"type": "string", "default": "public"}
                },
                "required": ["table"]
            },
        ),
        Tool(
            name="table_stats",
            description="Get table statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {"type": "string"},
                    "schema": {"type": "string", "default": "public"}
                },
                "required": ["table"]
            },
        ),
        Tool(
            name="connections_list",
            description="List active connections",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="locks_list",
            description="List current locks",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="slow_queries",
            description="Get slow queries from pg_stat_statements",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 20}
                },
                "required": []
            },
        ),
        Tool(
            name="vacuum_analyze",
            description="Run VACUUM ANALYZE",
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {"type": "string"},
                    "full": {"type": "boolean", "default": False}
                },
                "required": []
            },
        ),
        Tool(
            name="backup_dump",
            description="Create logical backup (pg_dump style output)",
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {"type": "string"},
                    "schema": {"type": "string", "default": "public"},
                    "data_only": {"type": "boolean", "default": False}
                },
                "required": []
            },
        ),
        Tool(
            name="explain_analyze",
            description="Run EXPLAIN ANALYZE on a query",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                    "params": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["sql"]
            },
        ),
        Tool(
            name="replication_status",
            description="Get replication status",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="health_check",
            description="Health check",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "query":
            return await handle_query(arguments)
        elif name == "execute":
            return await handle_execute(arguments)
        elif name == "tables_list":
            return await handle_tables_list(arguments)
        elif name == "table_schema":
            return await handle_table_schema(arguments)
        elif name == "indexes_list":
            return await handle_indexes_list(arguments)
        elif name == "table_stats":
            return await handle_table_stats(arguments)
        elif name == "connections_list":
            return await handle_connections_list(arguments)
        elif name == "locks_list":
            return await handle_locks_list(arguments)
        elif name == "slow_queries":
            return await handle_slow_queries(arguments)
        elif name == "vacuum_analyze":
            return await handle_vacuum_analyze(arguments)
        elif name == "backup_dump":
            return await handle_backup_dump(arguments)
        elif name == "explain_analyze":
            return await handle_explain_analyze(arguments)
        elif name == "replication_status":
            return await handle_replication_status(arguments)
        elif name == "health_check":
            return await handle_health_check(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== HELPER ====================

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            host="localhost",
            port=5432,
            user="postgres",
            password="postgres",
            database="postgres",
            min_size=1,
            max_size=10
        )
    return _pool


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_query(args: Dict) -> List[TextContent]:
    sql = args.get("sql", "")
    params = args.get("params", [])
    
    pool = await get_pool()
    async with _pool.acquire() as conn:
        try:
            if params:
                rows = await conn.fetch(sql, *params)
            else:
                rows = await conn.fetch(sql)
            return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2, default=str))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_execute(args: Dict) -> List[TextContent]:
    sql = args.get("sql", "")
    params = args.get("params", [])
    
    pool = await get_pool()
    async with _pool.acquire() as conn:
        try:
            if params:
                result = await conn.execute(sql, *params)
            else:
                result = await conn.execute(sql)
            return [TextContent(type="text", text=json.dumps({"status": "EXECUTED", "result": result}, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_tables_list(args: Dict) -> List[TextContent]:
    schema = args.get("schema", "public")
    sql = """
        SELECT table_name, table_type
        FROM information_schema.tables
        WHERE table_schema = $1
        ORDER BY table_name
    """
    pool = await get_pool()
    async with _pool.acquire() as conn:
        rows = await conn.fetch(sql, schema)
        return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2))]


async def handle_table_schema(args: Dict) -> List[TextContent]:
    table = args.get("table", "")
    schema = args.get("schema", "public")
    
    sql = """
        SELECT column_name, data_type, is_nullable, column_default,
               character_maximum_length, numeric_precision, numeric_scale
        FROM information_schema.columns
        WHERE table_schema = $1 AND table_name = $2
        ORDER BY ordinal_position
    """
    pool = await get_pool()
    async with _pool.acquire() as conn:
        rows = await conn.fetch(sql, schema, table)
        return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2, default=str))]


async def handle_indexes_list(args: Dict) -> List[TextContent]:
    table = args.get("table", "")
    schema = args.get("schema", "public")
    
    sql = """
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE schemaname = $1 AND tablename = $2
    """
    pool = await get_pool()
    async with _pool.acquire() as conn:
        rows = await conn.fetch(sql, schema, table)
        return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2))]


async def handle_table_stats(args: Dict) -> List[TextContent]:
    table = args.get("table", "")
    schema = args.get("schema", "public")
    
    sql = """
        SELECT schemaname, relname, n_live_tup, n_dead_tup,
               last_vacuum, last_autovacuum, last_analyze, last_autoanalyze
        FROM pg_stat_user_tables
        WHERE schemaname = $1 AND relname = $2
    """
    pool = await get_pool()
    async with _pool.acquire() as conn:
        row = await conn.fetchrow(sql, schema, table)
        if row:
            return [TextContent(type="text", text=json.dumps(dict(row), indent=2, default=str))]
        return [TextContent(type="text", text="Table not found")]


async def handle_connections_list(args: Dict) -> List[TextContent]:
    sql = """
        SELECT pid, usename, application_name, client_addr, state,
               query_start, state_change, wait_event_type, wait_event
        FROM pg_stat_activity
        WHERE pid <> pg_backend_pid()
        ORDER BY query_start
    """
    pool = await get_pool()
    async with _pool.acquire() as conn:
        rows = await conn.fetch(sql)
        return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2, default=str))]


async def handle_locks_list(args: Dict) -> List[TextContent]:
    sql = """
        SELECT l.locktype, l.database, l.relation, l.page, l.tuple,
               l.virtualxid, l.virtualxid, l.pid, l.mode, l.granted, l.fastpath
        FROM pg_locks l
        JOIN pg_stat_activity a ON l.pid = a.pid
        WHERE l.pid <> pg_backend_pid()
    """
    pool = await get_pool()
    async with _pool.acquire() as conn:
        rows = await conn.fetch(sql)
        return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2))]


async def handle_slow_queries(args: Dict) -> List[TextContent]:
    limit = args.get("limit", 20)
    
    sql = """
        SELECT query, calls, total_exec_time, mean_exec_time,
               rows, shared_blks_hit, shared_blks_read
        FROM pg_stat_statements
        ORDER BY mean_exec_time DESC
        LIMIT $1
    """
    pool = await get_pool()
    async with _pool.acquire() as conn:
        rows = await conn.fetch(sql, limit)
        return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2, default=str))]


async def handle_vacuum_analyze(args: Dict) -> List[TextContent]:
    table = args.get("table")
    full = args.get("full", False)
    
    pool = await get_pool()
    async with _pool.acquire() as conn:
        try:
            if table:
                if full:
                    await conn.execute(f"VACUUM FULL ANALYZE {table}")
                else:
                    await conn.execute(f"VACUUM ANALYZE {table}")
            else:
                if full:
                    await conn.execute("VACUUM FULL ANALYZE")
                else:
                    await conn.execute("VACUUM ANALYZE")
            return [TextContent(type="text", text=json.dumps({"status": "COMPLETED"}, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_backup_dump(args: Dict) -> List[TextContent]:
    table = args.get("table")
    schema = args.get("schema", "public")
    data_only = args.get("data_only", False)
    
    if not table:
        return [TextContent(type="text", text="Table required")]
    
    try:
        sql = f"SELECT * FROM {schema}.{table}"
        pool = await get_pool()
        async with _pool.acquire() as conn:
            rows = await conn.fetch(sql)
            if args.get("data_only"):
                output = "INSERT INTO {}.{} VALUES ".format(schema, table)
                values = []
                for row in rows:
                    values.append("(" + ",".join(repr(v) for v in row.values()) + ")")
                output += ",\n".join(values) + ";"
            else:
                # Full dump with CREATE TABLE
                cols = list(rows[0].keys()) if rows else []
                output = "CREATE TABLE {}.{} (\n".format(schema, table)
                output += ",\n".join(["  {} TEXT".format(c) for c in cols]) + "\n);\n\n"
                for row in rows:
                    vals = ",".join(repr(v) for v in row.values())
                    output += "INSERT INTO {}.{} VALUES ({});\n".format(schema, table, vals)
            return [TextContent(type="text", text=output)]
    except Exception as e:
        return [TextContent(type="text", text="Error: {}".format(str(e)))]


async def handle_explain_analyze(args: Dict) -> List[TextContent]:
    sql = args.get("sql", "")
    params = args.get("params", [])
    
    if not sql:
        return [TextContent(type="text", text="SQL required")]
    
    pool = await get_pool()
    async with _pool.acquire() as conn:
        try:
            if params:
                result = await conn.fetch(f"EXPLAIN ANALYZE {sql}", *params)
            else:
                result = await conn.fetch(f"EXPLAIN ANALYZE {sql}")
            return [TextContent(type="text", text="\n".join([r[0] for r in result]))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_replication_status(args: Dict) -> List[TextContent]:
    sql = """
        SELECT pid, application_name, client_addr, state,
               sent_lsn, write_lsn, flush_lsn, replay_lsn,
               write_lag, flush_lag, replay_lag, sync_state
        FROM pg_stat_replication
    """
    pool = await get_pool()
    async with _pool.acquire() as conn:
        rows = await conn.fetch(sql)
        return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2, default=str))]


async def handle_health_check(args: Dict) -> List[TextContent]:
    try:
        pool = await get_pool()
        async with _pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return [TextContent(type="text", text=json.dumps({"healthy": True, "status": "OK"}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"healthy": False, "error": str(e)}, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
