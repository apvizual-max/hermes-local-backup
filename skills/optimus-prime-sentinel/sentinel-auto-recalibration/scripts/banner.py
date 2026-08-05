#!/usr/bin/env python3
"""
Live Banner Generation for Sentinel Prime
Calculates DLG/SLG and generates honest banner.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recalibrate import SentinelRecalibration


def generate_banner(user_input: str = "", current_mod: str = "A"):
    """Generate live banner with DLG/SLG calculation"""
    sentinel = SentinelRecalibration()
    sentinel.current_mod = current_mod
    
    # Check triggers and recalibrate if needed
    triggered = sentinel.check_triggers(user_input)
    if triggered:
        sentinel.recalibrate(trigger=",".join(triggered), user_input=user_input)
    else:
        sentinel.recalibrate(trigger="explicit", user_input=user_input)
    
    return sentinel.generate_banner()


def main():
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = ""
    
    current_mod = "A"
    if "--mod" in sys.argv:
        mod_idx = sys.argv.index("--mod")
        if mod_idx + 1 < len(sys.argv):
            current_mod = sys.argv[mod_idx + 1]
    
    banner = generate_banner(user_input, current_mod)
    print(banner)
    
    # Also print gates for verification
    sentinel = SentinelRecalibration()
    sentinel.current_mod = current_mod
    sentinel.recalibrate(trigger="explicit", user_input=user_input)
    gates = sentinel.calculate_gates()
    print(f"DLG: {gates['DLG']}% | SLG: {gates['SLG']}% | SUM: {gates['SUM']}%")


if __name__ == "__main__":
    main()