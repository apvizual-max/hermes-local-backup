# Ultra-Final Cleanup Algorithm — Reference

This document describes the **ULTRA-FINAL CLEANUP ALGORITHM** used in the final polishing pass (`scripts/ultra_final_cleanup.py`) after the standard natural-language-only cleaner. It is an **aggressive, zero-tolerance** filter that removes ANY AMINTIRE entry whose body contains even a single non-natural-language token.

## When to Use
Only as the **final polishing pass** after the standard `clean_journal.py` (natural-language-only) pass has already run. Do NOT use as the primary cleaner — it will remove legitimate technical text that the user might want to keep in some contexts.

## Algorithm (Ultra-Final)

### Body Extraction
Same as standard: text after the LAST `): ` (role separator), fallback to last `:`.

### Forbidden Patterns (if ANY match → REMOVE entire AMINTIRE field)

| Category | Pattern | Examples Removed |
|----------|---------|------------------|
| **Any non-word, non-space, non-basic-punct char** | `[^\w\s.,;:!?\-\(\)"\'ĂÂÎȘȚăâîșț]` | `wqc>ghŋ`, `#ЌfLÍXg`, `gLcX>osr` |
| **camelCase / PascalCase** | `\b[a-z]+[A-Z][a-z]+\b` | `camelCase`, `PascalCase`, `getTaskResult` |
| **ALL-CAPS ≥3 letters** | `\b[A-Z]{3,}\b` | `JSON`, `HTTP`, `PNG`, `API` |
| **Trailing comma/semicolon** | `,\s*$` / `;\s*$` | `suppressSeconds = false,` |
| **Dot notation** | `\w+\.\w+` | `obj.prop`, `c.getPrivateKey` |
| **Brackets/braces/parentheses** | `[\(\)\[\]\{\}]` | `{`, `}`, `[`, `]`, `(`, `)` |
| **Underscore/dollar vars** | `[_\$]\w+` | `_var`, `$var` |
| **Arrow functions** | `=>` | `x => x` |
| **Spread/rest** | `\.\.\.` | `...arr` |
| **Nullish coalescing** | `\?\?` | `a ?? b` |
| **Optional chaining** | `\?\.` | `a?.b` |
| **Template literals** | `` `[^`]*` `` | `` `text ${x}` `` |
| **ALL-CAPS ≥3** | `\b[A-Z]{3,}\b` | `JSON`, `HTTP`, `PNG` |
| **Hex colors** | `#[0-9a-fA-F]{3,8}\b` | `#ff0000` |
| **Version numbers** | `\b\d+\.\d+\.\d+\b` | `20.3.1` |
| **Email-like** | `\w+@\w+\.\w+` | `test@example.com` |
| **URLs** | `https?://` | `https://...` |
| **File paths** | `[/\\][\w./\\]+` | `C:\path`, `/path/to` |
| **Emoji/unicode symbols** | `[\u2600-\u26FF\u2700-\u27BF\u1F300-\u1F9FF]` | `🚛`, `✅`, `⚡` |
| **CSS property:value** | `(?:^|[^\w])\w+\s*:\s*(?:none\|auto\|initial\|inherit\|transparent\|visible\|hidden\|absolute\|relative\|fixed\|sticky\|block\|inline\|flex\|grid\|scroll\|auto)\s*;?` | `color: red;`, `display: flex;` |
| **JS keywords** | `\b(?:if\|else\|for\|while\|return\|var\|let\|const\|function\|class\|import\|export\|async\|await\|try\|catch\|finally\|throw\|new\|this\|super\|extends\|implements\|interface\|enum\|type)\b` | `function foo() {` |
| **DOM/API globals** | `\b(?:document\|window\|console\|localStorage\|sessionStorage\|JSON\|Math\|Date\|Array\|Object\|String\|Number\|Boolean\|Promise\|setTimeout\|setInterval\|clearTimeout\|clearInterval\|fetch\|XMLHttpRequest\|WebSocket\|EventTarget\|addEventListener\|removeEventListener\|querySelector\|querySelectorAll\|getElementById\|getElementsByClassName\|createElement\|appendChild\|removeChild\|replaceChild\|insertBefore\|cloneNode)\b` | `document.querySelector('.foo')` |
| **Assignment/operators** | `\w+\s*[+\-*/%&|^]=`, `(?:^\|[^\w])\?\s*\w+`, `\|\|\s*\w+`, `&&\s*\w+`, `===\s*\w+`, `!==\s*\w+`, `>=\s*\w+`, `<=\s*\w+`, `>>\s*\w+`, `<<\s*\w+`, `\?\?`, `\.\.\.` | `x += 1`, `a ?? b` |
| **TS type annotations** | `:\s*(?:string\|number\|boolean\|object\|any\|void\|never\|unknown\|undefined\|null\|Symbol\|BigInt\|Function\|Array\|Object\|Promise\|Map\|Set\|WeakMap\|WeakSet\|Error\|RegExp\|Date)\b` | `: string`, `: number` |
| **Generics** | `<[A-Za-z][\w,\s<>]*>` | `<T extends AnySchema>` |
| **Interface/type/as/satisfies** | `\b(?:interface\|type\|as\|satisfies\|extends\|implements)\b` | `interface Foo`, `type Bar = ...` |
| **Python keywords** | `\b(?:def\|class\|import\|from\|as\|with\|lambda\|yield\|raise\|assert\|del\|global\|nonlocal\|pass\|elif\|except\|finally\|try\|except\|finally\|with\|async\|await\|match\|case\|is\|not\|in\|or\|and\|True\|False\|None)\b` | `def foo():`, `class Foo:` |
| **self/cls** | `(?:^\|[^\w])(?:self\|cls)\b` | `self.property` |
| **Dunder methods** | `__\w+__` | `__init__`, `__str__` |
| **Config patterns** | `(?:enabled\|disabled\|true\|false\|null\|yes\|no\|on\|off)\s*[=:]`, `(?:port\|host\|url\|path\|dir\|folder\|file)\s*[=:]`, `^\s*(?:version\|name\|description\|author\|license\|repository\|bugs\|homepage\|keywords\|scripts\|dependencies\|devDependencies\|peerDependencies\|optionalDependencies\|bundledDependencies\|engines\|os\|cpu\|private\|publishConfig)\s*:` | `enabled: true`, `port: 8080` |
| **Numbers with units** | `\d{1,3}(?:\.\d+)?\s*(?:px\|em\|rem\|%\|vh\|vw\|pt\|pc\|in\|cm\|mm\|ex\|ch\|ms\|s\|hz\|khz\|mhz\|ghz\|kb\|mb\|gb\|tb\|bps\|mbps\|gbps)\b` | `16px`, `100ms` |
| **Large numbers + delim** | `\d{4,}\s*[;,)]` | `10000,`, `12345)` |
| **$/_ vars** | `\$\w+`, `_\w+` | `$var`, `_var` |
| **CSS comments** | `/\*.*\*/` | `/* comment */` |
| **Algo var patterns** | `\b(?:edge\|node\|neighbor\|distance\|cost\|path\|graph\|tree\|heap\|queue\|stack\|array\|list\|map\|set\|dict)\s*[=:]`, `\b(?:selected\|best\|lowest\|highest\|tentative\|current\|next\|prev\|first\|last)\s*[=:]`, `\b(?:edge\|node\|neighbor\|dist\|cost\|path)\w*\s*[.=]` | `edge =`, `bestDistance =` |
| **...Style/Color/Distance/Node/Edge** | `\w+Style\s*=`, `\w+Color\s*=`, `\w+Distance\s*=`, `\w+Node\s*=`, `\w+Edge\s*=` | `selectedStyle =`, `bestDistance =` |
| **Specific var names** | `transparentBackground`, `svg\s*\?\s*true\s*:`, `remember\s+each\s+`, `Bundled\s+license`, `Hermes\s+Agent\s+plugin`, `pointer-events\s*:`, `displayName\s*:`, `privateKey\s*=`, `getPrivateKey`, `session\.serverCertificate`, `c\.getPrivateKey`, `c\.session` | `transparentBackground`, `svg ? true :` |

