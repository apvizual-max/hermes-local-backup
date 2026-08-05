"""
Grafana MCP Server
Grafana dashboards, datasources, alerts, and user management.
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

app = Server("grafana-mcp")

GRAFANA_URL = "http://localhost:3000"
GRAFANA_API_KEY = ""


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="datasource_create",
            description="Create a new datasource",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "access": {"type": "string", "default": "proxy"},
                    "url": {"type": "string"},
                    "access_token": {"type": "string"},
                    "database": {"type": "string"},
                    "user": {"type": "string"},
                    "password": {"type": "string"},
                    "json_data": {"type": "object"},
                    "secure_json_data": {"type": "object"}
                },
                "required": ["name", "type", "url"]
            },
        ),
        Tool(
            name="datasource_list",
            description="List all datasources",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="datasource_get",
            description="Get datasource by UID",
            inputSchema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"}
                },
                "required": ["uid"]
            },
        ),
        Tool(
            name="datasource_delete",
            description="Delete datasource by UID",
            inputSchema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"}
                },
                "required": ["uid"]
            },
        ),
        Tool(
            name="dashboard_create",
            description="Create or update a dashboard",
            inputSchema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"},
                    "title": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "timezone": {"type": "string", "default": "utc"},
                    "schema_version": {"type": "integer", "default": 16},
                    "version": {"type": "integer", "default": 0},
                    "panels": {"type": "array", "items": {"type": "object"}},
                    "templating": {"type": "object"},
                    "time": {"type": "object"},
                    "refresh": {"type": "string"}
                },
                "required": ["title"]
            },
        ),
        Tool(
            name="dashboard_get",
            description="Get dashboard by UID",
            inputSchema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"}
                },
                "required": ["uid"]
            },
        ),
        Tool(
            name="dashboard_delete",
            description="Delete dashboard by UID",
            inputSchema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"}
                },
                "required": ["uid"]
            },
        ),
        Tool(
            name="dashboard_list",
            description="List dashboards",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "tag": {"type": "string"},
                    "limit": {"type": "integer", "default": 50}
                },
                "required": []
            },
        ),
        Tool(
            name="alert_rule_create",
            description="Create or update an alert rule",
            inputSchema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"},
                    "title": {"type": "string"},
                    "condition": {"type": "string"},
                    "data": {"type": "array", "items": {"type": "object"}},
                    "interval_seconds": {"type": "integer", "default": 60},
                    "for_duration": {"type": "string", "default": "1m"},
                    "labels": {"type": "object"},
                    "annotations": {"type": "object"},
                    "no_data_state": {"type": "string", "default": "NoData"},
                    "exec_err_state": {"type": "string", "default": "Error"},
                    "folder_uid": {"type": "string"},
                    "rule_group": {"type": "string"}
                },
                "required": ["title", "condition", "data"]
            },
        ),
        Tool(
            name="alert_rule_list",
            description="List alert rules",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_uid": {"type": "string"},
                    "rule_group": {"type": "string"}
                },
                "required": []
            },
        ),
        Tool(
            name="alert_rule_delete",
            description="Delete alert rule by UID",
            inputSchema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"}
                },
                "required": ["uid"]
            },
        ),
        Tool(
            name="folder_create",
            description="Create a folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "uid": {"type": "string"},
                    "title": {"type": "string"},
                    "parent_uid": {"type": "string"}
                },
                "required": ["title"]
            },
        ),
        Tool(
            name="folder_list",
            description="List folders",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="user_create",
            description="Create a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "login": {"type": "string"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "role": {"type": "string", "default": "Viewer"},
                    "org_id": {"type": "integer", "default": 1}
                },
                "required": ["login", "name", "email"]
            },
        ),
        Tool(
            name="user_list",
            description="List users",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="annotation_create",
            description="Create an annotation",
            inputSchema={
                "type": "object",
                "properties": {
                    "time": {"type": "integer"},
                    "time_end": {"type": "integer"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "text": {"type": "string"},
                    "dashboard_uid": {"type": "string"},
                    "panel_id": {"type": "integer"}
                },
                "required": ["time", "text"]
            },
        ),
        Tool(
            name="annotation_list",
            description="List annotations",
            inputSchema={
                "type": "object",
                "properties": {
                    "from": {"type": "integer"},
                    "to": {"type": "integer"},
                    "tags": {"type": "string"},
                    "limit": {"type": "integer", "default": 100}
                },
                "required": ["from", "to"]
            },
        ),
        Tool(
            name="health_check",
            description="Check Grafana health",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="organization_list",
            description="List organizations",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="team_create",
            description="Create a team",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "org_id": {"type": "integer", "default": 1}
                },
                "required": ["name"]
            },
        ),
        Tool(
            name="team_list",
            description="List teams",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "datasource_create":
            return await handle_datasource_create(arguments)
        elif name == "datasource_list":
            return await handle_datasource_list(arguments)
        elif name == "datasource_get":
            return await handle_datasource_get(arguments)
        elif name == "datasource_delete":
            return await handle_datasource_delete(arguments)
        elif name == "dashboard_create":
            return await handle_dashboard_create(arguments)
        elif name == "dashboard_get":
            return await handle_dashboard_get(arguments)
        elif name == "dashboard_delete":
            return await handle_dashboard_delete(arguments)
        elif name == "dashboard_list":
            return await handle_dashboard_list(arguments)
        elif name == "alert_rule_create":
            return await handle_alert_rule_create(arguments)
        elif name == "alert_rule_list":
            return await handle_alert_rule_list(arguments)
        elif name == "alert_rule_delete":
            return await handle_alert_rule_delete(arguments)
        elif name == "folder_create":
            return await handle_folder_create(arguments)
        elif name == "folder_list":
            return await handle_folder_list(arguments)
        elif name == "user_create":
            return await handle_user_create(arguments)
        elif name == "user_list":
            return await handle_user_list(arguments)
        elif name == "annotation_create":
            return await handle_annotation_create(arguments)
        elif name == "annotation_list":
            return await handle_annotation_list(arguments)
        elif name == "health_check":
            return await handle_health_check(arguments)
        elif name == "organization_list":
            return await handle_organization_list(arguments)
        elif name == "team_create":
            return await handle_team_create(arguments)
        elif name == "team_list":
            return await handle_team_list(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== HELPER ====================

async def _request(method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
    headers = {"Authorization": f"Bearer {GRAFANA_API_KEY}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{GRAFANA_URL}/api/{endpoint}"
        if method == "GET":
            resp = await client.get(url, headers=headers, params=params)
        elif method == "POST":
            resp = await client.post(url, headers=headers, json=data)
        elif method == "PUT":
            resp = await client.put(url, headers=headers, json=data)
        elif method == "DELETE":
            resp = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unknown method: {method}")
        resp.raise_for_status()
        return resp.json()


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_datasource_create(args: Dict) -> List[TextContent]:
    req = DatasourceRequest(**arguments)
    data = req.model_dump(exclude_none=True)
    result = await _request("POST", "datasources", data)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_datasource_list(args: Dict) -> List[TextContent]:
    result = await _request("GET", "datasources")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_datasource_get(args: Dict) -> List[TextContent]:
    uid = args.get("uid", "")
    result = await _request("GET", f"datasources/uid/{uid}")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_datasource_delete(args: Dict) -> List[TextContent]:
    uid = args.get("uid", "")
    result = await _request("DELETE", f"datasources/uid/{uid}")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_dashboard_create(args: Dict) -> List[TextContent]:
    req = DashboardRequest(**arguments)
    dashboard = req.model_dump(exclude_none=True)
    data = {"dashboard": dashboard, "overwrite": True}
    result = await _request("POST", "dashboards/db", data)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_dashboard_get(args: Dict) -> List[TextContent]:
    uid = args.get("uid", "")
    result = await _request("GET", f"dashboards/uid/{uid}")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_dashboard_delete(args: Dict) -> List[TextContent]:
    uid = args.get("uid", "")
    result = await _request("DELETE", f"dashboards/uid/{uid}")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_dashboard_list(args: Dict) -> List[TextContent]:
    query = args.get("query", "")
    tag = args.get("tag", "")
    limit = args.get("limit", 50)
    
    params = {"limit": str(limit)}
    if query:
        params["query"] = query
    if tag:
        params["tag"] = tag
    
    result = await _request("GET", "search", params=params)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_alert_rule_create(args: Dict) -> List[TextContent]:
    req = AlertRuleRequest(**arguments)
    data = req.model_dump(exclude_none=True)
    result = await _request("POST", "provisioning/alert-rules", data)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_alert_rule_list(args: Dict) -> List[TextContent]:
    folder_uid = args.get("folder_uid")
    rule_group = args.get("rule_group")
    
    params = {}
    if folder_uid:
        params["folderUID"] = folder_uid
    if rule_group:
        params["ruleGroup"] = rule_group
    
    result = await _request("GET", "provisioning/alert-rules", params=params)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_alert_rule_delete(args: Dict) -> List[TextContent]:
    uid = args.get("uid", "")
    result = await _request("DELETE", f"provisioning/alert-rules/{uid}")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_folder_create(args: Dict) -> List[TextContent]:
    req = FolderRequest(**arguments)
    data = req.model_dump(exclude_none=True)
    result = await _request("POST", "folders", data)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_folder_list(args: Dict) -> List[TextContent]:
    result = await _request("GET", "folders")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_user_create(args: Dict) -> List[TextContent]:
    req = UserRequest(**arguments)
    data = req.model_dump(exclude_none=True)
    result = await _request("POST", "admin/users", data)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_user_list(args: Dict) -> List[TextContent]:
    result = await _request("GET", "users")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_annotation_create(args: Dict) -> List[TextContent]:
    req = AnnotationRequest(**arguments)
    data = req.model_dump(exclude_none=True)
    result = await _request("POST", "annotations", data)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_annotation_list(args: Dict) -> List[TextContent]:
    from_time = args.get("from", 0)
    to_time = args.get("to", 0)
    tags = args.get("tags", "")
    limit = args.get("limit", 100)
    
    params = {"from": str(from_time), "to": str(to_time), "limit": str(limit)}
    if tags:
        params["tags"] = tags
    
    result = await _request("GET", "annotations", params=params)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_health_check(args: Dict) -> List[TextContent]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(f"{GRAFANA_URL}/api/health")
            return [TextContent(type="text", text=json.dumps({
                "healthy": resp.status_code == 200,
                "status_code": resp.status_code,
                "response": resp.json() if resp.status_code == 200 else resp.text
            }, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_organization_list(args: Dict) -> List[TextContent]:
    result = await _request("GET", "orgs")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_team_create(args: Dict) -> List[TextContent]:
    req = TeamCreateRequest(**arguments)
    data = req.model_dump(exclude_none=True)
    result = await _request("POST", "teams", data)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_team_list(args: Dict) -> List[TextContent]:
    result = await _request("GET", "teams/search")
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
