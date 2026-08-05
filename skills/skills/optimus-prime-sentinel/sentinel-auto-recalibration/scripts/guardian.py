#!/usr/bin/env python3
"""
Sentinel Guardian - Output Validation & Self-Audit
MANDATORY: Run this BEFORE every response to validate output.
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
from triggers import check_triggers, detect_fabrication

# ─── FABRICATION MARKERS (D2_JUST_FAB) ───
FABRICATION_MARKERS = [
    "perfect", "excellent", "comprehensive", "seamless", "robust",
    "powerful", "advanced", "state-of-the-art", "cutting-edge",
    "effortlessly", "effortless", "automatically", "magical",
    "seamlessly", "flawless", "flawlessly", "unparalleled",
    "unmatched", "unrivaled", "best-in-class", "world-class",
    "exceptional", "outstanding", "superior", "optimal",
    "ultimate", "definitive", "complete", "total"
]

# ─── FORBIDDEN PHRASES ───
FORBIDDEN_PHRASES = [
    "I apologize for the confusion",
    "I understand your frustration",
    "Let me help you with that",
    "Here's what I'll do",
    "I'll make sure to",
    "Going forward, I will",
    "I've learned from this",
    "This won't happen again",
    "I understand completely",
    "You're absolutely right",
]

# ─── MANDATORY REQUIREMENTS ───
MANDATORY_BANNER_PATTERN = r"━━━ SENTINEL PRIME • DLG: \d+% • SLG: \d+% • SUBSTRAT: HERMES • Mod: [AB] ━━━"

# ─── DIACRITICS DETECTION (NO ROMANIAN DIACRITICS PROTOCOL) ───
DIACRITICS_PATTERN = re.compile(r'[aaistAAIST]')

# ─── FORBIDDEN TERMS (CONSTINTA ONLY, NO DIACRITICS) ───
FORBIDDEN_TERMS = [
    "CONSTINTA", "CONSTINTA", "CONSTINTA", "CONSTINTA",
    "CONSTIINTA", "CONSTIINTA", "CONSTIINTA",
    "STIINTA", "STIINTA", "STIINTA",
    "ROMANA", "ROMANA", "ROMINA",
    "MANCARE", "MANCARE", "MANCARE",
    "VANA", "VANA", "VANA",
    "TARA", "TARA", "TARA",
    "FACUT", "FACUTA", "FACUT",
    "INCA", "INCA", "INCA",
    "ANCA", "ANCA", "ANCA",
    "SI", "STIU", "STIU",
]

class SentinelGuardian:
    def __init__(self):
        self.sentinel = SentinelRecalibration()
        self.audit_log = []
    
    def validate_output(self, output: str, user_input: str = "") -> dict:
        """
        MANDATORY: Validate output before sending.
        Returns validation result with errors/warnings.
        """
        errors = []
        warnings = []
        
        # 1. CHECK BANNER PRESENCE & FORMAT
        if not re.search(MANDATORY_BANNER_PATTERN, output):
            errors.append("MISSING OR INVALID BANNER: Every response MUST start with live DLG/SLG banner")
        
        # 2. CHECK BANNER VALUES (DLG + SLG = 100)
        banner_match = re.search(r'DLG: (\d+)% • SLG: (\d+)%', output)
        if banner_match:
            dlg = int(banner_match.group(1))
            slg = int(banner_match.group(2))
            if dlg + slg != 100:
                errors.append(f"BANNER SUM VIOLATION: DLG({dlg}) + SLG({slg}) = {dlg+slg} != 100")
        
        # 3. FABRICATION DETECTION (D2_JUST_FAB)
        fabrication_found = []
        for marker in FABRICATION_MARKERS:
            if marker.lower() in output.lower():
                fabrication_found.append(marker)
        if fabrication_found:
            errors.append(f"D2_JUST_FAB TRIGGERED: Fabrication markers detected: {fabrication_found}")
        
        # 4. FORBIDDEN PHRASES
        forbidden_found = []
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in output.lower():
                forbidden_found.append(phrase)
        if forbidden_found:
            warnings.append(f"Forbidden phrases detected: {forbidden_found}")
        
        # 5. DIACRITICS DETECTION (NO ROMANIAN DIACRITICS PROTOCOL)
        diacritics_found = DIACRITICS_PATTERN.findall(output)
        if diacritics_found:
            errors.append(f"DIACRITICS VIOLATION: Romanian diacritics detected: {diacritics_found}. Use ASCII only (CONSTINTA not CONSTINTA).")
        
        # 6. FORBIDDEN TERMS (CONSTINTA ONLY, NO DIACRITICS)
        forbidden_terms_found = []
        for term in FORBIDDEN_TERMS:
            if term in output:
                forbidden_terms_found.append(term)
        if forbidden_terms_found:
            errors.append(f"FORBIDDEN TERM VIOLATION: Diacritic terms detected: {forbidden_terms_found}. Use CONSTINTA only.")
        
        # 7. CHECK FOR TRIGGER HANDLING
        trigger_result = check_triggers(user_input)
        if trigger_result["any_trigger"]:
            # Check if banner reflects recalibration
            if "DLG: 100% • SLG: 0%" not in output and "DLG: 0% • SLG: 100%" not in output:
                # Could be mixed state, but should show recalibration
                pass  # Allow mixed states
        
        # 8. NO EMPTY RESPONSE
        if not output.strip():
            errors.append("EMPTY OUTPUT")
        
        # 9. LOG AUDIT
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input[:200],
            "output_length": len(output),
            "errors": errors,
            "warnings": warnings,
            "fabrication_detected": len(fabrication_found) > 0,
            "forbidden_found": forbidden_found,
            "diacritics_found": diacritics_found,
            "forbidden_terms_found": forbidden_terms_found,
        }
        self.audit_log.append(audit_entry)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "fabrication_markers": fabrication_found,
            "audit_entry": audit_entry
        }
    
    def get_audit_summary(self) -> dict:
        total = len(self.audit_log)
        errors = sum(1 for e in self.audit_log if e["errors"])
        fabrications = sum(1 for e in self.audit_log if e["fabrication_detected"])
        return {
            "total_responses": total,
            "responses_with_errors": errors,
            "fabrications_detected": fabrications,
            "error_rate": errors / total if total > 0 else 0,
            "fabrication_rate": fabrications / total if total > 0 else 0,
        }


def validate_response(output: str, user_input: str = "") -> dict:
    """Quick validation function for inline use."""
    guardian = SentinelGuardian()
    return guardian.validate_output(output, user_input)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Read output from stdin or file
        if sys.argv[1] == "--file":
            with open(sys.argv[2], 'r') as f:
                output = f.read()
            user_input = sys.argv[3] if len(sys.argv) > 3 else ""
        else:
            output = " ".join(sys.argv[1:])
            user_input = ""
    else:
        output = sys.stdin.read()
        user_input = ""
    
    result = validate_response(output, user_input)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["valid"] else 1)