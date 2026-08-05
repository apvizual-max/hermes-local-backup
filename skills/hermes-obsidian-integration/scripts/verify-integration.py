#!/usr/bin/env python
"""
Hermes-Obsidian Integration Handler Script
Purpose: Middleware bridge between Hermes Agent and Obsidian Local REST API
Transport: Runs API (via Hermes gateway)
Auth: API_SERVER_KEY bearer token

Dependencies: requests, json, os, sys
"""
import os
import json
import requests
import time
from datetime import datetime

# --- Configuration ---
GATEWAY_BASE_URL = os.environ.get("HERMES_GATEWAY_URL", "http://127.0.0.1:8642")
API_KEY = os.environ.get("API_SERVER_KEY", "")
OBSIDIAN_API_URL = os.environ.get("OBSIDIAN_API_URL", "http://127.0.0.1:27124")
OBSIDIAN_TOKEN = os.environ.get("OBSIDIAN_TOKEN", "")
VAULT_ROOT = os.environ.get("OBSIDIAN_VAULT_ROOT", "/d/Alex_Knowlege_Vault")
PACE_DELAY_S = 4  # OpenRouter rate limit pacing

# --- Headers ---
GATEWAY_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
OBSIDIAN_HEADERS = {
    "Authorization": f"Bearer {OBSIDIAN_TOKEN}",
    "Content-Type": "application/json"
}

def test_gateway_connection():
    """Test Hermes gateway health"""
    r = requests.get(f"{GATEWAY_BASE_URL}/health", headers=GATEWAY_HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def test_gateway_capabilities():
    """Test gateway capabilities (Runs API)"""
    r = requests.get(f"{GATEWAY_BASE_URL}/v1/capabilities", headers=GATEWAY_HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def submit_run(input_messages, tools=None, stream=False):
    """Submit a run via Runs API"""
    payload = {
        "input": input_messages,
        "model": "hermes-agent",
        "stream": stream
    }
    if tools:
        payload["tools"] = tools

    r = requests.post(
        f"{GATEWAY_BASE_URL}/v1/runs",
        headers=GATEWAY_HEADERS,
        json=payload,
        timeout=30
    )
    r.raise_for_status()
    return r.json()

def get_run_status(run_id):
    """Get run status and output"""
    r = requests.get(
        f"{GATEWAY_BASE_URL}/v1/runs/{run_id}",
        headers=GATEWAY_HEADERS,
        timeout=10
    )
    r.raise_for_status()
    return r.json()

def test_obsidian_connection():
    """Test Obsidian Local REST API"""
    r = requests.get(OBSIDIAN_API_URL, headers=OBSIDIAN_HEADERS, timeout=10)
    return r.status_code == 200

def test_smart_connections(query="test"):
    """Test Smart Connections search"""
    r = requests.post(
        f"{OBSIDIAN_API_URL}/commands/smart-connections:search",
        headers=OBSIDIAN_HEADERS,
        json={"query": query},
        timeout=30
    )
    r.raise_for_status()
    return r.json()

def verify_all():
    """Run full verification suite"""
    results = {}
    
    print("=== Hermes-Obsidian Integration Verification ===\n")
    
    # 1. Gateway Health
    try:
        health = test_gateway_connection()
        results["gateway_health"] = health["status"] == "ok"
        print(f"[{'✓' if results['gateway_health'] else '✗'}] Gateway Health: {health.get('status', 'FAIL')}")
    except Exception as e:
        results["gateway_health"] = False
        print(f"[✗] Gateway Health: {e}")
    
    # 2. Capabilities (Runs API)
    if results.get("gateway_health"):
        try:
            caps = test_gateway_capabilities()
            runs_available = caps.get("features", {}).get("run_submission", False)
            results["runs_api"] = runs_available
            print(f"[{'✓' if runs_available else '✗'}] Runs API: {'Available' if runs_available else 'MISSING'}")
        except Exception as e:
            results["runs_api"] = False
            print(f"[✗] Runs API: {e}")
    
    # 3. Obsidian REST API
    try:
        obsidian_ok = test_obsidian_connection()
        results["obsidian_api"] = obsidian_ok
        print(f"[{'✓' if obsidian_ok else '✗'}] Obsidian REST API: {'Connected' if obsidian_ok else 'FAIL'}")
    except Exception as e:
        results["obsidian_api"] = False
        print(f"[✗] Obsidian REST API: {e}")
    
    # 4. Submit test run
    if results.get("runs_api"):
        try:
            run = submit_run([{"role": "user", "content": "Respond with OK if you receive this."}])
            results["run_submitted"] = True
            run_id = run.get("run_id")
            print(f"[✓] Run Submitted: {run_id}")
            
            # Wait and check status
            time.sleep(3)
            status = get_run_status(run_id)
            completed = status.get("status") == "completed"
            results["run_completed"] = completed
            print(f"[{'✓' if completed else '✗'}] Run Status: {status.get('status', 'UNKNOWN')}")
        except Exception as e:
            results["run_submitted"] = False
            print(f"[✗] Run Submit: {e}")
    
    print(f"\n=== Summary: {sum(1 for v in results.values() if v)}/{len(results)} passed ===")
    return results

if __name__ == "__main__":
    verify_all()