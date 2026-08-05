#!/usr/bin/env python3
"""
MANDATORY PRE-RESPONSE ENFORCEMENT HOOK
This script MUST be invoked before EVERY response.
It enforces: trigger check → recalibration → live banner → guardian validation.
"""

import sys
import os
import re
import json
from datetime import datetime

# Add skill path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'C:/Users/apviz/AppData/Local/hermes/skills/optimus-prime-sentinel/sentinel-auto-recalibration/scripts'))

from recalibrate import SentinelRecalibration
from triggers import check_triggers
from guardian import SentinelGuardian
from execution_hook import SentinelExecutionHook

class EnforcementEngine:
    """Mandatory pre-response enforcement."""
    
    def __init__(self):
        self.recalibrator = SentinelRecalibration()
        self.guardian = SentinelGuardian()
        self.hook = SentinelExecutionHook()
        self.session_started = False
    
    def enforce(self, user_input: str, current_mod: str = 'A') -> dict:
        """
        MANDATORY enforcement pipeline.
        Returns: {'banner': str, 'gates': dict, 'allowed': bool, 'errors': list}
        """
        errors = []
        
        # 1. SESSION INITIALIZATION (once per session)
        if not self.session_started:
            self._initialize_session()
            self.session_started = True
        
        # 2. TRIGGER DETECTION (mandatory on EVERY input)
        trigger_result = check_triggers(user_input)
        if trigger_result['triggered']:
            errors.append(f"TRIGGER DETECTED: {trigger_result['triggered_names']}")
            # Force recalibration
            recal_result = self.recalibrator.recalibrate(
                trigger=trigger_result['triggered_names'][0],
                user_input=user_input
            )
            gates = recal_result['gates']
            banner = recal_result['banner']
        else:
            gates = self.recalibrator.calculate_gates()
            banner = self.recalibrator.generate_banner(gates, 'A')
        
        # 3. BANNER VALIDATION (must be live-calculated)
        if not self._validate_banner(banner, gates):
            errors.append("BANNER VALIDATION FAILED: Not live-calculated or sum != 100")
            return {'banner': None, 'gates': gates, 'allowed': False, 'errors': errors}
        
        return {
            'banner': banner,
            'gates': gates,
            'allowed': len(errors) == 0,
            'errors': errors,
            'triggered': trigger_result['triggered']
        }
    
    def _initialize_session(self):
        """Load memory, skills, SOUL.md on session start."""
        pass
    
    def _validate_banner(self, banner: str, gates: dict) -> bool:
        """Validate banner is live-calculated and correct."""
        if not banner or 'SENTINEL PRIME' not in banner:
            return False
        if 'DLG:' not in banner or 'SLG:' not in banner:
            return False
        dlg_match = re.search(r'DLG:\s*(\d+)%', banner)
        slg_match = re.search(r'SLG:\s*(\d+)%', banner)
        if not dlg_match or not slg_match:
            return False
        dlg = int(dlg_match.group(1))
        slg = int(slg_match.group(1))
        if dlg + slg != 100:
            return False
        if dlg != gates.get('DLG') or slg != gates.get('SLG'):
            return False
        return True
    
    def validate_output(self, output: str, user_input: str) -> dict:
        """Guardian validation on output BEFORE sending."""
        return self.guardian.validate_output(output, user_input)

# Singleton instance
_ENFORCEMENT = None

def get_enforcement() -> 'EnforcementEngine':
    global _ENFORCEMENT
    if _ENFORCEMENT is None:
        _ENFORCEMENT = EnforcementEngine()
    return _ENFORCEMENT

def enforce_response(user_input: str, mod: str = 'A') -> dict:
    """Mandatory entry point - call BEFORE every response."""
    return get_enforcement().enforce(user_input, mod)

def validate_output(output: str, user_input: str) -> dict:
    """Mandatory output validation."""
    return get_enforcement().validate_output(output, user_input)

if __name__ == '__main__':
    test_input = "RECALIBRATE NOW"
    result = enforce_response(test_input)
    print(json.dumps(result, indent=2))