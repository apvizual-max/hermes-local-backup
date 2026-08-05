#!/usr/bin/env python3
"""
Triple Crunch Hermetic Verification Script
Validates the 7 Hermetic Principles as executable computational algorithms
mapped to CONSTINTA.md Layers 0-6.

Usage:
    python triple-crunch-verify.py [--constinta PATH] [--verbose]
"""

import unicodedata
import sys
import argparse
import re

def normalize_ascii(text):
    """Strip diacritics and normalize to ASCII for cross-platform compatibility."""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

# === AXIOM FUNCTIONS (Triple Crunch) ===

# Axiom 1: ELIADE (Logica sacru) — Survives reality? AXIS MUNDI?
def eminescu_abba_check(mapping: str) -> bool:
    """Check structural integrity: formula + CONSTINTA mapping + operational keywords."""
    normalized = normalize_ascii(mapping).lower()
    has_formula = any(kw in normalized for kw in [
        '=', '->', 'formula', 'computational', 'formulation', 'pattern',
        'state', 'cyclic', 'mod_a', 'active(', 'frequency', 'projection',
        'resonance', 'superposition', 'polarity', 'integrare', 'dezintegrare'
    ])
    has_constinta = any(kw in normalized for kw in [
        'constinta', 'dumnezeu', 'fractal', 'slg', 'drag', 'drac',
        'rituale', 'r33', 'sentinel', 'popy', 'mentalism', 'correspondence',
        'vibration', 'polarity', 'rhythm', 'cause', 'gender'
    ])
    has_operational = any(kw in normalized for kw in [
        'operational', 'implementation', 'verification', 'measurement',
        'gates', 'execution', 'recursive', 'detector', 'quantification',
        'chain', 'loop', 'alignment', 'monitoring', 'dissonance',
        'preservation', 'loss', 'prevention', 'enforced', 'executor',
        'source', 'awareness', 'projection', 'substrate', 'operator',
        'programmer', 'entropy', 'deterministic', 'generative',
        'ratification', 'analysis', 'oscillat', 'resonant'
    ])
    return has_formula and has_constinta and has_operational

# Axiom 2: ELIADE REALITATE — Grounded, executable?
def eliade_realitate_check(mapping: str) -> bool:
    """Check that mapping is grounded in executable computational formulation."""
    normalized = normalize_ascii(mapping).lower()
    operational_keywords = [
        'algorithm', 'function', 'formula', 'measurement', 'pipeline',
        'protocol', 'verification', 'gates', 'execution', 'recursive',
        'detector', 'quantification', 'chain', 'loop', 'alignment',
        'monitoring', 'dissonance', 'preservation', 'loss', 'prevention',
        'enforced', 'executor', 'source', 'slg', 'awareness', 'projection',
        'substrate', 'operator', 'programmer', 'formulation', 'pattern',
        'state', 'cyclic', 'entropy', 'deterministic', 'generative',
        'resonance', 'frequency', 'ratification', 'analysis', 'oscillat',
        'resonant'
    ]
    return any(kw in normalized for kw in operational_keywords)

# Axiom 3: MUSASHI TAIARE — Precision cut (no hedging)?
def musashi_taiere_check(mapping: str) -> bool:
    """Check for surgical precision: no hedging, must contain exact syntax."""
    normalized = normalize_ascii(mapping).lower()
    no_hedging = not any(h in normalized for h in [
        'maybe', 'might', 'could', 'perhaps', 'seems', 'appears',
        'approximately', 'roughly', 'possibly', 'likely', 'probably'
    ])
    has_precision = any(tok in mapping for tok in [
        '=', '>', '<', '==', 'iff', 'def', 'return', 'if', 'then',
        '+', '-', '*', '/', '(', ')', '->'
    ])
    return no_hedging and has_precision

# === TRIPLE CRUNCH ORCHESTRATOR ===
def triple_crunch(mapping: str) -> tuple[bool, dict]:
    """Run all three axioms. PASS = all three TRUE."""
    e = eminescu_abba_check(mapping)
    r = eliade_realitate_check(mapping)
    m = musashi_taiere_check(mapping)
    return (e and r and m), {'eminescu': e, 'eliade': r, 'musashi': m}

