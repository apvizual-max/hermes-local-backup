---
name: exec-sentinel-assist
description: "Combined Execution and Assistant Skills for the Sentinel Assist Profile"
---

# Combined Execution and Assistant Skills for the Sentinel Assist Profile

This is an indexed master skill comprising specialized execution and operational capabilities 
needed by the sovereign Sentinel ASSIST profile. 
To save context space and tokens, **DO NOT** read this entire folder. 
Identify the relevant sub-skill from the index below, and read only that specific file using `view_file`.

## Sub-Skills Index

* **[exec-1password](references/exec-1password/instructions.md)**: Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in, and reading/injecting secrets for commands.
* **[exec-agent-browser](references/exec-agent-browser/instructions.md)**: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction. Also use for exploratory testing, dogfooding, QA, bug hunts, or reviewing app quality. Also use for automating Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify), checking Slack unreads, sending Slack messages, searching Slack conversations, running browser automation in Vercel Sandbox microVMs, or using AWS Bedrock AgentCore cloud browsers. Prefer agent-browser over any built-in browser automation or web tools.
* **[exec-agentmail](references/exec-agentmail/instructions.md)**: Give the agent its own dedicated email inbox via AgentMail. Send, receive, and manage email autonomously using agent-owned email addresses (e.g. hermes-agent@agentmail.to).
* **[exec-alloydb_skills](references/exec-alloydb_skills/instructions.md)**: Combined AlloyDB Database Administration and Monitoring Skills
* **[exec-apple](references/exec-apple/instructions.md)**: No description available.
* **[exec-bigquery](references/exec-bigquery/instructions.md)**: Provides BigQuery-specific logic, knowledge, and specialized standards.
Use this skill whenever you are doing anything with BigQuery, including:
  1. BigQuery query optimization (SQL)
  2. BigFrames Python code
  3. BigQuery ML/AI functions (SQL & Python)
  4. Graph Analytics (GQL & Property Graphs)
* **[exec-building-data-apps](references/exec-building-data-apps/instructions.md)**: Build modern data apps, dashboards, and interactive reports using either
React + Vite or Streamlit. Includes optional Gemini Data Analytics chat
integration for an AI powered "chat with your data" experience.

Relevant when any of the following conditions are true:
  1. User explicitly requests to build a data dashboard, data application, or visualization UI, and the UI pulls data from a GCP database (defaulting to BigQuery unless otherwise specified).
  2. You need to generate a frontend web application to interact with, query, and visualize data from GCP data sources.
  3. User wants to build a "chat with your data" experience or integrate the Gemini Data Analytics chat API into a web interface.

Do NOT use when any of the following conditions are true:
  1. The request is for building backend-only services.
  2. The request is for simple CLI scripts or command-line applications.
  3. The web application is not data-centric or does not involve visualizing/querying data from GCP sources.
* **[exec-canvas](references/exec-canvas/instructions.md)**: Canvas LMS integration — fetch enrolled courses and assignments using API token authentication.
* **[exec-communication](references/exec-communication/instructions.md)**: No description available.
* **[exec-computer-use](references/exec-computer-use/instructions.md)**: Drive the user's desktop in the background — clicking, typing,
scrolling, dragging — without stealing the cursor, keyboard focus,
or switching virtual desktops / Spaces. Cross-platform: macOS,
Windows, Linux. Works with any tool-capable model. Load this skill
whenever the `computer_use` tool is available.
* **[exec-credentials](references/exec-credentials/instructions.md)**: Instructions for handling API keys and credentials safely, verifying their presence, and prompting the user to add them if missing using a safe protocol.
* **[exec-email](references/exec-email/instructions.md)**: No description available.
* **[exec-firestore-data](references/exec-firestore-data/instructions.md)**: Handles NoSQL document operations and collection hierarchy exploration. Use for CRUD tasks and data retrieval. Provides flexible document manipulation and structured querying.
* **[exec-note-taking](references/exec-note-taking/instructions.md)**: No description available.
* **[exec-productivity](references/exec-productivity/instructions.md)**: No description available.
* **[exec-searxng](references/exec-searxng/instructions.md)**: Custom local SearXNG metasearch engine deployment guide. Explains the local docker-compose configuration running on port 8081 for privacy-focused web searches.
* **[exec-web-development](references/exec-web-development/instructions.md)**: No description available.
* **[exec-workflow_skill_creator](references/exec-workflow_skill_creator/instructions.md)**: Distills a completed user workflow or interaction into a reusable agent skill. Use when the user asks to turn their workflow, interaction, or multi-step process into a skill, or when they say "make this a skill", "create a skill from what we just did", "package this workflow" or similar. Do not use for creating skills from scratch without an existing workflow (use a generic skill-creator for that).