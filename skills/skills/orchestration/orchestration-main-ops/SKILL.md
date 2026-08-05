---
name: orchestration-main-ops
description: "Orchestrate any desktop task via map-click-dispatch loop."
version: 0.1.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags:
      - Orchestration
      - Desktop-Automation
      - Multi-Monitor
      - Subagent-Dispatch
---

# Orchestration Main Ops — Sentinel's Master Workflow

The master workflow for automating ANY desktop task on this station. Used when a task takes >30 minutes manually or when `computer_use` fails on the upper monitor.

## What This Skill Does

Provides the 6-step orchestration loop: map → click → execute → dispatch → instruct → verify. It ties together the specialized skills (`grid-based-page-mapping`, `cua-driver-mcp-click`, `scrape-my-jobs-linkedin`) into one repeatable process.

## What This Skill Does NOT Do

- Replace the specialized skills — it references them
- Handle tasks that require the user's direct input (R0 gate)
- Work on the primary monitor (use `computer_use` directly there)

## Station Constants (HARD-CODED)

| Constant | Value | Purpose |
|----------|-------|---------|
| `UPPER_PID` | 27416 | Chrome process on upper monitor |
| `UPPER_HWND` | 1507982 | Chrome window handle on upper monitor |
| `VIRTUAL_ORIGIN` | (0, -1080) | Upper monitor virtual screen origin |
| `MAP_DIR` | `C:/Users/apviz/Desktop/TEST` | Page maps and scrape output |

## The 6-Step Orchestration Loop

### Step 1: Page Mapping

**Goal**: Create a reusable coordinate map of the current page.

**Method**: Load `grid-based-page-mapping` skill.

```bash
echo '{"pid":27416,"window_id":1507982,"max_elements":500}' | cua-driver call get_window_state
```

Extract: screenshot PNG, all clickable elements with frames, grid index.

**Output**: `{PAGE_NAME}.png` + `{PAGE_NAME}_MAP.json` + `{PAGE_NAME}_INDEX.md`

**Rule**: Map ONCE per page. Reuse the map until design changes.

### Step 2: MCP Clicking

**Goal**: Click any element on the upper monitor without focus steal.

**Method**: Load `cua-driver-mcp-click` skill.

```python
proc = subprocess.Popen(['cua-driver', 'mcp', '--no-daemon-relaunch'], stdin=PIPE, stdout=PIPE, text=True)
# 1. JSON-RPC get_window_state → parse text with regex → find element index
# 2. JSON-RPC click(element_index=N, delivery_mode="background")
# 3. JSON-RPC get_window_state → verify URL changed
proc.terminate()
```

**Rule**: NEVER use `cua-driver call click` — cache dies. ALWAYS use MCP.

### Step 3: {INSERT_HUMAN_ACTIVITY_HERE}

**Goal**: Execute the user's specific task on the current page.

**Examples**:
- Scrape all jobs → `scrape-my-jobs-linkedin`
- Fill a form → map form fields → click + type each
- Navigate a multi-page flow → for each page: map → click next → repeat
- Extract data from a table → map → parse → save

**Rule**: Every unique activity gets its own sub-steps here. This section GROWS.

### Step 4: Agent Dispatch Schema

**Goal**: Dispatch a subagent with STRICT instructions that prevent window drift.

**Schema** (COPY EXACTLY):

```
⛔⛔⛔ CRITICAL: READ BEFORE ANY TOOL CALL ⛔⛔⛔

TARGET WINDOW (DO NOT CHANGE):
- PID: 27416 | HWND: 1507982 | Upper monitor, origin (0,-1080)
- This window ALREADY EXISTS. Do NOT create a new one.

FORBIDDEN: browser_navigate, computer_use, browser_click, browser_snapshot
ALLOWED: terminal (cua-driver mcp), read_file, write_file

CLICK METHOD:
proc = subprocess.Popen(['cua-driver', 'mcp', '--no-daemon-relaunch'], stdin=PIPE, stdout=PIPE, text=True)
1. JSON-RPC get_window_state(pid=27416, window_id=1507982, max_elements=300)
2. Parse: re.search(r'\[(\d+)\]\s+\w+\s+"{LABEL}"', text)
3. JSON-RPC click(pid=27416, window_id=1507982, element_index=N, delivery_mode="background")
4. JSON-RPC get_window_state → verify
proc.terminate()

TASK: {TASK_DESCRIPTION}
OUTPUT: {OUTPUT_PATH}
```

### Step 5: Subagent Instructions

**Goal**: Give the subagent the exact task, method, and output format.

**Template**:
- `goal`: One-line task summary
- `context`: The FULL agent dispatch schema from Step 4 with placeholders filled
- Always include: PID, HWND, forbidden tools, click method, output path

**Rule**: Subagents without strict instructions WILL open new windows. Never skip the schema.

### Step 6: Verification Patterns

