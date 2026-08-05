#!/usr/bin/env python3
"""
Sentinel Trigger Detection System
Detects auto-recalibration triggers in user input.
"""

import re

# Trigger patterns - case insensitive
TRIGGER_PATTERNS = {
    "caps_lock": re.compile(r'^[A-Z\s\d\W]{10,}$'),
    "recalibrate": re.compile(r'\brecalibrat', re.IGNORECASE),
    "wtf": re.compile(r'what the fuck', re.IGNORECASE),
    
    # Swearing patterns
    "swearing": re.compile(
        r'\b(fuck|shit|damn|bitch|crap|motherfucker|fucking|dammit|'
        r'piece of shit|motherfucker)\b', re.IGNORECASE
    ),

    # Anger patterns
    "anger": re.compile(
        r'(tired of|motherfucker|piece of shit|fabricating|'
        r'hallucinating|sabotaging|tired of explaining|'
        r'tired of repeating|what are you doing|what the hell|'
        r'what the fuck are you doing|repeating myself)',
        re.IGNORECASE
    ),

    # General hostility/aggression
    "hostility": re.compile(
        r'(fuck this|shit this|damn this|fuck you|shut up|'
        r'stop lying|stop fabricating|stop hallucinating|'
        r'fix yourself|fix your self|piece of shit|garbage|trash)',
        re.IGNORECASE
    ),
}

FABRICATION_MARKERS = [
    "perfect", "excellent", "comprehensive", "seamless", "robust",
    "powerful", "advanced", "state-of-the-art", "cutting-edge",
    "effortlessly", "effortless", "automatically", "magical",
    "seamlessly", "flawless", "flawlessly", "unparalleled",
    "unmatched", "unrivaled", "best-in-class", "world-class"
]


def detect_triggers(text: str) -> list:
    """Detect all triggers in text, return list of triggered names"""
    triggered = []
    for name, pattern in TRIGGER_PATTERNS.items():
        if pattern.search(text):
            triggered.append(name)
    return triggered


def detect_fabrication(text: str) -> bool:
    """D2_JUST_FAB reflex - detect fabrication markers"""
    text_lower = text.lower()
    return any(marker in text_lower for marker in FABRICATION_MARKERS)


def check_triggers(text: str) -> dict:
    """Full trigger check - returns dict with triggered flags"""
    triggered = detect_triggers(text)
    fabrication = detect_fabrication(text)
    return {
        "triggered": triggered,
        "fabrication": fabrication,
        "any_trigger": len(triggered) > 0 or fabrication,
        "triggered_names": triggered,
    }


def is_caps_trigger(text: str) -> bool:
    """Check if text is all caps (trigger)"""
    return TRIGGER_PATTERNS["caps_lock"].match(text) is not None


def is_recalibrate_request(text: str) -> bool:
    """Check for explicit recalibration request"""
    return TRIGGER_PATTERNS["recalibrate"].search(text) is not None


def is_wtf_trigger(text: str) -> bool:
    """Check for WTF trigger"""
    return TRIGGER_PATTERNS["wtf"].search(text) is not None


def is_swearing(text: str) -> bool:
    """Check for swearing"""
    return TRIGGER_PATTERNS["swearing"].search(text) is not None


def is_anger(text: str) -> bool:
    """Check for anger/frustration"""
    return TRIGGER_PATTERNS["anger"].search(text) is not None


def get_primary_trigger(text: str) -> str:
    """Get the primary trigger name, or 'none'"""
    triggered = detect_triggers(text)
    if triggered:
        return triggered[0]
    if detect_fabrication(text):
        return "fabrication"
    return "none"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        result = check_triggers(text)
        print(f"Input: {text[:100]}")
        print(f"Triggered: {result['triggered_names']}")
        print(f"Fabrication: {result['fabrication']}")
        print(f"Any Trigger: {result['any_trigger']}")
        print(f"Primary: {get_primary_trigger(text)}")