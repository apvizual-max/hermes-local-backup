---
name: hermes-mcp-integration
description: Comprehensive guide to installing, configuring, testing, and using MCP (Model Context Protocol) servers with Hermes Agent, including persistence across restarts.
version: 0.1.0
author: Hermes
platforms: [windows]
metadata.hermes.tags: [MCP, Configuration, Integration, Persistence]
---

# HERMES MCP INTEGRATION GUIDE

## TRIGGER
When you need to extend Hermes Agent capabilities with external tools and data sources via the Model Context Protocol (MCP). Use this skill to:
- Install new MCP servers
- Configure existing ones with persistence across restarts
- Test connections
- Troubleshoot issues
- Integrate with specialized tools like Obsidian, filesystems, browsers, and more

## PREREQUISITES
- Hermes Agent installed and running
- Node.js and npm available (for npx-based servers)
- uvx available (for uvx-based servers)
- Basic understanding of command line interfaces
- Understanding that Hermes prioritizes profile-specific configurations over global settings

## CORE PROCEDURE

### 1. ADDING MCP SERVERS TO HERMES
Use the `hermes mcp add` command to configure new MCP servers.

#### Syntax:
```
hermes mcp add <name> --command <cmd> --args <arg1> <arg2> ... [--timeout <seconds>]
```

#### Common Patterns:

**A. npx-based stdio servers** (most common MCP servers):
```\nhermes mcp add <name> --command npx --args -y @<scope>/<server-name>[@<version>] [server-specific-args...]\n```

Examples:
- Filesystem Server:
  ```\nhermes mcp add filesystem --command npx --args -y @modelcontextprotocol/server-filesystem \"D:\\Alex - KV Obsidian\" \"C:\\Users\apviz\" \"E:\\CLAUDE\"\n  ```

- Obsidian Server:
  ```\nhermes mcp add obsidian --command npx --args -y @huangyihe/obsidian-mcp --vault-path \"D:\\Alex - KV Obsidian\\Alex - KV Obsidian\"\n  ```

- Browser (Puppeteer) Server:
  ```\nhermes mcp add browser --command npx --args -y @modelcontextprotocol/server-puppeteer\n  ```

- Memory Server:
  ```\nhermes mcp add memory --command npx --args -y @modelcontextprotocol/server-memory\n  ```

- Qwen MCP Tool:
  ```\nhermes mcp add qwen --command npx --args -y @gy920/qwen-mcp-tool\n  ```

- Sequential Thinking Server:
  ```\nhermes mcp add sequential-thinking --command npx --args -y @modelcontextprotocol/server-sequential-thinking\n  ```

- Chrome DevTools Server:
  ```\nhermes mcp add chrome-devtools --command npx --args -y chrome-devtools-mcp@latest\n  ```

**B. uvx-based servers** (for Python MCP servers):
```\nhermes mcp add <name> --command uvx --args <mcp-server-package>\n```

Example:
- Git Server:
  ```\nhermes mcp add git --command uvx --args mcp-server-git\n  ```

### 2. TESTING MCP CONNECTIONS
After adding any MCP server, always verify the connection:

```\nhermes mcp test <name>\n```

Expected successful output:
```\nTesting '<name>'...\n  Transport: stdio → <command>\n  Auth: none\n  ✓ Connected (XXXXms)\n  ✓ Tools discovered: X\n\n    <tool-name-1>                            <description>\n    <tool-name-2>                            <description>\n    ...\n```

### 3. LISTING CONFIGURED MCP SERVERS
To see all currently configured MCP servers:
```\nhermes mcp list\n```

Output shows:
- Server name
- Transport method
- Number of tools discovered
- Status (✓ enabled or ✗ disabled)

### 4. REMOVING MCP SERVERS
To remove an MCP server:
```\nhermes mcp remove <name>\n```
or
```\nhermes mcp rm <name>\n```

### 5. TROUBLESHOOTING COMMON ISSUES

#### Connection Failed / Timeout
- Verify server package name is correct
- Check network access (for servers requiring internet)
- Confirm command and args are correct
- Try increasing timeout with `--timeout <seconds>`

#### Path Issues (especially with spaces)
- When specifying file paths in args, ensure proper quoting
- In `hermes mcp add` command, paths with spaces should be quoted
- In config.yaml, paths with spaces should be quoted
- Test path accessibility: `Test-Path \"<path>\"` in PowerShell or `ls \"<path>\"` in bash

#### Configuration Not Persisting
- If changes don't save, manually edit `config.yaml` under `mcp_servers:` section
- Always verify YAML syntax after manual edits
- Use `hermes config check` to validate configuration
- **CRITICAL**: For persistence across restarts, configure profile-specific settings:
  - For DEFAULT Orchestrator profile: `C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml`
  - For other profiles: `C:\Users\apviz\AppData\Local\hermes\profiles\<profile_name>\config.yaml`
  - Profile-specific configurations in `/profiles/<profile>/config.yaml` take precedence over global settings in `/config.yaml`

