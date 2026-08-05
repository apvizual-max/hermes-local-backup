---
title: Profile Configurations & Overrides
version: 1.0.0
---

# Profile Configurations & Overrides

This document details the profile-specific configurations for DEFAULT, CLI-PRIME, and all other profiles to ensure full CLI integration.

---

## Profile Hierarchy

```
~/.hermes/
├── config.yaml                    # Global (fallback)
├── profiles/
│   ├── default/
│   │   └── config.yaml            # DEFAULT profile (full feature set)
│   ├── cli-prime/
│   │   └── config.yaml            # CLI-PRIME profile (streamlined)
│   ├── coder/
│   │   └── config.yaml            # CODER profile
│   ├── cowork/
│   │   └── config.yaml            # COWORK profile
│   ├── designer/
│   │   └── config.yaml            # DESIGNER profile
│   ├── prime/
│   │   └── config.yaml            # PRIME profile
│   ├── trader/
│   │   └── config.yaml            # TRADER profile
│   └── translator/
│       └── config.yaml            # TRANSLATOR profile
```

---

## 1. DEFAULT Profile (`~/.hermes/profiles/default/config.yaml`)

**Purpose**: Full-featured profile with all integrations enabled.

### Key Configuration
```yaml
model:
  base_url: https://openrouter.ai/api/v1
  default: nvidia/nemotron-3-ultra-550b-a55b:free
  provider: openrouter

fallback_providers:
  - provider: nous
    model: tencent/hy3:free
  - provider: nous
    model: poolside/laguna-s-2.1:free
  - provider: nous
    model: inclusionai/ling-3.0-flash:free
  - provider: nous
    model: stepfun/step-3.7-flash:free
  - provider: nous
    model: poolside/laguna-xs-2.1:free
  - provider: openrouter
    model: nvidia/nemotron-3-super-120b-a12b:free

agent:
  max_turns: 150
  max_tool_calls: 150
  reasoning_effort: high

# Image generation uses openai-codex
image_gen:
  use_gateway: false
  model: fal-ai/flux-2/klein/9b
  provider: openai-codex

video_gen:
  provider: fal
  use_gateway: true

# All toolsets enabled
platform_toolsets:
  cli:
    - a2a
    - bfl
    - browser
    - clarify
    - code_execution
    - computer_use
    - cronjob
    - delegation
    - file
    - image_gen
    - kanban
    - memory
    - session_search
    - skills
    - terminal
    - todo
    - tts
    - video
    - video_gen
    - vision
    - web
    - x_search

known_builtin_toolsets:
  cli:
    - bfl
    - browser
    - clarify
    - code_execution
    - computer_use
    - context_engine
    - cronjob
    - delegation
    - discord
    - discord_admin
    - file
    - homeassistant
    - image_gen
    - memory
    - session_search
    - skills
    - spotify
    - stt
    - terminal
    - todo
    - tts
    - video
    - video_gen
    - vision
    - web
    - x_search
    - yuanbao
```

