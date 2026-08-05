"""
Elasticsearch MCP Server
Elasticsearch cluster management, search, and analytics.
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


class IndexCreateRequest(BaseModel):
    name: str
    settings: Optional[Dict[str, Any]] = None
    mappings: Optional[Dict[str, Any]] = None

class DocumentIndexRequest(BaseModel):
    index: str
    id: Optional[str] = None
    document: Dict[str, Any]
    refresh: bool = False

class DocumentUpdateRequest(BaseModel):
    index: str
    id: str
    document: Optional[Dict[str, Any]] = None
    script: Optional[str] = None

class SearchRequest(BaseModel):
    index: str
    query: Dict[str, Any]
    size: int = 10
    from_: int = Field(default=0, alias="from")

class BulkIndexRequest(BaseModel):
    index: str
    documents: List[Dict[str, Any]]

class DeleteByQueryRequest(BaseModel):
    index: str
    query: Dict[str, Any]

class TemplateCreateRequest(BaseModel):
    name: str
    template: Dict[str, Any]
    priority: int = 100

class ILMPolicyRequest(BaseModel):
    name: str
    policy: Dict[str, Any]

class SnapshotCreateRepoRequest(BaseModel):
    name: str
    type: str
    settings: Dict[str, Any]

class SnapshotCreateRequest(BaseModel):
    repository: str
    name: str
    indices: Optional[List[str]] = None
    ignore_unavailable: bool = False
    include_global_state: bool = True

class SnapshotRestoreRequest(BaseModel):
    repository: str
    name: str
    indices: Optional[List[str]] = None
    rename_pattern: Optional[str] = None
    rename_replacement: Optional[str] = None

app = Server("elasticsearch-mcp")

ES_URL = "http://localhost:9200"


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="health_check",
            description="Check Elasticsearch cluster health",
            inputSchema={
                "type": "object",
                "properties": {
                    "detailed": {"type": "boolean", "default": False}
                },
                "required": []
            },
        ),
        Tool(
            name="cluster_stats",
            description="Get cluster statistics",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="indices_list",
            description="List all indices",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "default": "*"},
                    "include_system": {"type": "boolean", "default": False}
                },
                "required": []
            },
        ),
        Tool(
            name="index_create",
            description="Create an index",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "settings": {"type": "object"},
                    "mappings": {"type": "object"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="index_delete",
            description="Delete an index",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="index_exists",
            description="Check if index exists",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="document_index",
            description="Index a document",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "id": {"type": "string"},
                    "document": {"type": "object"},
                    "refresh": {"type": "boolean", "default": False}
                },
                "required": ["index", "document"]
            },
        ),
        Tool(
            name="document_get",
            description="Get a document by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "id": {"type": "string"}
                },
                "required": ["index", "id"]
            },
        ),
        Tool(
            name="document_update",
            description="Update a document",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "id": {"type": "string"},
                    "document": {"type": "object"},
                    "script": {"type": "string"}
                },
                "required": ["index", "id"]
            },
        ),
        Tool(
            name="document_delete",
            description="Delete a document",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "id": {"type": "string"}
                },
                "required": ["index", "id"]
            },
        ),
        Tool(
            name="search",
            description="Search documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "query": {"type": "object"},
                    "size": {"type": "integer", "default": 10},
                    "from": {"type": "integer", "default": 0}
                },
                "required": ["index", "query"]
            },
        ),
        Tool(
            name="search_scroll",
            description="Scroll through large result sets",
            inputSchema={
                "type": "object",
                "properties": {
                    "scroll_id": {"type": "string"},
                    "scroll": {"type": "string", "default": "1m"}
                },
                "required": ["scroll_id"]
            },
        ),
        Tool(
            name="bulk_index",
            description="Bulk index documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "documents": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["index", "documents"]
            },
        ),
        Tool(
            name="delete_by_query",
            description="Delete documents by query",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "query": {"type": "object"}
                },
                "required": ["index", "query"]
            },
        ),
        Tool(
            name="template_create",
            description="Create index template",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "template": {"type": "object"},
                    "priority": {"type": "integer", "default": 100}
                },
                "required": ["name", "template"]
            },
        ),
        Tool(
            name="template_get",
            description="Get index template",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="ilm_policy_create",
            description="Create ILM policy",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "policy": {"type": "object"}
                },
                "required": ["name", "policy"]
            },
        ),
        Tool(
            name="ilm_policy_get",
            description="Get ILM policy",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="snapshot_create_repo",
            description="Create snapshot repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "settings": {"type": "object"}
                },
                "required": ["name", "type", "settings"]
            },
        ),
        Tool(
            name="snapshot_create",
            description="Create snapshot",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository": {"type": "string"},
                    "name": {"type": "string"},
                    "indices": {"type": "array", "items": {"type": "string"}},
                    "ignore_unavailable": {"type": "boolean", "default": False},
                    "include_global_state": {"type": "boolean", "default": True}
                },
                "required": ["repository", "name"]
            },
        ),
        Tool(
            name="snapshot_restore",
            description="Restore snapshot",
            inputSchema={
                "type": "object",
                "properties": {
                    "repository": {"type": "string"},
                    "name": {"type": "string"},
                    "indices": {"type": "array", "items": {"type": "string"}},
                    "rename_pattern": {"type": "string"},
                    "rename_replacement": {"type": "string"}
                },
                "required": ["repository", "name"]
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "health_check":
            return await handle_health_check(arguments)
        elif name == "cluster_stats":
            return await handle_cluster_stats(arguments)
        elif name == "indices_list":
            return await handle_indices_list(arguments)
        elif name == "index_create":
            return await handle_index_create(arguments)
        elif name == "index_delete":
            return await handle_index_delete(arguments)
        elif name == "index_exists":
            return await handle_index_exists(arguments)
        elif name == "document_index":
            return await handle_document_index(arguments)
        elif name == "document_get":
            return await handle_document_get(arguments)
        elif name == "document_update":
            return await handle_document_update(arguments)
        elif name == "document_delete":
            return await handle_document_delete(arguments)
        elif name == "search":
            return await handle_search(arguments)
        elif name == "search_scroll":
            return await handle_search_scroll(arguments)
        elif name == "bulk_index":
            return await handle_bulk_index(arguments)
        elif name == "delete_by_query":
            return await handle_delete_by_query(arguments)
        elif name == "template_create":
            return await handle_template_create(arguments)
        elif name == "template_get":
            return await handle_template_get(arguments)
        elif name == "ilm_policy_create":
            return await handle_ilm_policy_create(arguments)
        elif name == "ilm_policy_get":
            return await handle_ilm_policy_get(arguments)
        elif name == "snapshot_create_repo":
            return await handle_snapshot_create_repo(arguments)
        elif name == "snapshot_create":
            return await handle_snapshot_create(arguments)
        elif name == "snapshot_restore":
            return await handle_snapshot_restore(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== HELPER FUNCTIONS ====================

ES_URL = "http://localhost:9200"


async def _request(endpoint: str, params: Dict = None, method: str = "GET", data: Dict = None) -> Dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{ES_URL}/{endpoint}"
        if method == "GET":
            resp = await client.get(url, params=params, timeout=30.0)
        elif method == "POST":
            resp = await client.post(url, json=data, params=params, timeout=30.0)
        elif method == "PUT":
            resp = await client.put(url, json=data, timeout=30.0)
        elif method == "DELETE":
            resp = await client.delete(url, timeout=30.0)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        resp.raise_for_status()
        return resp.json()


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_health_check(args: Dict) -> List[TextContent]:
    try:
        result = await _request("_cluster/health", params={})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_cluster_stats(args: Dict) -> List[TextContent]:
    try:
        result = await _request("_cluster/stats", params={})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_indices_list(args: Dict) -> List[TextContent]:
    pattern = args.get("pattern", "*")
    include_system = args.get("include_system", False)
    
    try:
        result = await _request(f"_cat/indices/{pattern}", params={"format": "json", "v": "true"})
        if not include_system:
            result = [i for i in result if not i.get("index", "").startswith(".")]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_index_create(args: Dict) -> List[TextContent]:
    req = IndexCreateRequest(**args)
    data = req.model_dump(exclude_none=True)
    result = await _request(f"{req.name}", method="PUT", data=data)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_index_delete(args: Dict) -> List[TextContent]:
    name = args.get("name", "")
    try:
        result = await _request(f"{name}", method="DELETE")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_index_exists(args: Dict) -> List[TextContent]:
    name = args.get("name", "")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.head(f"{ES_URL}/{name}")
            exists = resp.status_code == 200
            return [TextContent(type="text", text=json.dumps({"exists": exists, "index": name}, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_document_index(args: Dict) -> List[TextContent]:
    req = DocumentIndexRequest(**args)
    data = req.document
    url = f"{req.index}/_doc"
    if req.id:
        url += f"/{req.id}"
    params = {"refresh": str(req.refresh).lower()}
    
    try:
        result = await _request(url, method="POST", data=req.document, params=params)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_document_get(args: Dict) -> List[TextContent]:
    index = args.get("index", "")
    doc_id = args.get("id", "")
    try:
        result = await _request(f"{index}/_doc/{doc_id}")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_document_update(args: Dict) -> List[TextContent]:
    req = DocumentUpdateRequest(**args)
    data = {"doc": req.document}
    if req.script:
        data["script"] = {"source": req.script}
    
    try:
        result = await _request(f"{req.index}/_doc/{req.id}/_update", method="POST", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_document_delete(args: Dict) -> List[TextContent]:
    index = args.get("index", "")
    doc_id = args.get("id", "")
    try:
        result = await _request(f"{index}/_doc/{doc_id}", method="DELETE")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_search(args: Dict) -> List[TextContent]:
    req = SearchRequest(**args)
    data = req.model_dump(exclude_none=True)
    try:
        result = await _request(f"{req.index}/_search", method="POST", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_search_scroll(args: Dict) -> List[TextContent]:
    scroll_id = args.get("scroll_id", "")
    scroll = args.get("scroll", "1m")
    
    data = {"scroll": scroll, "scroll_id": scroll_id}
    try:
        result = await _request("_search/scroll", method="POST", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_bulk_index(args: Dict) -> List[TextContent]:
    req = BulkIndexRequest(**args)
    index = req.index
    documents = req.documents
    
    # Build bulk request body
    bulk_body = ""
    for doc in documents:
        bulk_body += json.dumps({"index": {"_index": index}}) + "\n"
        bulk_body += json.dumps(doc) + "\n"
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{ES_URL}/_bulk",
                content=bulk_body,
                headers={"Content-Type": "application/x-ndjson"},
                timeout=60.0
            )
            resp.raise_for_status()
            return [TextContent(type="text", text=json.dumps(resp.json(), indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_delete_by_query(args: Dict) -> List[TextContent]:
    req = DeleteByQueryRequest(**args)
    data = {"query": req.query}
    
    try:
        result = await _request(f"{req.index}/_delete_by_query", method="POST", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_template_create(args: Dict) -> List[TextContent]:
    req = TemplateCreateRequest(**args)
    data = req.model_dump(exclude_none=True)
    
    try:
        result = await _request(f"_index_template/{req.name}", method="PUT", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_template_get(args: Dict) -> List[TextContent]:
    name = args.get("name", "")
    try:
        result = await _request(f"_index_template/{name}")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_ilm_policy_create(args: Dict) -> List[TextContent]:
    req = ILMPolicyRequest(**args)
    data = req.policy
    
    try:
        result = await _request(f"_ilm/policy/{req.name}", method="PUT", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_ilm_policy_get(args: Dict) -> List[TextContent]:
    name = args.get("name", "")
    try:
        result = await _request(f"_ilm/policy/{name}")
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_snapshot_create_repo(args: Dict) -> List[TextContent]:
    req = SnapshotCreateRepoRequest(**args)
    data = {"type": req.type, "settings": req.settings}
    
    try:
        result = await _request(f"_snapshot/{req.name}", method="PUT", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_snapshot_create(args: Dict) -> List[TextContent]:
    req = SnapshotCreateRequest(**args)
    data = req.model_dump(exclude_none=True)
    
    try:
        result = await _request(f"_snapshot/{req.repository}/{req.name}", method="PUT", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_snapshot_restore(args: Dict) -> List[TextContent]:
    req = SnapshotRestoreRequest(**args)
    data = req.model_dump(exclude_none=True)
    
    try:
        result = await _request(f"_snapshot/{req.repository}/{req.name}/_restore", method="POST", data=data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
