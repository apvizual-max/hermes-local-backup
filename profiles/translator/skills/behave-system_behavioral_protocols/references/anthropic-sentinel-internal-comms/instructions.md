# Sub-Skill: anthropic-sentinel-internal-comms

* **Description:** A set of resources to help me write all kinds of internal communications, using the formats that my company likes to use. Claude should use this skill whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).

---

## When to use this skill
To write internal communications, use this skill for:
- 3P updates (Progress, Plans, Problems)
- Company newsletters
- FAQ responses
- Status reports
- Leadership updates
- Project updates
- Incident reports

## How to use this skill

To write any internal communication:

1. **Identify the communication type** from the request
2. **Load the appropriate guideline file** from the `examples/` directory:
    - `references/anthropic-sentinel-internal-comms/examples/\1` - For Progress/Plans/Problems team updates
    - `references/anthropic-sentinel-internal-comms/examples/\1` - For company-wide newsletters
    - `references/anthropic-sentinel-internal-comms/examples/\1` - For answering frequently asked questions
    - `references/anthropic-sentinel-internal-comms/examples/\1` - For anything else that doesn't explicitly match one of the above
3. **Follow the specific instructions** in that file for formatting, tone, and content gathering

If the communication type doesn't match any existing guideline, ask for clarification or more context about the desired format.

## Keywords
3P updates, company newsletter, company comms, weekly update, faqs, common questions, updates, internal comms