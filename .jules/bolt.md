## 2024-03-24 - Redundant Validation Checks
**Learning:** Found a codebase-specific anti-pattern in `enforcement_engine.py` where hardcoded lists used for text filtering (`FORBIDDEN_TERMS`) contained over 50% duplicate entries. Since this is on the agent's hot path (pre-response output validation), these duplicates caused redundant O(N) full-text searches for every response.
**Action:** When working with hardcoded validation lists in hot paths, ensure they are deduplicated (e.g., using `set()` or removing manual duplicates) to minimize unnecessary string traversals.
