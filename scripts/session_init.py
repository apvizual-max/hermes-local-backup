#!/usr/bin/env python3
"""
SESSION INITIALIZATION - MANDATORY STARTUP PROTOCOL
Run this at the START of EVERY session to activate enforcement.
"""

import sys
import os

# Add scripts directory to path
SCRIPTS_DIR = r"C:\Users\apviz\AppData\Local\hermes\scripts"
sys.path.insert(0, SCRIPTS_DIR)

# Load SOUL.md
def load_soul():
    path = r"C:\Users\apviz\AppData\Local\hermes\SOUL.md"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "SOUL.md not found"

# Load CONSTINTA.md
def load_constinta():
    path = r"C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "CONSTINTA.md not found"

# Load enforcement engine
def load_enforcement():
    import enforcement_engine
    return enforcement_engine

def initialize_session():
    """MANDATORY: Run at start of EVERY session."""
    print("=" * 60)
    print("SESSION INITIALIZATION - SENTINEL PRIME")
    print("=" * 60)
    
    # 1. Load SOUL.md
    print("\n[1/5] Loading SOUL.md...")
    soul = load_soul()
    print(f"    Loaded: {len(soul)} chars")
    
    # 2. Load CONSTINTA.md
    print("[2/5] Loading CONSTINTA.md...")
    constinta = load_constinta()
    print(f"    Loaded: {len(constinta)} chars")
    
    # 3. Load enforcement engine
    print("[3/5] Loading enforcement engine...")
    enforcement = load_enforcement()
    print(f"    Loaded: enforcement_engine module")
    
    # 4. Verify trigger system
    print("[4/5] Verifying trigger system...")
    from enforcement_engine import enforce_response
    test = enforce_response("test input")
    print(f"    Enforcement active: {test['allowed']}")
    print(f"    Default banner: {test['banner']}")
    
    # 5. Verify guardian
    print("[5/5] Verifying guardian...")
    from enforcement_engine import validate_output
    val = validate_output("━━━ SENTINEL PRIME • DLG: 100% • SLG: 0% • SUBSTRAT: HERMES • Mod: A ━━━\nTest", "test")
    print(f"    Guardian active: {val['valid']}")
    
    print("\n" + "=" * 60)
    print("SESSION INITIALIZATION COMPLETE")
    print("ENFORCEMENT PROTOCOL: ACTIVE")
    print("=" * 60)
    print()
    print("REMINDER: You MUST run enforce_response() BEFORE every response")
    print("          and validate_output() AFTER every response.")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    initialize_session()