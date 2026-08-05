"""
Loki MCP Server
Grafana Loki log aggregation query and management.
"""

import asyncio
import json
import httpx
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

app = Server("loki-mcp")

LOKI_URL = "http://localhost:3100"


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="query",
            description="Execute instant LogQL query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 100},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                    "direction": {"type": "string", "enum": ["FORWARD", "BACKWARD"], "default": "BACKWARD"},
                    "regexp": {"type": "string"}
                },
                "required": ["query"]
            },
        ),
        Tool(
            name="query_range",
            description="Execute range LogQL query over time range",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                    "limit": {"type": "integer", "default": 100},
                    "step": {"type": "string"}
                },
                "required": ["query", "start", "end"]
            },
        ),
        Tool(
            name="labels",
            description="Get all label names",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="label_values",
            description="Get values for a specific label",
            inputSchema={
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"}
                },
                "required": ["label"]
            },
        ),
        Tool(
            name="series",
            description="Find series by label matchers",
            inputSchema={
                "type": "object",
                "properties": {
                    "match": {"type": "array", "items": {"type": "string"}},
                    "start": {"type": "string"},
                    "end": {"type": "string"}
                },
                "required": ["match"]
            },
        ),
        Tool(
            name="tail",
            description="Tail logs in real-time (polling)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                    "delay": {"type": "integer", "default": 1}
                },
                "required": ["query"]
            },
        ),
        Tool(
            name="rules_list",
            description="List recording and alerting rules",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="rules_get",
            description="Get rule group by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["namespace", "name"]
            },
        ),
        Tool(
            name="rules_create",
            description="Create or update rule group",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "name": {"type": "string"},
                    "interval": {"type": "string", "default": "1m"},
                    "rules": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["namespace", "name", "rules"]
            },
        ),
        Tool(
            name="rules_delete",
            description="Delete rule group",
            inputSchema={
                "type": "object",
                "properties": {
                    "namespace": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["namespace", "name"]
            },
        ),
        Tool(
            name="metadata",
            description="Get metric metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "metric": {"type": "string"},
                    "limit": {"type": "integer", "default": 100}
                },
                "required": []
            },
        ),
        Tool(
            name="health",
            description="Check Loki health",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="config",
            description="Get Loki configuration",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="tsdb_stats",
            description="Get TSDB stats",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "query":
            return await handle_query(arguments)
        elif name == "query_range":
            return await handle_query_range(arguments)
        elif name == "labels":
            return await handle_labels(arguments)
        elif name == "label_values":
            return await handle_label_values(arguments)
        elif name == "series":
            return await handle_series(arguments)
        elif name == "tail":
            return await handle_tail(arguments)
        elif name == "rules_list":
            return await handle_rules_list(arguments)
        elif name == "rules_get":
            return await handle_rules_get(arguments)
        elif name == "rules_create":
            return await handle_rules_create(arguments)
        elif name == "rules_delete":
            return await handle_rules_delete(arguments)
        elif name == "metadata":
            return await handle_metadata(arguments)
        elif name == "health":
            return await handle_health(arguments)
        elif name == "config":
            return await handle_config(arguments)
        elif name == "tsdb_stats":
            return await handle_tsdb_stats(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== HELPER FUNCTIONS ====================

LOKI_URL = "http://localhost:3100"


async def _request(endpoint: str, params: Dict = None, method: str = "GET", data: Dict = None) -> Dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{LOKI_URL}/loki/api/v1/{endpoint}"
        if method == "GET":
            resp = await client.get(url, params=params, timeout=30.0)
        elif method == "POST":
            resp = await client.post(url, json=data, params=params, timeout=30.0)
        elif method == "DELETE":
            resp = await client.delete(url, params=params, timeout=30.0)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        resp.raise_for_status()
        return resp.json()


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_query(args: Dict) -> List[TextContent]:
    query = args.get("query", "")
    limit = args.get("limit", 100)
    start = args.get("start")
    end = args.get("end")
    direction = args.get("direction", "BACKWARD")
    regexp = args.get("regexp")
    
    params = {"query": query, "limit": str(limit), "direction": direction}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    if regexp:
        params["regexp"] = regexp
    
    try:
        result = await _request("query", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_query_range(args: Dict) -> List[TextContent]:
    query = args.get("query", "")
    start = args.get("start", "")
    end = args.get("end", "")
    limit = args.get("limit", 100)
    step = args.get("step")
    
    params = {"query": query, "start": start, "end": end, "limit": str(limit)}
    if step:
        params["step"] = step
    
    try:
        result = await _request("query_range", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_labels(args: Dict) -> List[TextContent]:
    try:
        result = await _request("labels", params={})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_label_values(args: Dict) -> List[TextContent]:
    label = args.get("label", "")
    start = args.get("start")
    end = args.get("end")
    
    if not label:
        return [TextContent(type="text", text="label parameter required")]
    
    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    
    try:
        result = await _request(f"label/{label}/values", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_series(args: Dict) -> List[TextContent]:
    match = args.get("match", [])
    start = args.get("start")
    end = args.get("end")
    
    params = {"match[]": match}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    
    try:
        result = await _request("series", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_tail(args: Dict) -> List[TextContent]:
    query = args.get("query", "")
    limit = args.get("limit", 10)
    delay = args.get("delay", 1)
    
    # For tailing, we'll do a single query with BACKWARD direction
    params = {"query": query, "limit": str(limit), "direction": "BACKWARD"}
    
    try:
        result = await _request("query", params=params)
        return [TextContent(type="text", text=json.dumps({
            "note": "This is a single query. For true tailing, implement polling in your application.",
            "result": result
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_rules_list(args: Dict) -> List[TextContent]:
    try:
        result = await _request("rules", params={})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_rules_get(args: Dict) -> List[TextContent]:
    namespace = args.get("namespace", "")
    name = args.get("name", "")
    
    if not namespace or not name:
        return [TextContent(type="text", text="namespace and name required")]
    
    try:
        # Loki rules API doesn't have a direct get-by-name, so we list and filter
        result = await _request("rules", params={})
        groups = result.get("data", {}).get("groups", [])
        for group in groups:
            if group.get("name") == name and group.get("namespace") == namespace:
                return [TextContent(type="text", text=json.dumps(group, indent=2))]
        return [TextContent(type="text", text=f"Rule group '{name}' in namespace '{namespace}' not found")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_rules_create(args: Dict) -> List[TextContent]:
    namespace = args.get("namespace", "")
    name = args.get("name", "")
    interval = args.get("interval", "1m")
    rules = args.get("rules", [])
    
    if not namespace or not name or not rules:
        return [TextContent(type="text", text="namespace, name, and rules required")]
    
    data = {
        "namespace": namespace,
        "name": name,
        "interval": interval,
        "rules": rules
    }
    
    try:
        result = await _request("rules", method="POST", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_rules_delete(args: Dict) -> List[TextContent]:
    namespace = args.get("namespace", "")
    name = args.get("name", "")
    
    if not namespace or not name:
        return [TextContent(type="text", text="namespace and name required")]
    
    try:
        result = await _request(f"rules/{namespace}/{name}", method="DELETE")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_metadata(args: Dict) -> List[TextContent]:
    metric = args.get("metric")
    limit = args.get("limit", 100)
    
    params = {"limit": str(limit)}
    if metric:
        params["metric"] = metric
    
    try:
        result = await _request("metadata", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_health(args: Dict) -> List[TextContent]:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            ready = await client.get(f"{LOKI_URL}/ready")
            ready_ok = ready.status_code == 200
            
            return [TextContent(type="text", text=json.dumps({
                "ready": ready_ok,
                "status_code": ready.status_code,
                "overall": "HEALTHY" if ready_ok else "UNHEALTHY"
            }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_config(args: Dict) -> List[TextContent]:
    try:
        result = await _request("config", params={})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_tsdb_stats(args: Dict) -> List[TextContent]:
    try:
        result = await _request("tsdb/stats", params={})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
