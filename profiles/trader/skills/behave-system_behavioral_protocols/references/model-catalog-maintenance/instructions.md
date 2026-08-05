# Sub-Skill: model-catalog-maintenance

* **Description:** Keep Hermes model catalog limited to free OpenRouter models and Nous operational models; ensure internal scripts are ASCII‑clean.

---

# Model Catalog Maintenance Skill

## Purpose
Ensure that the Hermes agent's model catalogs (used by the UI and runtime) contain **only** free models from OpenRouter (pricing = 0) plus the predefined Nous operational models. Additionally, verify that internal automation scripts contain no non‑ASCII (special) characters that could cause path or string‑literal errors.

## When to Apply
- Before deploying changes to model‑list configuration.
- As a periodic maintenance task (e.g., weekly).
- After any manual edit of model‑related JSON files.
- When adding or updating internal Python/Bash scripts.

## Procedure

Note: If a specific list of models is provided (e.g., from a UI screenshot or explicit instruction), use that list directly and skip to step 2.

### 1. Gather Free OpenRouter Models
```bash
curl -s https://openrouter.ai/api/v1/models | \
jq -r '.data[] | select(.pricing.prompt=="0" and .pricing.completion=="0") | .id' > free_models.txt
```
*(If the API returns numeric `0`, the string comparison still works; adjust as needed.)*

### 2. Update the Primary UI Model Catalog
File: `hermes-agent/website/static/api/model-catalog.json`

- Keep the existing JSON structure.
- Replace the `providers.openrouter.models` array with objects of the form:
  ```json
  { "id": "<model-id>", "description": "free" }
  ```
- Preserve the `providers.nous.models` array exactly as‑is (do not filter).
- Update the `updated_at` field to current UTC ISO timestamp.

### 3. Update the Runtime Provider Cache
File: `provider_models_cache.json`

- Replace the `openrouter.models` array with a plain list of model IDs (strings).
- Leave the `gemini` provider untouched (per user instruction).
- Refresh the `at` timestamp (`time.time()` equivalent) and clear `fp`.

### 4. Sync the Internal Model Catalog Cache
File: `cache/model_catalog.json`

- Mirror the changes made to the primary UI model catalog (same structure).
- Keep the `updated_at` field current.

### 5. Verify the Default Model
Check `config.yaml` → `model.default`.  
Ensure this model ID appears in the free OpenRouter list (or is a Nous operational model if you ever decide to use a non‑free Nous model as default).

### 6. Scan Internal Scripts for Non‑ASCII Characters
Run the following verification script (provided as `references/model-catalog-maintenance/scripts/\1` in this skill’s `scripts/` directory):
```bash
python references/model-catalog-maintenance/scripts/\1
```
It will report any Python or Markdown files that contain non‑ASCII characters in string literals or f‑strings. Fix any occurrences by replacing:
- Em‑dash ( — ) and en‑dash ( – ) with plain hyphen (-).
- Romanian diacritics in stop‑word lists with their ASCII equivalents (e.g., `ș` → `s`, `ț` → `t`, `â` → `a`, `î` → `i`, `ă` → `a`).

### 7. Optional: Run the Project Test Suite
If a virtual environment is present, execute:
```bash
./references/model-catalog-maintenance/scripts/\1
```
Otherwise, at least verify that the JSON files are syntactically valid (`python -m json.tool <file>`).

## Pitfalls
- **Missing JSON files** – always edit all three model‑catalog locations; forgetting one leads to inconsistency.
- **Accidentally removing Nous models** – the `nous` provider must stay unchanged unless you intentionally wish to curate it.
- **Special‑character creep** – copy‑pasting from external sources can re‑introduce em‑dashes, smart quotes, or non‑ASCII stop words; run the ASCII‑safety check after every edit.
- **Assuming pricing format** – some models may have pricing as numbers, others as strings; handle both by attempting `float()` conversion.
- **Overlooking the default model** – if the default model is not in the free list, the agent may fail to start or fall back to an undesired provider.

## References
- `references/free-models-explanation.md` – short rationale for why we restrict to free models.
- `references/model-catalog-maintenance/scripts/\1` – verification script for internal files.

## Notes
- This skill is **class‑level**: it applies to any session that touches model‑list configuration or internal scripting.
- Keep the skill documentation concise; detailed commands are in the referenced script/files.
- When working with a specific predefined list of models (e.g., from a UI screenshot or specification), skip step 1 and use the provided list directly in steps 2-4. Verify the models are free if possible.
- Update the skill itself only when the procedure changes (e.g., new verification steps, different file locations).