# PYTHON_MCP_TEMPLATE.md
# Complete boilerplate for creating a new Python-based MCP server for Hermes

# Python MCP Server Template

## Directory Structure

```
C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\<server-name>\
├── pyproject.toml
└── src\
    └── <package_name>\
        ├── __init__.py
        └── server.py
```

## pyproject.toml

```toml
[project]
name = "<server-name>-mcp"
version = "1.0.0"
description = "Description of what this MCP server does"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    "pydantic>=2.0",
    "pyyaml>=6.0",
]

[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

## src/\<package_name\>/__init__.py

```python
"""<Server name> MCP server for Hermes Agent."""
```

## src/\<package_name\>/server.py

```python
"""
<server-name> MCP Server
========================
Description of what this server does.

Tools:
  - tool_one: What it does
  - tool_two: What it does
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ── Server initialization ─────────────────────────────────────────────────────

app = Server("server-name")

# ── Tool definitions ──────────────────────────────────────────────────────────

@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="tool_one",
            description="What tool_one does. Be specific.",
            inputSchema={
                "type": "object",
                "properties": {
                    "required_param": {
                        "type": "string",
                        "description": "Description of the required parameter"
                    },
                    "optional_param": {
                        "type": "string",
                        "description": "Description of optional parameter",
                        "default": "default_value"
                    }
                },
                "required": ["required_param"]
            }
        ),
        Tool(
            name="tool_two",
            description="What tool_two does.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]


# ── Tool implementations ──────────────────────────────────────────────────────

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "tool_one":
            required = arguments.get("required_param", "")
            optional = arguments.get("optional_param", "default_value")
            
            # Do your work here
            result = {"status": "ok", "data": f"Processed: {required}"}
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]

        elif name == "tool_two":
            result = {"status": "ok", "message": "tool_two executed"}
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            return [TextContent(type="text", text=json.dumps({
                "error": f"Unknown tool: {name}"
            }))]

    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "error": str(e),
            "tool": name
        }))]


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

## Installation Commands

```powershell
$PIP = "C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\pip.exe"
$PYTHON = "C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"

# Install in editable mode (changes to server.py take effect immediately)
& $PIP install -e "C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\<server-name>"

# Verify installation
& $PYTHON -c "import <package_name>; print('OK:', <package_name>.__file__)"
```

## Config Entry (add to all profile configs)

```yaml
<server-name>:
  args:
  - -m
  - <package_name>.server
  command: python
  cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\<server-name>
  timeout: 60
```

## Quick Test

```powershell
$PYTHON = "C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
# Pipe an initialize + tools/list through the server
'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' |
& $PYTHON -m <package_name>.server
```
