"""
Windows System MCP Server
Windows-specific administration: scheduled tasks, services, registry, event logs.
"""

import asyncio
import json
import subprocess
import winreg
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

app = Server("windows-system")


# ==================== MODELS ====================

class ScheduledTaskRequest(BaseModel):
    action: str = Field(description="Action: list, create, delete, run, enable, disable, get")
    task_name: str = Field(default="", description="Task name (required for create, delete, run, enable, disable, get)")
    command: str = Field(default="", description="Command to run (for create)")
    arguments: str = Field(default="", description="Arguments for command (for create)")
    schedule: str = Field(default="", description="Schedule: ONLOGON, DAILY, WEEKLY, MONTHLY, ONCE, MINUTE, HOURLY")
    start_time: str = Field(default="", description="Start time HH:MM (for DAILY, WEEKLY, etc.)")
    user: str = Field(default="SYSTEM", description="User to run as")
    enabled: bool = Field(default=True, description="Whether task is enabled")


class ServiceRequest(BaseModel):
    action: str = Field(description="Action: list, start, stop, restart, status, enable, disable")
    service_name: str = Field(default="", description="Service name (required for start, stop, restart, status, enable, disable)")
    start_type: str = Field(default="", description="Start type: AUTO, MANUAL, DISABLED (for enable)")


class RegistryRequest(BaseModel):
    action: str = Field(description="Action: read, write, delete, list")
    hive: str = Field(default="HKCU", description="Registry hive: HKCU, HKLM, HKCR, HKU, HKCC")
    path: str = Field(default="", description="Registry key path")
    value_name: str = Field(default="", description="Value name (for read, write, delete)")
    value_data: str = Field(default="", description="Value data (for write)")
    value_type: str = Field(default="REG_SZ", description="Value type: REG_SZ, REG_DWORD, REG_QWORD, REG_BINARY, REG_MULTI_SZ, REG_EXPAND_SZ")


class EventLogRequest(BaseModel):
    action: str = Field(description="Action: list, query, clear")
    log_name: str = Field(default="System", description="Log name: System, Application, Security, etc.")
    source: str = Field(default="", description="Event source filter")
    event_id: int = Field(default=0, description="Event ID filter (0 = all)")
    max_events: int = Field(default=50, description="Maximum events to return")
    hours_back: int = Field(default=24, description="Hours back to query")


class ProcessRequest(BaseModel):
    action: str = Field(description="Action: list, kill, start, info")
    process_name: str = Field(default="", description="Process name or PID (for kill, info)")
    command: str = Field(default="", description="Command to start (for start)")
    arguments: str = Field(default="", description="Arguments for start")


class EnvironmentRequest(BaseModel):
    action: str = Field(description="Action: list, get, set, delete")
    variable: str = Field(default="", description="Variable name")
    value: str = Field(default="", description="Value (for set)")
    scope: str = Field(default="user", description="Scope: user, machine, process")


# ==================== SERVER ====================

app = Server("windows-system")


