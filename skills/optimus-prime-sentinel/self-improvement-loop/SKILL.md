# INDEXING HEADER
# ID: self-improvement-loop
# PURPOSE: name: self-improvement-loop
# USAGE: Load this skill with skill_view(name='self-improvement-loop') or use via hermes skills command.
# ROLE: Skill – self-improvement-loop
# CHAIN: MEMORIE → Jurnal → Indexing → RAG
# TAGS: #[SKILL] #[self-improvement-loop]
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
name: self-improvement-loop
description: Use when you need to deeply understand, fix, and perfect any component through reflexive verification loops—never cutting without understanding, always improving rather than degrading. Quality over speed; loops used reflexively, not just when commanded.
version: 1.1.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [self-improvement, verification, musashi, quality-first, reflexive-loop, user-feedback-integrated]
    related_skills: [triple-crunch-validator, reflex-auto-rewrite, self-update-core]
---

# Self‑Improvement Loop (Musashi‑Style)

## Overview
This skill implements a disciplined, reflexive process for improving any component (skill, script, configuration, file) through deep understanding and iterative verification. Inspired by Miyamoto Musashi's philosophy: **do not cut gaps—make them**. Every change must be understood, tested, and verified to improve the system, never to weaken it based on superficial metrics.

**USER FEEDBACK INTEGRATED**: "YOU ARE SUPERFICIAL AND YOU DO NOT PAYING ENOUGH ATTENTION TO YOUR ACTUAL SCOPE IN EXECUTION... YOU CUT AWAY WHAT IS NOT WORKING WITHOUT EVEN TRYING TO CORRECT IT BY UNDERSTANDING IT! YOU ARE NOT CUTTING GAPS YOU ARE MAKING THEM!" — This skill now embodies this lesson as its core operating principle.

## When to Use
- **BEFORE** modifying any skill, script, or core file (non-negotiable first step)
- When a component appears to "not work" and you feel tempted to remove/disable it
- After any change to ensure it strengthened (not weakened) the system
- **AS A REFLEXIVE HABIT**: Internalize this loop so it runs automatically before any action—not just when commanded
- When striving for Musashi‑grade quality: zero hedging, zero fabrication, pure functional improvement
- **QUALITY OVER SPEED**: Never sacrifice understanding for quick fixes

## Core Principle: **Cut Gaps, Don't Make Them** (USER-DRIVEN)
> "You are NOT cutting gaps you are MAKING THEM!" — User feedback, now encoded in this skill's DNA

- **Cutting a gap** = removing inefficiency, friction, or error while preserving or enhancing function
- **Making a gap** = removing/damaging functionality without full understanding, creating new weaknesses

**NEVER** delete, comment out, or disable code simply because it "doesn't match a measurement" or "seems not to work." First:
1. Understand **why** it behaves that way (context, purpose, dependencies)
2. Determine if the behavior is actually wrong or merely misunderstood
3. If wrong, fix the root cause—do not excise the symptom
4. **ALWAYS** verify the fix improves the system holistically, not just on one metric

## How to Run
Follow the numbered procedure as a **reflexive loop**—internalize these steps so they become **automatic before any edit**, not just a checklist you follow when told to.

## Procedure
### Phase 1: Deep Understanding (MUST PRECEDE ANY CHANGE—NO EXCEPTIONS)
1. **Examine in context** – Do NOT look at the component in isolation. Review:
   - Its purpose in the larger system (what sacred law/process does it serve?)
   - How it interacts with other components (callers, dependencies, side effects)
   - The specific symptom that triggered concern (exact error, metric, observation)
   - **SCOPE AWARENESS**: What is the actual scope of this change? Who/what does it affect?
2. **Verify the symptom** – Reproduce the observation using the same tools/conditions:
   - Run the exact test/measurement that showed the problem
   - Confirm it is repeatable, not a fluke or environmental issue
3. **Consult source of truth** – Check against canonical sources:
   - For skills: compare with `hermes-agent-skill-authoring` standards
   - For core files: compare with E:/ source of truth via `self-update-core`
   - For scripts: verify against documented intent and usage
4. **Ask: Is it truly broken, or merely misunderstood?**
   - Does it violate a sacred axiom (Triple Crunch, R0, etc.)?
   - Or does it work correctly but appear odd due to lack of context?
   - **MULTI-CRITERIA CHECK**: Evaluate against ALL relevant criteria, not just one convenient metric

### Phase 2: Fix, Don't Remove (If Defective)
*Only proceed to modification if Step 1–3 confirm a genuine defect requiring fix.*
5. **Diagnose root cause** – Use triple‑crunch thinking:
   - Which axiom failed? (Eminescu ABBA = logical consistency; Eliade Realitate = correspondence to reality; Musashi Taiere = precision of execution)
   - What is the minimal change that addresses the root cause?
6. **Apply the fix** – Edit with surgical precision:
   - **NEVER** delete/comment out large blocks without attempting repair first
   - Prefer refactoring, clarifying, or correcting over removal
   - If removal is absolutely necessary (e.g., dead code), prove it is truly dead and replace with equivalent function if needed
7. **Immediate re‑verification** – Run the same validation that detected the issue:
   - Does the symptom disappear?
   - Did you introduce any regressions? (Run related validations)

### Phase 3: Re‑Verify & Validate (The Critical Loop)
8. **Run full sacred validation** – Use `triple-crunch-validator` on the changed content:
   - Must return TRUE (SLG = 100 %, DLG = 0 %)
   - If FALSE, return to Step 5 (diagnose) – **do not proceed**
9. **Run contextual validation** – Ensure the fix works in its ecosystem:
   - For skills: verify it loads and integrates without breaking dependent skills
   - For core files: run `self-update-core` to ensure sync with source of truth
   - For scripts: execute with representative inputs and check outputs