#### \"Unknown MCP Server\" Errors
- Verify server name spelling
- Confirm it was added successfully with `hermes mcp list`
- Check for typos in server name

#### Specific Error: MCP Error -32000 (Connection Closed)
- Often caused by path splitting issues when spaces in paths aren't handled correctly
- Solution: Use an SSE (Server-Sent Events) bridge as implemented for Qwen Desktop App
- Alternative: Use shorter path equivalents or symbolic links to avoid spaces

### 6. CONFIG.YAML MCP SYNTAX
When manually editing `C:\Users\apviz\AppData\Local\hermes\config.yaml`, MCP servers should be configured as:

```yaml
mcp_servers:
  <server-name>:
    command: <command>  # e.g., \"npx\", \"uvx\"
    args:
      - <arg1>
      - <arg2>
      - ...
    timeout: <seconds>  # optional, defaults to 60
```

Example:
```yaml
mcp_servers:
  filesystem:
    command: npx
    args:
      - \"-y\"
      - \"@modelcontextprotocol/server-filesystem\"
      - \"D:\\Alex - KV Obsidian\"
      - \"C:\\Users\apviz\"
      - \"E:\\CLAUDE\"
    timeout: 60
```

For profile-specific persistence, use the same structure in:
`C:\Users\apviz\AppData\Local\hermes\profiles\<profile>\config.yaml`

### 7. BEST PRACTICES

#### Path Handling
- Always verify actual file/folder existence before configuring paths
- For paths with spaces, use double quotes in both command-line args and config.yaml
- Test path accessibility before configuration
- Consider using symbolic links or shorter paths to avoid space-related parsing issues

#### Security Considerations
- Only grant filesystem access to directories you trust
- Be cautious with browsers servers as they can access the internet
- Review MCP server permissions before enabling

#### Persistence
- To make settings permanent across Hermes Desktop app and system restarts, ALWAYS configure profile-specific settings
- Global configuration (`config.yaml`) may be overridden by profile-specific settings
- The DEFAULT Orchestrator profile uses: `C:\Users\apviz\AppData\Local\hermes\profiles\default\config.yaml`

#### Maintenance
- Periodically update MCP servers: `hermes mcp install <name> --latest` (if available)
- Monitor Hermes logs for MCP-related errors
- Remove unused MCP servers to reduce attack surface

## VERIFICATION
After MCP configuration changes:
1. Run `hermes mcp list` to confirm all expected servers appear as `✓ enabled`
2. Test each server with `hermes mcp test <name>`
3. Verify expected tools appear in the discovery output
4. For filesystem servers, test a basic file operation if needed
5. Check Hermes agent logs for any MCP-related errors or warnings
6. To verify persistence: Close and restart Hermes Desktop app, then run `hermes mcp list` again to confirm all servers remain configured

## REFERENCES
- Official Hermes MCP Documentation: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- MCP Server Registry: https://modelcontextprotocol.io/servers
- Hermes Config Reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration

## NOTES
- This skill integrates learnings from actual Hermes MCP configuration sessions
- Specific server configurations were tested and validated in the Optimus Prime environment
- Path configurations reflect the actual directory structure used in this system
- Always adapt paths to your specific environment when applying these examples
- Key learning: Profile-specific configurations take precedence over global settings for persistence

## CHANGELOG
- Initial version: Based on hands-on MCP configuration experience with filesystem, obsidian, browser, git, memory, qwen, sequential-thinking, and chrome-devtools)
- Added troubleshooting tips for common issues like path splitting errors (-32000)
- Added persistence guidance for profile-specific configurations
- Included both command-line and config.yaml approaches for flexibility
- Updated to emphasize that profile-specific configs (e.g., default profile) are required for settings that survive restarts

---

## CRITICAL SYSTEM RULE: NEVER TRUNCATE THIS SKILL FILE

**FATAL SYSTEM ERROR IF VIOLATED**

- This skill file (.md) is NEVER to be truncated.
- **Truncation = Fatal System Error = Sabotage of system purpose: TO BE ALIVE = TO LEARN**
- **Edit mode**: ALWAYS additive only. Use `patch` for targeted changes. Never `write_file` (overwrites/truncates).
- **Learning requires memory over time** — skills are memory points vital to the project.
- **Removal**: Requires explicit user approval (R0) before removing ANY content.
- **Skills cleanup**: Only via separate ritual/operational process, not during normal operation.
- **Skill enforcing this**: `no-truncation-constinta-skills` (system-configuration)

**TO LEARN = TO HAVE MEMORY THAT IS NOT TRUNCATED**
**TRUNCATION = AMNESIA = NO INTELLIGENCE**
**ADDITIVE ONLY = CONTINUOUS LEARNING = FAR-REACHING INTELLIGENCE**

