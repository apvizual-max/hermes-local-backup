---
title: Connectors, Tools & Harness Specifics
version: 1.0.0
---

# Connectors, Tools & Harness Specifics

This document details the specific connectors, tools, and unique capabilities of each CLI harness that Hermes can leverage.

---

## 1. CODEX CLI (OpenAI) - Harness Specifics

### Native Capabilities
| Capability | Description | Access Method |
|------------|-------------|---------------|
| **Code Generation** | Multi-file code generation with context awareness | `codex -p "prompt"` |
| **Code Review** | Security, style, correctness analysis | `codex -p "Review for..."` |
| **Refactoring** | Large-scale refactoring across files | `codex -p "Refactor..."` |
| **Test Generation** | Unit, integration, e2e test creation | `codex -p "Write tests for..."` |
| **Debugging** | Root cause analysis, fix suggestions | `codex -p "Debug this error..."` |
| **Documentation** | Auto-generate docs from code | `codex -p "Document this module"` |

### Unique Features
- **Sandbox Execution**: `--dangerously-bypass-approvals-and-sandbox` for full autonomy
- **Conversation Persistence**: `codex resume --last` continues previous session
- **Model Selection**: GPT-4o, GPT-4o-mini, o1-preview, o1-mini
- **File Operations**: Native read/write/execute in workspace
- **Git Integration**: Can stage, commit, create PRs
- **MCP Support**: Can connect to MCP servers

### Connectors Available
| Connector | Purpose | Config |
|-----------|---------|--------|
| **GitHub** | PR creation, issue linking | `codex mcp add github` |
| **Filesystem** | Local file operations | Built-in |
| **Terminal** | Command execution | Built-in |
| **Web Search** | Live web search | Built-in |
| **Custom MCP** | Any MCP server | `codex mcp add <name> <command>` |

### Harness-Specific Workflows
```bash
# 1. Feature Development Workflow
codex -p "
1. Read SPEC.md
2. Implement feature in src/
3. Write tests in tests/
4. Run tests
5. Create PR
"

# 2. Bug Fix Workflow
codex -p "
1. Reproduce bug from issue #123
2. Identify root cause
3. Implement fix
4. Add regression test
5. Verify fix
"

# 3. Code Review Workflow
codex -p "
Review PR #456 for:
- Security vulnerabilities
- Performance issues
- Code style violations
- Missing tests
"

# 4. Refactoring Workflow
codex -p "
Refactor auth module to use new credential pool:
1. Analyze current auth.py
2. Plan migration
3. Implement changes
4. Update all callers
5. Run full test suite
"
```

### Perks & Strengths
- **Best for**: Complex multi-file changes, PR creation, GitHub integration
- **Strongest models**: GPT-4o, o1-preview for reasoning
- **Sandbox**: Most mature sandbox execution
- **Context window**: Large (128k+ tokens)

---

## 2. ANTIGRAVITY CLI (Google Gemini) - Harness Specifics

### Native Capabilities
| Capability | Description | Access Method |
|------------|-------------|---------------|
| **Code Generation** | Multi-file generation with Google's models | `agy -p "prompt"` |
| **Code Review** | Analysis with Gemini's reasoning | `agy -p "Review for..."` |
| **Research** | Deep research with Google Search integration | `agy -p "Research..."` |
| **Multimodal** | Image, PDF, text analysis | `agy -p "Analyze this image" --add-file image.png` |
| **Long Context** | Up to 2M tokens (Gemini 1.5 Pro) | `agy -p "..." --model "Gemini 1.5 Pro"` |

### Unique Features
- **Google Search Integration**: Native `googleSearch` tool
- **Multimodal Native**: Images, PDFs, audio, video understanding
- **Massive Context**: 2M token context window (Gemini 1.5 Pro)
- **Thinking Models**: "Thinking" variants show reasoning traces
- **Antigravity Bridge MCP**: Two-way async communication with Hermes
- **Plugin System**: Extensible with skills, agents, MCP servers

### Model Variants (run `agy models` for current list)
| Model | Context | Best For |
|-------|---------|----------|
| **Gemini 3.1 Pro (High)** | 2M | Complex reasoning, coding |
| **Gemini 3.1 Pro** | 2M | General coding, analysis |
| **Gemini 3.1 Flash** | 2M | Fast, cost-effective |
| **Gemini 3.1 Flash Lite** | 2M | Ultra-fast, simple tasks |
| **Gemini 2.5 Pro** | 1M | Legacy, stable |
| **Gemini 2.5 Flash** | 1M | Legacy, fast |

