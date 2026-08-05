# EXCLUDED_PATHS.md
# Paths that must NEVER be modified during system-wide text replacement

# Excluded Paths Reference

## Absolute Exclusions (Never Touch)

```
OGLINDA - CASA\       ← Personal archive — READ ONLY under any circumstances
.git\                 ← Version control metadata
venv\                 ← Python virtual environment (managed by pip)
node_modules\         ← npm packages (managed by npm)
__pycache__\          ← Python bytecode (auto-generated)
dist\                 ← Build artifacts
build\                ← Build artifacts
.eggs\                ← Python egg build artifacts
```

## File Type Exclusions

```
*.pyc        ← Compiled Python bytecode
*.pyd        ← Python DLL extension
*.exe        ← Windows executable binary
*.dll        ← Windows DLL binary
*.so         ← Linux shared object
*.png        ← Image file
*.jpg        ← Image file
*.gif        ← Image file
*.ico        ← Icon file
*.db         ← SQLite database (binary)
*.sqlite     ← SQLite database (binary)
*.zip        ← Archive
*.tar.gz     ← Archive
*.whl        ← Python wheel package
```

## Conditional Inclusions

These paths are included but with special care:

| Path | Include? | Notes |
|------|----------|-------|
| `cron\*.log` | YES | Text content; check modification time |
| `logs\*.log` | YES | Text content; large files — scan only |
| `backups\*` | YES | Include .md and .yaml files inside |
| `state-snapshots\*` | YES | Include all text files inside |
| `.env` | NO | Secrets file — do not read or modify |
| `gateway_state.json` | NO | Runtime state — may be locked |
| `data\state.db` | NO | Binary SQLite database |

## How to Exclude in Python

```python
EXCLUDE_DIRS = {
    'OGLINDA - CASA',
    '.git',
    'venv',
    'node_modules',
    '__pycache__',
    '.eggs',
    'dist',
    'build',
}

EXCLUDE_EXTENSIONS = {
    '.pyc', '.pyd', '.exe', '.dll', '.so',
    '.png', '.jpg', '.gif', '.ico',
    '.db', '.sqlite', '.zip', '.tar',
    '.whl',
}

def should_exclude(path: Path) -> bool:
    # Check any part of the path matches an excluded dir
    if any(ex in path.parts for ex in EXCLUDE_DIRS):
        return True
    # Check file extension
    if path.suffix.lower() in EXCLUDE_EXTENSIONS:
        return True
    # Check for .env files (secrets)
    if path.name == '.env':
        return True
    return False
```

## How to Exclude in PowerShell

```powershell
$ExcludeDirs = @("OGLINDA - CASA", ".git", "venv", "node_modules", "__pycache__")

Get-ChildItem $root -Recurse -File |
    Where-Object {
        $path = $_.FullName
        -not ($ExcludeDirs | Where-Object { $path -like "*$_*" })
    } |
    Where-Object { $_.Extension -notin @('.pyc', '.exe', '.dll', '.db', '.sqlite') }
```
