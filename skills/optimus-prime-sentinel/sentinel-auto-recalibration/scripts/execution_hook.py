#!/usr/bin/env python3
"""
MANDATORY EXECUTION HOOK
This MUST be the FIRST thing that runs before ANY response generation.
Enforces: Trigger detection → Recalibration → Honest Banner → Response
"""

import sys
import os
import re
import json
from datetime import datetime

# Add skill scripts to path
skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(skill_dir, "scripts"))

from recalibrate import SentinelRecalibration
from triggers import check_triggers
from guardian import SentinelGuardian


class SentinelExecutionHook:
    """
    MANDATORY EXECUTION HOOK
    This MUST be called as the VERY FIRST operation in every response cycle.
    """
    
    def __init__(self):
        self.sentinel = SentinelRecalibration()
        self.guardian = SentinelGuardian()
        self.execution_log = []
    
    def execute_pre_response(self, user_input: str, current_mod: str = "A") -> dict:
        """
        MANDATORY PRE-RESPONSE HOOK
        Call this FIRST before generating ANY response.
        
        Returns:
            dict with: banner, gates, triggered, valid, errors
        """
        # 1. DETECT TRIGGERS in user input
        trigger_result = check_triggers(user_input)
        triggered = trigger_result["triggered_names"]
        
        # 2. EXECUTE RECALIBRATION if triggered
        trigger_name = ",".join(triggered) if triggered else "explicit"
        recal_result = self.sentinel.recalibrate(trigger=trigger_name, user_input=user_input)
        
        # 3. GENERATE HONEST BANNER
        banner = self.sentinel.generate_banner()
        
        # 4. CALCULATE GATES
        gates = self.sentinel.calculate_gates()
        
        # 5. LOG EXECUTION
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input[:200],
            "triggered": triggered,
            "trigger_name": trigger_name,
            "gates": gates,
            "banner": banner,
            "mod": current_mod,
        }
        self.execution_log.append(execution_record)
        
        return {
            "banner": banner,
            "gates": gates,
            "triggered": triggered,
            "trigger_name": trigger_name,
            "timestamp": recal_result["timestamp"],
            "mod": current_mod,
        }
    
    def validate_and_guard_response(self, draft_output: str, user_input: str) -> dict:
        """
        MANDATORY POST-GENERATION VALIDATION
        Run this on your draft response BEFORE sending.
        Returns validation result. If invalid, you MUST regenerate.
        """
        result = self.guardian.validate_output(draft_output, user_input)
        
        # Log validation
        validation_record = {
            "timestamp": datetime.now().isoformat(),
            "draft_length": len(draft_output),
            "valid": result["valid"],
            "errors": result["errors"],
            "warnings": result["warnings"],
        }
        self.execution_log.append(validation_record)
        
        return result
    
    def enforce_hard_limits(self, call_count: int) -> bool:
        """Check hard limits - return False if limit exceeded"""
        MAX_CALLS = 150
        if call_count >= MAX_CALLS:
            return False
        return True
    
    def get_execution_summary(self) -> dict:
        """Get summary of this session's execution"""
        return {
            "total_executions": len(self.execution_log),
            "calls_remaining": 150 - len([e for e in self.execution_log if "gates" in e]),
            "triggers_fired": sum(1 for e in self.execution_log if e.get("triggered")),
        }


# ─── GLOBAL SINGLETON ───
_GLOBAL_HOOK = None

def get_execution_hook() -> SentinelExecutionHook:
    """Get or create the global execution hook"""
    global _GLOBAL_HOOK
    if _GLOBAL_HOOK is None:
        _GLOBAL_HOOK = SentinelExecutionHook()
    return _GLOBAL_HOOK


# ─── MANDATORY ENTRY POINT ───
def mandatory_pre_response(user_input: str, current_mod: str = "A") -> str:
    """
    CALL THIS FIRST IN EVERY RESPONSE.
    Returns the honest banner that MUST be printed.
    """
    hook = get_execution_hook()
    result = hook.execute_pre_response(user_input, current_mod)
    print(result["banner"])
    return result["banner"]


def validate_before_send(draft_output: str, user_input: str) -> bool:
    """
    CALL THIS BEFORE SENDING RESPONSE.
    Returns True if valid, False if must regenerate.
    """
    hook = get_execution_hook()
    result = hook.validate_and_guard_response(draft_output, user_input)
    if not result["valid"]:
        print(f"VALIDATION FAILED: {result['errors']}")
        return False
    return True


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = ""
    
    # Test the hook
    hook = SentinelExecutionHook()
    result = hook.execute_pre_response(user_input)
    print(f"Banner: {result['banner']}")
    print(f"Gates: {result['gates']}")
    print(f"Triggered: {result['triggered']}")