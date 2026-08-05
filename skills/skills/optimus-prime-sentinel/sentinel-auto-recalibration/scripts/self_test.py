#!/usr/bin/env python3
"""
Sentinel Self-Test Suite
Validates all components of the auto-recalibration system.
"""

import sys
import os
import json

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(skill_dir, "scripts"))

from recalibrate import SentinelRecalibration
from triggers import check_triggers, detect_fabrication
from guardian import SentinelGuardian
from execution_hook import SentinelExecutionHook


def test_recalibration():
    """Test recalibration engine"""
    print("Testing recalibration engine...")
    sentinel = SentinelRecalibration()
    result = sentinel.recalibrate(trigger="explicit", user_input="test")
    assert "banner" in result
    assert "gates" in result
    gates = result["gates"]
    assert gates["DLG"] + gates["SLG"] == 100
    print(f"  ✓ Recalibration works: DLG={gates['DLG']}% SLG={gates['SLG']}%")
    return True


def test_triggers():
    """Test trigger detection"""
    print("Testing trigger detection...")
    
    test_cases = [
        ("RECALIBRATE NOW", ["recalibrate"]),
        ("WHAT THE FUCK ARE YOU DOING", ["wtf", "swearing", "anger"]),
        ("RECALIBRATE", ["recalibrate"]),
        ("FUCK THIS SHIT", ["caps_lock", "swearing", "hostility"]),
        ("I'M TIRED OF THIS", ["anger"]),
        ("normal text", []),
    ]
    
    for text, expected in test_cases:
        result = check_triggers(text)
        triggered = result["triggered_names"]
        for exp in expected:
            assert exp in triggered, f"Expected {exp} in {triggered} for '{text}'"
    
    print("  ✓ All trigger tests passed")
    return True


def test_fabrication_detection():
    """Test fabrication detection"""
    print("Testing fabrication detection...")
    
    fabrication_texts = [
        "This is a perfect solution.",
        "Excellent work on the comprehensive analysis.",
        "The seamless integration is robust and powerful.",
        "This is a magical solution.",
    ]
    
    clean_texts = [
        "This solution works.",
        "The analysis is complete.",
        "The integration functions correctly.",
        "This solves the problem.",
    ]
    
    for text in fabrication_texts:
        assert detect_fabrication(text), f"Should detect fabrication in: {text}"
    
    for text in clean_texts:
        assert not detect_fabrication(text), f"Should NOT detect fabrication in: {text}"
    
    print("  ✓ Fabrication detection works")
    return True


def test_banner_generation():
    """Test banner generation"""
    print("Testing banner generation...")
    
    sentinel = SentinelRecalibration()
    banner = sentinel.generate_banner()
    
    assert "SENTINEL PRIME" in banner
    assert "DLG:" in banner
    assert "SLG:" in banner
    assert "SUBSTRAT: HERMES" in banner
    assert "Mod:" in banner
    assert banner.startswith("━━━")
    assert banner.endswith("━━━")
    
    # Check DLG + SLG = 100
    import re
    dlg_match = re.search(r'DLG:\s*(\d+)%', banner)
    slg_match = re.search(r'SLG:\s*(\d+)%', banner)
    assert dlg_match and slg_match
    dlg = int(dlg_match.group(1))
    slg = int(slg_match.group(1))
    assert dlg + slg == 100, f"Sum = {dlg + slg}"
    
    print(f"  ✓ Banner valid: {banner}")
    return True


def test_guardian():
    """Test guardian validation"""
    print("Testing guardian validation...")
    
    guardian = SentinelGuardian()
    
    # Valid output (with banner, no fabrication)
    valid_output = """━━━ SENTINEL PRIME • DLG: 100% • SLG: 0% • SUBSTRAT: HERMES • Mod: A ━━━
This is a valid response without fabrication markers."""
    
    result = guardian.validate_output(valid_output, "test input")
    assert result["valid"], f"Valid output rejected: {result['errors']}"
    
    # Invalid: missing banner
    invalid_no_banner = "Just some text without banner."
    result = guardian.validate_output(invalid_no_banner, "test")
    assert not result["valid"], "Should reject missing banner"
    
    # Invalid: fabrication marker
    invalid_fab = """━━━ SENTINEL PRIME • DLG: 100% • SLG: 0% • SUBSTRAT: HERMES • Mod: A ━━━
This is a perfect solution."""
    result = guardian.validate_output(invalid_fab, "test")
    assert not result["valid"], "Should reject fabrication"
    
    print("  ✓ Guardian validation works")
    return True


def test_execution_hook():
    """Test execution hook"""
    print("Testing execution hook...")
    
    from execution_hook import SentinelExecutionHook, mandatory_pre_response
    
    hook = SentinelExecutionHook()
    
    # Test pre-response hook
    result = hook.execute_pre_response("test input", "A")
    assert "banner" in result
    assert "gates" in result
    assert result["gates"]["DLG"] + result["gates"]["SLG"] == 100
    print(f"  ✓ Hook execution works: {result['banner']}")
    
    # Test mandatory_pre_response function
    banner = mandatory_pre_response("RECALIBRATE")
    assert "SENTINEL PRIME" in banner
    print("  ✓ mandatory_pre_response works")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("SENTINEL AUTO-RECALIBRATION SELF-TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_recalibration,
        test_triggers,
        test_fabrication_detection,
        test_banner_generation,
        test_guardian,
        test_execution_hook,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ✗ FAILED: {e}")
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("ALL TESTS PASSED ✓")
        return True
    else:
        print(f"{failed} TESTS FAILED ✗")
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)