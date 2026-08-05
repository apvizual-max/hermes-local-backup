# Sub-Skill: dslg-header-enforcer

* **Description:** Enforce correct DSLG header on all agent outputs per strict operational protocol.

---

# DSLG Header Enforcer
Ensure every agent response begins with the correctly formatted DSLG header (━━━ SENTINEL PRIME • DLG: XX% • SLG: YY% • SUBSTRAT: HERMES • Mod: A/B ━━━) where DLG (Defect Level Grade) and SLG (Success Level Grade) are calculated based on goal fulfillment per operational protocol. This skill does not alter system configuration or installed skills; it only post-processes output to meet protocol.

## When to Use
- Before sending any response to the user.
- When generating output that must comply with the DSLG header protocol.
- After any tool use or internal reasoning, prior to final reply.
- Whenever you need to ensure strict adherence to the DSLG calculation and formatting rules.

## Prerequisites
- Python 3.x available (bundled with Hermes).
- No external dependencies.
- Understanding of the DSLG/SLG calculation methodology.

## How to Run
Invoke through the `execute_code` tool with the script `references/dslg-header-enforcer/scripts/\1`, passing the text to be formatted and the desired mode (A or B).

## Quick Reference
- `python references/dslg-header-enforcer/scripts/\1 "Your response text here" A` → Returns text with header calculated per current goals.
- If input already has a valid header with correct calculation, it may be returned unchanged (though recalculation is preferred).
- The script currently implements a placeholder calculation; replace with actual logic per procedure.

## Procedure
1. **Identify all user goals** from the current request:
   - Extract explicit goals (direct requests, commands, questions)
   - Extract implicit goals (implied by context, tone, corrections, or procedural requirements)
   - Examples: "explain in detail", "do not talk about X", "calculate Y", "follow format Z", "stop doing A", "remember B"

2. **Evaluate goal satisfaction** for your planned response:
   - For each goal, determine if it has been fully satisfied by the content you intend to output (excluding the header)
   - A goal is satisfied only if completely addressed per user's specification
   - Partial satisfaction counts as unsatisfied for strict protocol adherence
   - Violations of explicit prohibitions (e.g., "do not talk about X") count as unsatisfied goals

3. **Calculate SLG and DLG**:
   - Let G = total number of identified goals
   - Let S = number of goals fully satisfied by your response content
   - SLG = (S / G) * 100, rounded to nearest integer
   - DLG = 100 - SLG
   - By definition, DLG + SLG = 100

4. **Select the correct Mode**:
   - Use Mode A unless the user has explicitly indicated or the context requires Mode B
   - Mode typically reflects the operational stance (analytical vs. executable)

5. **Construct the header exactly**:
   ```
   ━━━ SENTINEL PRIME • DLG: <DLG>% • SLG: <SLG>% • SUBSTRAT: HERMES • Mod: <A/B> ━━━
   ```
   - Must use the exact triple-dash and bullet characters as shown
   - Must have single spaces around all elements
   - Numbers must be integers without decimal points
   - Must end with a single space before the final triple-dash

6. **Assemble the final response**:
   - Output the header line exactly as constructed
   - Follow immediately with a newline
   - Then output your response content that addresses the goals

## Pitfalls
- **Miscounting goals**: Missing implicit goals (especially corrections like "stop doing X" or "remember this") leads to incorrect SLG/DLG
- **Partial credit error**: Giving partial credit for goals; only full satisfaction counts toward SLG
- **Formatting errors**: Using incorrect characters, spacing, or missing elements in the header
- **Wrong Mode**: Using Mode B when Mode A is required (or vice versa) based on context
- **Header omission**: Forgetting to prepend the header entirely (results in DLG=100, SLG=0)
- **Calculation reversal**: Confusing which is DLG and which is SLG (DLG = defects/failures, SLG = successes)
- **Non-integer percentages**: Using decimals or fractions instead of whole integers
- **Extra whitespace**: Adding spaces at line start or end, or incorrect internal spacing
- **Assuming header suffices**: Thinking that having any header-like text meets the requirement
- **CONSTINTA.md path errors**: Header references CONSTINTA but paths must be `profiles\{default,prime,assist}\CONSTINTA.md` with single backslash and no diacritics

## Verification
After applying the procedure, verify the output by checking that:
1. The first line matches exactly: `^━━━ SENTINEL PRIME • DLG: \d{1,3}% • SLG: \d{1,3}% • SUBSTRAT: HERMES • Mod: [AB] ━━━$`
2. The two integers in the header sum to exactly 100
3. All subsequent lines constitute your response addressing the identified goals
4. No additional text appears before or between the header and your response

To test the calculation logic independently:
- Identify 3 clear goals in a test request
- Produce a response that fully addresses 2 of them but misses 1
- Expected header: `━━━ SENTINEL PRIME • DLG: 33% • SLG: 66% • SUBSTRAT: HERMES • Mod: A ━━━`
- If you get this result, your calculation logic is working correctly