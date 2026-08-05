#!/usr/bin/env python3
"""Setup Google Workspace MCP credentials directory.

Creates the ~/.google-mcp/ directory for Google OAuth credentials.
The user must then download their Google OAuth JSON credentials from
Google Cloud Console and save as credentials.json in this directory.

Run: python3 C:/Users/apviz/AppData/Local/hermes/scripts/setup_google_workspace.py
"""
import os
from pathlib import Path

def main():
    home = Path.home()
    cred_dir = home / ".google-mcp"
    
    # Create directory
    cred_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created: {cred_dir}")
    
    # Check for credentials
    cred_file = cred_dir / "credentials.json"
    token_file = cred_dir / "token.json"
    
    if cred_file.exists():
        print(f"✅ credentials.json exists at {cred_file}")
    else:
        print(f"\n❌ credentials.json NOT found at {cred_file}")
        print(f"\n📝 To set up Google Workspace MCP:")
        print(f"   1. Go to https://console.cloud.google.com/")
        print(f"   2. Create a new project or select existing")
        print(f"   3. Enable APIs: Google Drive, Gmail, Calendar, Docs, Sheets API")
        print(f"   4. Create OAuth 2.0 Client ID (Desktop application)")
        print(f"   5. Download JSON credentials")
        print(f"   6. Save as: {cred_file}")
        print(f"\n📁 Directory contents after setup:")
    
    if token_file.exists():
        print(f"✅ token.json exists (auth token cached)")
    else:
        print(f"   token.json will be created on first auth flow")
    
    # List directory
    print(f"\n📂 {cred_dir} contents:")
    if cred_dir.exists():
        for f in cred_dir.iterdir():
            print(f"   {f.name}")
    else:
        print("   (empty)")

if __name__ == "__main__":
    main()
