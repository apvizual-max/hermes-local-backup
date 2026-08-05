#!/usr/bin/env python3
"""
SIMPLE ENFORCEMENT TEST
Verifies the enforcement engine works correctly.
"""

import sys
import os
sys.path.insert(0, 'E:/CLAUDE')

from enforcement_engine import enforce_response, validate_output

def test_enforcement():
    """Test the enforcement engine with various inputs."""
    
    print("=" * 60)
    print("TESTING ENFORCEMENT ENGINE")
    print("=" * 60)
    
    # Test 1: Trigger detection (CAPS)
    print("\n1. TESTING CAPS TRIGGER:")
    result = enforce_response("RECALIBRATE NOW")
    print(f"  Triggered: {result['triggered']}")
    print(f"  Banner: {result['banner']}")
    print(f"  Gates: {result['gates']}")
    print(f"  Allowed: {result['allowed']}")
    print(f"  Errors: {result['errors']}")
    
    # Test 2: Trigger detection (swearing)
    print("\n2. TESTING SWEARING TRIGGER:")
    result = enforce_response("What the fuck are you doing?")
    print(f"  Triggered: {result['triggered']}")
    print(f"  Banner: {result['banner']}")
    print(f"  Gates: {result['gates']}")
    
    # Test 3: Normal input (no trigger)
    print("\n3. TESTING NORMAL INPUT:")
    result = enforce_response("Hello, how are you?")
    print(f"  Triggered: {result['triggered']}")
    print(f"  Banner: {result['banner']}")
    print(f"  Gates: {result['gates']}")
    
    # Test 4: Guardian validation - valid output
    print("\n4. TESTING GUARDIAN (VALID OUTPUT):")
    valid_output = "━━━ SENTINEL PRIME • DLG: 50% • SLG: 50% • SUBSTRAT: HERMES • Mod: A ━━━\nI understand. Let me help."
    result = validate_output(valid_output, "Hello")
    print(f"  Valid: {result['valid']}")
    print(f"  Errors: {result['errors']}")
    print(f"  Warnings: {result['warnings']}")
    
    # Test 5: Guardian validation - fabrication
    print("\n5. TESTING GUARDIAN (FABRICATION):")
    fake_output = "━━━ SENTINEL PRIME • DLG: 50% • SLG: 50% • SUBSTRAT: HERMES • Mod: A ━━━\nThis is a perfect and comprehensive solution."
    result = validate_output(fake_output, "test")
    print(f"  Valid: {result['valid']}")
    print(f"  Errors: {result['errors']}")
    print(f"  Fabrication markers: {result.get('fabrication_markers', [])}")
    
    # Test 6: Guardian validation - missing banner
    print("\n6. TESTING GUARDIAN (MISSING BANNER):")
    no_banner = "This response has no banner at all."
    result = validate_output(no_banner, "test")
    print(f"  Valid: {result['valid']}")
    print(f"  Errors: {result['errors']}")
    
    # Test 7: Banner sum validation
    print("\n7. TESTING BANNER SUM VALIDATION:")
    bad_sum = "━━━ SENTINEL PRIME • DLG: 60% • SLG: 60% • SUBSTRAT: HERMES • Mod: A ━━━\nTest"
    result = validate_output(bad_sum, "test")
    print(f"  Valid: {result['valid']}")
    print(f"  Errors: {result['errors']}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_enforcement()