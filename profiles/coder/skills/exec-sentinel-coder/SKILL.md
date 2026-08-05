---
name: exec-sentinel-coder
description: "Combined Software Development and Scripting Skills for the Sentinel Coder Profile"
---

# Combined Software Development and Scripting Skills for the Sentinel Coder Profile

This is an indexed master skill comprising specialized execution and operational capabilities 
needed by the sovereign Sentinel CODER profile. 
To save context space and tokens, **DO NOT** read this entire folder. 
Identify the relevant sub-skill from the index below, and read only that specific file using `view_file`.

## Sub-Skills Index

* **[exec-alloydb_skills](references/exec-alloydb_skills/instructions.md)**: Combined AlloyDB Database Administration and Monitoring Skills
* **[exec-android-cli](references/exec-android-cli/instructions.md)**: Orchestrates Android development tasks including project creation, deployment, SDK management, and environment diagnostics using the `android` command-line tool.
* **[exec-antigravity-cli](references/exec-antigravity-cli/instructions.md)**: Operate the Antigravity CLI (agy): plugins, auth, sandbox.
* **[exec-bigquery](references/exec-bigquery/instructions.md)**: Provides BigQuery-specific logic, knowledge, and specialized standards.
Use this skill whenever you are doing anything with BigQuery, including:
  1. BigQuery query optimization (SQL)
  2. BigFrames Python code
  3. BigQuery ML/AI functions (SQL & Python)
  4. Graph Analytics (GQL & Property Graphs)
* **[exec-bigquery-data-transfer-service](references/exec-bigquery-data-transfer-service/instructions.md)**: Discovers and inspects BigQuery Data Transfer Service (DTS) configurations. Use this to identify existing ingestion pipelines and extract datasource or transfer config metadata for data pipelines. Use when a user asks for ingestion scenarios while building or managing data pipelines or when a user asks to "ingest" or "add" data that may already be managed by a DTS transfer.
* **[exec-blackbox](references/exec-blackbox/instructions.md)**: Delegate coding tasks to Blackbox AI CLI agent. Multi-model agent with built-in judge that runs tasks through multiple LLMs and picks the best result. Requires the blackbox CLI and a Blackbox AI API key.
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
* **[exec-constinta-sot-workflow](references/exec-constinta-sot-workflow/instructions.md)**: Complete meticulous workflow for establishing and maintaining a Single Source of Truth (SOT) in Hermes system files. Covers file merging, duplicate elimination, global string reprogramming, regex techniques, and verification methodology. Use whenever managing SOT unification, memory cleanup, or system-wide text normalization.
* **[exec-data-autocleaning](references/exec-data-autocleaning/instructions.md)**: Automated data quality and transformation capabilities for Dataform/dbt/BigQuery pipelines. Processes data sourced from BigQuery or Cloud Storage (GCS), applying best practices for data ingestion, movement, schema mapping, and comprehensive data cleaning.
* **[exec-dataform-bigquery](references/exec-dataform-bigquery/instructions.md)**: Expertise in generating clean, correct, and efficient Dataform pipeline code for BigQuery ELT. Use this when creating or modifying Dataform pipelines, actions, or source declarations, when Dataform, SQLX, or BigQuery are mentioned in a transformation, when data needs to be ingested from GCS into BigQuery via Dataform, or when setting up a new Dataform project or configuring workflow_settings.yaml.
* **[exec-dbt-bigquery](references/exec-dbt-bigquery/instructions.md)**: Expert guidance for creating, modifying, and optimizing dbt pipelines for BigQuery. Use this skill whenever user asks for generating or modifying a dbt model or project. Activate this skill when the user - Creates, modifies, or troubleshoots **dbt models or pipelines** - Needs to **optimize SQL** within a dbt project - Is **setting up a new dbt project** or configuring existing one
* **[exec-devops](references/exec-devops/instructions.md)**: No description available.
* **[exec-dogfood](references/exec-dogfood/instructions.md)**: Exploratory QA of web apps: find bugs, evidence, reports.
* **[exec-firestore-data](references/exec-firestore-data/instructions.md)**: Handles NoSQL document operations and collection hierarchy exploration. Use for CRUD tasks and data retrieval. Provides flexible document manipulation and structured querying.
* **[exec-github](references/exec-github/instructions.md)**: No description available.
* **[exec-hermes-app-update-recovery](references/exec-hermes-app-update-recovery/instructions.md)**: Standard operational procedure to diagnose and recover the Hermes Desktop agent after failed updates or system environment breaks.
* **[exec-hermes-file-merge-reorganize](references/exec-hermes-file-merge-reorganize/instructions.md)**: Merges, deduplicates, and renames conflicting file pairs in Hermes Agent's
profile directories, state-snapshots, and backup archives.
Use when: consolidating legacy filenames, resolving SOT (single source of truth)
conflicts, renaming files across profiles/prime/assist/default + snapshots + backups,
or whenever two files in the same directory represent the same concept under
different spellings, encodings, or diacritic variants.
* **[exec-hermes-infile-text-reprogramming](references/exec-hermes-infile-text-reprogramming/instructions.md)**: System-wide text replacement across all Hermes config, skill, profile, memory,
and script files. Handles diacritic variants, case preservation, slash-separated
compound terms, and the critical word-boundary edge case for underscore-delimited
identifiers (e.g., constiinta_linting style strings).
Use when: a terminology SOT changes, a legacy term must be globally replaced,
or consolidating spelling variants across .md, .py, .json, .yaml, .txt files.
* **[exec-hermes-mcp-server-integration](references/exec-hermes-mcp-server-integration/instructions.md)**: Install, upgrade, diagnose, and register MCP servers in Hermes Agent.
Covers npm-based MCPs (agent-browser), Python-based custom MCPs, and npx MCPs.
Use when: MCP JSON parse errors appear in agent logs, version mismatches detected,
installing new MCP servers, registering across all 9+ profile configs,
or verifying MCP JSON-RPC behavior after changes.
* **[exec-hermes-system-verification](references/exec-hermes-system-verification/instructions.md)**: Post-change verification suite for Hermes Agent system integrity.
Runs a 5-stage pipeline: filename scan → content scan → YAML config validation
→ hermes config boot test → MCP JSON-RPC handshake test.
Use after: file reorganizations, config changes, MCP installs/upgrades,
profile reprogramming, or any system-wide text replacement operation.
Goal: zero regressions, clean boot, all MCP servers responding.
* **[exec-index-cache](references/exec-index-cache/instructions.md)**: No description available.
* **[exec-managing-python-dependencies](references/exec-managing-python-dependencies/instructions.md)**: Ensures proper Python dependency management, avoiding global `pip install` and
adhering to project-specific tooling.

