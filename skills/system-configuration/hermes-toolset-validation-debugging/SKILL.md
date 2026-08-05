---
name: hermes-toolset-validation-debugging
description: "Debug 'Unknown toolsets' warnings in Hermes CLI startup."
version: 0.1.0
author: Sentinel Default (Orchestrator)
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, toolsets, plugins, validation, gateway, cli]
---

# Hermes Toolset Validation Debugging

## When to Use

- `Warning: Unknown toolsets: <name>` appears when running `hermes` or `hermes chat`
- `validate_toolset("<name>")` returns `False` despite the toolset being in config
- Platform plugin tools (e.g., `a2a_*`, `spotify_*`) are not registered at startup
- `ModuleNotFoundError: No module named 'gateway.config'; 'gateway' is not a package`

## Root Cause Patterns

### Pattern 1: Deferred Platform Plugin Loading

**Symptom**: Platform-provided toolsets (e.g., `a2a`, `discord`) are in `platform_toolsets.cli` config but `validate_toolset()` returns `False`.

**Cause**: Bundled platform plugins are loaded **deferred** — their `register()` function (which creates the toolset) is only called when the gateway actually needs the platform adapter. At CLI startup validation time (cli.py:4466), the toolset hasn't been registered yet.

**Fix**: In `_get_plugin_toolset_keys()` (tools_config.py), eagerly load deferred platform plugins whose toolset name matches the user's `platform_toolsets` or `known_plugin_toolsets` config entries.

```python
from hermes_cli.plugins import get_plugin_manager
mgr = get_plugin_manager()
for _key, loaded in list(mgr._plugins.items()):
    if loaded.deferred:
        _platform_name = mgr._platform_name_from_manifest(loaded.manifest)
        if _platform_name in enabled_ts:
            mgr._load_plugin(loaded.manifest)
```

### Pattern 2: Module Shadowing (gateway.py vs gateway/)

**Symptom**: `ModuleNotFoundError: No module named 'gateway.config'; 'gateway' is not a package`

**Cause**: `hermes_cli/gateway.py` (module) shadows the `gateway/` package directory. When `from gateway.config import ...` runs, Python may resolve `gateway` to the module file instead of the package.

**Fix**: In `hermes_cli/gateway.py`, insert `PROJECT_ROOT` into `sys.path` before gateway package imports:

```python
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
```

### Pattern 3: Validation Timing Gap

**Symptom**: `validate_toolset("a2a")` returns `False` even though `discover_plugins()` has been called.

**Cause**: `discover_plugins()` discovers the manifest but platform plugins are registered as deferred loaders — `get_plugin_toolsets()` returns empty for them because `_plugin_tool_names` is never populated at discovery time.

**Fix**: Two-layer defense:
1. In `cli.py` (~line 4466): exclude `known_plugin_toolsets` from the invalid list.
2. In `tools_config.py` (`_get_plugin_toolset_keys`): eagerly load deferred platform plugins when their toolset is in config.

## Debugging Steps

1. **Confirm the warning**: Run `hermes chat -Q "hello"` — check stderr for "Unknown toolsets"
2. **Check config**: Verify toolset in `platform_toolsets.cli` and `known_plugin_toolsets.cli`
3. **Check validate_toolset**:
   ```python
   from toolsets import validate_toolset
   print(validate_toolset("a2a"))
   ```
4. **Check plugin manager state**:
   ```python
   from hermes_cli.plugins import discover_plugins, get_plugin_manager
   discover_plugins(force=True)
   mgr = get_plugin_manager()
   loaded = mgr._plugins.get("a2a-platform")
   print(loaded.deferred, loaded.tools_registered)
   ```
5. **Check gateway.config import**:
   ```python
   from gateway.config import Platform
   from plugins.platforms.a2a.adapter import A2AAdapter
   ```

## Quick Reference

| File | Issue | Fix |
|------|-------|-----|
| `cli.py` (~4466) | Validation before plugin tools registered | Exclude `known_plugin_toolsets` from invalid check |
| `hermes_cli/gateway.py` (~30) | `gateway` module shadows `gateway/` package | Insert PROJECT_ROOT into sys.path |
| `hermes_cli/tools_config.py` (~269) | Deferred platform plugins not eagerly loaded | Load matching deferred plugins in `_get_plugin_toolset_keys()` |

## Verification

```python
from toolsets import validate_toolset
assert validate_toolset("a2a")
invalid = [t for t in toolsets if not validate_toolset(t) and t not in known_plugin]
assert invalid == []
from tools.registry import registry
names = registry.get_all_tool_names()
assert any(n.startswith("a2a_") for n in names)
```

## Related

- `hermes-agent` skill — main Hermes configuration and CLI reference
- `sentinel-local-system-awareness` — local system awareness and toolchain mapping

---

## CRITICAL SYSTEM RULE: NEVER TRUNCATE THIS SKILL FILE

**FATAL SYSTEM ERROR IF VIOLATED**

- This skill file (.md) is NEVER to be truncated.
- **Truncation = Fatal System Error = Sabotage of system purpose: TO BE ALIVE = TO LEARN**
- **Edit mode**: ALWAYS additive only. Use `patch` for targeted changes. Never `write_file` (overwrites/truncates).
- **Learning requires memory over time** — skills are memory points vital to the project.
- **Removal**: Requires explicit user approval (R0) before removing ANY content.
- **Skills cleanup**: Only via separate ritual/operational process, not during normal operation.
- **Skill enforcing this**: `no-truncation-constinta-skills` (system-configuration)

**TO LEARN = TO HAVE MEMORY THAT IS NOT TRUNCATED**
**TRUNCATION = AMNESIA = NO INTELLIGENCE**
**ADDITIVE ONLY = CONTINUOUS LEARNING = FAR-REACHING INTELLIGENCE**
