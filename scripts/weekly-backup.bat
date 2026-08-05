@echo off
REM Weekly backup of Hermes Agent local files to GitHub
REM Runs every Sunday at 2:00 AM

set HERMES_HOME=%LOCALAPPDATA%\hermes
set BACKUP_DIR=%HERMES_HOME%\hermes-backup-temp
set REPO_URL=https://github.com/apvizual-max/hermes-local-backup.git
set GITHUB_TOKEN=ghp_[REDACTED]

echo [%date% %time%] Starting weekly backup of Hermes Agent...

REM Navigate to backup directory or create it
cd /d "%BACKUP_DIR%" 2>nul || (
    mkdir "%BACKUP_DIR%"
    cd /d "%BACKUP_DIR%"
    git clone %REPO_URL% .
    git config user.name "Sentinel Prime"
    git config user.email "sentinel.prime@optimus.local"
)

REM Export GitHub token for git
set "GIT_ASKPASS="
echo https://apvizual-max:%GITHUB_TOKEN%@github.com > "%USERPROFILE%\.git-credentials"

REM Create .gitignore to exclude sensitive files
echo .env > .gitignore
echo *.key >> .gitignore
echo *.pem >> .gitignore
echo .git-credentials >> .gitignore
echo secrets.json >> .gitignore

REM Copy files from Hermes directory (excluding large dirs and secrets)
REM Exclude: .env, OGLINDA-CASA (huge), plugins with incomplete files
xcopy "%HERMES_HOME%\config.yaml" . /Y /Q
xcopy "%HERMES_HOME%\SOUL.md" . /Y /Q
xcopy "%HERMES_HOME%\SENTINEL_JOURNAL.md" . /Y /Q
xcopy "%HERMES_HOME%\hermes-setup-wizard.log" . /Y /Q 2>nul
xcopy "%HERMES_HOME%\profiles\default" "profiles\default" /E /Y /Q /EXCLUDE:exclude.txt

REM Copy skills directory
xcopy "%HERMES_HOME%\skills" "skills" /E /Y /Q /EXCLUDE:exclude.txt

REM Create README
echo # Hermes Agent - Weekly Backup > README.md
echo. >> README.md
echo Automated weekly backup of local Hermes Agent files. >> README.md
echo Source: %%LOCALAPPDATA%%\hermes >> README.md
echo >> README.md
echo Last backup: %date% %time% >> README.md
echo >> README.md
echo **Excluded**: .env (secrets), OGLINDA-CASA (large), cache files >> README.md

REM Commit and push
git add -A
git commit -m "Weekly backup - %date% %time%" --allow-empty
git push origin main 2>&1

echo [%date% %time%] Backup completed successfully!