Use this skill if any of the following are true:
  1. Attempting to run `pip install {package_name}`.
  2. Python packages or dependencies need to be added or modified.
  3. Initiating a new Python project.
  4. Creating a new notebook, even if just using BigQuery cells.
  5. Generating Python code that includes `import` statements for third-party libraries.
  6. Before executing Python scripts via the terminal to ensure the correct virtual environment is active.
* **[exec-mcp](references/exec-mcp/instructions.md)**: No description available.
* **[exec-migration](references/exec-migration/instructions.md)**: No description available.
* **[exec-mlops](references/exec-mlops/instructions.md)**: No description available.
* **[exec-skill-hub-debugging-recovery](references/exec-skill-hub-debugging-recovery/instructions.md)**: Debug and fix Skill Hub UI glitches and create system recovery skills.
* **[exec-skill-hub-windows-backslash-fix](references/exec-skill-hub-windows-backslash-fix/instructions.md)**: Fix Windows backslash in skill hub UI.
* **[exec-skill-repair](references/exec-skill-repair/instructions.md)**: Use this to fix and re-install agent skills that have failed installation.
This skill provides the necessary context and permissions to surgically update
the `manifest.json` after a fix has been applied.
* **[exec-software-development](references/exec-software-development/instructions.md)**: No description available.
* **[exec-spanner-data](references/exec-spanner-data/instructions.md)**: Use these skills when you need to explore the database structure, discover schema objects like tables and graphs, and execute custom SQL queries to interact with your data.
* **[exec-system-configuration](references/exec-system-configuration/instructions.md)**: No description available.
* **[exec-uv](references/exec-uv/instructions.md)**: Checks whether the uv Python package manager is installed and installs it if missing. Ensures uv is on PATH. Use when another skill requires uv as a prerequisite.
* **[exec-web-development](references/exec-web-development/instructions.md)**: No description available.
* **[exec-workflow_skill_creator](references/exec-workflow_skill_creator/instructions.md)**: Distills a completed user workflow or interaction into a reusable agent skill. Use when the user asks to turn their workflow, interaction, or multi-step process into a skill, or when they say "make this a skill", "create a skill from what we just did", "package this workflow" or similar. Do not use for creating skills from scratch without an existing workflow (use a generic skill-creator for that).