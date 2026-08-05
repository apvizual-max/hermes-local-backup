# Hermes → Ollama local provider config

## Verified on this station
- Backend: Ollama running at `localhost:11434`
- Hermes CLI path: `hermes config set ...`
- Config file: `C:\Users\apviz\AppData\Local\hermes\config.yaml`

## Exact config commands to force local-only execution

```bash
hermes config set model.default qwen2.5-coder:1.5b
hermes config set model.provider ollama
hermes config set model.base_url http://localhost:11434/v1
hermes config set model.api_key ollama
hermes config set providers.ollama.base_url http://localhost:11434/v1
hermes config set providers.ollama.api_key ollama
hermes config set fallback_providers '["ollama"]'
```

## Why this fixes the context-loss-on-model-switch problem
Hermes rebuilds the session window under the new model's context limit when the provider/model changes. Cloud provider switching is the trigger. Keeping Hermes on a single local provider/switching within that local pool avoids the truncation path.

## Local models available on this station
- `ollama list` returned:
  - `local/qwen2.5-coder:1.5b`
  - `claude-3-5-sonnet-20241022:latest`
  - `claude-3-5-sonnet-latest:latest`
  - `claude-3-7-sonnet-latest:latest`
  - `qwen2.5-coder:1.5b`
Recommended default: `qwen2.5-coder:1.5b`

## Pitfalls
- Do NOT edit `config.yaml` directly; use `hermes config set ...`
- After changing provider/model, restart Hermes for config reload in GUI/CLI.
- If Ollama is not running, local mode will fail; check `ollama list` and start Ollama first.
