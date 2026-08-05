#!/bin/bash
# GitHub Backup Script for Hermes Agent
# Run via cron: every Sunday at 2:00 AM
set -e

echo "=== Hermes Weekly Backup Started: $(date) ==="

# Ensure we're in the right environment
export GH_TOKEN="${GH_TOKEN:-}"
export GIT_TERMINAL_PROMPT=0

# Run the Python backup script
python "C:\Users\apviz\AppData\Local\hermes\scripts\backup-hermes.py"

echo "=== Backup Complete: $(date) ==="
