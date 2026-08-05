#!/usr/bin/env python3
"""Fix Windows path backslash issues in Hermes YAML config files."""
from pathlib import Path
import re

HERMES_ROOT = Path(r"C:\Users\apviz\AppData\Local\hermes")

# Files to fix
config_files = [
    HERMES_ROOT / "config.yaml",
    HERMES_ROOT / "profiles" / "default" / "config.yaml",
]

for config_path in config_files:
    if not config_path.exists():
        print(f"❌ Not found: {config_path}")
        continue

    content = config_path.read_text()
    original = content

    # Fix double-quoted Windows paths that have backslash escape issues
    # Convert quoted paths to use forward slashes
    # Pattern: "C:\Users\..." -> C:/Users/...
    pattern = r'"([A-Z]:\\Users\\[^"]*)"'
    def to_forward_slash(m):
        path = m.group(1)
        return path.replace('\\', '/')

    content = re.sub(pattern, to_forward_slash, content)

    # Also fix quoted paths with Program Files
    pattern2 = r'"(C:\\Program Files\\[^"]*)"'
    content = re.sub(pattern2, to_forward_slash, content)

    if content != original:
        config_path.write_text(content)
        print(f"✅ Fixed: {config_path}")
    else:
        print(f"⚠️  No changes needed: {config_path}")

print("\n--- Verification ---")
import yaml
for config_path in config_files:
    if config_path.exists():
        try:
            with open(config_path) as f:
                yaml.safe_load(f)
            print(f"✅ YAML valid: {config_path}")
        except yaml.YAMLError as e:
            print(f"❌ YAML error in {config_path}: {e}")
