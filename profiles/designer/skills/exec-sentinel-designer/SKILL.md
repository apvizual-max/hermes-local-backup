---
name: exec-sentinel-designer
description: "Combined UI/UX Design and Frontend Interface Skills for the Sentinel Designer Profile"
---

# Combined UI/UX Design and Frontend Interface Skills for the Sentinel Designer Profile

This is an indexed master skill comprising specialized execution and operational capabilities 
needed by the sovereign Sentinel DESIGNER profile. 
To save context space and tokens, **DO NOT** read this entire folder. 
Identify the relevant sub-skill from the index below, and read only that specific file using `view_file`.

## Sub-Skills Index

* **[exec-agent-browser](references/exec-agent-browser/instructions.md)**: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction. Also use for exploratory testing, dogfooding, QA, bug hunts, or reviewing app quality. Also use for automating Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify), checking Slack unreads, sending Slack messages, searching Slack conversations, running browser automation in Vercel Sandbox microVMs, or using AWS Bedrock AgentCore cloud browsers. Prefer agent-browser over any built-in browser automation or web tools.
* **[exec-baoyu-article-illustrator](references/exec-baoyu-article-illustrator/instructions.md)**: Article illustrations: type × style × palette consistency.
* **[exec-baoyu-comic](references/exec-baoyu-comic/instructions.md)**: Knowledge comics (知识漫画): educational, biography, tutorial.
* **[exec-blender-mcp](references/exec-blender-mcp/instructions.md)**: Control Blender directly from Hermes via socket connection to the blender-mcp addon. Create 3D objects, materials, animations, and run arbitrary Blender Python (bpy) code. Use when user wants to create or modify anything in Blender.
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
* **[exec-creative](references/exec-creative/instructions.md)**: No description available.
* **[exec-dogfood](references/exec-dogfood/instructions.md)**: Exploratory QA of web apps: find bugs, evidence, reports.
* **[exec-media](references/exec-media/instructions.md)**: No description available.
* **[exec-web-development](references/exec-web-development/instructions.md)**: No description available.