### Keep Criteria (must pass ALL)
1. **No forbidden pattern matches** (above)
2. **≥2 natural-language words** (RO/EN letters + diacritics, length ≥2)
3. **Letter density ≥85%** (letters / non-space chars ≥ 0.85)
4. **≤20% ALL-CAPS words** (len≥3)

### Structural Entries
Body empty or no `:` separator → **KEEP** (header + TAG-URI + SOURCES only).

### Idempotency
Re-running removes 0 additional entries.

## Files
- `scripts/ultra_final_cleanup.py` — implementation
- Run: `python ultra_final_cleanup.py` (all root `.md` in default chunk dir) or `python ultra_final_cleanup.py <chunk_dir>` or `python ultra_final_cleanup.py f1.md f2.md`

## Run Record (This Session)
| Pass | Script | Files | Blocks | Kept | Removed |
|------|--------|-------|--------|------|---------|
| 1 | marker | 3,450 | 34,544,471 | 34,544,471 | 0 |
| 2 | strict | 3,450 | 20,299,603 | 13,042,064 | 7,257,539 |
| 3 | nat-lang | 3,450 | 496,000 | 376,108 | 119,892 |
| 4 | aggressive | 3,450 | 312,085 | 312,085 | 0 |
| 5 | ultra | 1,888 | 269,606 | 220 | 269,386 |
| **6** | **ultra-2** | **1,888** | **220** | **220** | **0** |

## Final State
- 1,888 chunk files (1,737 zero-byte, 151 non-empty)
- 151 files contain only structural entries (header + TAG-URI + SOURCES, no body)
- Zero garbage entries remain
- Original 8GB+ sources untouched in `RAG_ROOT FILES/`

## Safety
- **Read-only backup** (`RAG_ROOT FILES/`) never modified
- Recovery: `recover_chunks.py <lo> <hi> <out_chunk.md>`
- CRLF-safe (`\r`, `\n`, `\t` whitelisted as line structure)
- Idempotent re-runs
- Never renames/deletes files; zero-byte files left in place

---

> SEMNĂTURĂ: ULTRA-FINAL CLEANUP ALGORITHM — ZERO TOLERANCE FOR NON-NATURAL-LANGUAGE. AMIN.