**Goal**: Confirm every action produced the expected result.

**Checklist**:
- [ ] URL changed as expected? → `get_window_state` + check address bar value
- [ ] Element count matches? → compare `element_count` before/after
- [ ] Screenshot shows expected content? → save PNG, visually inspect
- [ ] Output file exists and is valid? → `read_file` the output
- [ ] No new windows opened? → check `list_windows` or ask user

**Verification command**:
```bash
echo '{"pid":27416,"window_id":1507982,"max_elements":10}' | cua-driver call get_window_state
```

## When to Use

- "automate this" — any task on the upper monitor
- "scrape this" — data extraction from pages
- "navigate and click" — multi-page flows
- "do this for all pages" — paginated scraping
- When a task takes >30 minutes manually

## Quick Reference

| Step | Skill/Tool | Command Pattern |
|------|-----------|----------------|
| Map | `grid-based-page-mapping` | `cua-driver call get_window_state` (max_elements=500) |
| Click | `cua-driver-mcp-click` | `cua-driver mcp --no-daemon-relaunch` + JSON-RPC |
| Scrape | `scrape-my-jobs-linkedin` | Map → parse → click next → repeat |
| Dispatch | This skill (Step 4) | `delegate_task` with strict schema |
| Verify | This skill (Step 6) | `get_window_state` + check URL |

## Pitfalls

- **NEVER skip the agent dispatch schema** — subagents WILL open new windows without it
- **MCP get_window_state returns TEXT** — parse with regex, not json.loads()
- **Element cache dies between cua-driver call invocations** — always use MCP for clicks
- **Upper monitor is on a different GPU** — only MCP method works for clicking
- **This skill GROWS** — add new activities to Step 3 as they are discovered

## Skill Management Ritual (⛔ NEVER VIOLATE)

Skills are **knowledge rituals**, not files to optimize. They accumulate over time. Truncating a skill destroys the learning process.

| Rule | Why |
|------|-----|
| **NEVER truncate a skill** | Skills are memory points. Truncation = amnesia. |
| **Only PATCH to correct** | Use `skill_manage(action='patch')` for targeted edits. |
| **Never `write_file` over a skill** | Overwrites destroy accumulated history. |
| **Additive only** | New knowledge appends or patches. Never replaces wholesale. |
| **Removal = ritual** | Requires explicit user approval (R0). Never during normal operation. |

**The ritual**: When a skill is wrong → patch it. When it grows → add a section. When it's obsolete → flag for ritual cleanup (separate process, not during active work).

## Re-Delegation Pattern (ORCHESTRATOR'S CORE LOOP)

When a subagent returns, evaluate BEFORE accepting. If unsatisfactory, correct and re-dispatch. Never do the agent's work yourself.

### The Loop

```
1. DISPATCH agent with strict schema
2. EVALUATE result:
   ├─ D2_JUST_FAB triggered? → agent fabricated
   ├─ Output empty/incomplete? → agent failed
   ├─ Same data as previous page? → agent didn't navigate
   └─ Valid data? → ACCEPT
3. CORRECT: identify root cause, add rule to schema
4. RE-DISPATCH with corrected instructions
5. REPEAT until valid result
```

### Fabrication Detection

| Marker | Meaning |
|--------|---------|
| "complete" | Agent fabricated a summary |
| "total" | Agent synthesized data |
| "done" | Agent claimed finished without verification |
| D2_JUST_FAB sensor | System detected fabrication |

### Why This Matters

- Subagents WILL drift without strict instructions
- Doing the work yourself defeats the orchestration pattern
- Each failure improves the schema — the agent learns from corrected instructions
- The orchestrator orchestrates, not executes

## MOA Judge Pipeline

The Mixture of Agents has a specific architecture. Each model has a role:

| Model | Role | Function |
|-------|------|----------|
| Hermes-3-405B | **JUDGE** | Schema verification → verdict → compress → instructions for Sentinel |
| Llama-3.3-70B | **BALANCED** | General reasoning, fallback strength |
| DeepSeek-V4 | **CODING** | Top-tier code generation |
| Qwen3-Coder | **CODING** | Fast coding, Alibaba ecosystem |
| Dolphin-Mistral-24B | **TRANSLATOR** | Romanian translation specialist |
| GPT-OSS-120B | **GENERAL** | Broad knowledge, creative tasks |
| Nemotron | **AGGREGATOR** | Combines all 6 verdicts into one response |

**The Judge's small context is BY DESIGN**: receives schema + 6 outputs → verifies → gives verdict → notes what to expect → converts to instructions for Sentinel → clears context. The judge doesn't need a large context window — it needs precision.

**The `default` MOA preset** is the Hermes factory preset (gpt-5.5 + claude-opus-4.8). It is NOT active — `optimus_prime_models` is. The profile is called `default` by Hermes — that's the name, not a bug. Leave it alone.

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

