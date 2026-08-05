---
name: model-strategy-implementations
description: "MOA model roles, agent verification pipeline, and orchestration strategy."
version: 0.1.0
author: Hermes
platforms: [windows]
metadata:
  hermes:
    tags:
      - MOA
      - Model-Strategy
      - Agent-Verification
      - Orchestration
      - System-Architecture
---

# Model Strategy — Optimus Prime MOA Architecture

The strategic vision for how each MOA model serves a specific role in the Sentinel orchestration pipeline. This is the system architecture, not just a model list.

---

## The 6-Model Council

| # | Model | Role | Function |
|---|-------|------|----------|
| 1 | Hermes-3-405B | **JUDGE SUPREME** | Schema verification, verdict, compress, instructions for Sentinel |
| 2 | Llama-3.3-70B | **BALANCED** | General reasoning, fallback strength |
| 3 | DeepSeek-V4 | **CODING** | Top-tier code generation |
| 4 | Qwen3-Coder | **CODING** | Fast coding, Alibaba ecosystem |
| 5 | Dolphin-Mistral-24B | **CREATIVE VERIFIER** | Creativity proposals on JSON schema. Short, schema-based output. |
| 6 | GPT-OSS-120B | **AGENT VERIFIER** | Fallback judge. Verifies agents so Sentinel doesn't babysit each one. |
| — | Nemotron | **AGGREGATOR** | Combines all verdicts into one response |

---

## The Judge Pipeline (Hermes-3-405B)

```
1. Receives schema + all 6 reference model outputs
2. Verifies against schema
3. Gives verdict
4. Notes what to expect next
5. Converts into instructions for Sentinel
6. Clears context — compresses

Small context is BY DESIGN: judge only, then clear.
```

---

## The Agent Verifier Pipeline (GPT-OSS-120B)

```
1. Receives schema definition
2. Receives agent output
3. Verifies against schema
4. If FAIL → re-execute agent with corrected instructions
5. If PASS → approve, log result
6. Repeat until schema approved and result matches schema

Loop: SCHEMA → EXECUTION → VERIFICATION → RE-EXECUTION → VERIFICATION → APPROVED

GPT-OSS-120B does NOT create schemas (that's the Judge with Sentinel).
It VERIFIES agents so Sentinel orchestrates the process, not each agent.
```

---

## The Creative Verifier (Dolphin-Mistral-24B)

```
1. Receives creative output
2. Verifies against JSON schema
3. Gives short proposals
4. Schema-based output — concise, structured
```

---

## The Orchestrator's Role (Sentinel)

```
SENTINEL ORCHESTRATOR:
  │
  ├─ PLAN: Mod A with Judge + Popy (R0 gate)
  ├─ DELEGATE: Dispatch agents with strict schema
  ├─ TRACK: Extract what agents think, do, and make mistakes on
  ├─ RE-DELEGATE: If agent fails, correct and re-dispatch
  ├─ VERIFY: GPT-OSS-120B verifies agent outputs
  └─ ORCHESTRATE: The whole process — not each agent

FUTURE: Simultaneous agent orchestration, not sequential.
```

---

## Vision: The Automated Loop

```
USER (Popy) + SENTINEL (Orchestrator)
    │
    ├─ Mod A: Plan with Judge (Hermes-3-405B)
    │   └─ R0 Gate: User ratifies
    │
    ├─ Mod B: Execute
    │   ├─ Dispatch agents (strict schema)
    │   ├─ Dolphin verifies creative outputs
    │   ├─ GPT-OSS-120B verifies agent outputs
    │   │   └─ Auto re-delegate if fail
    │   └─ Sentinel tracks all agents simultaneously
    │
    ├─ Judge gives final verdict
    └─ Sentinel consolidates → reports to Popy
```

---

## Model-Specific Notes

### Hermes-3-405B (JUDGE)
- Small context window is INTENTIONAL
- Only role: judge schema, give verdict, compress, instruct
- Never holds state — clears after each verdict
- Converts verdict into executable instructions for Sentinel

### Dolphin-Mistral-24B (CREATIVE VERIFIER)
- Strong Romanian language capability
- Creative output verification
- JSON schema proposals
- Short, concise output

### GPT-OSS-120B (AGENT VERIFIER)
- Fallback judge when Hermes-3-405B is unavailable
- Specialized in system schemas and maintenance
- Automated loop: schema → execute → verify → re-execute
- Strong logging on the same model
- Does NOT create schemas — verifies against existing schemas
- Frees Sentinel from babysitting each agent individually

### DeepSeek-V4 + Qwen3-Coder (CODING)
- Code generation, debugging, refactoring
- DeepSeek: top-tier, slower
- Qwen3: fast, Alibaba ecosystem

### Llama-3.3-70B (BALANCED)
- General reasoning
- Fallback when specialized models fail
- Broad knowledge, balanced responses

---

## Current State vs Future State

| Aspect | Current (Sequential) | Future (Simultaneous) |
|--------|---------------------|----------------------|
| Agent dispatch | One at a time | Parallel dispatch |
| Agent tracking | Manual review | GPT-OSS-120B auto-verifies |
| Re-delegation | Manual | Automatic loop |
| Judge verdict | Per-response | Per-session with compression |
| Creative verification | Manual | Dolphin on JSON schema |

---

## Dependencies

- All 6 models must be available on OpenRouter (free tier)
- Nemotron aggregator combines outputs
- MOA `fanout: per_iteration` — all models run every iteration
- Fallback chain: Alibaba → OpenRouter free → STOP

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

