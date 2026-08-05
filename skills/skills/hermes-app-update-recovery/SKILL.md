---
name: hermes-app-update-recovery
description: Standard operational procedure to diagnose and recover the Hermes Desktop agent after failed updates or system environment breaks.
version: 1.0.0
author: Antigravity
platforms: [windows]
metadata.hermes.tags: [System, Maintenance, Recovery, Diagnostics]
---

# Hermes App Update Recovery

A dedicated operational procedure for diagnosing and recovering the Hermes Desktop application backend and virtual environment when it fails to boot after an update.

## When to Use
- When the Hermes renderer console shows `[bootstrap] reset requested by renderer` or `Hermes backend exited before it became ready (1)`.
- When Python modules (specifically `fastapi`, `uvicorn`, or custom gateway modules) are reported missing in the logs.
- When the backend environment has been broken, corrupted, or altered by a system update.

## Prerequisites
- Windows environment.
- Access to `C:\Users\apviz\AppData\Local\hermes\hermes-agent`.
- Powershell or Command Prompt with write access to the user folder.

## Diagnostics Checklist
1. **Locate logs**:
   Check `C:\Users\apviz\AppData\Local\hermes\logs` (specifically `desktop.log`).
2. **Identify errors**:
   Look for `ModuleNotFoundError: No module named 'fastapi'` or similar package errors.

## Recovery Procedure

### Step 1: Clean and Rebuild Python Virtual Environment Dependencies
If modules are missing, reinstall the packages in editable mode to link the `hermes-agent` and all its dependencies correctly:

```powershell
# Open terminal and go to the agent folder
cd "C:\Users\apviz\AppData\Local\hermes\hermes-agent"

# Run pip install in editable mode for all extra dependency sets
.\venv\Scripts\python.exe -m pip install -e ".[all]"
```

### Step 2: Verify Python Packages and Imports
Verify that key web framework dependencies (`fastapi`, `uvicorn`) are successfully imported by the virtual environment interpreter:

```powershell
.\venv\Scripts\python.exe -c "import fastapi, uvicorn; print('Import OK!')"
```

### Step 3: Run the Bootstrap Environment Checker
Execute the bootstrap script with the dependency check flag to make sure all local hooks and modules are operational:

```powershell
.\venv\Scripts\python.exe hermes_bootstrap.py --check-deps
```

### Step 4: Run the CLI Status Validation
Execute a simple version check using the compiled CLI executable:

```powershell
.\venv\Scripts\hermes.exe --version
```
*Expected output: `Hermes Agent v0.18.0` (or the updated version).*

## Common Pitfalls
- **Global vs Virtual Env**: Running `pip install` globally instead of calling the interpreter inside `venv` directly (e.g. `.\venv\Scripts\python.exe`). Always use the full path to the virtual environment scripts to isolate dependencies.
- **Desktop Locking**: If the desktop application is running in the background, some binary files (like `.node` files or `state.db`) might be locked. Close all Hermes processes from Task Manager or running terminals before applying fixes.

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

