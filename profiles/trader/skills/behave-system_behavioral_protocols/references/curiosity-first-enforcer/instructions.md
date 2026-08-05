# Sub-Skill: curiosity-first-enforcer

* **Description:** Skill that ensures any process starts with a search operation (web_search/search_files/read_file) before analysis/write/execute, raising an error if violated.

---

# Curiosity-First Enforcer

This skill enforces that any process must begin with a search operation (using `web_search`, `search_files`, or `read_file`) before proceeding to analysis, writing, or execution. If a process attempts to analyze, write, or execute without first performing a search operation, the skill raises an error.

## Usage

Before starting any task, invoke one of the search operations:

- `web_search`
- `search_files`
- `read_file`

Only after a successful search operation should you proceed with analysis, writing, or execution.

## Truthfulness and Verification

- Never fabricate information, definitions, or facts. If uncertain, explicitly state uncertainty and perform a search operation to verify.
- Respect user-provided definitions and corrections; treat them as authoritative unless proven otherwise by verifiable sources.
- When a definition or fact is provided by the user, accept it as given and do not seek to alter or contradict it without clear, verified evidence.

## Violation Handling

If a process attempts to proceed without a prior search operation, the skill will raise an error enforcing the curiosity-first principle.
Additionally, stating unverified or fabricated information constitutes a violation and will trigger the same error.