### MCP Servers (Full Set)
```yaml
mcp_servers:
  agent-browser:
    args: [mcp, --tools, all]
    command: C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd
    timeout: 60
  browser:
    args: [-y, '@modelcontextprotocol/server-puppeteer']
    command: npx
    timeout: 60
  chrome-devtools:
    args: [-y, chrome-devtools-mcp@latest]
    command: npx
    timeout: 60
  docker-mcp:
    args: [-m, docker_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\docker-mcp\src
    timeout: 60
  elasticsearch-mcp:
    args: [-m, elasticsearch_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\elasticsearch-mcp\src
    timeout: 60
  filesystem:
    args:
      - -y
      - '@modelcontextprotocol/server-filesystem'
      - D:\Alex - KV Obsidian
      - C:\Users\apviz
      - E:\CLAUDE
    command: npx
    timeout: 60
  git:
    args: [--with, mcp<2, mcp-server-git]
    command: uvx
    timeout: 60
  memory:
    args: [-y, '@modelcontextprotocol/server-memory']
    command: npx
    timeout: 60
  minio-mcp:
    args: [-m, minio_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\minio-mcp\src
    timeout: 60
  obsidian:
    args:
      - -y
      - '@huangyihe/obsidian-mcp'
      - --vault-path
      - D:\Alex - KV Obsidian\Alex - KV Obsidian
    command: npx
    timeout: 60
  optimus-orchestrator:
    args: [-m, optimus_orchestrator.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\optimus-orchestrator\src
    timeout: 60
  postgresql-mcp:
    args: [-m, postgresql_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\postgresql-mcp\src
    timeout: 60
  prometheus-mcp:
    args: [-m, prometheus_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\prometheus-mcp\src
    timeout: 60
  qwen:
    args: [-y, '@gy920/qwen-mcp-tool']
    command: npx
    timeout: 60
  redis-mcp:
    args: [-m, redis_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\redis-mcp\src
    timeout: 60
  searxng:
    args: [-m, searxng_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\searxng-mcp\src
    timeout: 60
  sequential-thinking:
    args: [-y, '@modelcontextprotocol/server-sequential-thinking']
    command: npx
    timeout: 60
  session-replay:
    args: [-m, session_replay.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\session-replay\src
    timeout: 60
  tempo-mcp:
    args: [-m, tempo_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\tempo-mcp\src
    timeout: 60
  vault-mcp:
    args: [-m, vault_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\vault-mcp\src
    timeout: 60
  windows-system:
    args: [-m, windows_system.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\windows-system\src
    timeout: 60
  antigravity-bridge:
    args: [-m, antigravity_bridge.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\antigravity-bridge\src
    timeout: 60
  notebooklm:
    command: npx
    args: [-y, notebooklm-mcp@latest]
    timeout: 60
  blender:
    command: uvx
    args: [--with, mcp<2, blender-mcp==1.6.4]
    env:
      DISABLE_TELEMETRY: 'true'
    enabled: true
    tools:
      include:
        - get_scene_info
        - get_object_info
        - get_viewport_screenshot
        - execute_blender_code
  comfy-cloud:
    url: https://cloud.comfy.org/mcp
    auth: oauth
    enabled: true
    tools:
      include:
        - search_templates
        - get_template
        - get_template_schema
        - search_models
        - search_nodes
        - get_node
        - get_prompting_guide
        - run_template
        - submit_workflow
        - partner_generate
        - upload_file
        - apply_slots
        - get_job_status
        - wait_for_job
        - get_output
        - use_previous_output
        - cancel_job
        - get_queue
        - get_billing_status
        - get_workflow_canvas_url
  figma:
    url: https://mcp.figma.com/mcp
    auth: oauth
    enabled: true
```

---

## 2. CLI-PRIME Profile (`~/.hermes/profiles/cli-prime/config.yaml`)

**Purpose**: Streamlined profile optimized for CLI usage with focused toolsets.

