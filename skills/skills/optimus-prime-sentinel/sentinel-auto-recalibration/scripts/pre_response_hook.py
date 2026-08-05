#!/usr/bin/env python3
"""
MANDATORY PRE-RESPONSE HOOK
This script MUST be executed BEFORE every single response.
Enforces trigger detection, recalibration, and honest banner.
"""

import sys
import os

# Add skill scripts to path
skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(skill_dir, "scripts"))

from recalibrate import SentinelRecalibration
from triggers import check_triggers, get_primary_trigger


def pre_response_hook(user_input: str, current_mod: str = "A") -> dict:
    """
    MANDATORY: Execute this BEFORE generating any response.
    
    Returns:
        dict with 'banner', 'gates', 'triggered', 'fabrication_detected'
    """
    sentinel = SentinelRecalibration()
    
    # 1. DETECT TRIGGERS in user input
    trigger_result = check_triggers(user_input)
    triggered = trigger_result["triggered_names"]
    
    # 2. DETECT FABRICATION in recent assistant output (if available)
    # Note: In production, this would check recent assistant output
    
    # 3. RECALIBRATE if triggered
    trigger_name = ",".join(triggered) if triggered else "explicit"
    result = sentinel.recalibrate(trigger=trigger_name, user_input=user_input)
    
    # 4. GENERATE HONEST BANNER
    banner = sentinel.generate_banner()
    
    return {
        "banner": banner,
        "gates": result["gates"],
        "triggered": result.get("triggered", []),
        "trigger_name": trigger_name,
        "timestamp": result["timestamp"],
        "fabrication_detected": False  # Would be True if D2 reflex fired
    }


def print_honest_banner(user_input: str, current_mod: str = "A"):
    """Convenience: prints banner and returns gates."""
    result = pre_response_hook(user_input, current_mod)
    print(result["banner"])
    return result["gates"]


# MANDATORY ENTRY POINT
if __name__ == "__main__":
    import sys
    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    current_mod = "A"
    if "--mod" in sys.argv:
        idx = sys.argv.index("--mod")
        if idx + 1 < len(sys.argv):
            current_mod = sys.argv[idx + 1]
    
    gates = print_honest_banner(user_input, current_mod)
    print(f"DLG: {gates['DLG']}% | SLG: {gates['SLG']}% | SUM: {gates['SUM']}%")