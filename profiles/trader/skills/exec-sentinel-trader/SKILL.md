---
name: exec-sentinel-trader
description: "Combined Financial Management and Risk Analysis Skills for the Sentinel Trader Profile"
---

# Combined Financial Management and Risk Analysis Skills for the Sentinel Trader Profile

This is an indexed master skill comprising specialized execution and operational capabilities 
needed by the sovereign Sentinel TRADER profile. 
To save context space and tokens, **DO NOT** read this entire folder. 
Identify the relevant sub-skill from the index below, and read only that specific file using `view_file`.

## Sub-Skills Index

* **[exec-bigquery](references/exec-bigquery/instructions.md)**: Provides BigQuery-specific logic, knowledge, and specialized standards.
Use this skill whenever you are doing anything with BigQuery, including:
  1. BigQuery query optimization (SQL)
  2. BigFrames Python code
  3. BigQuery ML/AI functions (SQL & Python)
  4. Graph Analytics (GQL & Property Graphs)
* **[exec-bigquery-data-transfer-service](references/exec-bigquery-data-transfer-service/instructions.md)**: Discovers and inspects BigQuery Data Transfer Service (DTS) configurations. Use this to identify existing ingestion pipelines and extract datasource or transfer config metadata for data pipelines. Use when a user asks for ingestion scenarios while building or managing data pipelines or when a user asks to "ingest" or "add" data that may already be managed by a DTS transfer.
* **[exec-blockchain](references/exec-blockchain/instructions.md)**: No description available.
* **[exec-dbt-bigquery](references/exec-dbt-bigquery/instructions.md)**: Expert guidance for creating, modifying, and optimizing dbt pipelines for BigQuery. Use this skill whenever user asks for generating or modifying a dbt model or project. Activate this skill when the user - Creates, modifies, or troubleshoots **dbt models or pipelines** - Needs to **optimize SQL** within a dbt project - Is **setting up a new dbt project** or configuring existing one
* **[exec-finance](references/exec-finance/instructions.md)**: No description available.
* **[exec-firestore-data](references/exec-firestore-data/instructions.md)**: Handles NoSQL document operations and collection hierarchy exploration. Use for CRUD tasks and data retrieval. Provides flexible document manipulation and structured querying.
* **[exec-payments](references/exec-payments/instructions.md)**: No description available.
* **[exec-searxng](references/exec-searxng/instructions.md)**: Custom local SearXNG metasearch engine deployment guide. Explains the local docker-compose configuration running on port 8081 for privacy-focused web searches.