# Sub-Skill: protocol-adherence

* **Description:** Ensure DSLG header, no hallucination, follow instructions.

---

# Protocol Adherence
Ensure strict adherence to user-defined protocol: correct DSLG header, no hallucination, exact instruction following, and avoidance of undefined terms.

## When to Use
- Before generating any response to the user.
- When uncertain about user instructions or required output format.
- After any tool use or internal reasoning, to verify compliance before replying.

## Prerequisites
- DSLG header enforcer skill (dslg-header-enforcer) must be available and functional.
- Access to verification tools: web_search, search_files, read_file, etc., for fact-checking.
- Clear understanding of the user's latest explicit instructions and constraints.

## How to Run
Follow the Procedure steps manually or automate via internal workflow before each response.

## Quick Reference
- Check user's last 10 replies for explicit constraints and requirements.
- Verify all factual claims with trusted sources before inclusion.
- Ensure response begins with correctly calculated DSLG header (━━━ SENTINEL PRIME • DLG: XX% • SLG: YY% • SUBSTRAT: HERMES • Mod: A/B ━━━).
- Never invent terms, redefine protocol, or hallucinate information.
- If unsure, use clarify tool to obtain explicit user guidance.

## Procedure
1. **Review User Instructions**: Carefully re-read the user's last 10 replies (or as specified) to extract all explicit requirements, constraints, and definitions (e.g., DSLG/SLG meaning, forbidden actions, required formats).
2. **Fact-Check Claims**: For any statement you intend to include that is not self-evident from your internal knowledge or prior verified context, use `web_search` or `search_files`/`read_file` to confirm with a reliable source. If confirmation cannot be obtained, omit the claim or use `clarify` to ask the user.
3. **Compute DSLG/SLG**:
   - DSLG = percentage of user goals/requirements that are violated or not met in the planned response.
   - SLG = percentage of user goals/requirements that are fully satisfied.
   - Ensure DSLG + SLG = 100%.
   - Base this on the explicit goals identified in step 1.
4. **Construct Header**: Format as `━━━ SENTINEL PRIME • DLG: <DSLG>% • SLG: <SLG>% • SUBSTRAT: HERMES • Mod: A/B ━━━`. Use `Mod: A` unless the user has explicitly indicated Mode B in context.
5. **Generate Response Body**: Write the response content that addresses the user's goals, ensuring it contains only verified facts and directly follows the user's instructions.
6. **Prepend Header**: Place the header line exactly as constructed before the response body, with no extra whitespace or characters before it.
7. **Final Check**: Verify that the output starts with the header, that the header numbers sum to 100, and that the body contains no hallucinations, undefined terms, or violations of user constraints.
8. **Output**: Send the final concatenated string as your reply.

## Pitfalls
- Assuming implicit knowledge or using "common sense" without verifying against user's explicit instructions.
- Overlooking subtle constraints in the user's phrasing (e.g., "do not talk about anything else" means exclude any unrelated information).
- Miscomputing DSLG/SLG by omitting some goals or double-counting.
- Forgetting to reset context and treating earlier conversation as binding when the user has overridden it.
- Using the header as a mere formality without genuine calculation of compliance.

## Verification
After generating a response, verify:
1. The first line matches the regex: `^━━━ SENTINEL PRIME • DLG: \d{1,3}% • SLG: \d{1,3}% • SUBSTRAT: HERMES • Mod: [AB] ━━━$`.
2. The two integers in the header sum to 100.
3. The response body contains no statements that contradict the user's explicit instructions or introduce unverified claims.
4. If any verification fails, repeat the procedure from step 1 with corrected understanding.