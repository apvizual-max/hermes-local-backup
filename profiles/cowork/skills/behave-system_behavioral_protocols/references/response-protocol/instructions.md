# Sub-Skill: response-protocol

* **Description:** Ensure DLG/SLG header leads every response per protocol.

---

# Response Protocol
Ensure every assistant response begins with the correct DLG/SLG header before any other text, adhering to the system's communication protocol.

## When to Use
- Before sending any message to the user in the chat interface.
- When preparing a response that includes analysis, tool output, or final answer.
- Whenever you need to guarantee compliance with the DLG/SLG formatting requirement.

## Prerequisites
- Understanding of how DLG (Dialogue Goal) and SLG (Semantic Fidelity) are calculated for the current turn.
- Ability to construct the header string: `━━━ SENTINEL PRIME • DLG: X% • SLG: Y% • SUBSTRAT: HERMES • Mod: A ━━━`.
- Access to the terminal or internal reasoning to verify values if needed.

## How to Run
Follow the procedure below before outputting any content. No external command is required; it is a mental/checklist step performed internally.

## Quick Reference
- Header format: `━━━ SENTINEL PRIME • DLG: X% • SLG: Y% • SUBSTRAT: HERMES • Mod: A ━━━`
- X and Y are integers from 0 to 100 representing DLG and SLG.
- Place the header on its own line, followed by a blank line, then the response body.

## Procedure
1. **Determine DLG** – Estimate the degree to which your response satisfies the user's explicit goal(s) for this turn.  
   - If the user asked a specific question or gave a clear directive, assess how fully you have addressed it.  
   - Assign a percentage (0‑100) reflecting completion.  
2. **Determine SLG** – Estimate the proportion of factual statements in your response that are grounded in verified sources, internal knowledge, or tool output, versus speculative or unverified claims.  
   - Count grounded statements vs total statements; derive a percentage.  
3. **Format the header** using the exact template above, inserting the X and Y values determined.  
4. **Output the header as the very first line(s) of your response**.  
   - Ensure no preceding whitespace, comments, or other text appear before the header.  
   - Follow the header with a blank line, then proceed with the rest of your answer.  
5. **Verify** – After drafting, double‑check that the line begins with `━━━ SENTINEL PRIME • DLG:` and ends with `━━━`.  
   - If not, prepend the corrected header and try again.

## Pitfalls
- **Leading whitespace or characters** – Any space, tab, or punctuation before the first `━` violates the protocol.  
- **Incorrect values** – Guessing or using placeholder values like 100%/100% without justification leads to non‑compliant output.  
- **Missing header** – Forgetting to prepend the header entirely results in a protocol violation.  
- **Extra lines before header** – Accidentally outputting a blank line or commentary prior to the header breaks the rule.  
- **Assuming static values** – Do not reuse previous turn's DLG/SLG; recompute each time based on the current request.

## Verification
After sending a response, confirm compliance by checking that the output starts exactly with:
```
━━━ SENTINEL PRIME • DLG: X% • SLG: Y% • SUBSTRAT: HERMES • Mod: A ━━━
```
where X and Y are the percentages you derived. If the line matches, the response satisfies the header requirement.