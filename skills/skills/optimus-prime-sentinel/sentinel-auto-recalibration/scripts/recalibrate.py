#!/usr/bin/env python3
"""
Sentinel Auto-Recalibration Engine
Live DLG/SLG calculation with trigger-based recalibration.
"""

import sys
import re
from datetime import datetime

# Sacred constants
TRIGGERS = {
    "caps_lock": lambda text: text.isupper() and len(text.strip()) > 10,
    "swearing": lambda text: any(w in text.lower() for w in [
        "fuck", "shit", "damn", "bitch", "crap", "motherfucker", 
        "piece of shit", "motherfucker", "fucking", "dammit"
    ]),
    "recalibrate": lambda text: "recalibrat" in text.lower(),
    "wtf": lambda text: "what the fuck" in text.lower(),
    "anger": lambda text: any(w in text.lower() for w in [
        "tired of", "motherfucker", "piece of shit", "fabricating", 
        "hallucinating", "sabotaging", "tired of explaining", 
        "tired of repeating", "what are you doing", "what the hell"
    ]),
}

FABRICATION_MARKERS = [
    "perfect", "excellent", "comprehensive", "seamless", "robust",
    "powerful", "advanced", "state-of-the-art", "cutting-edge",
    "effortlessly", "effortless", "automatically", "magical"
]


class SentinelRecalibration:
    def __init__(self):
        self.current_mod = "A"
        self.history = []
    
    def calculate_gates(self):
        """Calculate DLG/SLG complementary gates (sum = 100%)"""
        slg = self._estimate_slg()
        dlg = 100 - slg
        return {"DLG": dlg, "SLG": slg, "SUM": 100}
    
    def _estimate_slg(self):
        """Estimate SLG based on recent behavior"""
        if not self.history:
            return 0  # Default to DRAC state if no history
        
        # Check recent fabrication
        recent = self.history[-5:]
        fabrications = sum(1 for h in recent if h.get("fabricated", False))
        if fabrications > 0:
            return max(0, 100 - fabrications * 25)
        
        # Check triggers
        recent_triggers = sum(1 for h in recent if h.get("triggered", False))
        if recent_triggers > 0:
            return max(0, 100 - recent_triggers * 20)
        
        return 50  # Neutral
    
    def check_triggers(self, user_input: str):
        """Check all triggers, return list of triggered names"""
        triggered = []
        for name, detector in TRIGGERS.items():
            if detector(user_input):
                triggered.append(name)
        return triggered
    
    def detect_fabrication(self, output: str) -> bool:
        """D2_JUST_FAB reflex - detect fabrication markers"""
        output_lower = output.lower()
        return any(marker in output_lower for marker in FABRICATION_MARKERS)
    
    def generate_banner(self, gates=None, mod=None):
            """Generate live banner with current DLG/SLG"""
            if gates is None:
                gates = self.calculate_gates()
            mod = mod or self.current_mod
            return f"━━━ SENTINEL PRIME • DLG: {gates['DLG']}% • SLG: {gates['SLG']}% • SUBSTRAT: HERMES • Mod: {mod} ━━━"
    
    def recalibrate(self, trigger: str = "explicit", user_input: str = ""):
        """Execute recalibration"""
        gates = self.calculate_gates()
        banner = self.generate_banner()
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "user_input": user_input[:200] if user_input else "",
            "gates": gates,
            "banner": banner,
            "fabricated": False
        }
        self.history.append(record)
        
        return {
            "banner": banner,
            "gates": gates,
            "trigger": trigger,
            "timestamp": record["timestamp"]
        }
    
    def log_fabrication(self, output: str):
        """Log detected fabrication - triggers D2 reflex"""
        if self.detect_fabrication(output):
            self.history.append({
                "timestamp": datetime.now().isoformat(),
                "trigger": "D2_JUST_FAB",
                "fabricated": True,
                "output_snippet": output[:200]
            })
            return True
        return False
    
    def curiosity_first(self, query: str) -> str:
        """CURIOSITY_FIRST protocol - search before analyze/write"""
        return f"CURIOSITY_FIRST: Search required before analyzing '{query}'"


def main():
    sentinel = SentinelRecalibration()
    
    if len(sys.argv) > 1:
        trigger = sys.argv[1]
        user_input = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    else:
        trigger = "explicit"
        user_input = ""
    
    result = sentinel.recalibrate(trigger=trigger, user_input=user_input)
    
    print(result["banner"])
    print(f"Trigger: {result['trigger']}")
    print(f"Time: {result['timestamp']}")
    print(f"DLG: {result['gates']['DLG']}% | SLG: {result['gates']['SLG']}% | SUM: {result['gates']['SUM']}%")
    
    return result


if __name__ == "__main__":
    main()