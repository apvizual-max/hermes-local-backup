# HERMES_PROFILE_PATHS.md
# All profile config paths that must be updated when registering a new MCP server

# Hermes Profile Config Paths

## When to Update ALL These Files

Any time you:
- Install a new MCP server
- Change MCP server command/args
- Change MCP server timeout or path
- Perform a system upgrade

> [!IMPORTANT]
> Missing any of these files means that profile will use the OLD config
> and the MCP server will NOT be available in that profile.

## Complete List of Config Files to Update

```
# Root (affects all profiles as fallback)
C:\Users\apviz\AppData\Local\hermes\config.yaml

# Individual profile configs
C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml
C:\Users\apviz\AppData\Local\hermes\profiles\prime\config.yaml
C:\Users\apviz\AppData\Local\hermes\profiles\assist\config.yaml
C:\Users\apviz\AppData\Local\hermes\profiles\cli-prime\config.yaml
C:\Users\apviz\AppData\Local\hermes\profiles\coder\config.yaml
C:\Users\apviz\AppData\Local\hermes\profiles\cowork\config.yaml
C:\Users\apviz\AppData\Local\hermes\profiles\designer\config.yaml
C:\Users\apviz\AppData\Local\hermes\profiles\trader\config.yaml
C:\Users\apviz\AppData\Local\hermes\profiles\translator\config.yaml

# Optimal snapshot (used for system restore)
C:\Users\apviz\AppData\Local\hermes\state-snapshots\20260711-095000-optimal-config\config.yaml
```

## MCP Server Block Format (for `mcp_servers` section)

```yaml
mcp_servers:
  existing-server:
    # ... existing entries ...

  new-mcp-server:            # ← your new server entry
    args:
    - -m
    - package_name.server
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\new-server
    timeout: 60
```

## Verification Command

```powershell
# Check all profiles have the new server registered
$serverName = "antigravity-bridge"
foreach ($f in (Get-ChildItem "C:\Users\apviz\AppData\Local\hermes\profiles\*\config.yaml")) {
    $has = (Get-Content $f -Raw) -match $serverName
    Write-Host "$(Split-Path (Split-Path $f -Parent) -Leaf): $($has ? 'OK' : 'MISSING')"
}
```

## YAML Formatting Rules

1. `mcp_servers:` is a top-level key (no indent)
2. Each server name is indented 2 spaces: `  server-name:`
3. Server config keys are indented 4 spaces: `    command: python`
4. After bulk PowerShell insertion: check for `60moa:` merge artifact
   - Fix: `$content -replace "60moa:", "60\r\nmoa:"`
5. Always use `Set-Content ... -Encoding UTF8 -NoNewline` to preserve line endings
