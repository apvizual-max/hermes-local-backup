# Natural Language Rule (User's "Words Only" Directive)

## User's Exact Directive

> "I DO NOT READ CODE! JUST WORDS! the CODE we index with another method you are to remove ALL CODE, all symbolds...EVERYTHING EXCEPT COMMON LANGUADGE NATURAL LANGUADGE WORDS, either in romanian or ENGLISH. if an Amintire field has after ":" enything ELSE than words, and more than 1 word is needed to pass, otherwise, you need to remove it, not keep it. I DO NOT READ CODE, and we do not index characters or CODE here, ONLY I SAY AGAIN READABLE WORDS PLEASE!"

## Decision Rule (STRICT)

**KEEP** an AMINTIRE field ONLY IF the body (text after the last `): ` on the header line) satisfies BOTH:

1. **Contains ≥2 natural-language words** (Romanian/English letters + diacritics, length ≥ 2)
2. **Contains NO forbidden content:**
   - Binary/encrypted garbage (control bytes ord<32 except space/tab/newline, U+FFFD, 0x7F)
   - Code/symbols: `camelCase`, `PascalCase`, `snake_case`, `dot.notation`, `::`, `->`, `=>`
   - JSON/YAML/Config: `key: value`, `---`, `...`, `[`, `]`, `{`, `}`, `=`, `:=`
   - File paths/extensions: `.md`, `.png`, `.exe`, `/path/`, `C:\`, `./`, `../`
   - Hex hashes/IDs: `[0-9a-f]{8,}`, `[A-F0-9]{8,}`
   - CSS/JS/TS/Python patterns: `function`, `class`, `const`, `let`, `var`, `import`, `export`, `console.log`, `=>`, `async`, `await`
   - CSS: `property: value;`, `#hex`, `rgba()`, `px`, `em`, `rem`, `%`, `vh`, `vw`
   - URLs: `http://`, `https://`, `ftp://`
   - Email-like: `user@domain`
   - Emoji-only or symbol-only content
   - Single tokens: `PNG`, `true`, `false`, `null`, `auto`, `none`, `initial`, `inherit`
   - Garbled unicode: `wqc>ghŋ`, `ij+Olfxˉ`, `Qzіcql&`, `J<rvX Ls`

**REMOVE the ENTIRE AMINTIRE field** (header + TAG-URI + SOURCES + `---`) if body fails above.

**EXCEPTIONS:**
- Field with NO `:` separator (structural file-reference entry) → **KEEP**
- Body with emoji/markdown WRAPPING real words → **KEEP** if ≥2 real words present
  - Example KEPT: `🚛 **DOAMNE AJUTA. AMIN.**` (3 words: DOAMNE, AJUTA, AMIN)
  - Example KEPT: `🚛 **Constructiv adversarial activat. Fara hedging. Raspuns brutal-onest la...**`

---

## Positive Filter Algorithm (CORRECT)

```python
def is_natural_language(body):
    body = body.strip()
    if not body:
        return False  # structural entry -> KEEP handled upstream
    
    # 1. No control bytes (except \r\n\t)
    for ch in body:
        if is_control(ch):
            return False
    
    # 2. At least 2 natural-language words
    words = WORD_RE.findall(body)  # [A-Za-zAAISTaaist]{2,}
    if len(words) < 2:
        return False
    
    # 3. Letters >= 70% of non-space chars (natural language is letter-dense)
    letters = sum(1 for c in body if c.isalpha())
    nonspace = sum(1 for c in body if not c.isspace())
    if nonspace == 0 or letters / nonspace < 0.70:
        return False
    
    # 4. Not mostly ALL-CAPS code identifiers
    all_caps = sum(1 for w in words if w.isupper() and len(w) >= 3)
    if words and all_caps / len(words) > 0.2:
        return False
    
    # 5. No forbidden patterns (code/config/symbols)
    if FORBIDDEN_RE.search(body):
        return False
    
    return True
```

---

## Verification Gate (MANDATORY BEFORE ANY FULL RUN)

```python
def test_on_known_readable():
    """MUST pass before ANY full cleaning run"""
    backup = read_file("backup/1-10001.md")
    cleaned = clean(backup)
    original_count = count_readable(backup)
    cleaned_count = count_readable(cleaned)
    assert cleaned_count >= original_count * 0.95, \
        f"DROPPED READABLE: {original_count} -> {cleaned_count}. STOP. FIX FILTER."
```

**If readable count drops → STOP. Fix filter. DO NOT proceed to full run.**

