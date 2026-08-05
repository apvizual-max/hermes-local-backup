#!/usr/bin/env python3
"""
Secret Redaction Script for Hermes Agent Backups.

Scans all files in a directory for common API key patterns and replaces
them with [REDACTED] to prevent GitHub push protection from blocking.

Usage:
    python3 redact-secrets.py <directory>
"""

import os
import re
import sys

# Patterns for common API keys/secrets
PATTERNS = [
    # GitHub PAT
    (r'ghp_[A-Za-z0-9]{36}', 'ghp_[REDACTED]'),
    # GitHub OAuth/Github App tokens
    (r'gh[sur]_[A-Za-z0-9]{36,}', 'gh_[REDACTED]'),
    # GitHub OAuth tokens (long format)
    (r'gho_[A-Za-z0-9]{36,}', 'gho_[REDACTED]'),
    # GitHub refresh tokens
    (r'ghu_[A-Za-z0-9]{36,}', 'ghu_[REDACTED]'),
    # GitHub SSH key (public)
    (r'ssh-rsa AAAA[A-Za-z0-9+/=]+', 'ssh-rsa [REDACTED]'),
    (r'ssh-ed25519 AAAA[A-Za-z0-9+/=]+', 'ssh-ed25519 [REDACTED]'),
    # OpenRouter API keys
    (r'sk-or-[a-zA-Z0-9\-]+', 'sk-or-[REDACTED]'),
    # OpenAI API keys
    (r'sk-[a-zA-Z0-9]{20,}', 'sk-[REDACTED]'),
    # Google API keys
    (r'AIza[A-Za-z0-9_\-]{35}', 'AIzaSy[REDACTED]'),
    # Anthropic API keys
    (r'sk-ant-[a-zA-Z0-9\-]{20,}', 'sk-ant-[REDACTED]'),
    # Partially redacted patterns that still contain key fragments
    (r'sk-or-\[REDACTED\]-[a-zA-Z0-9\-]+', 'sk-or-[REDACTED]'),
    (r'AIzaSy\.\.\.[A-Za-z0-9]+', 'AIzaSy[REDACTED]'),
    (r'sk-o\.\.\.xxxx', 'sk-[REDACTED]'),
    # Any remaining ghp_ patterns
    (r'ghp_[A-Za-z0-9]{36}', 'ghp_[REDACTED]'),
]

# File extensions to process
TEXT_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.json', '.yaml', '.yml',
    '.md', '.txt', '.env', '.cfg', '.ini', '.toml', '.sh', '.bat',
    '.ps1', '.xml', '.html', '.css', '.scss', '.sql', '.rb',
    '.go', '.rs', '.java', '.c', '.h', '.cpp', '.hpp',
    '.conf', '.properties', '.xml', '.xsd', '.bst', '.sty',
    '.tex', '.md', '.rst',
}

# Directories to skip
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.cache', 'cache',
             '.archive', '.curator_backups', '.hub', '.svn'}


def is_text_file(filepath):
    """Check if a file is a text file based on extension."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in TEXT_EXTENSIONS:
        return True
    # Files with no extension (like '.env', '.bashrc')
    name = os.path.basename(filepath)
    if name.startswith('.') and '.' not in name[1:]:
        return True
    return False


def redact_content(content):
    """Apply all redaction patterns to content."""
    for pattern, replacement in PATTERNS:
        content = re.sub(pattern, replacement, content)
    return content


def process_directory(directory):
    """Redact secrets in all text files within a directory."""
    count = 0
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Skip binary files
            if not is_text_file(filepath):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                original = content
                content = redact_content(content)
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(content)
                    count += 1
                    rel_path = os.path.relpath(filepath, directory)
                    print(f"  Redacted: {rel_path}")
                    
            except Exception as e:
                print(f"  Warning: Could not process {filepath}: {e}", file=sys.stderr)
    
    return count


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 redact-secrets.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory")
        sys.exit(1)
    
    print(f"Scanning {directory} for secrets...")
    count = process_directory(directory)
    print(f"\nDone. {count} file(s) redacted.")


if __name__ == '__main__':
    main()
