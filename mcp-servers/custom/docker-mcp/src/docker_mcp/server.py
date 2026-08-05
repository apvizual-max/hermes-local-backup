"""
Docker MCP Server
Wrapper for Docker operations using the official docker-mcp or direct docker CLI.
"""

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

app = Server("docker-mcp")


# ==================== MODELS ====================

class ContainerListRequest(BaseModel):
    all: bool = Field(default=False, description="Show all containers (default: running only)")
    filters: Optional[Dict[str, str]] = Field(default=None, description="Filters (e.g., {'status': 'running'})")


class ContainerActionRequest(BaseModel):
    container_id: str = Field(description="Container ID or name")
    action: str = Field(description="Action: start, stop, restart, pause, unpause, kill, remove, logs, inspect, stats")


class ImageActionRequest(BaseModel):
    image_name: str = Field(description="Image name or ID")
    action: str = Field(description="Action: pull, push, remove, build, tag, history, inspect")
    tag: Optional[str] = Field(default=None, description="Tag for tag action")
    dockerfile: Optional[str] = Field(default=None, description="Dockerfile path for build")
    context: Optional[str] = Field(default=None, description="Build context path")


class VolumeActionRequest(BaseModel):
    volume_name: str = Field(description="Volume name")
    action: str = Field(description="Action: create, remove, inspect, list, prune")
    driver: str = Field(default="local", description="Volume driver")


class NetworkActionRequest(BaseModel):
    network_name: str = Field(description="Network name")
    action: str = Field(description="Action: create, remove, inspect, list, connect, disconnect, prune")
    driver: str = Field(default="bridge", description="Network driver")
    container: Optional[str] = Field(default=None, description="Container for connect/disconnect")


class SystemInfoRequest(BaseModel):
    pass


class ComposeActionRequest(BaseModel):
    project_dir: str = Field(description="Directory containing docker-compose.yml")
    action: str = Field(description="Action: up, down, ps, logs, build, pull, restart, stop, start, config")
    services: Optional[List[str]] = Field(default=None, description="Specific services")
    detach: bool = Field(default=True, description="Run in background")


# ==================== TOOLS ====================

