---
name: exec-sentinel-cowork
description: "Combined Systems CEO and Autonomous Task Delegation Skills for the Sentinel Cowork Profile"
---

# Combined Systems CEO and Autonomous Task Delegation Skills for the Sentinel Cowork Profile

This is an indexed master skill comprising specialized execution and operational capabilities 
needed by the sovereign Sentinel COWORK profile. 
To save context space and tokens, **DO NOT** read this entire folder. 
Identify the relevant sub-skill from the index below, and read only that specific file using `view_file`.

## Sub-Skills Index

* **[exec-antigravity-delegation](references/exec-antigravity-delegation/instructions.md)**: How to delegate tasks and communicate with Antigravity AI via the  antigravity-bridge MCP server. Use when you need Antigravity to execute a task, when a task requires Antigravity's specific capabilities (web research, code  generation, complex analysis), or when coordinating with Antigravity as part  of a larger orchestration workflow.
* **[exec-autonomous-ai-agents](references/exec-autonomous-ai-agents/instructions.md)**: No description available.
* **[exec-bigquery-data-transfer-service](references/exec-bigquery-data-transfer-service/instructions.md)**: Discovers and inspects BigQuery Data Transfer Service (DTS) configurations. Use this to identify existing ingestion pipelines and extract datasource or transfer config metadata for data pipelines. Use when a user asks for ingestion scenarios while building or managing data pipelines or when a user asks to "ingest" or "add" data that may already be managed by a DTS transfer.
* **[exec-computer-use](references/exec-computer-use/instructions.md)**: Drive the user's desktop in the background — clicking, typing,
scrolling, dragging — without stealing the cursor, keyboard focus,
or switching virtual desktops / Spaces. Cross-platform: macOS,
Windows, Linux. Works with any tool-capable model. Load this skill
whenever the `computer_use` tool is available.
* **[exec-data-autocleaning](references/exec-data-autocleaning/instructions.md)**: Automated data quality and transformation capabilities for Dataform/dbt/BigQuery pipelines. Processes data sourced from BigQuery or Cloud Storage (GCS), applying best practices for data ingestion, movement, schema mapping, and comprehensive data cleaning.
* **[exec-devops](references/exec-devops/instructions.md)**: No description available.
* **[exec-github](references/exec-github/instructions.md)**: No description available.
* **[exec-hermes-antigravity-bridge](references/exec-hermes-antigravity-bridge/instructions.md)**: Two-way communication bridge between Hermes Agent and Antigravity AI.
Uses a shared file-based IPC queue (inbox/outbox/history) located at:
C:\Users\apviz\AppData\Local\hermes\pairing\antigravity\
Use when: Hermes has delegated a task via ag_delegate_task or ag_send_message,
when checking inbox for pending tasks from Hermes, writing responses to outbox,
or when setting up, testing, or maintaining the bridge infrastructure.
Antigravity = EXECUTOR role. Hermes = ORCHESTRATOR role.
* **[exec-productivity](references/exec-productivity/instructions.md)**: No description available.
* **[exec-workflow_skill_creator](references/exec-workflow_skill_creator/instructions.md)**: Distills a completed user workflow or interaction into a reusable agent skill. Use when the user asks to turn their workflow, interaction, or multi-step process into a skill, or when they say "make this a skill", "create a skill from what we just did", "package this workflow" or similar. Do not use for creating skills from scratch without an existing workflow (use a generic skill-creator for that).