---

## Worked Examples

| Input Body | Decision | Reason |
|------------|----------|--------|
| `🚛 **DOAMNE AJUTA. AMIN.**` | **KEEP** | 3 words: DOAMNE, AJUTA, AMIN |
| `PNG` | **REMOVE** | 1 word only |
| `Z+j jݗzYǅa*OH> oOAf` | **REMOVE** | 0 real words, symbols |
| `pointer-events: none;` | **REMOVE** | CSS property |
| `privateKey = c.getPrivateKey(...)` | **REMOVE** | Code assignment |
| `captureAsn1: "subjectPublicKeyInfo"` | **REMOVE** | JSON-like |
| `Respira. Esti aici. Eu sunt aici. Citesc acum.` | **KEEP** | 8 Romanian words |
| `tau uman, comportament in sesiune noua, actiune fizica).` | **KEEP** | Romanian words |
| `daca itti vine a crede...tre sa fii programator sa descifrezi ce e asta cnad vii` | **KEEP** | Romanian words |
| `isVirtualHostableS3Bucket,` | **REMOVE** | camelCase identifier |
| `wqc>ghŋ` | **REMOVE** | Garbled unicode |
| `Ii  uƽoi/yu` | **REMOVE** | Garbled unicode |
| `Expected tag %x, read %x` | **REMOVE** | Code/log format |
| `unlinkedCollapsed: true` | **REMOVE** | Config/JSON |
| `switcher:Open quick switcher: false` | **REMOVE** | Config |
| `hermes-agent:Open Hermes smart graph: false` | **REMOVE** | Config |
| `for (var name in all)` | **REMOVE** | Code |
| `return to;` | **REMOVE** | Code |
| `var IconsHelper = class {` | **REMOVE** | Code |
| `var DebugHelper = class {` | **REMOVE** | Code |
| `constructor(plugin) {` | **REMOVE** | Code |
| `this.plugin.registerEvent(this.plugin.app.workspace.on(` | **REMOVE** | Code |
| `this.plugin.registerEvent(this.plugin.app.workspace.on(` | **REMOVE** | Code |
| `svg ? true : transparentBackground` | **REMOVE** | Code ternary |
| `remember each edge's real color so` | **KEEP** | English sentence |
| `/* Hermes Agent plugin styles */` | **REMOVE** | CSS comment |
| `/*! Bundled license information:` | **REMOVE** | License comment |
| `if you want to view the source, please visit the github repository of this plugin` | **KEEP** | English sentence |
| `for (var name in all)` | **REMOVE** | Code |
| `return to;` | **REMOVE** | Code |
| `var IconsHelper = class {` | **REMOVE** | Code |
| `var DebugHelper = class {` | **REMOVE** | Code |
| `constructor(plugin) {` | **REMOVE** | Code |
| `this.plugin.registerEvent(this.plugin.app.workspace.on(` | **REMOVE** | Code |
| `this.plugin.registerEvent(this.plugin.app.workspace.on(` | **REMOVE** | Code |
| `svg ? true : transparentBackground` | **REMOVE** | Code ternary |
| `remember each edge's real color so` | **KEEP** | English sentence |
| `/* Hermes Agent plugin styles */` | **REMOVE** | CSS comment |
| `/*! Bundled license information:` | **REMOVE** | License comment |
| `if you want to view the source, please visit the github repository of this plugin` | **KEEP** | English sentence |
| `for (var name in all)` | **REMOVE** | Code |
| `return to;` | **REMOVE** | Code |
| `var IconsHelper = class {` | **REMOVE** | Code |
| `var DebugHelper = class {` | **REMOVE** | Code |
| `constructor(plugin) {` | **REMOVE** | Code |
| `this.plugin.registerEvent(this.plugin.app.workspace.on(` | **REMOVE** | Code |
| `this.plugin.registerEvent(this.plugin.app.workspace.on(` | **REMOVE** | Code |
| `svg ? true : transparentBackground` | **REMOVE** | Code ternary |
| `remember each edge's real color so` | **KEEP** | English sentence |

---

## CRLF Safety (CRITICAL)

```python
def is_control(c):
    if c in '\r\n\t':  # CRLF/tab are LINE STRUCTURE, never corruption
        return False
    o = ord(c)
    return (o < 32) or o == 0x7f or o == 0xfffd
```

**ALWAYS test on known-readable file FIRST. If readable count drops → STOP.**

---

**SEMNATURA: DOAR CUVINTE NATURALE. AMIN.**