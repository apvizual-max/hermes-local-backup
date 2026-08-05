"""
SearXNG MCP Server
Simple wrapper to connect to running SearXNG instance via HTTP.
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

app = Server("searxng-mcp")

SEARXNG_URL = "http://localhost:8081"

class SearchRequest(BaseModel):
    query: str = Field(description="Search query")
    categories: Optional[str] = Field(default=None, description="Categories to search")
    engines: Optional[str] = Field(default=None, description="Engines to use")
    language: Optional[str] = Field(default=None, description="Language code")
    pageno: int = Field(default=1, description="Page number")
    time_range: Optional[str] = Field(default=None, description="Time range: day, week, month, year")
    format: str = Field(default="json", description="Response format")

class SuggestRequest(BaseModel):
    query: str = Field(description="Query for suggestions")

@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="search",
            description="Search using SearXNG",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "categories": {"type": "string"},
                    "engines": {"type": "string"},
                    "language": {"type": "string"},
                    "pageno": {"type": "integer", "default": 1},
                    "time_range": {"type": "string"},
                    "format": {"type": "string", "default": "json"}
                },
                "required": ["query"]
            },
        ),
        Tool(
            name="suggest",
            description="Get search suggestions",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            },
        ),
        Tool(
            name="health_check",
            description="Check SearXNG health",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "search":
            req = SearchRequest(**arguments)
            return await handle_search(req)
        elif name == "suggest":
            req = SuggestRequest(**arguments)
            return await handle_suggest(req)
        elif name == "health_check":
            return await handle_health_check(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]

async def handle_search(req: SearchRequest) -> List[TextContent]:
    params = {"q": req.query, "format": req.format}
    if req.categories:
        params["categories"] = req.categories
    if req.engines:
        params["engines"] = req.engines
    if req.language:
        params["language"] = req.language
    if req.pageno > 1:
        params["pageno"] = str(req.pageno)
    if req.time_range:
        params["time_range"] = req.time_range
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Hermes-Agent/1.0",
        "Accept": "application/json, text/html;q=0.9",
        "X-Forwarded-For": "127.0.0.1",
        "X-Real-IP": "127.0.0.1",
    }
    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        resp = await client.get(f"{SEARXNG_URL}/search", params=params)
        resp.raise_for_status()
        return [TextContent(type="text", text=resp.text)]

async def handle_suggest(req: SuggestRequest) -> List[TextContent]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Hermes-Agent/1.0",
        "Accept": "application/json, text/html;q=0.9",
        "X-Forwarded-For": "127.0.0.1",
        "X-Real-IP": "127.0.0.1",
    }
    async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
        resp = await client.get(f"{SEARXNG_URL}/api/suggest", params={"q": req.query})
        resp.raise_for_status()
        return [TextContent(type="text", text=resp.text)]

async def handle_health_check(args: Dict) -> List[TextContent]:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Hermes-Agent/1.0",
            "X-Forwarded-For": "127.0.0.1",
            "X-Real-IP": "127.0.0.1",
        }
        async with httpx.AsyncClient(timeout=5.0, headers=headers) as client:
            resp = await client.get(f"{SEARXNG_URL}/")
            return [TextContent(type="text", text=json.dumps({
                "healthy": resp.status_code == 200,
                "status_code": resp.status_code
            }))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "healthy": False,
            "error": str(e)
        }))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
