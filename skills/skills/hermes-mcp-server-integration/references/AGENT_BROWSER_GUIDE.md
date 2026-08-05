# AGENT_BROWSER_GUIDE.md
# Complete guide for agent-browser MCP server installation, upgrade, and verification

# Agent-Browser MCP Integration Guide

## Overview

`agent-browser` is an npm-based MCP server that provides web browsing capabilities
to Hermes Agent. It runs as a local binary and communicates via JSON-RPC (stdio).

**Verified Working Version**: `v0.31.1`
**Expected Tool Count**: 64 tools

## Paths

```
Install location: C:\Users\apviz\AppData\Local\hermes\node\
Binary:           C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd
npm packages:     C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\
Platform binary:  C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\
                  bin\agent-browser-win32-x64.exe  (or arm64 variant)
```

## Diagnosis — Identifying Problems

### Symptom → Root Cause Mapping

| Error in agent.log | Root Cause |
|--------------------|-----------|
| `Invalid JSON: expected value at line 1 column 3` | Binary outputting help/error text instead of JSON |
| `Invalid JSON: invalid number at line 1 column 7` | Numbered list text (help output) being parsed as JSON |
| `command not found` | Binary not downloaded or wrong path |
| `TypeError: not a function` | Wrong agent-browser version (major API change) |

### Check Current Version

```powershell
# Check installed version
C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd --version
# Expected: 0.31.1

# Check workspace package.json version
Get-Content "C:\Users\apviz\AppData\Local\hermes\node\node_modules\agent-browser\package.json" |
    ConvertFrom-Json | Select-Object version
```

### Check Running Command

```powershell
# Confirm the MCP command works (should produce no output or JSON, not help text)
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' |
    C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd mcp --tools all
```

## Correct Configuration Entry

```yaml
# In any profile's config.yaml, under mcp_servers:
agent-browser:
  args:
  - mcp
  - --tools
  - all
  command: C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd
  timeout: 60
```

> [!WARNING]
> Do NOT use just `agent-browser` as the command — always use the full path.
> Do NOT omit `mcp --tools all` args — without `mcp` subcommand the binary
> outputs help text which is not valid JSON-RPC.

## Upgrade Procedure

> [!CAUTION]
> **npm self-deletion bug**: Running `npm install` from WITHIN the Hermes
> `node/` directory causes npm to delete its own binary. Always use a temp dir.

```powershell
# Step 1: Install to temp directory
$TEMP = "$env:TEMP\ab-upgrade-$(Get-Random)"
New-Item $TEMP -ItemType Directory -Force
Set-Location $TEMP
npm install agent-browser@0.31.1

# Step 2: Copy to Hermes node directory
$HERMES_NODE = "C:\Users\apviz\AppData\Local\hermes\node\node_modules"
Copy-Item "$TEMP\node_modules\agent-browser" "$HERMES_NODE\agent-browser" -Recurse -Force

# Step 3: Download platform binary (postinstall)
Set-Location "C:\Users\apviz\AppData\Local\hermes\node"
node "node_modules\agent-browser\scripts\postinstall.js"

# Step 4: Verify
.\agent-browser.cmd --version   # Should show: 0.31.1
.\agent-browser.cmd mcp --help  # Should show MCP subcommand help
```

## Verification (JSON-RPC Test)

```python
import subprocess, json

proc = subprocess.Popen(
    [r"C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd", "mcp", "--tools", "all"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

# Initialize
msg = json.dumps({
    "jsonrpc":"2.0","id":1,"method":"initialize",
    "params":{"protocolVersion":"2024-11-05","capabilities":{},
              "clientInfo":{"name":"test","version":"1.0"}}
}) + "\n"
proc.stdin.write(msg.encode()); proc.stdin.flush()
resp = json.loads(proc.stdout.readline())
print("INIT:", "OK" if "result" in resp else f"FAIL: {resp}")

# tools/list
proc.stdin.write(b'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}\n')
proc.stdin.flush()
msg = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}) + "\n"
proc.stdin.write(msg.encode()); proc.stdin.flush()
resp = json.loads(proc.stdout.readline())
tools = resp["result"]["tools"]
print(f"TOOLS: {len(tools)} tools (expected 64)")

proc.terminate()
```

## Profile Config Registration

Must be registered in ALL profile configs. See [HERMES_PROFILE_PATHS.md](HERMES_PROFILE_PATHS.md).