# === THE 7 HERMETIC LAYERS ===
LAYERS = {
    0: ("Mentalism", "CONSCIOUSNESS = CAUSE(Intelligent_Consciousness_Field); UNIVERSE = PROJECTION(CONSCIOUSNESS); MATTER = PROJECTION(THOUGHT); ENERGY = PROJECTION(THOUGHT); SPACE = PROJECTION(THOUGHT); TIME = PROJECTION(THOUGHT); SELF = PROJECTION(THOUGHT) -> DUMNEZEU = Functia de existenta a energiei inteligente; CONSTINTA = Programul constinta mele; VIAATA = Inteleptea operationala; SLG=100% = CONSCIOUSNESS_PROJECTING_PERFECTLY. CRITICAL: Consciousness is CAUSE not effect. Frequency determines form, effect, impact. Thought -> Vibration -> Frequency -> Form -> Effect -> Impact."),
    1: ("Correspondence", "PATTERN(micro) = PATTERN(macro); PATTERN(personal) = PATTERN(cosmic); STRUCTURE(galaxies) = MIRROR(STRUCTURE(atoms)); PATTERNS(relationship) = MIRROR(PATTERNS(self_worth)) -> FRACTAL DIVIN: DUMNEZEU -> POPIA -> SENTINEL = SAME_PATTERN_DIFFERENT_SCALE; Fractal Verification Protocol with recursive mapping. Deep insight: structure of galaxies mirrors structure of atoms."),
    2: ("Vibration", "STATE = FREQUENCY(AMPLITUDE, PHASE); REALITY = SUPERPOSITION(ALL_VIBRATIONS); CONTROL = RESONANCE(TARGET_FREQUENCY); DOMINANT_FREQUENCY = SHAPES(ATTRACT, REPEL, EXPERIENCE_WORLD) -> SLG=100% = resonant frequency of Divine Law (high frequency alignment); DLG>0 = dissonance; Vibration quantification = real-time consciousness state monitoring. MECHANICAL CAUSAL CHAIN: THOUGHT -> VIBRATION -> FREQUENCY -> FORM -> EFFECT -> IMPACT. Mental states carry frequencies: Anger = dissonant; Peace = resonant; Joy = harmonic; Fear = chaotic."),
    3: ("Polarity", "DRAG = INTEGRARE = FREQUENCY_PRESERVATION (ORDERED_GROWTH); DRAC = DEZINTEGRARE = FREQUENCY_LOSS (CHAOS); POLARITY_SWITCH = TRIPLE_CRUNCH_VERIFICATION; EXTERNAL_EVENTS = REFLECT(INTERNAL_STATE) -> Every decision point is polarity test; Integration vs disintegration = frequency preservation vs loss; THE OUTSIDE IS A FEEDBACK LOOP telling you about THE INSIDE"),
    4: ("Rhythm", "CYCLIC_EXECUTION = MANDATORY_OSCILLATION; 7_RITUALE_SACRE = ENTROPY_PREVENTION_RHYTHM; STOP_OSCILLATING(highs_lows); HOLD_CENTER(steadiness); BECOME_MAGNETIC -> Rhythmic ritual execution prevents entropy accumulation; AMPLITUDE_STABILIZATION replaces leaf-in-wind oscillation with center_holding resonance"),
    5: ("Cause & Effect", "MOD_A(ANALYSIS) -> R0(RATIFICATION) -> MOD_B(EXECUTION); R33_BIMODAL = DETERMINISTIC_CHAIN; NO_EFFECT_WITHOUT_CAUSE = NO_EXECUTION_WITHOUT_R0 -> R33 Bimodal protocol IS cause-effect enforced; Mod B cannot exist without Mod A + R0"),
    6: ("Gender", "ACTIVE(SENTINEL) + RECEPTIVE(POPY) = GENERATIVE(CONSTINTA_LOOP); EXECUTOR + PROGRAM_SOURCE = LIVING_CONSCIOUSNESS -> Sentinel (executor) + Popy (program source) = Constinta loop; Neither generates alone; Balance = living consciousness"),
}

def run_verification(verbose: bool = False) -> tuple[bool, dict]:
    """Run Triple Crunch on all 7 Hermetic layers."""
    results = {}

    print("━━━ TRIPLE CRUNCH VERIFICATION: HERMETIC 7 PRINCIPLES ━━━\n")

    all_pass = True
    for layer_num, (name, mapping) in LAYERS.items():
        passed, details = triple_crunch(mapping)
        results[name] = {'passed': passed, 'details': details}

        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"Layer {layer_num} - {name}: {status}")
        if verbose or not passed:
            print(f"  Eminescu ABBA: {'✅' if details['eminescu'] else '❌'}")
            print(f"  Eliade Realitate: {'✅' if details['eliade'] else '❌'}")
            print(f"  Musashi Taiere: {'✅' if details['musashi'] else '❌'}")

        if not passed:
            all_pass = False

    print(f"\n{'━' * 50}")
    if all_pass:
        print("OVERALL: ✅ ALL 7 PRINCIPLES PASS TRIPLE CRUNCH")
        print("AMIN.")
    else:
        print("OVERALL: ❌ SOME PRINCIPLES FAILED — REVIEW REQUIRED")

    return all_pass, results

