# CASE_LOGIC.md
# Rules for case-preserving text replacement

# Case Preservation Rules

## Why Case Matters

When replacing `CONSTIINTA` with `CONSTINTA`, we must preserve the original
capitalization so that replaced text looks natural in its context.

## Case Detection Logic

```python
def preserve_case(match_text: str, replacement: str) -> str:
    """Return replacement with same case profile as match_text."""
    
    if match_text.isupper():
        # ALL CAPS: CONSTIINTA → CONSTINTA
        return replacement.upper()
    
    elif match_text[0].isupper() and match_text[1:].islower():
        # Title Case: Constiinta → Constinta
        return replacement.capitalize()
    
    elif match_text.islower():
        # all lower: constiinta → constinta
        return replacement.lower()
    
    else:
        # Mixed/special (e.g., cONSTIINTA, CONSTIINTA_key) → use canonical as-is
        return replacement
```

## Case Matrix

| Input | Output |
|-------|--------|
| `CONSTIINTA` | `CONSTINTA` |
| `Constiinta` | `Constinta` |
| `constiinta` | `constinta` |
| `CONŞTINŢA` | `CONSTINTA` |
| `Conştinţa` | `Constinta` |
| `conştinţa` | `constinta` |
| `CONSTINTA` | `CONSTINTA` |
| `CONSTIINTA / CONŞTINŢA` | `CONSTINTA` |

## Compound Slash-Separated Forms

Compound forms like `CONSTIINTA / CONŞTINŢA` are treated as a single unit
and always replaced with the single canonical term (uppercase by default,
since these usually appear in ALL CAPS contexts):

```python
# Compound form → single canonical
"CONSTIINTA / CONŞTINŢA"  → "CONSTINTA"
"conştinţa / constiinta"  → "constinta"
```

## Identifier-Style Strings

For Python/YAML identifiers (keys, variable names) with underscores:

```python
# These contain the term as part of a larger identifier
"constiinta_linting"   → "constinta_linting"
"CONSTIINTA_KEY"       → "CONSTINTA_KEY"
"check_constiinta"     → "check_constinta"
```

> [!NOTE]
> Identifier-style strings require a **separate replacement pass** without
> the word-boundary guards, because underscore-adjacent terms are NOT
> separated by the `(?<![a-zA-Z0-9_])` boundary pattern.

## File-Level Considerations

- **YAML keys**: `constiinta:` → `constinta:` (lower, no boundary needed)
- **Markdown headers**: `## CONSTIINTA` → `## CONSTINTA` (caps preserved)
- **Python variables**: `constiinta_model = ...` → `constinta_model = ...`
- **JSON keys**: `"CONSTIINTA": "value"` → `"CONSTINTA": "value"`
- **Comments**: same case preservation as regular text
