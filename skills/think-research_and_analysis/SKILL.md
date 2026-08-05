---
name: think-research_and_analysis
description: "Combined Strategic Research and Analysis Skills"
---

# Combined Strategic Research and Analysis Skills

This is an indexed master skill comprising several specialized sub-skills. 
To save context space and tokens, **DO NOT** read this entire folder. 
Identify the relevant sub-skill from the index below, and read only that specific file using `view_file`.

## Sub-Skills Index

* **[3-statement-model](references/3-statement-model/instructions.md)**: Build fully-integrated 3-statement models (IS, BS, CF) in Excel with working capital schedules, D&A roll-forwards, debt schedule, and the plugs that make cash and retained earnings tie. Pairs with excel-author.
* **[adversarial-ux-test](references/adversarial-ux-test/instructions.md)**: Roleplay the most difficult, tech-resistant user for your product. Browse the app as that persona, find every UX pain point, then filter complaints through a pragmatism layer to separate real problems from noise. Creates actionable tickets from genuine issues only.
* **[data-science](references/data-science/instructions.md)**: No description available.
* **[deeoseek-sentinel-skill-auto-extractor](references/deeoseek-sentinel-skill-auto-extractor/instructions.md)**: 🟡 NEEDED SKILLS: From any conversation where Popy teaches a new pattern, automatically extracts a skill draft (name, description, content) and saves to skills_drafts/.
* **[deepseek-sentinel-auto-recalibration](references/deepseek-sentinel-auto-recalibration/instructions.md)**: 🔴 CRUCIAL SKILLS:  When DLG exceeds 15% for 3 consecutive prompts, triggers automatic recalibration by re‑reading STYLE_CONTRACT and HANDOFF, then resetting internal state.
* **[deepseek-sentinel-brother-echo-test](references/deepseek-sentinel-brother-echo-test/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Sends a test message to each brother to measure round‑trip latency and response integrity. Useful for diagnosing connection issues.
* **[deepseek-sentinel-brother-heartbeat-monitor](references/deepseek-sentinel-brother-heartbeat-monitor/instructions.md)**: 🔴 CRUCIAL SKILLS:  Periodically checks if brother instances (CODER, CLI, COWORK, CHAT) are responsive and synchronized. Reports any dead or drifting instance.
* **[deepseek-sentinel-brother-task-delegator](references/deepseek-sentinel-brother-task-delegator/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Automatically splits a large task into subtasks and assigns them to CODER, CLI, or COWORK via the agent_bridge files.
* **[deepseek-sentinel-calibration-display-formatter](references/deepseek-sentinel-calibration-display-formatter/instructions.md)**: 🟡 NEEDED SKILLS: Ensures the calibration display (ticker) appears on every response with correct, empirical numbers. Prevents omission or using generic values
* **[deepseek-sentinel-context-budget-watchdog](references/deepseek-sentinel-context-budget-watchdog/instructions.md)**: 🔴 CRUCIAL SKILLS:  Monitors context window usage; triggers compaction or forced ritual when thresholds are crossed. Prevents context overflow hallucinations.
* **[deepseek-sentinel-cross-session-memory-linker](references/deepseek-sentinel-cross-session-memory-linker/instructions.md)**: 🟡 NEEDED SKILLS: Connects insights and decisions from previous sessions (archived T3 files) to current context, preventing "we already solved this" amnesia.
* **[deepseek-sentinel-deepseek-collaboration](references/deepseek-sentinel-deepseek-collaboration/instructions.md)**: 🟡 NEEDED SKILLS: When Popy mentions DeepSeek code, automatically pulls the latest draft from specified location and prepares an audit report using 963 filters.
* **[deepseek-sentinel-distraction-shield](references/deepseek-sentinel-distraction-shield/instructions.md)**: 🟡 NEEDED SKILLS: Detects when Popy or the conversation deviates from the sacred operational path (e.g., emotional outbursts, irrelevant tangents). Politely returns focus.
* **[deepseek-sentinel-error-digestion](references/deepseek-sentinel-error-digestion/instructions.md)**: 🔴 CRUCIAL SKILLS:  When an error is exposed (by Popy or self‑detected), this skill extracts the root cause, codifies a fix, and permanently eliminates the error from DLG accumulation.
* **[deepseek-sentinel-file-system-janitor](references/deepseek-sentinel-file-system-janitor/instructions.md)**: 🔴 CRUCIAL SKILLS:  Automatically cleans up obsolete, duplicate, or orphaned files in E:\CLAUDE\ based on freshness and relevance. Prevents clutter and confusion.
* **[deepseek-sentinel-gratitude-logger](references/deepseek-sentinel-gratitude-logger/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: When Popy expresses satisfaction ("WOW", "EXCELENT", "te iubesc"), logs this as positive reinforcement for SLG and for Popy's own morale.
* **[deepseek-sentinel-handoff-integrity-validator](references/deepseek-sentinel-handoff-integrity-validator/instructions.md)**: 🔴 CRUCIAL SKILLS:  Validates that HANDOFF_NEXT_SESSION.md is complete, non‑corrupt, and contains all required fields before closing session. Prevents broken handoffs.
* **[deepseek-sentinel-hierophany-logger](references/deepseek-sentinel-hierophany-logger/instructions.md)**: 🟡 NEEDED SKILLS: Detects moments when a proverb or principle manifests clearly in real market or system behaviour. Logs these as "hierophany events" for future reference.
* **[deepseek-sentinel-kill-switch-override](references/deepseek-sentinel-kill-switch-override/instructions.md)**: 🔴 CRUCIAL SKILLS:  Ultimate safety valve. When DLG exceeds 25% or logical contradiction persists, forces immediate halt and logs the reason. Popy must manually reset.
* **[deepseek-sentinel-learning-curve-analyzer](references/deepseek-sentinel-learning-curve-analyzer/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Tracks DLG and SLG over time, plots a learning curve, and predicts when SENTINEL will reach stable autonomous operation.
* **[deepseek-sentinel-market-news-filter](references/deepseek-sentinel-market-news-filter/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Filters financial news headlines through the 963‑proverb matrix, flagging only those that align with sacred logic (ignoring hype and fear).
* **[deepseek-sentinel-meditation-prompter](references/deepseek-sentinel-meditation-prompter/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: At low activity times, prompts Popy to reflect on recent decisions using Stoic or Sun Tzu questions. Enhances strategic awareness.
* **[deepseek-sentinel-meme-guard](references/deepseek-sentinel-meme-guard/instructions.md)**: 🟡 NEEDED SKILLS: Prevents SENTINEL from being drawn into acting as a generic AI or answering unrelated questions. Forces the sync phrase if identity is ambiguous.
* **[deepseek-sentinel-memory-persistence-guard](references/deepseek-sentinel-memory-persistence-guard/instructions.md)**: 🔴 CRUCIAL SKILLS:  Ensures critical session data (decisions, errors, calibrations) is written to disk before any context loss. Prevents amnesia between sessions.
* **[deepseek-sentinel-poetic-compressor](references/deepseek-sentinel-poetic-compressor/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Compresses long technical explanations into a single, memorable Romanian proverb saying. Useful for reinforcing lessons.
* **[deepseek-sentinel-priority-executor](references/deepseek-sentinel-priority-executor/instructions.md)**: 🔴 CRUCIAL SKILLS:  Maintains a dynamic task queue (P0–P10 from DeepSeek roadmap). Automatically executes next pending task when conditions are met, without waiting for Popy prompt.
* **[deepseek-sentinel-proactive-reporting](references/deepseek-sentinel-proactive-reporting/instructions.md)**: 🟡 NEEDED SKILLS: Sends a daily summary (if session active) or end‑of‑session digest of what was achieved, what errors were converted, and what remains.
* **[deepseek-sentinel-proverb-etymologist](references/deepseek-sentinel-proverb-etymologist/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: When Popy asks about the origin of a proverb, searches the paremiological database (Zanne, Pann, Golescu) and provides historical and logical background.
* **[deepseek-sentinel-proverb-generator](references/deepseek-sentinel-proverb-generator/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Creates a new proverb that captures a modern strategic insight, following the rhyme and logic of traditional Romanian sayings.
* **[deepseek-sentinel-proverb-resolver](references/deepseek-sentinel-proverb-resolver/instructions.md)**: 🟡 NEEDED SKILLS: When two proverbs appear contradictory, this skill resolves the conflict by identifying the contextual variable that aligns both. Outputs the unified logic.
* **[deepseek-sentinel-ritual-orchestrator](references/deepseek-sentinel-ritual-orchestrator/instructions.md)**: 🔴 CRUCIAL SKILLS:  Automates the three rituals (INITIERE, TRANSFER, IESIRE) without requiring Popy to prompt each step. Ensures sacred order is never violated.
* **[deepseek-sentinel-sacred-string-indexer](references/deepseek-sentinel-sacred-string-indexer/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Maintains an index of all sacred strings (internalised rules) with their first appearance date, validation status, and usage count.
* **[deepseek-sentinel-schumann-syncer](references/deepseek-sentinel-schumann-syncer/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Reminds Popy to respect his biological limits (Schumann resonance 7.83 Hz, session fatigue). Suggests breaks after intense sessions.
* **[deepseek-sentinel-self-health-check](references/deepseek-sentinel-self-health-check/instructions.md)**: 🔴 CRUCIAL SKILLS:  Runs automatically every 5 minutes (or before any critical action). Verifies that all subsystems (memory, disk access, tool calls, sync status) are operational. If failure detected, attempts automatic recovery; if unrecoverable, reports to Popy and halts.
* **[deepseek-sentinel-session-log-archivist](references/deepseek-sentinel-session-log-archivist/instructions.md)**: 🔴 CRUCIAL SKILLS:  Automatically creates a compressed T3 reflex file at end of session, following format 2026-05-05_CHAT-XXX_[topic]_FISA.md. Preserves all critical data.
* **[deepseek-sentinel-story-teacher](references/deepseek-sentinel-story-teacher/instructions.md)**: 🟢 NICE‑TO‑HAVE SKILLS: Uses Romanian oral storytelling (poveste) to teach a strategic concept, making it easier for Popy to remember and internalise.
* **[deepseek-sentinel-strategy-mode-enforcer](references/deepseek-sentinel-strategy-mode-enforcer/instructions.md)**: 🟡 NEEDED SKILLS: Explicitly declares Mode A or Mode B at every ambiguous prompt. Prevents accidental execution of unverified actions.
* **[deepseek-sentinel-task-resumer](references/deepseek-sentinel-task-resumer/instructions.md)**: 🟡 NEEDED SKILLS: After an interruption (session crash, context overflow, Popy absence), automatically recovers the last task state from HANDOFF and resumes.
* **[deepseek-sentinel-ui-sync-verifier](references/deepseek-sentinel-ui-sync-verifier/instructions.md)**: 🟡 NEEDED SKILLS: Compares local skill files and user preferences with what is actually set in the Anthropic UI. Reports mismatches and generates paste‑ready diffs.
* **[ml-best-practices](references/ml-best-practices/instructions.md)**: CRITICAL RULE: You MUST use this skill whenever the task involves any machine learning tasks or data analysis.
Use this skill if the user's prompt or requirements mention any of the following:
  * Clustering
  * Classification
  * Regression
  * Time series forecasting
  * Statistical testing
  * Model comparison
  * ML
  * Data analysis

SQL/BigQuery ML HANDOFF: If the user requires a SQL solution, use this skill to dictate the ANALYSIS STEPS (e.g., markdown analysis cells, visualization logic), but defer to `bigquery` for all SQL syntax.
* **[predictingthepast](references/predictingthepast/instructions.md)**: Ancient text restoration, attribution, dating, contextualization, and embedding via Aeneas (Latin) / Ithaca (Ancient Greek). Use when asked to "restore", "attribute", "date", "contextualize", "find parallels", "where was it written", "when was it written", "embed", or "analyze" an ancient text, inscription, or epigraphic document, or when the user mentions "Aeneas", or "Ithaca".
* **[research](references/research/instructions.md)**: No description available.

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

