# HERMES_PATHS.md
# Complete reference of all critical paths in the Hermes system

# Hermes System Paths Reference

## Root & Core

| Path | Purpose |
|------|---------|
| `C:\Users\apviz\AppData\Local\hermes\` | HERMES_HOME — root of all Hermes data |
| `C:\Users\apviz\AppData\Local\hermes\config.yaml` | Root config (applies to all profiles) |
| `C:\Users\apviz\AppData\Local\hermes\.env` | API keys and secrets |
| `C:\Users\apviz\AppData\Local\hermes\hermes-agent\` | Python package source |
| `C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\` | Python virtual environment |
| `C:\Users\apviz\AppData\Local\hermes\node\` | Node.js binaries and npm packages |

## Executables

| Executable | Purpose |
|-----------|---------|
| `...\hermes-agent\venv\Scripts\python.exe` | Hermes Python interpreter |
| `...\hermes-agent\venv\Scripts\pip.exe` | Package installer (use this, NOT global pip) |
| `...\node\agent-browser.cmd` | agent-browser MCP server |
| `...\node\node.exe` | Node.js runtime |

## Profile Directories

| Path | Profile |
|------|---------|
| `profiles\default\config.yaml` | Default profile |
| `profiles\prime\config.yaml` | Prime profile |
| `profiles\assist\config.yaml` | Assist profile |
| `profiles\cli-prime\config.yaml` | CLI-Prime profile |
| `profiles\coder\config.yaml` | Coder profile |
| `profiles\cowork\config.yaml` | Co-work profile |
| `profiles\designer\config.yaml` | Designer profile |
| `profiles\trader\config.yaml` | Trader profile |
| `profiles\translator\config.yaml` | Translator profile |

Each profile directory may contain:
- `config.yaml` — profile-level config overrides
- `SOUL.md` — profile identity/personality
- `CONSTINTA.md` — SOT for CONSTINTA concept
- `skills/` — profile-specific skills
- `memories/` — profile memory files

## Snapshots & Backups

| Path | Purpose |
|------|---------|
| `state-snapshots\` | Named system state snapshots |
| `state-snapshots\20260711-095000-optimal-config\` | Known-good optimal config snapshot |
| `backups\` | Automatic backup archives |
| `LATEST_SYSTEM_RESTORE_POINT.md` | Instructions for restoring from optimal snapshot |

## MCP Servers

| Path | Server |
|------|--------|
| `mcp-servers\custom\antigravity-bridge\` | Hermes↔Antigravity bridge |
| `mcp-servers\custom\optimus-orchestrator\` | Task orchestrator MCP |
| `mcp-servers\custom\session-replay\` | Session replay MCP |
| `mcp-servers\custom\hermes-profile\` | Profile management MCP |
| `mcp-servers\custom\windows-system\` | Windows system tools MCP |

## Communication Bridge

| Path | Purpose |
|------|---------|
| `pairing\antigravity\inbox\` | Tasks from Hermes → Antigravity reads |
| `pairing\antigravity\outbox\` | Responses from Antigravity → Hermes reads |
| `pairing\antigravity\history\` | Archived completed tasks |
| `pairing\antigravity\status.json` | Bridge queue health |

## Logs & State

| Path | Purpose |
|------|---------|
| `logs\` | Hermes agent logs |
| `cron\` | Scheduled task outputs |
| `gateway_state.json` | Live gateway session state (auth token, WS info) |
| `data\state.db` | Persistent SQLite state database |

## Skills

| Path | Purpose |
|------|---------|
| `skills\` | Hermes-native skills (available to Hermes) |
| `C:\Users\apviz\OneDrive\Documents\Antigravity - Projects\Antigravity - config\skills\` | Antigravity skills |
| `.agents\skills\` | Workspace-scoped skills (if present) |

## Exclusion List (Never Touch)

```
OGLINDA - CASA\      ← Archive — READ ONLY
.git\                ← Version control
venv\                ← Python venv (managed by pip)
node_modules\        ← npm packages (managed by npm)
__pycache__\         ← Python bytecode (auto-generated)
*.pyc               ← Compiled Python (auto-generated)
```