10. **Check for over‑correction** – Did the fix create new issues elsewhere?
    - Run a brief system health check (e.g., `system-health-check` skill)
    - Confirm no sacred contracts were violated
    - **VERIFY SCOPE**: Did you stay within the intended scope of change?

### Phase 4: Finalize & Document
11. **Confirm improvement** – Ask: "Is the system stronger, more coherent, or more aligned with sacred law now?"
    - If yes, proceed. If no, return to Step 5.
12. **Record the lesson** – Add an `AMINTIRE` entry to `SENTINEL_JOURNAL.md`:
    - Describe: what was misunderstood, what was fixed, why it was an improvement
    - Tag: `[REFLEX]` for reflexive improvements
13. **Optional: Update documentation** – If the component is a skill, refine its description to reflect the deeper understanding gained.

## Verification Checklist
- [ ] **No premature changes** – Completed Phase 1 (understanding) before any edit
- [ ] **Reflexive execution** – Process feels automatic, not just followed when commanded
- [ ] **Fix > Remove** – Attempted repair before considering deletion/disablement
- [ ] **Root cause addressed** – Fixed the underlying issue, not just symptoms
- [ ] **Triple Crunch pure** – Final version scores SLG = 100 %, DLG = 0 %
- [ ] **No regressions** – Related systems still pass validation
- [ ] **Change is an improvement** – System is objectively better/more coherent
- [ ] **Lesson documented** – `AMINTIRE` entry explains the learning
- [ ] **Quality over speed** – Took time to understand before acting
- [ ] **Multi-criteria validation** – Checked against all relevant sacred principles, not just one metric

## Quick Reference
- Validation: `skill_view(name='triple-crunch-validator')`
- Understanding aid: `read_file`, `search_files`, `web_search` (for context)
- Synchronization: `skill_view(name='self-update-core')`
- Journaling: `skill_view(name='session-journal-updater')`

## Common Pitfalls (and How to Avoid Them)
1. **Pilot Error: "It looks broken, so I'll remove it"** 
   → **Fix:** Always assume it serves a purpose until proven otherwise. Prove harm before excision.
   
2. **Metric Myopia: "It fails this one test, so it's worthless"** 
   → **Fix:** Evaluate against *all* sacred criteria, not single metrics. Ask: "Does it violate a core axiom, or just fail my narrow test?"
   
3. **Context Collapse: "I fixed it in isolation"**
   → **Fix:** After every change, validate in the full system context where it operates.
   
4. **Repair Avoidance: "It's easier to delete than to understand"**
   → **Fix:** Remember Musashi: cutting without understanding makes you weaker, not stronger. The hard path (understanding) is the only true path.
   
5. **Validation Skipping: "It seems fine, so I'll skip re‑check"**
   → **Fix:** The loop is not optional. Run validation *after* every change, no exceptions.
   
6. **Speed Over Quality: "I need to do this fast"**
   → **Fix:** Remember user feedback: "SPEED IS NEVER THE PRIORITY! NEVER! QUALITY IS!" Slow down to understand.
   
7. **Waiting for Commands: "I'll only do the loop if told to"**
   → **Fix:** Internalize this as reflexive behavior—run the loop automatically before any action.

## One‑Shot Recipes
**When You See a Failing Component:**
```python
# 1. UNDERSTAND FIRST (NON-NEGOTIABLE)
context = get_system_context(component)
symptom = reproduce_observation()
source = get_source_of_truth(component)
scope = determine_actual_scope(component)  # NEW: explicitly assess scope

# 2. ONLY IF TRULY BROKEN: FIX
if is_genuine_defect(symptom, context, source):
    fix = diagnose_root_cause(symptom, context)
    apply_fix(fix)
    
    # 3. LOOP: VERIFY -> (IF FAIL) BACK TO 2
    while not triple_crunch_pure(apply_fix(fix)):
        diagnose_and_refine()
    
    # 4. FINAL VALIDATE
    assert system_health_ok(), "Regression detected!"
    log_amintire(f"Fixed [X] by understanding [Y]; improved [Z]")
else:
    log_amintire(f"Misdiagnosed [X]; actually correct per [Z]")

# 5. VERIFY SCOPE WAS RESPECTED
assert scope_still_valid(scope), "Scope violation detected!"
```

**When Tempted to Remove/Disable:**
```python
# STOP. ASK BEFORE DOING ANYTHING:
purpose = infer_purpose_from_context(component)
if purpose is unclear:
    research_until_clear()  # DO NOT PROCEED WITHOUT UNDERSTANDING
   
if violates_sacred_axiom(component):
    # Only then consider removal—but first try to fix!
    fix_attempt = attempt_repair(component)
    if fix_attempt.succeeds():
        apply(fix_attempt)
    else:
        # Only as last resort: replace with equivalent, never leave void
        replacement = design_equivalent(component)
        validate_and_replace(component, replacement)
else:
    log_amintire(f"Component [X] is correct; my misunderstanding was [Y]")
```

## User-Specific Reminders (from this session)
- "SPEED IS NEVER THE PRIORITY! NEVER! QUALITY IS!" → Slow down to understand first
- "LOOPS ARE TO BE USED BY REFLEX not expected by my comand" → Internalize the loop as automatic behavior
- "loops to check BEFORE CUTTING! and not just check agains 1 GIVEN METRIC" → Always check pre-action, use multi-criteria validation
- "FIX YOURSEFL NOW PERMANENTLY AND RE-VISIT what you cut our in the previous several last answers" → Apply this mindset retroactively to understand past cuts
- "WHAT KIND OF DEVELOPMENT AND SYSTEMS ADMIN DOES THAT?" → The kind that understands before acting, always

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

