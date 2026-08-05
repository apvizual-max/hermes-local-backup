#!/usr/bin/env python3
"""
clean_journal.py - Sentinel DATA_CLEANING utility (ULTRA-STRICT natural-language-only rule).

USER RULE (final, strict):
  Header: AMINTIRE-<n> — <date> — <desc> (<ROLE>): <body>
  KEEP the entire field ONLY IF body has >= 2 natural-language words (RO/EN, diacritics ok)
  AND consists SOLELY of natural-language characters: letters, spaces, and benign punctuation.
  REMOVE the ENTIRE field if body contains ANY of:
    - binary/encrypted garbage (control bytes except \r\n\t)
    - the prior-pass marker '[CORRUPTED_BINARY_CONTENT_REMOVED]'
    - ANY non-natural-language pattern: code, JSON, YAML, markdown, paths, camelCase, 
      ALL-CAPS identifiers, hex, emoji, symbols, assignments, dot notation, brackets,
      braces, semicolons, colons (except in natural sentences), CSS, JS/TS/Python code,
      config key:value, generics, type annotations, $/_ vars, file extensions, etc.
    - fewer than 2 natural-language words
  A field with NO ':' separator (structural file-reference entry) is KEPT.

CONSTRAINTS: never rename/delete files; all-corrupt file -> 0 bytes; root .md only; idempotent.
LOCATION: referenced by NAME only (user relocates scripts, keeps names).
Chunk dir resolved from: CLI dir-arg > JOURNAL_CHUNK_DIR env > default.

Usage:
  python clean_journal.py                 # all root .md in resolved chunk dir
  python clean_journal.py <chunk_dir>     # all root .md in given dir
  python clean_journal.py f1.md f2.md     # only named files (basename or abs)
"""
import os
import re
import sys

DEFAULT_CHUNK_DIR = r"E:\CLAUDE\SENTINEL_JOURNAL - INDEX RAG - 00_KV_SECOND BRAIN"
AMINTIRE_HDR = re.compile(r'^AMINTIRE-\d+\s')
MARKER = '[CORRUPTED_BINARY_CONTENT_REMOVED]'

# Natural-language word = RO/EN letters + diacritics, length >= 2
WORD_RE = re.compile(r'[A-Za-zAAISTaaist]{2,}')

# =============================================================================
# FORBIDDEN PATTERNS — if ANY matches in the body, REMOVE the entire AMINTIRE field
# =============================================================================
FORBIDDEN_PATTERNS = [
    # --- YAML / frontmatter / structured data ---
    r'^\s*[a-z_][a-z0-9_]*:\s',          # key: value at line start (YAML)
    r'^\s*---\s*$',                       # YAML document separator
    r'^\s*\.\.\.\s*$',                    # YAML document end
    r'^\s*[#@]\s',                        # YAML anchor/alias or comment at start
    r':\s*[\[{]',                          # value starting with [ or { (inline YAML/JSON)
    
    # --- File paths ---
    r'[a-zA-Z]:[/\\]',                    # Windows drive path C:\ or C:/
    r'(?:^|[^\w])(?:/|\.\./|\.\./)[\w./-]+',  # Unix/relative paths
    r'(?:^|[^\w])[~/][\w./-]+',           # ~/ or relative paths
    
    # --- File extensions (must be followed by delimiter or end) ---
    r'\.(?:md|png|jpg|jpeg|gif|bmp|tiff|webp|svg|ico|txt|py|js|ts|json|yaml|yml|toml|ini|cfg|conf|log|csv|xml|html|htm|css|scss|sh|bat|ps1|sql|db|sqlite|pdf|doc|docx|xls|xlsx|ppt|pptx|zip|tar|gz|rar|7z|exe|dll|so|bin|iso|img)(?:\s|[.,;:!?)\)\}\'>]|$)',
    
    # --- Code / markdown / wiki syntax ---
    r'`{1,3}',                            # backticks (inline code, code blocks)
    r'\[\[',                             # wiki link start
    r'\]\]',                             # wiki link end
    r'\[[^\]]*\]\([^)]+\)',              # markdown link [text](url)
    r'!\[[^\]]*\]\([^)]+\)',             # markdown image ![alt](url)
    r'^\s*#{1,6}\s',                     # markdown heading
    r'^\s*[-*+]\s',                       # markdown list item
    r'^\s*>\s',                          # markdown blockquote
    r'^\s*\d+\.\s',                       # markdown numbered list
    r'^\s*[-=]{3,}\s*$',                 # markdown hr / table separator
    r'\|.*\|',                            # markdown table row
    r'[*_]{2,}',                          # **bold**, __italic__, ***bold italic***
    r'[<>]{2,}',                          # << >> or similar
    
    # --- File tree drawing characters ---
    r'[├└│─]',                            # box drawing chars
    
    # --- Identifiers / code patterns ---
    r'\b[a-z]+(?:-[a-z]+){2,}\b',        # kebab-case with 3+ segments
    r'\b[a-z]+(?:_[a-z]+){2,}\b',        # snake_case with 3+ segments
    r'\b[A-Z][a-z]+(?:[A-Z][a-z]+){2,}\b', # PascalCase 3+ segments
    r'\b[A-Z]{3,}\b',                     # ALL-CAPS 3+ letters (code identifiers)
    
    # --- Project-specific all-caps keywords ---
    r'\b(?:OBSIDIAN|SECOND|BRAIN|SYSTEM|FOLDER|HERMES|OGLINDA|CASA|VAULT|ARCHIVE|INDEX|LINKS|README|SCREENSHOTS?|THUMBNAILS?)\b',
    
    # --- Technical symbols ---
    r'[→←↑↓↔⇒⇐⇔]',
    r'[▶▷▸▹►]',
    r'[★☆✦✧✩✪✫✬✭✮✯✰]',
    r'[✓✔✕✖✗✘☑☒]',
    r'[ℹ⚠⚡⚙🔧🔨🛠🔩⚙️]',
    
    # --- URLs / hashes ---
    r'(?:https?|ftp)://',
    r'\b[0-9a-f]{8,}\b',                 # hex hashes/IDs
    r'\b[A-F0-9]{8,}\b',                 # uppercase hex
]

