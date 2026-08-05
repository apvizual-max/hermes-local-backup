"""
Tempo MCP Server
Grafana Tempo distributed tracing query and management.
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

app = Server("tempo-mcp")

TEMPO_URL = "http://localhost:3200"


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="trace_query",
            description="Search traces using TraceQL",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                    "limit": {"type": "integer", "default": 100}
                },
                "required": ["query"]
            },
        ),
        Tool(
            name="trace_get",
            description="Get full trace by Trace ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "trace_id": {"type": "string"}
                },
                "required": ["trace_id"]
            },
        ),
        Tool(
            name="trace_search",
            description="Search traces using Lucene query syntax",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                    "limit": {"type": "integer", "default": 20}
                },
                "required": ["query"]
            },
        ),
        Tool(
            name="services_list",
            description="List all services",
            inputSchema={
                "type": "object",
                "properties": {
                    "start": {"type": "string"},
                    "end": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="service_stats",
            description="Get statistics for a service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"}
                },
                "required": ["service"]
            },
        ),
        Tool(
            name="metrics_summary",
            description="Get metrics summary (RED metrics)",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="trace_tail",
            description="Tail recent traces for a service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["service"]
            },
        ),
        Tool(
            name="health",
            description="Check Tempo health",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="config",
            description="Get Tempo configuration",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "trace_query":
            return await handle_trace_query(arguments)
        elif name == "trace_get":
            return await handle_trace_get(arguments)
        elif name == "trace_search":
            return await handle_trace_search(arguments)
        elif name == "services_list":
            return await handle_services_list(arguments)
        elif name == "service_stats":
            return await handle_service_stats(arguments)
        elif name == "metrics_summary":
            return await handle_metrics_summary(arguments)
        elif name == "trace_tail":
            return await handle_trace_tail(arguments)
        elif name == "health":
            return await handle_health(arguments)
        elif name == "config":
            return await handle_config(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== HELPER FUNCTIONS ====================

TEMPO_URL = "http://localhost:3200"


async def _request(endpoint: str, params: Dict = None, method: str = "GET", data: Dict = None) -> Dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{TEMPO_URL}/api/{endpoint}"
        if method == "GET":
            resp = await client.get(url, params=params, timeout=30.0)
        elif method == "POST":
            resp = await client.post(url, json=data, timeout=30.0)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        resp.raise_for_status()
        return resp.json()


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_trace_query(args: Dict) -> List[TextContent]:
    query = args.get("query", "")
    start = args.get("start")
    end = args.get("end")
    limit = args.get("limit", 100)
    
    params = {"query": query, "limit": str(limit)}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    
    try:
        result = await _request("search", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_trace_get(args: Dict) -> List[TextContent]:
    trace_id = args.get("trace_id", "")
    if not trace_id:
        return [TextContent(type="text", text="trace_id required")]
    
    try:
        result = await _request(f"traces/{trace_id}")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_trace_search(args: Dict) -> List[TextContent]:
    query = args.get("query", "")
    start = args.get("start")
    end = args.get("end")
    limit = args.get("limit", 20)
    
    if not query:
        return [TextContent(type="text", text="query required")]
    
    params = {"q": query, "limit": str(limit)}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    
    try:
        result = await _request("search", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_services_list(args: Dict) -> List[TextContent]:
    start = args.get("start")
    end = args.get("end")
    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    
    try:
        result = await _request("services", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_service_stats(args: Dict) -> List[TextContent]:
    service = args.get("service", "")
    start = args.get("start")
    end = args.get("end")
    
    if not service:
        return [TextContent(type="text", text="service required")]
    
    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    
    try:
        result = await _request(f"services/{service}/stats", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_metrics_summary(args: Dict) -> List[TextContent]:
    service = args.get("service")
    start = args.get("start")
    end = args.get("end")
    params = {}
    if service:
        params["service"] = service
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    
    try:
        result = await _request("metrics/summary", params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_trace_tail(args: Dict) -> List[TextContent]:
    service = args.get("service", "")
    limit = args.get("limit", 10)
    
    if not service:
        return [TextContent(type="text", text="service required")]
    
    # Query recent traces for service
    query = f'{{.service.name = "{service}"}}'
    params = {"query": query, "limit": str(limit)}
    
    try:
        result = await _request("search", params=params)
        return [TextContent(type="text", text=json.dumps({
            "note": "This is a search query. For true tailing, implement polling in your application.",
            "result": result
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_health(args: Dict) -> List[TextContent]:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            ready = await client.get(f"{TEMPO_URL}/ready")
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


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
