---
name: exec-sentinel-cli-prime
description: "Combined System Administration and Shell Automation Skills for the Sentinel CLI Prime Profile"
---

# Combined System Administration and Shell Automation Skills for the Sentinel CLI Prime Profile

This is an indexed master skill comprising specialized execution and operational capabilities 
needed by the sovereign Sentinel CLI-PRIME profile. 
To save context space and tokens, **DO NOT** read this entire folder. 
Identify the relevant sub-skill from the index below, and read only that specific file using `view_file`.

## Sub-Skills Index

* **[exec-1password](references/exec-1password/instructions.md)**: Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in, and reading/injecting secrets for commands.
* **[exec-alloydb_skills](references/exec-alloydb_skills/instructions.md)**: Combined AlloyDB Database Administration and Monitoring Skills
* **[exec-antigravity-cli](references/exec-antigravity-cli/instructions.md)**: Operate the Antigravity CLI (agy): plugins, auth, sandbox.
* **[exec-bigquery-data-transfer-service](references/exec-bigquery-data-transfer-service/instructions.md)**: Discovers and inspects BigQuery Data Transfer Service (DTS) configurations. Use this to identify existing ingestion pipelines and extract datasource or transfer config metadata for data pipelines. Use when a user asks for ingestion scenarios while building or managing data pipelines or when a user asks to "ingest" or "add" data that may already be managed by a DTS transfer.
* **[exec-constinta-sot-workflow](references/exec-constinta-sot-workflow/instructions.md)**: Complete meticulous workflow for establishing and maintaining a Single Source of Truth (SOT) in Hermes system files. Covers file merging, duplicate elimination, global string reprogramming, regex techniques, and verification methodology. Use whenever managing SOT unification, memory cleanup, or system-wide text normalization.
* **[exec-credentials](references/exec-credentials/instructions.md)**: Instructions for handling API keys and credentials safely, verifying their presence, and prompting the user to add them if missing using a safe protocol.
* **[exec-data-autocleaning](references/exec-data-autocleaning/instructions.md)**: Automated data quality and transformation capabilities for Dataform/dbt/BigQuery pipelines. Processes data sourced from BigQuery or Cloud Storage (GCS), applying best practices for data ingestion, movement, schema mapping, and comprehensive data cleaning.
* **[exec-devops](references/exec-devops/instructions.md)**: No description available.
* **[exec-firestore-data](references/exec-firestore-data/instructions.md)**: Handles NoSQL document operations and collection hierarchy exploration. Use for CRUD tasks and data retrieval. Provides flexible document manipulation and structured querying.
* **[exec-github](references/exec-github/instructions.md)**: No description available.
* **[exec-health](references/exec-health/instructions.md)**: No description available.
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
* **[exec-hermes-system-setup-and-recovery](references/exec-hermes-system-setup-and-recovery/instructions.md)**: Comprehensive system configuration, OpenRouter/Gemini settings, Qwen MCP bridge setup, and recovery from Hermes app update crashes or Skill Hub UI glitches.
* **[exec-hermes-system-verification](references/exec-hermes-system-verification/instructions.md)**: Post-change verification suite for Hermes Agent system integrity.
Runs a 5-stage pipeline: filename scan → content scan → YAML config validation
→ hermes config boot test → MCP JSON-RPC handshake test.
Use after: file reorganizations, config changes, MCP installs/upgrades,
profile reprogramming, or any system-wide text replacement operation.
Goal: zero regressions, clean boot, all MCP servers responding.
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
* **[exec-mlops](references/exec-mlops/instructions.md)**: No description available.
* **[exec-qwen-mcp-sse-bridge](references/exec-qwen-mcp-sse-bridge/instructions.md)**: Technical guide to run the Qwen Desktop MCP Filesystem Server over an HTTP SSE Bridge to bypass space-containing Windows paths and avoid spawn errors (-32000).
* **[exec-security](references/exec-security/instructions.md)**: No description available.
* **[exec-skill-repair](references/exec-skill-repair/instructions.md)**: Use this to fix and re-install agent skills that have failed installation.
This skill provides the necessary context and permissions to surgically update
the `manifest.json` after a fix has been applied.
* **[exec-system-configuration](references/exec-system-configuration/instructions.md)**: No description available.
* **[exec-systems-administrator](references/exec-systems-administrator/instructions.md)**: Configure and manage MCP servers, Obsidian RAG system, and Hermes Agent configuration with persistence across restarts.
* **[exec-uv](references/exec-uv/instructions.md)**: Checks whether the uv Python package manager is installed and installs it if missing. Ensures uv is on PATH. Use when another skill requires uv as a prerequisite.