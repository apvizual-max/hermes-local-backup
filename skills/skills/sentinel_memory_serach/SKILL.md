---
name: sentinel_memory_serach
description: Combined Semantic Memory and Elasticsearch Search Assistant Prompts
---

# Skill Bundle: Sentinel Memory Search

This skill bundle manages semantic memory indexing and incorporates the Elastic Search Labs prompt library to help agents perform discovery, evaluation, policy generation, and context search.

## Zonal Boundaries
The Thoth Function indexes local storage within the following boundaries:
* **Zone C:\ (System Root)**: Readable configurations, logs, and text-based system states.
* **Zone E:\ (Operational Center)**: Core logic substrate and knowledge vault.
* **Zone D:\ (Data Repository)**: Full semantic data indexing.

## Table of Contents

### Core Prompts
1. [Technical Discovery Assistant](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/technical-discovery-assistant/instructions.md)
2. [Security Policy Generator](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/security-policy-generator/instructions.md)
3. [Negotiation Assistant](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/negotiation-assistant/instructions.md)
4. [Meeting Summary Assistant](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/meeting-summary-assistant/instructions.md)
5. [Generate Test Cases For Evaluation](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/generate-test-cases-for-evaluation/instructions.md)
6. [Generate Seed Indices For Evaluation Data](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/generate-seed-indices-for-evaluation-data/instructions.md)
7. [Expand Evaluation Dataset From Seed Indices](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/expand-evaluation-dataset-from-seed-indices/instructions.md)
8. [Ciso Incident Summary](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/ciso-incident-summary/instructions.md)
9. [Asset Inventory Diagrams](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/asset-inventory-diagrams/instructions.md)
10. [Analyzing Soc Security Case](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/references/analyzing-soc-security-case/instructions.md)

## Ingestion Script
* **[Thoth Ingestion Crawler](file:///C:/Users/apviz/.gemini/skills/sentinel_memory_serach/scripts/thoth_ingest.py)**: Index local files into Elasticsearch.

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