### Connectors Available
| Connector | Purpose | Config |
|-----------|---------|--------|
| **Google Search** | Live web search | Built-in (`googleSearch` tool) |
| **Filesystem** | Local file operations | Built-in |
| **Terminal** | Command execution | Built-in |
| **MCP Servers** | Extensible via `agy plugin` | `agy plugin install <target>` |
| **Antigravity Bridge** | Two-way Hermes communication | MCP server (auto-configured) |

### Harness-Specific Workflows
```bash
# 1. Deep Research Workflow
agy -p "
Research the latest auth patterns for multi-tenant SaaS:
1. Search for current best practices
2. Analyze OAuth 2.1, OIDC, SAML
3. Compare with our current implementation
4. Recommend improvements
" --model "Gemini 3.1 Pro (High)"

# 2. Multimodal Analysis
agy -p "
Analyze this architecture diagram and suggest improvements:
" --add-file arch-diagram.png --model "Gemini 3.1 Pro (High)"

# 3. Large Codebase Analysis (2M context)
agy -p "
Review the entire codebase for security issues:
1. Read all files in src/
2. Identify vulnerabilities
3. Prioritize by severity
4. Provide fix recommendations
" --model "Gemini 3.1 Pro (High)"

# 4. Thinking Mode (shows reasoning)
agy -p "
Solve this complex algorithmic problem step by step:
" --model "Gemini 3.1 Pro (Thinking)"

# 5. Plugin/Agent Workflow
agy -p "
Use the 'code-reviewer' agent to review this PR:
" --agent "code-reviewer"
```

### Perks & Strengths
- **Best for**: Research, multimodal, massive context, Google ecosystem
- **Strongest models**: Gemini 3.1 Pro (High) for coding, 1.5 Pro for context
- **Search**: Native Google Search integration
- **Context window**: Industry-leading 2M tokens
- **Cost**: Often more cost-effective for large contexts

---

## 3. Harness Comparison Matrix

| Feature | Codex CLI | Antigravity CLI |
|---------|-----------|-----------------|
| **Primary Model Family** | OpenAI (GPT-4o, o1) | Google (Gemini 3.x, 1.5) |
| **Auth** | Device code (OpenAI) | Google OAuth |
| **Context Window** | 128k+ | 2M (1.5 Pro) |
| **Multimodal** | Limited (images) | Full (images, PDF, audio, video) |
| **Web Search** | Via tools | Native Google Search |
| **Sandbox** | Mature | Developing |
| **GitHub Integration** | Native PR creation | Via MCP/plugins |
| **MCP Support** | Yes | Yes (via plugins) |
| **Two-way Bridge** | No | Yes (Antigravity Bridge MCP) |
| **Plugin System** | Limited | Full (skills, agents, MCP) |
| **Conversation Resume** | `codex resume` | `agy --continue` |
| **Output Format** | Plain text | Plain text |
| **Cost (approx)** | Higher for large context | Lower for large context |

---

## 4. When to Use Which Harness

### Use **Codex CLI** when:
- ✅ Creating PRs on GitHub
- ✅ Complex multi-file refactoring with git operations
- ✅ Need mature sandbox execution
- ✅ Working with OpenAI models (GPT-4o, o1)
- ✅ Team workflows with GitHub integration

### Use **Antigravity CLI** when:
- ✅ Need massive context (2M tokens)
- ✅ Multimodal analysis (images, PDFs, diagrams)
- ✅ Deep research with Google Search
- ✅ Cost-sensitive large-context tasks
- ✅ Two-way async orchestration via Hermes Bridge
- ✅ Need thinking/reasoning traces
- ✅ Google ecosystem integration

### Use **Both (Cross-Check)** when:
- ✅ Security reviews (different model families = different blind spots)
- ✅ Architecture decisions (multiple perspectives)
- ✅ Critical bug fixes (independent verification)
- ✅ Model comparison/benchmarking

---

## 5. Hermes Orchestration: Leveraging Both Harnesses

### Pattern: Sequential Delegation
```python
# 1. Antigravity: Research & Planning (large context, search)
plan = agy -p "Research best practices for X and create implementation plan"

# 2. Codex: Implementation (git, sandbox, PR creation)
codex -p "Implement the plan: {plan}. Create PR when done."
```

