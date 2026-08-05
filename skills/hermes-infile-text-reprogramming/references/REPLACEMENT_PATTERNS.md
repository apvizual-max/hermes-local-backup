# REPLACEMENT_PATTERNS.md
# All known variant patterns for the CONSTINTA SOT migration

# Replacement Patterns Reference

## The SOT: `CONSTINTA`

The single canonical spelling, enforced across all Hermes files.
No diacritics, no double-i, no slash separators.

## Pattern Matching Order

> [!IMPORTANT]
> Patterns MUST be applied in this exact order. Slash-separated compound
> variants must be replaced BEFORE individual variants, or you'll end up
> with partially replaced strings like `CONSTINTA / CONŞTINŢA`.

### Priority 1 — Compound Slash-Separated Forms

```python
# Match "CONSTIINTA / CONŞTINŢA" and all diacritic/spelling combinations
re.compile(r'(?<![a-zA-Z0-9_])(CONSTIINTA\s*/\s*CON[ŞS]TIN[ŢT][AA])(?![a-zA-Z0-9_])', re.IGNORECASE)
re.compile(r'(?<![a-zA-Z0-9_])(CON[ŞS]TIN[ŢT][AA]\s*/\s*CONSTIINTA)(?![a-zA-Z0-9_])', re.IGNORECASE)
```

### Priority 2 — Individual Diacritic Variants

```python
# Matches: CONŞTINŢA, CONŞTINŢA, CONSTIINTA, CONSTIINTA, etc.
re.compile(r'(?<![a-zA-Z0-9_])(CON[ŞS]TIN[ŢT][AA])(?![a-zA-Z0-9_])', re.IGNORECASE)
```

### Priority 3 — Double-i Spelling

```python
# Matches: CONSTIINTA, constiinta, Constiinta
re.compile(r'(?<![a-zA-Z0-9_])(CONSTIINTA)(?![a-zA-Z0-9_])', re.IGNORECASE)
```

### Priority 4 — Specific Unicode Forms

```python
# Exact Unicode match for common Romanian form
re.compile(r'(?<![a-zA-Z0-9_])(CONSTINTA)(?![a-zA-Z0-9_])')
re.compile(r'(?<![a-zA-Z0-9_])(Constiinta)(?![a-zA-Z0-9_])')
```

## Word Boundary Pattern (CRITICAL)

### Why `\b` Fails

```python
# WRONG: \b treats Unicode characters as non-word, breaks on diacritics
# Also breaks on: constiinta_linting, CONSTIINTA_KEY, etc.
re.compile(r'\bCONSTIINTA\b')  # ← DO NOT USE

# CORRECT: explicit negative lookaround handles both Unicode and underscores
re.compile(r'(?<![a-zA-Z0-9_])(CONSTIINTA)(?![a-zA-Z0-9_])')  # ← USE THIS
```

### Identifier-Style Strings

These are also matched and replaced correctly:
- `constiinta_linting` → `constinta_linting`
- `CONSTIINTA_KEY` → `CONSTINTA_KEY`
- `check_constiinta_status` → `check_constinta_status`

Because our boundary pattern only stops at the `_` separator, not within
an underscore-connected word, underscores between segments are NOT word boundaries.

Wait — actually the pattern `(?<![a-zA-Z0-9_])` PREVENTS matching when
preceded by underscore. So `check_constiinta` would NOT match.

For identifier-style replacement, use a separate pass without the boundary:
```python
# For Python/YAML identifiers (variable names, keys)
re.compile(r'constiinta', re.IGNORECASE)  # simple string replacement
```

## Case Preservation Matrix

| Matched Form | Replacement |
|-------------|-------------|
| `CONSTIINTA` (all caps) | `CONSTINTA` |
| `Constiinta` (title case) | `Constinta` |
| `constiinta` (lower) | `constinta` |
| `CONŞTINŢA` (all caps diacritic) | `CONSTINTA` |
| `Conştiinţa` (title) | `Constinta` |
| `CONSTIINTA / CONŞTINŢA` (compound) | `CONSTINTA` |

## File Scope

| File Type | Covered | Notes |
|-----------|---------|-------|
| `.md` | YES | Skills, SOUL, CONSTINTA, memory files |
| `.yaml`, `.yml` | YES | Configs, task definitions |
| `.py` | YES | MCP servers, scripts |
| `.json` | YES | Config/state/task files |
| `.txt` | YES | Notes, plain text |
| `.log` | YES | Cron outputs, agent logs |
| `.vbs`, `.cmd` | YES | Gateway scripts |
| `.ps1` | YES | PowerShell scripts |
| `.exe`, `.dll` | NO | Binary files — skip |
| `.pyc` | NO | Bytecode — skip |