FORBIDDEN_RE = [re.compile(p) for p in FORBIDDEN_PATTERNS]

# =============================================================================
# HELPERS
# =============================================================================

def is_control(c):
    """True if c is a corruption control byte.
    CRLF / tab are LINE STRUCTURE, never corruption. (Critical bug fix: \r was falsely flagged.)"""
    if c in '\r\n\t':
        return False
    o = ord(c)
    return (o < 32) or o == 0x7f or o == 0xfffd

def get_body(header):
    """Extract body text after the last '): ' (role separator), fallback to last ':'."""
    idx = header.rfind('): ')
    if idx != -1:
        return header[idx + 3:]
    idx = header.rfind(':')
    if idx != -1:
        return header[idx + 1:]
    return ''

def is_natural_language(body):
    """True ONLY if body looks like a readable RO/EN sentence/fragment."""
    body = body.strip()
    if not body:
        return False  # no separator / empty -> structural entry (handled separately)
    
    # 1. No binary control bytes
    for ch in body:
        if is_control(ch):
            return False
    
    # 2. No forbidden patterns (code, markdown, paths, symbols, etc.)
    for rx in FORBIDDEN_RE:
        if rx.search(body):
            return False
    
    # 3. Must have at least 2 natural-language words
    words = WORD_RE.findall(body)
    if len(words) < 2:
        return False
    
    # 4. Letters >= 85% of non-space chars (natural language is letter-dense)
    letters = sum(1 for c in body if c.isalpha())
    nonspace = sum(1 for c in body if not c.isspace())
    if nonspace == 0 or letters / nonspace < 0.85:
        return False
    
    # 5. Not mostly all-caps words (code identifiers)
    all_caps_words = sum(1 for w in words if w.isupper() and len(w) >= 3)
    if words and all_caps_words / len(words) > 0.2:
        return False
    
    return True

def should_remove(header):
    """True => remove the entire AMINTIRE field."""
    if MARKER in header:
        return True
    body = get_body(header)
    if body.strip() == '':
        return False  # structural entry (no ':' or empty body) -> KEEP
    return not is_natural_language(body)

def split_blocks(lines):
    """Split lines into AMINTIRE blocks (header + continuation lines)."""
    blocks, cur = [], []
    for ln in lines:
        if AMINTIRE_HDR.match(ln):
            if cur:
                blocks.append(cur)
            cur = [ln]
        else:
            cur.append(ln)
    if cur:
        blocks.append(cur)
    return blocks

def process_file(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    blocks = split_blocks(lines)
    kept, removed = [], 0
    for b in blocks:
        if b and AMINTIRE_HDR.match(b[0]) and should_remove(b[0]):
            removed += 1
            continue
        kept.append(b)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        for b in kept:
            f.writelines(b)
    os.replace(tmp, path)
    return len(blocks), len(kept), removed

def resolve_chunk_dir():
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        return sys.argv[1]
    env = os.environ.get('JOURNAL_CHUNK_DIR')
    if env and os.path.isdir(env):
        return env
    return DEFAULT_CHUNK_DIR

def main():
    chunk_dir = resolve_chunk_dir()
    file_args = [a for a in sys.argv[1:] if not os.path.isdir(a)]
    if file_args:
        targets = []
        for a in file_args:
            if os.path.isabs(a) and os.path.isfile(a):
                targets.append(a)
            else:
                cand = os.path.join(chunk_dir, a)
                if os.path.isfile(cand):
                    targets.append(cand)
    else:
        targets = [os.path.join(chunk_dir, f) for f in os.listdir(chunk_dir)
                   if f.endswith('.md') and os.path.isfile(os.path.join(chunk_dir, f))]
    
    tk = tr = rm = 0
    for fp in targets:
        tb, kb, rm0 = process_file(fp)
        tk += tb; tr += kb; rm += rm0
        print(f"  {os.path.basename(fp)}: blocks={tb} kept={kb} removed={rm0}")
    print(f"\nDONE. Folder={chunk_dir}\nTotal: blocks={tk} kept={tr} removed={rm}")

if __name__ == '__main__':
    main()