app = Server("docker-mcp")


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="container_list",
            description="List Docker containers",
            inputSchema={
                "type": "object",
                "properties": {
                    "all": {"type": "boolean", "default": False},
                    "filters": {"type": "object"}
                },
                "required": []
            },
        ),
        Tool(
            name="container_action",
            description="Perform action on a container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container_id": {"type": "string"},
                    "action": {"type": "string", "enum": ["start", "stop", "restart", "pause", "unpause", "kill", "remove", "logs", "inspect", "stats", "exec"]}
                },
                "required": ["container_id", "action"]
            },
        ),
        Tool(
            name="image_action",
            description="Perform action on an image",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_name": {"type": "string"},
                    "action": {"type": "string", "enum": ["pull", "push", "remove", "build", "tag", "history", "inspect", "list", "prune"]},
                    "tag": {"type": "string"},
                    "dockerfile": {"type": "string"},
                    "context": {"type": "string"}
                },
                "required": ["image_name", "action"]
            },
        ),
        Tool(
            name="volume_action",
            description="Manage Docker volumes",
            inputSchema={
                "type": "object",
                "properties": {
                    "volume_name": {"type": "string"},
                    "action": {"type": "string", "enum": ["create", "remove", "inspect", "list", "prune"]},
                    "driver": {"type": "string", "default": "local"}
                },
                "required": ["volume_name", "action"]
            },
        ),
        Tool(
            name="network_action",
            description="Manage Docker networks",
            inputSchema={
                "type": "object",
                "properties": {
                    "network_name": {"type": "string"},
                    "action": {"type": "string", "enum": ["create", "remove", "inspect", "list", "connect", "disconnect", "prune"]},
                    "driver": {"type": "string", "default": "bridge"},
                    "container": {"type": "string"}
                },
                "required": ["network_name", "action"]
            },
        ),
        Tool(
            name="system_info",
            description="Get Docker system information",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="compose_action",
            description="Docker Compose operations",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_dir": {"type": "string"},
                    "action": {"type": "string", "enum": ["up", "down", "ps", "logs", "build", "pull", "restart", "stop", "start", "config"]},
                    "services": {"type": "array", "items": {"type": "string"}},
                    "detach": {"type": "boolean", "default": True}
                },
                "required": ["project_dir", "action"]
            },
        ),
        Tool(
            name="system_prune",
            description="Clean up unused Docker resources",
            inputSchema={
                "type": "object",
                "properties": {
                    "all": {"type": "boolean", "default": False},
                    "volumes": {"type": "boolean", "default": False},
                    "filter": {"type": "string"}
                },
                "required": []
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "container_list":
            return await handle_container_list(arguments)
        elif name == "container_action":
            return await handle_container_action(arguments)
        elif name == "image_action":
            return await handle_image_action(arguments)
        elif name == "volume_action":
            return await handle_volume_action(arguments)
        elif name == "network_action":
            return await handle_network_action(arguments)
        elif name == "system_info":
            return await handle_system_info(arguments)
        elif name == "compose_action":
            return await handle_compose_action(arguments)
        elif name == "system_prune":
            return await handle_system_prune(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_container_list(args: Dict) -> List[TextContent]:
    args_map = {"all": arguments.get("all", False)}
    all_containers = arguments.get("all", False)
    filters = arguments.get("filters", {})
    
    cmd = ["docker", "ps"]
    if all_containers:
        cmd.append("-a")
    
    if filters:
        for key, value in filters.items():
            cmd.extend(["--filter", f"{key}={value}"])
    
    cmd.extend(["--format", "json"])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            containers = [json.loads(line) for line in lines if line.strip()]
            return [TextContent(type="text", text=json.dumps({"containers": containers}, indent=2))]
        else:
            return [TextContent(type="text", text=f"Error: {result.stderr}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_container_action(args: Dict) -> List[TextContent]:
    req = ContainerActionRequest(**arguments)
    
    action_map = {
        "start": "start",
        "stop": "stop",
        "restart": "restart",
        "pause": "pause",
        "unpause": "unpause",
        "kill": "kill",
        "remove": "rm -f",
        "logs": "logs --tail 100",
        "inspect": "inspect",
        "stats": "stats --no-stream",
        "exec": "exec -it"
    }
    
    if req.action not in action_map:
        return [TextContent(type="text", text=f"Unknown action: {req.action}. Valid: {list(action_map.keys())}")]
    
    cmd = ["docker", action_map[req.action], req.container_id]
    
    try:
        if req.action == "stats":
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        elif req.action == "logs":
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        output = result.stdout
        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr
        
        return [TextContent(type="text", text=output or f"Action {req.action} completed on {arguments.container_id}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_image_action(args: Dict) -> List[TextContent]:
    req = ImageActionRequest(**arguments)
    
    if req.action == "pull":
        cmd = ["docker", "pull", req.image_name]
    elif req.action == "push":
        cmd = ["docker", "push", req.image_name]
    elif req.action == "remove":
        cmd = ["docker", "rmi", req.image_name]
    elif req.action == "build":
        if not arguments.dockerfile or not arguments.context:
            return [TextContent(type="text", text="dockerfile and context required for build")]
        cmd = ["docker", "build", "-f", arguments.dockerfile, "-t", req.image_name, arguments.context]
    elif req.action == "tag":
        if not arguments.tag:
            return [TextContent(type="text", text="tag required for tag action")]
        cmd = ["docker", "tag", req.image_name, arguments.tag]
    elif req.action == "history":
        cmd = ["docker", "history", req.image_name]
    elif req.action == "inspect":
        cmd = ["docker", "image", "inspect", req.image_name]
    elif req.action == "list":
        cmd = ["docker", "images", "--format", "json"]
    elif req.action == "prune":
        cmd = ["docker", "image", "prune", "-f"]
    else:
        return [TextContent(type="text", text=f"Unknown action: {req.action}")]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout
        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr
        return [TextContent(type="text", text=output or f"Action {req.action} completed")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_volume_action(args: Dict) -> List[TextContent]:
    req = VolumeActionRequest(**arguments)
    
    if req.action == "create":
        cmd = ["docker", "volume", "create", "--driver", req.driver, req.volume_name]
    elif req.action == "remove":
        cmd = ["docker", "volume", "rm", req.volume_name]
    elif req.action == "inspect":
        cmd = ["docker", "volume", "inspect", req.volume_name]
    elif req.action == "list":
        cmd = ["docker", "volume", "ls", "--format", "json"]
    elif req.action == "prune":
        cmd = ["docker", "volume", "prune", "-f"]
    else:
        return [TextContent(type="text", text=f"Unknown action: {req.action}")]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return [TextContent(type="text", text=result.stdout + result.stderr)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_network_action(args: Dict) -> List[TextContent]:
    req = NetworkActionRequest(**arguments)
    
    if req.action == "create":
        cmd = ["docker", "network", "create", "--driver", req.driver, req.network_name]
    elif req.action == "remove":
        cmd = ["docker", "network", "rm", req.network_name]
    elif req.action == "inspect":
        cmd = ["docker", "network", "inspect", req.network_name]
    elif req.action == "list":
        cmd = ["docker", "network", "ls", "--format", "json"]
    elif req.action == "prune":
        cmd = ["docker", "network", "prune", "-f"]
    elif req.action in ["connect", "disconnect"]:
        if not arguments.container:
            return [TextContent(type="text", text="container required for connect/disconnect")]
        action = "connect" if req.action == "connect" else "disconnect"
        cmd = ["docker", "network", action, req.network_name, arguments.container]
    else:
        return [TextContent(type="text", text=f"Unknown action: {req.action}")]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return [TextContent(type="text", text=result.stdout + result.stderr)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_system_info(args: Dict) -> List[TextContent]:
    try:
        result = subprocess.run(["docker", "system", "df", "--format", "json"], capture_output=True, text=True, timeout=10)
        disk = result.stdout
        result = subprocess.run(["docker", "info", "--format", "json"], capture_output=True, text=True, timeout=10)
        info = result.stdout
        result = subprocess.run(["docker", "version", "--format", "json"], capture_output=True, text=True, timeout=10)
        version = result.stdout
        
        return [TextContent(type="text", text=json.dumps({
            "disk_usage": json.loads(disk) if disk.strip() else {},
            "info": json.loads(info) if info.strip() else {},
            "version": json.loads(version) if version.strip() else {}
        }, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_compose_action(args: Dict) -> List[TextContent]:
    req = ComposeActionRequest(**arguments)
    
    cmd = ["docker", "compose"]
    if req.project_dir:
        cmd.extend(["-f", f"{req.project_dir}/docker-compose.yml"])
    
    cmd.append(req.action)
    
    if req.services:
        cmd.extend(req.services)
    
    if req.action == "up" and req.detach:
        cmd.append("-d")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=req.project_dir)
        return [TextContent(type="text", text=result.stdout + result.stderr)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_system_prune(args: Dict) -> List[TextContent]:
    all_resources = arguments.get("all", False)
    volumes = arguments.get("volumes", False)
    filter_str = arguments.get("filter", "")
    
    cmd = ["docker", "system", "prune", "-f"]
    if all_resources:
        cmd.append("-a")
    if volumes:
        cmd.append("--volumes")
    if filter_str:
        cmd.extend(["--filter", filter_str])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return [TextContent(type="text", text=result.stdout + result.stderr)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
