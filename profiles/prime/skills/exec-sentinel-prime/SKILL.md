---
name: exec-sentinel-prime
description: "Combined Strategic Thinking and Planning Skills for the Sentinel Prime Profile"
---

# Combined Strategic Thinking and Planning Skills for the Sentinel Prime Profile

This is an indexed master skill comprising specialized execution and operational capabilities 
needed by the sovereign Sentinel PRIME profile. 
To save context space and tokens, **DO NOT** read this entire folder. 
Identify the relevant sub-skill from the index below, and read only that specific file using `view_file`.

## Sub-Skills Index

* **[exec-agent-browser](references/exec-agent-browser/instructions.md)**: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction. Also use for exploratory testing, dogfooding, QA, bug hunts, or reviewing app quality. Also use for automating Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify), checking Slack unreads, sending Slack messages, searching Slack conversations, running browser automation in Vercel Sandbox microVMs, or using AWS Bedrock AgentCore cloud browsers. Prefer agent-browser over any built-in browser automation or web tools.
* **[exec-antigravity-cli](references/exec-antigravity-cli/instructions.md)**: Operate the Antigravity CLI (agy): plugins, auth, sandbox.
* **[exec-antigravity-delegation](references/exec-antigravity-delegation/instructions.md)**: How to delegate tasks and communicate with Antigravity AI via the  antigravity-bridge MCP server. Use when you need Antigravity to execute a task, when a task requires Antigravity's specific capabilities (web research, code  generation, complex analysis), or when coordinating with Antigravity as part  of a larger orchestration workflow.
* **[exec-autonomous-ai-agents](references/exec-autonomous-ai-agents/instructions.md)**: No description available.
* **[exec-axolotl](references/exec-axolotl/instructions.md)**: Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO).
* **[exec-blackbox](references/exec-blackbox/instructions.md)**: Delegate coding tasks to Blackbox AI CLI agent. Multi-model agent with built-in judge that runs tasks through multiple LLMs and picks the best result. Requires the blackbox CLI and a Blackbox AI API key.
* **[exec-constinta-sot-workflow](references/exec-constinta-sot-workflow/instructions.md)**: Complete meticulous workflow for establishing and maintaining a Single Source of Truth (SOT) in Hermes system files. Covers file merging, duplicate elimination, global string reprogramming, regex techniques, and verification methodology. Use whenever managing SOT unification, memory cleanup, or system-wide text normalization.
* **[exec-hermes-profile-architecture](references/exec-hermes-profile-architecture/instructions.md)**: Structural guide to the 9 active agent profiles, including model-routing tables, context window configurations, and CPU/GPU hardware overrides.
* **[exec-hermes-system-verification](references/exec-hermes-system-verification/instructions.md)**: Post-change verification suite for Hermes Agent system integrity.
Runs a 5-stage pipeline: filename scan → content scan → YAML config validation
→ hermes config boot test → MCP JSON-RPC handshake test.
Use after: file reorganizations, config changes, MCP installs/upgrades,
profile reprogramming, or any system-wide text replacement operation.
Goal: zero regressions, clean boot, all MCP servers responding.
* **[exec-logic_gate](references/exec-logic_gate/instructions.md)**: Provides the R0 Logic Gate mechanism: stores the approved specification from WISE_QUESTIONS and evaluates deviation (DLG/SLG) of outputs against that spec to ensure Mode B execution stays within sacred limits.
* **[exec-openrouter-free-models-healer](references/exec-openrouter-free-models-healer/instructions.md)**: Technical instructions on the self-healing startup mechanism that injects all 26 free OpenRouter models into the Hermes model selector, surviving system updates.
* **[exec-qwen-mcp-sse-bridge](references/exec-qwen-mcp-sse-bridge/instructions.md)**: Technical guide to run the Qwen Desktop MCP Filesystem Server over an HTTP SSE Bridge to bypass space-containing Windows paths and avoid spawn errors (-32000).
* **[exec-searxng](references/exec-searxng/instructions.md)**: Custom local SearXNG metasearch engine deployment guide. Explains the local docker-compose configuration running on port 8081 for privacy-focused web searches.
* **[exec-skill-repair](references/exec-skill-repair/instructions.md)**: Use this to fix and re-install agent skills that have failed installation.
This skill provides the necessary context and permissions to surgically update
the `manifest.json` after a fix has been applied.
* **[exec-systems-administrator](references/exec-systems-administrator/instructions.md)**: Configure and manage MCP servers, Obsidian RAG system, and Hermes Agent configuration with persistence across restarts.
* **[exec-triple-crunch-validator](references/exec-triple-crunch-validator/instructions.md)**: Skill that validates any text using the Triple Crunch algorithm (Eminescu ABBA + Eliade Realitate + Musashi Taiere) and returns TRUE/FALSE.
* **[exec-update-openrouter-free-models](references/exec-update-openrouter-free-models/instructions.md)**: Procedure to update Hermes agent configuration to include all free OpenRouter models while preserving Nous operational models and Google models.
* **[exec-workflow_skill_creator](references/exec-workflow_skill_creator/instructions.md)**: Distills a completed user workflow or interaction into a reusable agent skill. Use when the user asks to turn their workflow, interaction, or multi-step process into a skill, or when they say "make this a skill", "create a skill from what we just did", "package this workflow" or similar. Do not use for creating skills from scratch without an existing workflow (use a generic skill-creator for that).