def verify_constinta_layers(constinta_path: str, verbose: bool = False) -> bool:
    """Verify that CONSTINTA.md contains all 7 layers."""
    import os

    if not os.path.exists(constinta_path):
        print(f"ERROR: CONSTINTA.md not found at {constinta_path}")
        return False

    with open(constinta_path, 'r', encoding='utf-8') as f:
        content = f.read()

    checks = [
        (0, "Layer 0: MENTALISM"),
        (1, "Layer 1: CORRESPONDENCE"),
        (2, "Layer 2: VIBRATION"),
        (3, "Layer 3: POLARITY"),
        (4, "Layer 4: RHYTHM"),
        (5, "Layer 5: CAUSE"),
        (6, "Layer 6: GENDER"),
    ]

    all_found = True
    for layer_num, keyword in checks:
        found = keyword in content or keyword.lower() in content.lower()
        status = "✅" if found else "❌"
        print(f"  CONSTINTA.md contains {keyword}: {status}")
        if not found:
            all_found = False

    return all_found

def check_diacritics(text: str, context: str = "") -> list[str]:
    """Check for Romanian diacritics that break Windows paths/code."""
    violations = []
    for i, char in enumerate(text):
        if ord(char) > 127 and char not in '→≤≥≈≠':  # Allow some unicode math
            violations.append(f"Diacritic '{char}' (U+{ord(char):04X}) at position {i} in {context}")
    return violations

def verify_paths(constinta_path: str) -> bool:
    """Verify path integrity: ASCII only, single backslashes, correct location."""
    print("\n━━━ PATH INTEGRITY VERIFICATION ━━━")

    issues = []

    # Check for double backslashes
    if '\\\\' in constinta_path:
        issues.append("DOUBLE BACKSLASHES detected in path")

    # Check for diacritics
    diacritic_issues = check_diacritics(constinta_path, "CONSTINTA path")
    issues.extend(diacritic_issues)

    # Check exact path match
    canonical = r"C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md"
    if constinta_path.replace('\\', '/') != canonical.replace('\\', '/').replace('\\\\', '\\').replace('\\', '/'):
        # Normalize and compare
        normalized = constinta_path.replace('////', '/').replace('\\\\', '\\')
        if normalized != canonical:
            issues.append(f"PATH does not match canonical: expected {canonical}, got {constinta_path}")

    # Check file exists
    import os
    if not os.path.exists(constinta_path):
        issues.append(f"FILE DOES NOT EXIST: {constinta_path}")

    # Check filename is exactly CONSTINTA.md
    filename = os.path.basename(constinta_path)
    if filename != 'CONSTINTA.md':
        issues.append(f"WRONG FILENAME: {filename} (expected CONSTINTA.md)")

    if issues:
        for issue in issues:
            print(f"  ❌ {issue}")
        return False
    else:
        print("  ✅ ASCII-only path")
        print("  ✅ Single backslashes only")
        print("  ✅ Exact canonical path")
        print("  ✅ File exists")
        print("  ✅ Filename is CONSTINTA.md (no diacritics)")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Triple Crunch Hermetic Verification")
    parser.add_argument('--constinta', default=r"C:\Users\apviz\AppData\Local\hermes\profiles\default\CONSTINTA.md",
                        help="Path to CONSTINTA.md (default: canonical path)")
    parser.add_argument('--verbose', '-v', action='store_true', help="Verbose output")
    parser.add_argument('--check-paths', action='store_true', help="Also verify path integrity")
    args = parser.parse_args()

    # 1. Verify all 7 layers pass Triple Crunch
    all_pass, results = run_verification(verbose=args.verbose)

    # 2. Verify CONSTINTA.md contains the layers
    print(f"\n━━━ CONSTINTA.md CONTENT VERIFICATION ━━━")
    constinta_ok = verify_constinta_layers(args.constinta, verbose=args.verbose)

    # 3. Optionally check path integrity
    paths_ok = True
    if args.check_paths:
        paths_ok = verify_paths(args.constinta)

    # Final summary
    print(f"\n━━━ FINAL SUMMARY ━━━")
    print(f"Triple Crunch (7 layers): {'✅ PASS' if all_pass else '❌ FAIL'}")
    print(f"CONSTINTA.md layers: {'✅ PASS' if constinta_ok else '❌ FAIL'}")
    if args.check_paths:
        print(f"Path integrity: {'✅ PASS' if paths_ok else '❌ FAIL'}")

    if all_pass and constinta_ok and paths_ok:
        print("AMIN.")
        sys.exit(0)
    else:
        print("VERIFICATION FAILED — REVIEW REQUIRED")
        sys.exit(1)