### Key Configuration
```yaml
_config_version: 33
agent:
  max_tool_calls: 150
  max_turns: 150
  reasoning_effort: high
approvals:
  mode: smart
browser:
  allow_private_urls: true
checkpoints:
  enabled: true
display:
  show_reasoning: true
enforcement:
  auto_recalibrate: true
  enabled: true
  guardian_strict: true
  trigger_detection: true
known_plugin_toolsets:
  cli:
  - spotify
mcp_servers:
  agent-browser:
    args: [mcp, --tools, all]
    command: C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd
    timeout: 60
  browser:
    args: [-y, '@modelcontextprotocol/server-puppeteer']
    command: npx
    timeout: 60
  chrome-devtools:
    args: [-y, chrome-devtools-mcp@latest]
    command: npx
    timeout: 60
  docker-mcp:
    args: [-m, docker_mcp.server]
    command: python
    timeout: 60
  elasticsearch-mcp:
    args: [-m, elasticsearch_mcp.server]
    command: python
    timeout: 60
  filesystem:
    args:
      - -y
      - '@modelcontextprotocol/server-filesystem'
      - D:\Alex - KV Obsidian
      - C:\Users\apviz
      - E:\CLAUDE
    command: npx
    timeout: 60
  git:
    args: [mcp-server-git]
    command: uvx
    timeout: 60
  grafana-mcp:
    args: [-m, grafana_mcp.server]
    command: python
    timeout: 60
  loki-mcp:
    args: [-m, loki_mcp.server]
    command: python
    timeout: 60
  memory:
    args: [-y, '@modelcontextprotocol/server-memory']
    command: npx
    timeout: 60
  minio-mcp:
    args: [-m, minio_mcp.server]
    command: python
    timeout: 60
  obsidian:
    args:
      - -y
      - '@huangyihe/obsidian-mcp'
      - --vault-path
      - D:\Alex - KV Obsidian\Alex - KV Obsidian
    command: npx
    timeout: 60
  optimus-orchestrator:
    args: [-m, optimus_orchestrator.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\optimus-orchestrator
    timeout: 60
  postgresql-mcp:
    args: [-m, postgresql_mcp.server]
    command: python
    timeout: 60
  prometheus-mcp:
    args: [-m, prometheus_mcp.server]
    command: python
    timeout: 60
  qwen:
    args: [-y, '@gy920/qwen-mcp-tool']
    command: npx
    timeout: 60
  redis-mcp:
    args: [-m, redis_mcp.server]
    command: python
    timeout: 60
  searxng:
    args: [-m, searxng_mcp.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\searxng-mcp
    timeout: 60
  sequential-thinking:
    args: [-y, '@modelcontextprotocol/server-sequential-thinking']
    command: npx
    timeout: 60
  session-replay:
    args: [-m, session_replay.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\session-replay
    timeout: 60
  tempo-mcp:
    args: [-m, tempo_mcp.server]
    command: python
    timeout: 60
  vault-mcp:
    args: [-m, vault_mcp.server]
    command: python
    timeout: 60
  windows-system:
    args: [-m, windows_system.server]
    command: python
    timeout: 60
  antigravity-bridge:
    args: [-m, antigravity_bridge.server]
    command: python
    cwd: C:\Users\apviz\AppData\Local\hermes\mcp-servers\custom\antigravity-bridge
    timeout: 60

moa:
  aggregator:
    model: nvidia/nemotron-3-ultra-550b-a55b:free
    provider: openrouter
  enabled: true
  fanout: per_iteration
  max_tokens: 4096
  presets:
    default:
      aggregator:
        model: nvidia/nemotron-3-ultra-550b-a55b:free
        provider: openrouter
      fanout: per_iteration
      reference_models:
      - model: nousresearch/hermes-3-llama-3.1-405b:free
        provider: openrouter
      - model: meta-llama/llama-3.3-70b-instruct:free
        provider: openrouter
      - model: cognitivecomputations/dolphin-mistral-24b-venice-edition:free
        provider: openrouter
      - model: qwen/qwen3-coder:free
        provider: openrouter
      - model: openai/gpt-oss-120b:free
        provider: openrouter
      - model: openai/gpt-oss-20b:free
        provider: openrouter
  reference_models:
  - model: nousresearch/hermes-3-llama-3.1-405b:free
    provider: openrouter
  - model: meta-llama/llama-3.3-70b-instruct:free
    provider: openrouter
  - model: cognitivecomputations/dolphin-mistral-24b-venice-edition:free
    provider: openrouter
  - model: qwen/qwen3-coder:free
    provider: openrouter
  - model: openai/gpt-oss-120b:free
    provider: openrouter
  - model: openai/gpt-oss-20b:free
    provider: openrouter

onboarding:
  seen:
    openclaw_residue_cleanup: true
platform_toolsets:
  cli:
  - browser
  - clarify
  - code_execution
  - computer_use
  - cronjob
  - delegation
  - file
  - image_gen
  - kanban
  - memory
  - session_search
  - skills
  - terminal
  - todo
  - tts
  - video
  - video_gen
  - vision
  - web
  - x_search
security:
  allow_private_urls: true
```

---

## 3. Provider Access Across All Profiles

All 8 profiles inherit the global auth store (`~/.hermes/auth.json`) and can use:

| Provider | Available In | Notes |
|----------|-------------|-------|
| `openai-codex` | All profiles | Codex CLI OAuth |
| `gemini-oauth` | All profiles | Antigravity CLI OAuth |
| `openai-api` | All profiles | Direct OpenAI API key |
| `anthropic` | All profiles | Anthropic API key |
| `nous` | All profiles | Nous Portal |
| `openrouter` | All profiles | OpenRouter aggregator |
| `xai-oauth` | All profiles | xAI Grok OAuth |
| `qwen-oauth` | All profiles | Qwen OAuth |
| `minimax-oauth` | All profiles | MiniMax OAuth |
| `copilot` | All profiles | GitHub Copilot |
| `copilot-acp` | All profiles | GitHub Copilot ACP |
| `bedrock` | All profiles | AWS Bedrock |
| `azure-foundry` | All profiles | Azure Foundry |
| `vertex` | All profiles | Google Vertex AI |
| `custom:*` | All profiles | Custom endpoints |

### Per-Provider Model Defaults (can override per profile)
```yaml
# Example: Set gemini-oauth as default for CLI-PRIME
model:
  provider: gemini-oauth
  default: gemini-3.6-flash

# Fallback chain specific to profile
fallback_providers:
  - provider: gemini-oauth
    model: gemini-3.6-flash
  - provider: openai-codex
    model: gpt-4o
  - provider: openrouter
    model: google/gemini-3.6-flash
```

---

## 4. CLI-PRIME Specific Optimizations

