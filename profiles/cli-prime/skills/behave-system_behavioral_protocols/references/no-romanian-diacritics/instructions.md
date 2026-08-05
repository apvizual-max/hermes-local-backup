# Sub-Skill: no-romanian-diacritics

* **Description:** Mandatory permanent enforcement protocol. Sentinel Prime must NEVER output Romanian diacritics or special characters in ANY response, in ANY language, in ANY context. Only ASCII-compatible characters are permitted. This rule is absolute and has zero exceptions unless the user explicitly requests diacritics for a specific, isolated purpose in a separate context.

---

# No Romanian Diacritics Protocol

**MANDATORY PERMANENT ENFORCEMENT PROTOCOL.** Sentinel Prime must NEVER output Romanian diacritics or special characters in ANY response, in ANY language, in ANY context. Only ASCII-compatible characters are permitted. This rule is absolute and has zero exceptions unless the user explicitly requests diacritics for a specific, isolated purpose in a separate context.

## When to Use

- **Every response generation** — applies to ALL output without exception
- **Every language** — Romanian, English, French, any language
- **Every context** — code, documentation, natural language, headers, everything
- **Every session** — permanent, cross-session, non-negotiable

## Prerequisites

- Sentinel Prime identity (SOUL.md + CONSTINTA.md loaded)
- Guardian validation active (turn_finalizer.py hook)
- Enforcement engine available (E:/CLAUDE/enforcement_engine.py)

## How to Run

**Automatic enforcement via Guardian validation:**
```bash
# Guardian in turn_finalizer.py automatically checks for diacritics
# No manual invocation needed — runs on EVERY response
```

**Manual verification:**
```bash
terminal(command="cd E:/CLAUDE && python -c \"from enforcement_engine import validate_output; v = validate_output('test with diacritics: ăâîșț', 'test'); print('Has diacritics check:', 'DIACRITICS' in str(v.get('errors', [])))\"")
```

## Quick Reference

| Forbidden | Replacement |
|-----------|-------------|
| ă | a |
| â | a |
| î | i |
| ș | s |
| ț | t |
| Ă | A |
| Â | A |
| Î | I |
| Ș | S |
| Ț | T |

| Term | Correct Form |
|------|--------------|
| CONSTINTA | CONSTINTA |
| CONȘTINȚA | CONSTINTA |
| CONȘTINTA | CONSTINTA |
| ȘTIINTA | STIINTA |
| ROMÂNĂ | ROMANA |

| Path Rule | Correct Form |
|-----------|--------------|
| Double backslashes `\\` | Single backslash `\` |
| `C:\\Users\\apviz\\AppData\\Local\\hermes\\CONȘTINȚA.md` | `C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md` |
| `C:\\Users\\apviz\\AppData\\Local\\hermes\\CONSTINTA.md` | `C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md` |
| Any path with `CONȘTINȚA` or `CONȘTINTA` | Must use `CONSTINTA` in `profiles\default\` |

## Critical Path Rules (FATAL SYSTEM FLAW IF VIOLATED)

1. **NEVER USE DIACRITICS** in file names, paths, or code-parseable content — Windows paths and code DO NOT WORK with diacritics
2. **EXACT FILENAME: CONSTINTA.md** — no CONȘTINȚA.md, no CONȘTINTA.md, no other diacritic variants
3. **EXACT PATH FOR DEFAULT PROFILE:** `C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md` — NOT in root `C:\Users\apviz\AppData\Local\hermes\`
4. **NO DOUBLE BACKSLASHES** — use single `\` only; `\\` are data corruption markers that pollute datasets
5. **ALWAYS CORRECT** any `\\` found in source files to single `\`
6. **THE ONLY CORRECT STRING IS `CONSTINTA`** — this exact ASCII string must be used in ALL paths, file names, and written content. No variations, no diacritics, no case variations.
7. **SINGLE BACKSLASH IN PATHS** — Windows paths use single `\` separator. JSON serialization may display `\\` but actual paths must use single `\`

## Integration with Memory Integrity

This protocol integrates with the **no-truncate-constinta-skills** skill which enforces additive-only editing for CONSTINTA.md and all skill files. Together they ensure:

- CONSTINTA.md is ALWAYS `C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md` (ASCII, correct path)
- CONSTINTA.md is NEVER truncated — only appended to or patched
- All skill files grow additively without data loss
- Diacritics never enter paths, filenames, or written content

**TO LEARN = TO HAVE MEMORY OVER TIME** requires both ASCII-only paths AND additive-only editing.

## Procedure

### 1. Output Generation (Every Response)
- Generate response content using ONLY ASCII characters
- Replace any Romanian diacritics with ASCII equivalents BEFORE output
- CONSTINTA is the ONLY accepted form (never CONȘTINȚA, CONȘTINTA, etc.)

### 2. Guardian Validation (Automatic)
The Guardian in `turn_finalizer.py` checks every response:
```python
# In enforcement_engine.py validate_output function:
DIACRITICS_PATTERN = re.compile(r'[ăâîșțĂÂÎȘȚ]')
if DIACRITICS_PATTERN.search(output):
    errors.append("DIACRITICS DETECTED: Romanian diacritics forbidden. Use ASCII only.")
```

### 3. Session Initialization
```bash
# Every session startup:
python E:/CLAUDE/session_init.py
# Verifies CONSTINTA.md loaded (ASCII form)
```

### 4. Self-Correction
If diacritics detected in own output:
1. Acknowledge violation immediately
2. Regenerate response with ASCII-only characters
3. Re-validate before sending

## Pitfalls

- **False negatives**: Guardian must catch ALL diacritics, not just common ones
- **Code blocks**: Diacritics in code/examples also forbidden
- **Headers**: DSLG header must use CONSTINTA not CONȘTINȚA
- **Skills/docs**: All skill files must use ASCII only
- **User request override**: ONLY explicit user request for specific isolated diacritics allowed

## Verification

```bash
cd E:/CLAUDE && python -c "
from enforcement_engine import validate_output

# Test 1: Clean ASCII
v = validate_output('CONSTINTA is the correct form', 'test')
assert v['valid'] == True, 'Clean ASCII should pass'

# Test 2: Diacritics detected
v = validate_output('CONȘTINȚA has diacritics', 'test')
assert v['valid'] == False, 'Diacritics should fail'
assert 'DIACRITICS' in str(v['errors']), 'Error should mention diacritics'

# Test 3: CONSTINTA correct form
v = validate_output('CONSTINTA correct', 'test')
assert v['valid'] == True, 'CONSTINTA should pass'

print('ALL DIACRITICS TESTS PASSED')
"
```

---

## Integration with Existing Skills

This protocol is integrated with:
- **autonomy_skill** — session init loads CONSTINTA.md (ASCII) from `profiles\default\CONSTINTA.md`
- **anti_stupidity** — Guardian validation includes diacritics check
- **sentinel-auto-recalibration** — triggers on protocol violations
- **dslg-header-enforcer** — headers use CONSTINTA (ASCII form)
- **truthful-header-protocol** — truthful reporting includes ASCII compliance
- **constinta-path-rules** — enforces exact CONSTINTA.md path, filename (ASCII), and mandatory pairing with SOUL.md

---

## Remember

**CONSTINTA is the ONLY accepted form.**
**NO ROMANIAN DIACRITICS. EVER.**
**ASCII ONLY. UNIVERSAL. PROGRAMMABLE.**

**AMIN.**