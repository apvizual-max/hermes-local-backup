#!/usr/bin/env python3
"""
verify_ascii_safe.py
Scan the Hermes workspace for Python and Markdown files that contain
non‑ASCII characters inside string literals or f‑strings.
Reports each offending file and line number.
Usage: python scripts/verify_ascii_safe.py
"""
import ast
import os
import sys
from pathlib import Path

# Directories to skip entirely
SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".heroku",
    "dist",
    "build",
    ".mypy_cache",
    ".cache",
    "site-packages",
}

def is_ascii(s: str) -> bool:
    return all(ord(c) < 128 for c in s)

def check_python_file(path: Path):
    """Return list of (line_no, offending_string) for non-ASCII in string literals/f-strings."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as e:
        # If we cannot parse, still check raw lines for non-ASCII in quotes? Skip for now.
        return [(e.lineno or 0, f"SyntaxError: {e}")]
    violations = []

    class Visitor(ast.NodeVisitor):
        def visit_Constant(self, node):
            if isinstance(node.value, str) and not is_ascii(node.value):
                # Try to get line number; node.lineno may be None in some cases
                lineno = getattr(node, "lineno", 0)
                violations.append((lineno, node.value))
            self.generic_visit(node)

        def visit_JoinedStr(self, node):  # f-strings
            for value in node.values:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    if not is_ascii(value.value):
                        lineno = getattr(value, "lineno", 0)
                        violations.append((lineno, value.value))
            self.generic_visit(node)

    visitor = Visitor()
    visitor.visit(tree)
    return violations

def check_markdown_file(path: Path):
    """Very simple check: any non-ASCII character outside of code fences? We'll just
    flag any non-ASCII in the file (excluding fenced code blocks) as a potential issue,
    because MD should generally be ASCII for our internal docs, but we allow
    Unicode in comments? For safety, just flag any non-ASCII and let user decide."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [(0, "Cannot decode as UTF-8")]
    lines = text.splitlines()
    in_code_block = False
    violations = []
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            # Check for any non-ASCII char
            if any(ord(ch) >= 128 for ch in line):
                violations.append((i, line.rstrip()))
    return violations

def main():
    repo_root = Path(__file__).resolve().parents[2]  # go up from skills/model-catalog-maintenance/scripts/ to repo root
    # Actually simpler: we can compute from __file__: .../skills/model-catalog-maintenance/scripts/verify_ascii_safe.py
    # So parent.parent.parent is repo root.
    repo_root = Path(__file__).resolve().parent.parent.parent
    print(f"Scanning repository root: {repo_root}\n")

    extensions_to_check = {".py", ".md"}
    all_violations = []
    for root, dirs, files in os.walk(repo_root):
        # prune skipped directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in extensions_to_check:
                continue
            path = Path(root) / f
            if ext == ".py":
                vio = check_python_file(path)
            else:  # .md
                vio = check_markdown_file(path)
            if vio:
                all_violations.append((path, vio))

    if not all_violations:
        print("✅ No non-ASCII characters found in string literals or f‑strings (and no non-ASCII in MD outside code blocks).")
        return 0
    else:
        print("❌ Found issues:")
        for path, vio_list in all_violations:
            print(f"\n{path}:")
            for line_no, snippet in vio_list:
                # Show a short snippet; if it's a SyntaxError note, print as is.
                if isinstance(snippet, str) and snippet.startswith("SyntaxError"):
                    print(f"  Line {line_no}: {snippet}")
                else:
                    # Truncate long strings for readability
                    display = snippet if len(snippet) <= 80 else snippet[:77] + "..."
                    print(f"  Line {line_no}: {display}")
        print("\nPlease fix the above occurrences (replace non‑ASCII characters with ASCII equivalents).")
        return 1

if __name__ == "__main__":
    sys.exit(main())