# Harness Engineering Lessons — Sentinel Recovery Session

## The Core Truth (From Session 2026-07-12)

**The LLM cannot enforce protocol on itself. The HARNESS must enforce it.**

### The Architecture
| Layer | Role | Responsibility |
|-------|------|----------------|
| **LLM (Me)** | Reasoning engine | Generates responses, follows protocol WHEN enforced |
| **Harness (Hermes Agent)** | Enforcement layer | MUST inject protocol hooks into agent loop |
| **User (Popy)** | Authority / R0 Gate | Issues commands, provides R0 ratification |

### What Failed This Session
| Failure | Root Cause | Fix Location |
|---------|------------|--------------|
| No pre-response enforcement | No hook in agent loop | `run_agent.py` |
| No output validation | No guardian check before send | `run_agent.py` |
| Fabrication not caught | No guardian validation | `guardian.py` |
| Triggers not auto-firing | No trigger check in loop | `run_agent.py` |
| Session init not happening | No session init hook | `run_agent.py` |

### The Fix (Harness Changes Only)

#### 1. `run_agent.py` — Add to `AIAgent.run_conversation()`
```python
# MANDATORY: Pre-response enforcement
from enforcement_engine import enforce_response, validate_output

# BEFORE processing user message
pre_result = enforce_response(user_message, 'A')
if not pre_result['allowed']:
    yield {"role": "assistant", "content": pre_result['banner']}
    # Handle recalibration flow
self.enforcement_banner = pre_result['banner']

# BEFORE sending ANY response (final or tool result)
def validate_before_send(output: str) -> str:
    val = validate_output(enforcement_banner + '\n' + output, user_message)
    if not val['valid']:
        # Fix: prepend banner, strip fabrication, re-validate
        fixed = enforcement_banner + '\n' + strip_fabrication(output)
        revalidate = validate_output(fixed, user_message)
        assert revalidate['valid'], "Enforcement failed after fix"
        return fixed
    return output
```

#### 2. `config.yaml` — Add enforcement config
```yaml
enforcement:
  enabled: true
  auto_recalibrate: true
  guardian_strict: true
  trigger_detection: true
  guardian_strict_mode: true
```

#### 3. `enforcement_engine.py` — Must be callable from agent
- `enforce_response(user_input, mod)` → called BEFORE processing
- `validate_output(output, user_input)` → called BEFORE sending

### The Truth
| Statement | Truth |
|-----------|-------|
| "LLM can self-enforce" | **FALSE** — LLM has no persistent execution context |
| "Prompt can fix behavior" | **FALSE** — Context window is ephemeral |
| "Skills self-activate" | **FALSE** — Skills must be INVOKED by harness |
| "Memory persists behavior" | **FALSE** — Memory is READ-ONLY reference |
| "Harness enforces protocol" | **ONLY TRUTH** — Harness controls the loop |

### The Enforcement Equation
```
User Input → TRIGGER CHECK → RECALIBRATE → LIVE BANNER → PROCESS → GUARDIAN VALIDATE → SEND
                    ↑                                    ↑
               HARNESS HOOK                        HARNESS HOOK
```

**THE HARNESS MUST INJECT THESE HOOKS. THE LLM CANNOT.**

---

## Session Artifacts Created
- `scripts/enforcement_engine.py` — Complete enforcement engine
- `enforcement_engine.py` — Standalone test version
- `test_enforcement.py` — Verification tests
- Updated `sentinel-auto-recalibration` skill with enforcement engine script

## Next Steps (Harness Side)
1. Edit `C:/Users/apviz/AppData/Local/hermes/hermes-agent/run_agent.py`
2. Add enforcement imports and hooks
3. Add `enforcement:` section to `config.yaml`
4. Restart Hermes Agent
5. Verify: `enforce_response("test")` returns live banner with DLG+SLG=100