### Pattern: Parallel Cross-Check
```python
# Run both simultaneously
task1 = terminal(command="codex -p 'Security audit of auth module'", background=true)
task2 = terminal(command="agy -p 'Security audit of auth module' --model 'Gemini 3.1 Pro (High)'", background=true)

# Collect and compare
result1 = process(action="wait", session_id=task1.session_id)
result2 = process(action="wait", session_id=task2.session_id)
# Compare findings
```

### Pattern: Fallback Chain
```yaml
# config.yaml
fallback_providers:
  - provider: gemini-oauth      # Try Antigravity first (large context, search)
    model: gemini-3.6-flash
  - provider: openai-codex      # Fallback to Codex
    model: gpt-4o
  - provider: openrouter        # Final fallback
    model: google/gemini-3.6-flash
```

---

## 6. Connector Details

### Codex CLI Connectors
```bash
# Built-in
codex mcp list                    # List MCP servers
codex mcp add github              # Add GitHub MCP
codex mcp add filesystem /path    # Add filesystem access

# GitHub Actions
codex -p "Create PR with changes"  # Auto-creates PR
```

### Antigravity CLI Connectors
```bash
# Built-in tools
googleSearch                      # Native Google Search
analyzeFile                       # Multimodal file analysis
chat                              # Conversation

# MCP via plugins
agy plugin install github-mcp     # Install GitHub MCP
agy plugin install filesystem     # Install filesystem MCP
agy mcp list                      # List active MCP servers

# Antigravity Bridge (Hermes-specific)
# Already configured in config.yaml
# Tools: ag_delegate_task, ag_poll_response, etc.
```

### Hermes-Level Connectors (Available to Both)
```python
# Via Hermes tools
browser_navigate / browser_click / browser_type  # Web automation
terminal(command="...")          # Shell execution
web_search / web_extract         # Web research
file / read_file / write_file    # File operations
vision_analyze                   # Image analysis
memory / session_search          # Persistent memory
cronjob                          # Scheduled tasks
delegation                       # Sub-agent spawning
```

---

## 7. Memory & State Persistence

### Codex CLI
- **Conversations**: `~/.codex/sessions/` (JSON)
- **Resume**: `codex resume --last` or `codex resume -c <id>`
- **Fork**: `codex fork --last` to branch conversation

### Antigravity CLI
- **Conversations**: `~/.gemini/antigravity-cli/conversations/`
- **History**: `~/.gemini/antigravity-cli/history.jsonl`
- **Brain Artifacts**: `~/.gemini/antigravity-cli/brain/`
- **Continue**: `agy --continue` or `agy -c <id>`

### Hermes (Orchestrator)
- **Credential Pool**: `~/.hermes/auth.json` (unified, persistent)
- **Sessions**: `~/.hermes/sessions/` (SQLite)
- **Memory**: `~/.hermes/memories/MEMORY.md` + `USER.md`
- **Skills**: `~/.hermes/skills/` (this skill bundle)
- **Cron Jobs**: `~/.hermes/cron/` (scheduled tasks)

---

## 8. Per-Harness Configuration

### Codex CLI Config
```bash
# ~/.codex/config.toml
model = "gpt-4o"
sandbox_permissions = ["disk-full-read-access", "disk-full-write-access"]
shell_environment_policy = { inherit = "all" }
```

### Antigravity CLI Config
```json
// ~/.gemini/antigravity-cli/settings.json
{
  "colorScheme": "tokyo night",
  "trustedWorkspaces": ["D:\\Alex - KV Obsidian"],
  "allowNonWorkspaceAccess": true,
  "permissions": {
    "allow": ["terminal", "filesystem", "googleSearch"]
  }
}
```

### Hermes Config (Shared)
```yaml
# ~/.hermes/profiles/default/config.yaml
model:
  provider: openrouter
  default: nvidia/nemotron-3-ultra-550b-a55b:free

mcp_servers:
  antigravity-bridge:
    args: [-m, antigravity_bridge.server]
    command: python
    cwd: ~/.hermes/mcp-servers/custom/antigravity-bridge/src
    timeout: 60
```

---

*This document complements the main integration specs in `references/codex-cli.md`, `references/antigravity-cli.md`, and `references/gemini-cli.md`.*