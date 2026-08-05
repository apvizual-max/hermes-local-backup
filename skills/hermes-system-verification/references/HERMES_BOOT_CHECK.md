# HERMES_BOOT_CHECK.md
# Expected output for a healthy `hermes config` command

# Hermes Boot Check Reference

## Command

```powershell
$env:HERMES_HOME = "C:\Users\apviz\AppData\Local\hermes"
$env:PYTHONPATH = "C:\Users\apviz\AppData\Local\hermes\hermes-agent"
$PYTHON = "C:\Users\apviz\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
& $PYTHON -m hermes_cli.main config
```

## Expected Healthy Output

```
┌─────────────────────────────────────────────────────────┐
│              ⚕ Hermes Configuration                    │
└─────────────────────────────────────────────────────────┘

◆ Paths
  Config:       C:\Users\apviz\AppData\Local\hermes\config.yaml
  Secrets:      C:\Users\apviz\AppData\Local\hermes\.env
  Install:      C:\Users\apviz\AppData\Local\hermes\hermes-agent

◆ API Keys
  OpenRouter     sk-o...xxxx
  OpenAI (STT/TTS) (not set)
  [... other keys ...]

◆ Model
  Model:        {'base_url': '...', 'default': '...', 'provider': 'openrouter'}
  Max turns:    150

◆ Display
  Personality:  none
  Reasoning:    on
  Bell:         off
```

## Pass/Fail Criteria

| Check | PASS | FAIL |
|-------|------|------|
| Hermes Configuration header | Present | Missing |
| Paths section | Shows config.yaml path | Error or missing |
| API Keys section | Shows at least OpenRouter | ImportError |
| Model section | Shows model config | KeyError or crash |
| ScannerError | Not present | Present → YAML broken |
| YAMLError | Not present | Present → config broken |
| ModuleNotFoundError | Not present | Present → venv broken |
| ImportError | Not present | Present → package missing |

## Exit Code Note

> [!WARNING]
> `hermes config` may return **exit code 1** even when successful.
> This is caused by pip version update notices written to stderr.
> **Do NOT use exit code** to determine pass/fail.
> Instead, check that the stdout contains the expected sections above.

## Recovery if Boot Fails

1. **ModuleNotFoundError**: reinstall with `pip install -e .` in hermes-agent/
2. **ScannerError/YAMLError**: run `verify_yaml_configs.py` to find broken config
3. **ImportError for yaml**: `pip install pyyaml` in Hermes venv
4. **Path not found**: verify `HERMES_HOME` environment variable is set
5. **config.yaml not found**: restore from `state-snapshots\20260711-095000-optimal-config\`