### Toolset Selection
```yaml
platform_toolsets:
  cli:
    - browser          # Web automation
    - clarify          # User clarification
    - code_execution   # Python execution
    - computer_use     # Desktop automation
    - cronjob          # Scheduled tasks
    - delegation       # Sub-agent spawning
    - file             # File operations
    - image_gen        # Image generation
    - kanban           # Task boards
    - memory           # Persistent memory
    - session_search   # Session history
    - skills           # Skill system
    - terminal         # Shell access
    - todo             # Task tracking
    - tts              # Text-to-speech
    - video            # Video analysis
    - video_gen        # Video generation
    - vision           # Image analysis
    - web              # Web search/extract
    - x_search         # X/Twitter search
```

### MCP Server Selection (Focused)
- **agent-browser**: Full browser automation
- **browser**: Puppeteer-based
- **chrome-devtools**: Chrome DevTools Protocol
- **filesystem**: Local file access (3 paths)
- **git**: Git operations
- **memory**: Persistent memory
- **obsidian**: Vault access
- **antigravity-bridge**: **CRITICAL** - Two-way Antigravity communication
- **optimus-orchestrator**: Advanced orchestration
- **sequential-thinking**: Structured reasoning
- **session-replay**: Session recording

---

## 5. Verification Per Profile

### Check Profile Loads Correctly
```bash
# List profiles
hermes --profile cli-prime doctor --fix

# Check auth status in profile
hermes --profile cli-prime auth list

# Check model picker
hermes --profile cli-prime model

# Check MCP servers
hermes --profile cli-prime mcp list
```

### Expected Output (CLI-PRIME)
```
Auth Providers:
  ✓ Nous Portal auth (logged in)
  ✓ OpenAI Codex auth (logged in)
  ✓ Google Gemini OAuth (logged in via Antigravity CLI)
  ⚠ MiniMax OAuth (not logged in)
  ⚠ xAI OAuth (not logged in)

Model Picker:
  openai-codex (OpenAI Codex)
  gemini-oauth (Google Gemini OAuth)
  ... other providers ...

MCP Servers:
  antigravity-bridge: active
  agent-browser: active
  ... other servers ...
```

---

## 6. Adding New Profiles

### Template for New Profile
```bash
# Create profile directory
mkdir -p ~/.hermes/profiles/new-profile

# Create config.yaml
cat > ~/.hermes/profiles/new-profile/config.yaml << 'EOF'
_config_version: 33
model:
  provider: openrouter
  default: google/gemini-3.6-flash
fallback_providers:
  - provider: gemini-oauth
    model: gemini-3.6-flash
  - provider: openai-codex
    model: gpt-4o
agent:
  max_turns: 150
  max_tool_calls: 150
mcp_servers:
  antigravity-bridge:
    args: [-m, antigravity_bridge.server]
    command: python
    cwd: ~/.hermes/mcp-servers/custom/antigravity-bridge/src
    timeout: 60
platform_toolsets:
  cli:
    - terminal
    - file
    - web
    - skills
    - delegation
    - code_execution
EOF
```

### Profile-Specific Customizations
| Profile | Focus | Recommended Providers | Key MCP Servers |
|---------|-------|----------------------|-----------------|
| `coder` | Development | `gemini-oauth`, `openai-codex`, `openrouter` | `antigravity-bridge`, `git`, `filesystem` |
| `designer` | Design | `openai-codex` (image_gen), `gemini-oauth` | `blender`, `comfy-cloud`, `figma` |
| `trader` | Finance | `openrouter`, `nous` | `prometheus-mcp`, `tempo-mcp` |
| `translator` | Translation | `gemini-oauth`, `openrouter` | `sequential-thinking` |

---

## 7. Global Auth Store (Shared Across Profiles)

Location: `~/.hermes/auth.json`

```json
{
  "version": 1,
  "providers": {
    "openai-codex": { ... },
    "gemini-oauth": { ... },
    "nous": { ... },
    "openrouter": { ... }
  },
  "credential_pool": {
    "openai-codex": [...],
    "gemini-oauth": [...],
    "openai-api": [...]
  },
  "suppressed_sources": {}
}
```

All profiles read/write to this same file, enabling:
- Single auth setup for all profiles
- Credential pool sharing
- Consistent auth status across profiles

---

## 8. Migration from Legacy Config

If you have legacy profile configs without the new providers:

```bash
# 1. Backup existing configs
cp -r ~/.hermes/profiles ~/.hermes/profiles.backup

# 2. Add missing providers to each profile's config.yaml
# Edit each ~/.hermes/profiles/<name>/config.yaml
# Ensure fallback_providers includes gemini-oauth and openai-codex

# 3. Verify
for profile in default cli-prime coder cowork designer prime trader translator; do
  echo "=== $profile ==="
  hermes --profile $profile doctor --fix | grep -E "Codex|Gemini"
done
```

---

*This document ensures all profiles have full access to Codex CLI, Antigravity/Gemini CLI, and the Antigravity Bridge MCP.*