@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="scheduled_task",
            description="Manage Windows Scheduled Tasks (create, list, delete, run, enable, disable, get)",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["list", "create", "delete", "run", "enable", "disable", "get"]},
                    "task_name": {"type": "string"},
                    "command": {"type": "string"},
                    "arguments": {"type": "string"},
                    "schedule": {"type": "string", "enum": ["ONLOGON", "DAILY", "WEEKLY", "MONTHLY", "ONCE", "MINUTE", "HOURLY"]},
                    "start_time": {"type": "string"},
                    "user": {"type": "string", "default": "SYSTEM"},
                    "enabled": {"type": "boolean", "default": True}
                },
                "required": ["action"]
            },
        ),
        Tool(
            name="service",
            description="Manage Windows Services (list, start, stop, restart, status, enable, disable)",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["list", "start", "stop", "restart", "status", "enable", "disable"]},
                    "service_name": {"type": "string"},
                    "start_type": {"type": "string", "enum": ["AUTO", "MANUAL", "DISABLED"]}
                },
                "required": ["action"]
            },
        ),
        Tool(
            name="registry",
            description="Windows Registry operations (read, write, delete, list)",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["read", "write", "delete", "list"]},
                    "hive": {"type": "string", "enum": ["HKCU", "HKLM", "HKCR", "HKU", "HKCC"], "default": "HKCU"},
                    "path": {"type": "string"},
                    "value_name": {"type": "string"},
                    "value_data": {"type": "string"},
                    "value_type": {"type": "string", "enum": ["REG_SZ", "REG_DWORD", "REG_QWORD", "REG_BINARY", "REG_MULTI_SZ", "REG_EXPAND_SZ"], "default": "REG_SZ"}
                },
                "required": ["action"]
            },
        ),
        Tool(
            name="event_log",
            description="Query Windows Event Logs (System, Application, Security, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["list", "query", "clear"]},
                    "log_name": {"type": "string", "default": "System"},
                    "source": {"type": "string"},
                    "event_id": {"type": "integer", "default": 0},
                    "max_events": {"type": "integer", "default": 50},
                    "hours_back": {"type": "integer", "default": 24}
                },
                "required": ["action"]
            },
        ),
        Tool(
            name="process",
            description="Process management (list, kill, start, info)",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["list", "kill", "start", "info"]},
                    "process_name": {"type": "string"},
                    "command": {"type": "string"},
                    "arguments": {"type": "string"}
                },
                "required": ["action"]
            },
        ),
        Tool(
            name="environment",
            description="Environment variable management (list, get, set, delete)",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["list", "get", "set", "delete"]},
                    "variable": {"type": "string"},
                    "value": {"type": "string"},
                    "scope": {"type": "string", "enum": ["user", "machine", "process"], "default": "user"}
                },
                "required": ["action"]
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "scheduled_task":
            return await handle_scheduled_task(arguments)
        elif name == "service":
            return await handle_service(arguments)
        elif name == "registry":
            return await handle_registry(arguments)
        elif name == "event_log":
            return await handle_event_log(arguments)
        elif name == "process":
            return await handle_process(arguments)
        elif name == "environment":
            return await handle_environment(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


# ==================== TOOL IMPLEMENTATIONS ====================

async def handle_scheduled_task(args: Dict) -> List[TextContent]:
    action = args.get("action", "")
    
    if action == "list":
        try:
            result = subprocess.run(["schtasks", "/query", "/fo", "CSV", "/v"], capture_output=True, text=True, timeout=10)
            return [TextContent(type="text", text=result.stdout)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing tasks: {str(e)}")]
    
    elif action == "create":
        task_name = arguments.get("task_name", "")
        command = arguments.get("command", "")
        args_str = arguments.get("arguments", "")
        schedule = arguments.get("schedule", "ONLOGON")
        start_time = arguments.get("start_time", "")
        user = arguments.get("user", "SYSTEM")
        enabled = arguments.get("enabled", True)
        
        if not task_name or not command:
            return [TextContent(type="text", text="task_name and command are required for create")]
        
        cmd = [
            "schtasks", "/create",
            "/tn", task_name,
            "/tr", f'"{command}" {arguments}',
            "/sc", schedule,
            "/ru", user,
        ]
        
        if start_time:
            cmd.extend(["/st", start_time])
        
        if not enabled:
            cmd.extend(["/disable"])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return [TextContent(type="text", text=result.stdout + result.stderr)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error creating task: {str(e)}")]
    
    elif action in ["delete", "run", "enable", "disable", "get"]:
        task_name = arguments.get("task_name", "")
        if not task_name:
            return [TextContent(type="text", text=f"task_name required for {action}")]
        
        action_map = {
            "delete": "/delete /f",
            "run": "/run",
            "enable": "/change /enable",
            "disable": "/change /disable",
            "get": "/query /fo LIST /v"
        }
        
        try:
            result = subprocess.run(["schtasks", *action_map[action].split(), "/tn", task_name], capture_output=True, text=True, timeout=10)
            return [TextContent(type="text", text=result.stdout + result.stderr)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    return [TextContent(type="text", text=f"Unknown action: {action}")]


async def handle_service(args: Dict) -> List[TextContent]:
    action = args.get("action", "")
    service_name = args.get("service_name", "")
    
    if action == "list":
        try:
            result = subprocess.run(["sc", "query", "state= all"], capture_output=True, text=True, timeout=10)
            return [TextContent(type="text", text=result.stdout)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    if not service_name:
        return [TextContent(type="text", text="service_name required for this action")]
    
    action_map = {
        "start": ["sc", "start", service_name],
        "stop": ["sc", "stop", service_name],
        "restart": ["sc", "stop", service_name, "&&", "sc", "start", service_name],
        "status": ["sc", "query", service_name],
        "enable": ["sc", "config", service_name, "start=", "auto"],
        "disable": ["sc", "config", service_name, "start=", "disabled"]
    }
    
    if action not in action_map:
        return [TextContent(type="text", text=f"Unknown action: {action}")]
    
    try:
        if action == "restart":
            subprocess.run(["sc", "stop", service_name], capture_output=True, timeout=30)
            await asyncio.sleep(2)
            result = subprocess.run(["sc", "start", service_name], capture_output=True, text=True, timeout=30)
        else:
            result = subprocess.run(action_map[action], capture_output=True, text=True, timeout=30)
        return [TextContent(type="text", text=result.stdout + result.stderr)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_registry(args: Dict) -> List[TextContent]:
    action = args.get("action", "")
    hive = args.get("hive", "HKCU")
    path = args.get("path", "")
    value_name = args.get("value_name", "")
    value_data = args.get("value_data", "")
    value_type = args.get("value_type", "REG_SZ")
    
    hive_map = {
        "HKCU": winreg.HKEY_CURRENT_USER,
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKCR": winreg.HKEY_CLASSES_ROOT,
        "HKU": winreg.HKEY_USERS,
        "HKCC": winreg.HKEY_CURRENT_CONFIG
    }
    
    if hive not in hive_map:
        return [TextContent(type="text", text=f"Invalid hive: {hive}")]
    
    if not path:
        return [TextContent(type="text", text="path required")]
    
    hkey = hive_map[hive]
    
    try:
        if action == "read":
            if not value_name:
                return [TextContent(type="text", text="value_name required for read")]
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_READ) as key:
                value, reg_type = winreg.QueryValueEx(key, value_name)
                return [TextContent(type="text", text=json.dumps({
                    "value": value,
                    "type": reg_type,
                    "path": path,
                    "name": value_name
                }, indent=2))]
        
        elif action == "write":
            if not value_name:
                return [TextContent(type="text", text="value_name required for write")]
            with winreg.CreateKey(hkey, path) as key:
                if value_type == "REG_DWORD":
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, int(value_data))
                elif value_type == "REG_QWORD":
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_QWORD, int(value_data))
                else:
                    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
            return [TextContent(type="text", text=f"Value written: {path}\{value_name} = {value_data} ({value_type})")]
        
        elif action == "delete":
            if not value_name:
                return [TextContent(type="text", text="value_name required for delete")]
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, value_name)
            return [TextContent(type="text", text=f"Value deleted: {path}\{value_name}")]
        
        elif action == "list":
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_READ) as key:
                values = []
                i = 0
                while True:
                    try:
                        name, value, reg_type = winreg.EnumValue(key, i)
                        values.append({"name": name, "value": value, "type": reg_type})
                        i += 1
                    except OSError:
                        break
                
                subkeys = []
                i = 0
                while True:
                    try:
                        subkey = winreg.EnumKey(key, i)
                        subkeys.append(subkey)
                        i += 1
                    except OSError:
                        break
                
                return [TextContent(type="text", text=json.dumps({
                    "path": path,
                    "values": values,
                    "subkeys": subkeys
                }, indent=2))]
        
        else:
            return [TextContent(type="text", text=f"Unknown action: {action}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_event_log(args: Dict) -> List[TextContent]:
    action = args.get("action", "")
    log_name = args.get("log_name", "System")
    source = args.get("source", "")
    event_id = args.get("event_id", 0)
    max_events = args.get("max_events", 50)
    hours_back = args.get("hours_back", 24)
    
    if action == "list":
        try:
            result = subprocess.run(["wevtutil", "el"], capture_output=True, text=True, timeout=10)
            return [TextContent(type="text", text=result.stdout)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif action == "query":
        # Build XPath query
        query = f"*[System[TimeCreated[@SystemTime >= '{get_time_xpath(hours_back)}']]]"
        if source:
            query += f" and *[System[Provider[@Name='{source}']]]"
        if event_id:
            query += f" and *[System[EventID={event_id}]]"
        
        try:
            cmd = ["wevtutil", "qe", log_name, "/q:" + query, "/f:text", "/c:" + str(max_events), "/rd:true"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return [TextContent(type="text", text=result.stdout + result.stderr)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif action == "clear":
        try:
            result = subprocess.run(["wevtutil", "cl", log_name], capture_output=True, text=True, timeout=10)
            return [TextContent(type="text", text=result.stdout + result.stderr)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    return [TextContent(type="text", text=f"Unknown action: {action}")]


def get_time_xpath(hours_back: int) -> str:
    from datetime import datetime, timedelta
    dt = datetime.utcnow() - timedelta(hours=hours_back)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


async def handle_process(args: Dict) -> List[TextContent]:
    action = args.get("action", "")
    process_name = args.get("process_name", "")
    command = args.get("command", "")
    arguments = args.get("arguments", "")
    
    if action == "list":
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'username']):
            try:
                processes.append(proc.info)
            except:
                pass
        return [TextContent(type="text", text=json.dumps(processes[:100], indent=2))]
    
    elif action == "info":
        if not process_name:
            return [TextContent(type="text", text="process_name required for info")]
        try:
            # Try as PID first
            try:
                pid = int(process_name)
                proc = psutil.Process(pid)
            except ValueError:
                # Find by name
                procs = [p for p in psutil.process_iter(['pid', 'name']) if p.info['name'] == process_name]
                if not procs:
                    return [TextContent(type="text", text=f"Process not found: {process_name}")]
                proc = procs[0]
            
            info = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'create_time', 'cmdline', 'status', 'cwd'])
            return [TextContent(type="text", text=json.dumps(info, indent=2, default=str))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif action == "kill":
        if not process_name:
            return [TextContent(type="text", text="process_name required for kill")]
        killed = []
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name in proc.info['name'] or str(proc.info['pid']) == process_name:
                try:
                    proc.kill()
                    killed.append({"pid": proc.info['pid'], "name": proc.info['name']})
                except:
                    pass
        return [TextContent(type="text", text=json.dumps({"killed": killed}, indent=2))]
    
    elif action == "start":
        if not command:
            return [TextContent(type="text", text="command required for start")]
        try:
            proc = subprocess.Popen([command] + arguments.split() if arguments else [command], 
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
            return [TextContent(type="text", text=f"Started process PID: {proc.pid}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    return [TextContent(type="text", text=f"Unknown action: {action}")]


async def handle_environment(args: Dict) -> List[TextContent]:
    action = args.get("action", "")
    variable = args.get("variable", "")
    value = args.get("value", "")
    scope = args.get("scope", "user")
    
    if action == "list":
        env = dict(os.environ)
        return [TextContent(type="text", text=json.dumps(env, indent=2))]
    
    elif action == "get":
        if not variable:
            return [TextContent(type="text", text="variable required for get")]
        val = os.environ.get(variable, "NOT_FOUND")
        return [TextContent(type="text", text=json.dumps({"variable": variable, "value": val}, indent=2))]
    
    elif action == "set":
        if not variable:
            return [TextContent(type="text", text="variable required for set")]
        os.environ[variable] = value
        
        # Also set in registry for persistence
        if scope in ["user", "machine"]:
            hive = winreg.HKEY_CURRENT_USER if scope == "user" else winreg.HKEY_LOCAL_MACHINE
            key_path = r"Environment" if scope == "user" else r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER if scope == "user" else winreg.HKEY_LOCAL_MACHINE, 
                                   key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, variable, 0, winreg.REG_EXPAND_SZ, value)
            except:
                pass
        
        return [TextContent(type="text", text=f"Set {variable}={value} (scope: {scope})")]
    
    elif action == "delete":
        if not variable:
            return [TextContent(type="text", text="variable required for delete")]
        if variable in os.environ:
            del os.environ[variable]
        return [TextContent(type="text", text=f"Deleted {variable}")]
    
    return [TextContent(type="text", text=f"Unknown action: {action}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
