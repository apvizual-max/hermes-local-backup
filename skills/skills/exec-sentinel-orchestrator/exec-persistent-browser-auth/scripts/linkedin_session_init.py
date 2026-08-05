#!/usr/bin/env python3
"""
LinkedIn Persistent Session Initialization
Run this ONCE to establish the authenticated session.
After that, use the session name 'linkedin-session' in headless mode.

Includes workarounds for Chrome Apps deprecation (2022).
"""

import subprocess
import sys
import time

SESSION_NAME = "linkedin-session"
LINKEDIN_URL = "https://www.linkedin.com"
LINKEDIN_FEED = "https://www.linkedin.com/feed/"
AGENT_BROWSER_CMD = r"C:\Users\apviz\AppData\Local\hermes\node\agent-browser.cmd"

def run_agent_browser(args):
    """Run agent-browser CLI command."""
    cmd = [AGENT_BROWSER_CMD] + args
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.stdout:
        print(f"STDOUT: {result.stdout}")
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    return result.returncode == 0

def launch_real_chrome(url):
    """Launch user's actual Chrome via desktop shortcut (bypasses Chrome Apps deprecation)."""
    import os
    chrome_shortcut = r"C:\Users\Public\Desktop\Google Chrome.lnk"
    if os.path.exists(chrome_shortcut):
        print(f"Launching real Chrome via shortcut: {chrome_shortcut}")
        subprocess.Popen(f'start "" "{chrome_shortcut}" "{url}"', shell=True)
        return True
    else:
        print(f"Chrome shortcut not found at: {chrome_shortcut}")
        return False

def main():
    print("=" * 60)
    print("LinkedIn Persistent Session Setup")
    print("=" * 60)
    print()
    print("⚠️  NOTE: Chrome Apps deprecated since 2022.")
    print("   The desktop shortcut at:")
    print(r"   C:\Users\apviz\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Chrome Apps\LinkedIn   Feed.lnk")
    print("   NO LONGER WORKS as a standalone app.")
    print()
    print("Choose your setup method:")
    print("  1. agent-browser persistent session (RECOMMENDED for automation)")
    print("  2. Launch REAL Chrome via desktop shortcut (uses your actual profile)")
    print("  3. Create modern PWA shortcut (for manual use)")
    print()
    choice = input("Enter choice [1/2/3]: ").strip()
    
    if choice == "2":
        # Launch real Chrome
        print("\nLaunching your actual Chrome browser...")
        print("This uses YOUR existing Chrome profile with all logins/extensions.")
        print("If you're already logged into LinkedIn, you're done!")
        launch_real_chrome(LINKEDIN_FEED)
        print("\n✅ Chrome launched. Check if you're logged in.")
        return
    
    elif choice == "3":
        # Instructions for PWA
        print("\n📱 To create a modern PWA shortcut that WORKS:")
        print("1. Open Chrome and go to:", LINKEDIN_FEED)
        print("2. Click ⋮ menu → More tools → Create shortcut...")
        print("3. Check 'Open as window'")
        print("4. Click Create")
        print("5. New shortcut appears in Start Menu → Chrome Apps (works!)")
        return
    
    # Default: choice 1 - agent-browser session
    print()
    print("This will open a VISIBLE browser window with a DEDICATED profile.")
    print("You must:")
    print("  1. Log in with your email/password")
    print("  2. Complete 2FA (SMS, authenticator app, or email)")
    print("  3. Navigate to feed/jobs/messages to verify access")
    print("  4. Close the browser when done")
    print()
    print(f"Session will be saved as: {SESSION_NAME}")
    print("Cookies (including li_at) will persist for ~1 year")
    print()
    input("Press ENTER to start...")
    
    # Phase 1: Headed browser with session persistence
    success = run_agent_browser([
        "open",
        "--url", LINKEDIN_URL,
        "--headed", "true",
        "--session", SESSION_NAME,
        "--restore", "auto",
        "--restore-save", "auto"
    ])
    
    if not success:
        print("ERROR: Failed to launch browser")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("Browser closed. Session saved.")
    print("=" * 60)
    print()
    print("Next time, run headless automation with:")
    print(f"  agent-browser open --url {LINKEDIN_FEED} --session {SESSION_NAME} --restore auto --restore-save auto")
    print()
    print("Or use Hermes MCP tools with session='linkedin-session'")

if __name__ == "__main__":
    main()