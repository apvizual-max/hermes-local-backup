"""
Prometheus MCP Server
Query metrics, alerting rules, service discovery for monitoring.
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

app = Server("prometheus-mcp")


# ==================== MODELS ====================

class QueryRequest(BaseModel):
    query: str = Field(description="PromQL query string")
    time: Optional[str] = Field(default=None, description="RFC3339 timestamp or Unix timestamp")
    timeout: str = Field(default="30s", description="Query timeout")


class QueryRangeRequest(BaseModel):
    query: str = Field(description="PromQL query string")
    start: str = Field(description="Start timestamp (RFC3339 or Unix)")
    end: str = Field(description="End timestamp (RFC3339 or Unix)")
    step: str = Field(description="Query resolution step width (e.g., '15s', '1m', '1h')")
    timeout: str = Field(default="30s", description="Query timeout")


class SeriesRequest(BaseModel):
    match: List[str] = Field(description="Series selectors (e.g., ['up', 'http_requests_total{job=\"api\"}'])")
    start: Optional[str] = Field(default=None, description="Start timestamp")
    end: Optional[str] = Field(default=None, description="End timestamp")


class LabelValuesRequest(BaseModel):
    label: str = Field(description="Label name")
    match: Optional[List[str]] = Field(default=None, description="Series selectors")


class AlertsRequest(BaseModel):
    filter: Optional[str] = Field(default=None, description="Filter alerts (e.g., 'alertname=~.*')")


class RulesRequest(BaseModel):
    type: str = Field(default="all", description="Rule type: alert, recording, all")


class TargetsRequest(BaseModel):
    state: Optional[str] = Field(default=None, description="Target state: active, dropped, any")


class MetadataRequest(BaseModel):
    metric: Optional[str] = Field(default=None, description="Metric name filter")
    limit: int = Field(default=100, description="Maximum results")


# ==================== SERVER ====================

app = Server("prometheus-mcp")

# Configuration - set via environment or config
PROMETHEUS_URL = "http://localhost:9090"


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="query",
            description="Execute instant PromQL query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "time": {"type": "string"},
                    "timeout": {"type": "string", "default": "30s"}
                },
                "required": ["query"]
            },
        ),
        Tool(
            name="query_range",
            description="Execute range PromQL query over time range",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                    "step": {"type": "string"},
                    "timeout": {"type": "string", "default": "30s"}
                },
                "required": ["query", "start", "end", "step"]
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
            name="label_values",
            description="Get values for a specific label",
            inputSchema={
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "match": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["label"]
            },
        ),
        Tool(
            name="alerts",
            description="Get active alerts",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="rules",
            description="Get alerting and recording rules",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["alert", "recording", "all"], "default": "all"}
                },
                "required": []
            },
        ),
        Tool(
            name="targets",
            description="Get scrape targets status",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {"type": "string", "enum": ["active", "dropped", "any"]}
                },
                "required": []
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
            description="Check Prometheus health and readiness",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="config",
            description="Get Prometheus configuration",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="flags",
            description="Get Prometheus runtime flags",
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
        elif name == "series":
            return await handle_series(arguments)
        elif name == "label_values":
            return await handle_label_values(arguments)
        elif name == "alerts":
            return await handle_alerts(arguments)
        elif name == "rules":
            return await handle_rules(arguments)
        elif name == "targets":
            return await handle_targets(arguments)
        elif name == "metadata":
            return await handle_metadata(arguments)
        elif name == "health":
            return await handle_health(arguments)
        elif name == "config":
            return await handle_config(arguments)
        elif name == "flags":
            return await handle_flags(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== TOOL IMPLEMENTATIONS ====================

async def _request(endpoint: str, params: Dict = None) -> Dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{PROMETHEUS_URL}/api/v1/{endpoint}"
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


async def handle_query(args: Dict) -> List[TextContent]:
    query = args.get("query", "")
    time = args.get("time")
    timeout = args.get("timeout", "30s")
    
    params = {"query": query, "timeout": timeout}
    if time:
        params["time"] = time
    
    try:
        result = await _request("query", params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_query_range(args: Dict) -> List[TextContent]:
    query = args.get("query", "")
    start = args.get("start", "")
    end = args.get("end", "")
    step = args.get("step", "")
    timeout = args.get("timeout", "30s")
    
    params = {"query": query, "start": start, "end": end, "step": step, "timeout": timeout}
    
    try:
        result = await _request("query_range", params)
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
        result = await _request("series", params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_label_values(args: Dict) -> List[TextContent]:
    label = args.get("label", "")
    match = args.get("match", [])
    
    if not label:
        return [TextContent(type="text", text="label parameter required")]
    
    params = {"match[]": match} if match else {}
    
    try:
        result = await _request(f"label/{label}/values", params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_alerts(args: Dict) -> List[TextContent]:
    filter_str = args.get("filter")
    params = {}
    if filter_str:
        params["filter"] = filter_str
    
    try:
        result = await _request("alerts", params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_rules(args: Dict) -> List[TextContent]:
    req_type = args.get("type", "all")
    
    try:
        result = await _request("rules", {})
        if req_type != "all":
            groups = result.get("data", {}).get("groups", [])
            filtered = [g for g in groups if g.get("type") == req_type]
            result = {"status": "success", "data": {"groups": filtered}}
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_targets(args: Dict) -> List[TextContent]:
    state = args.get("state")
    params = {}
    if state:
        params["state"] = state
    
    try:
        result = await _request("targets", params)
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
        result = await _request("metadata", params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_health(args: Dict) -> List[TextContent]:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check ready
            ready = await client.get(f"{PROMETHEUS_URL}/-/ready")
            ready_ok = ready.status_code == 200
            
            # Check healthy
            healthy = await client.get(f"{PROMETHEUS_URL}/-/healthy")
            healthy_ok = healthy.status_code == 200
            
            return [TextContent(type="text", text=json.dumps({
                "ready": ready_ok,
                "healthy": healthy_ok,
                "overall": "HEALTHY" if ready_ok and healthy_ok else "DEGRADED"
            }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_config(args: Dict) -> List[TextContent]:
    try:
        result = await _request("status/config", {})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_flags(args: Dict) -> List[TextContent]:
    try:
        result = await _request("status/flags", {})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
