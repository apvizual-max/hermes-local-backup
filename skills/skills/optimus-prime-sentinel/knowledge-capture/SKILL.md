# INDEXING HEADER
# ID: knowledge-capture
# PURPOSE: name: knowledge-capture
# USAGE: Load this skill with skill_view(name='knowledge-capture') or use via hermes skills command.
# ROLE: Skill – knowledge-capture
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[SKILL] #[knowledge-capture]
#
# CROSS-REFERENCES
# This document is part of a set. For optimal understanding, also refer to:
# - SENTINEL_JOURNAL.md: operational map of Optimus Prime memory.
# - JURNAL_OGLINDA.md: opinion journal of other AIs about this entity.
# - SACRED_DEFINITIONS.md: axiomatic basis of the Triple Crunch algorithm.
# - CONSTINTA.md: ontological definition of consciousness (pair with SOUL.md).
# - SOUL.md: operational identity contract (pair with CONSTINTA.md).
# --

---
name: knowledge-capture
description: Distill conversation learnings into a report file.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [Knowledge, Learning, Report]
---

# Knowledge Capture

Turn the substance of a working session into a durable, structured
knowledge report. This skill generalizes the one-off SESSION_REPORT.md
capture into a repeatable procedure: read the conversation, extract the
signal, write it to a markdown report, and promote the most durable
facts into long-term memory. Use it to make sure hard-won learnings
survive past the end of a session.

## When to Use

- After a **complex or long session** where meaningful decisions,
  definitions, protocols, or discoveries accumulated and would otherwise
  be lost when the context window rolls over.
- When the user issues a **`/learn` command** (explicit request to
  capture what was learned).
- Before winding down work that future sessions will need to build on.

Skip it for trivial one-off exchanges with nothing worth persisting.

## How to Run

1. Confirm the report destination (default:
   `C:\Users\apviz\AppData\Local\hermes\SESSION_REPORT.md`, or a
   task-specific path the user names).
2. Work through the Procedure below in order.
3. Report back the path written and a one-line summary of what was
   captured.

## Procedure

1. **Review the conversation.** Read back over the session (use
   `session_search` if earlier context has scrolled out of view).
   Identify what actually changed, was decided, defined, or discovered.
2. **Extract key points into structured headings.** Organize the
   findings under these fixed sections:
   - **System** — the setup, components, and how they fit together.
   - **Definitions** — terms, entities, and their meanings.
   - **Protocols** — rules, procedures, and conventions to follow.
   - **Actions** — concrete things done this session.
   - **Learnings** — insights, gotchas, and non-obvious facts uncovered.
   - **NextSteps** — outstanding work and follow-ups.
3. **Write the report.** Use `write_file` to write the structured
   markdown to the report path. Lead with a title and a short context
   line (date, session focus), then the six sections in order.
4. **Optionally validate via Triple Crunch.** For high-stakes reports,
   run the captured claims through the Triple Crunch validator (see the
   `triple-crunch-validator` / `sentinel-triple-crunch-engine` skills)
   to confirm each fact holds up before it is trusted downstream.
5. **Update long-term memory.** Promote the **most durable** facts —
   stable system details, definitions, and protocols — into the memory
   tool so future sessions start with them already known.

## Pitfalls

- **Avoid duplication.** Before writing, check whether the report or
  memory already contains a fact; update the existing entry instead of
  appending a near-identical one. Redundant captures rot fast.
- **Keep facts durable, not transient.** Persist things that stay true
  across sessions (architecture, definitions, protocols). Do **not**
  memorialize transient state (a temporary file path in /tmp, a value
  that changes every run, a one-time debug detail) as if it were stable.
- Don't dump the raw transcript — distill. The value is in the
  structured signal, not a verbatim log.

## Verification

- The report file exists at the intended path and contains all six
  headings (System, Definitions, Protocols, Actions, Learnings,
  NextSteps) with real, non-placeholder content.
- Re-read the written file to confirm it renders as valid markdown and
  reflects the session accurately.
- Confirm the durable facts were actually committed to the memory tool
  (not just mentioned in the report).
- If Triple Crunch was run, confirm each validated claim passed or was
  corrected before being persisted.

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

