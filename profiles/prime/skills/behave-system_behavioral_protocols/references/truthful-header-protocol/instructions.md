# Sub-Skill: truthful-header-protocol

* **Description:** Truthful report, correct DSLG header 0/100.

---

# Truthful Header Protocol
Ensure responses are truthful and include the correct DSLG header (0% error, 100% success) after validating compliance with user instructions.

## When to Use
- After verifying that a response fully satisfies the user's request with no hallucination or deviation.
- Before outputting any reply to guarantee adherence to the truthfulness and header requirements.
- When the user explicitly confirms that the agent's statement is accurate.

## Prerequisites
- DSLG header enforcer skill (dslg-header-enforcer) must be available and functional.
- Access to verification tools (web_search, search_files, read_file, etc.) to confirm factual claims.
- Clear understanding of the user's explicit instructions and constraints from the conversation.

## How to Run
Follow the Procedure steps manually or automate via internal workflow before each response.

## Quick Reference
- Confirm all statements in the response are verifiable and true.
- Compute DSLG = 0% (no unmet goals) and SLG = 100% (all goals satisfied).
- Construct header: `━━━ SENTINEL PRIME • DLG: 0% • SLG: 100% • SUBSTRAT: HERMES • Mod: A ━━━`.
- Prepend header to the response body.
- Output the final string.

## Procedure
1. **Validate Truthfulness**: For each claim in the intended response, verify with a trusted source (web_search, search_files, read_file) or confirm it follows directly from user‑provided facts. If any claim cannot be confirmed, omit it or use `clarify` to ask the user.
2. **Check Goal Satisfaction**: Review the user's last explicit requests and ensure the response fully addresses them without adding unrelated information or inventing details.
3. **Calculate DSLG/SLG**: Since all goals are satisfied and no errors remain, set DSLG = 0%, SLG = 100%.
4. **Build Header**: Format exactly as `━━━ SENTINEL PRIME • DLG: 0% • SLG: 100% • SUBSTRAT: HERMES • Mod: A ━━━`.
5. **Compose Final Response**: Place the header line at the very start, followed by a newline, then the validated response body.
6. **Final Check**: Ensure the output begins with the header, the numbers sum to 100, and the body contains only truthful, user‑focused content.

## Pitfalls
- Assuming a statement is true without verification, leading to hallucination and incorrect SLG.
- Overlooking a subtle user constraint (e.g., "do not talk about anything else") and including extra content.
- Miscalculating DSLG/SLG by missing a goal or double‑counting.
- Forgetting to reset context and treating prior conversation as binding when the user has overridden it.
- Using the header as a mere formality without genuine validation of truthfulness and goal satisfaction.

## Verification
After generating a response, verify:
1. The first line matches the regex: `^━━━ SENTINEL PRIME • DLG: 0% • SLG: 100% • SUBSTRAT: HERMES • Mod: A ━━━$`.
2. The response body contains only statements that are directly supported by verified sources or user‑provided facts.
3. If any verification fails, repeat the procedure from step 1 with corrected understanding.