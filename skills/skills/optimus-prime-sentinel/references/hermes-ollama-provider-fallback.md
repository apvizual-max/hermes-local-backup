# Hermes Ollama Provider Fallback — Observed Behavior

## Symptom
After setting provider/model via CLI:
- `hermes config set model.provider ollama`
- `hermes config set model.default <local-model>`
- `hermes config set providers.ollama.base_url http://localhost:11434/v1`
- `hermes config set providers.ollama.api_key ollama`
- `hermes config set fallback_providers '[\"ollama\"]'`

Running `hermes -p <profile> model` may still show:
- `Warning: Unknown provider 'ollama'. Check 'hermes model' for available providers, or run 'hermes doctor' to diagnose config issues. Falling back to auto provider detection.`
- Active provider becomes an unrelated cloud provider despite YAML saying `ollama`

## Implication
Writing YAML/config keys is not equivalent to registering the provider in Hermes' runtime provider registry. Treat CLI-selected provider as the source of truth, not manual config writes alone.

## Verified Probe Pattern
Run in order:
1. `hermes -p default model`
2. `hermes -p prime model`
3. `hermes -p assist model`
Inspect "Active provider:" and "Current model:" lines for each profile.

## Fix Path
Use `hermes model` interactive flow or provider CLI registration Hermes expects; do not rely on `hermes config set model.provider ollama` as a standalone config.
