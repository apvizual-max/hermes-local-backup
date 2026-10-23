## 2023-10-23 - Batch File I/O in Processing Scripts
**Learning:** Found O(n) file I/O operations (open/write/close) inside tight inner loops in data processing scripts (`scripts/process_to_completion.py`, etc.). This causes severe performance degradation when processing thousands of files.
**Action:** Always batch I/O operations by accumulating results in memory (e.g., using a list buffer) and writing them all at once per batch or per file, reducing the overhead of context switching and file descriptor management.
