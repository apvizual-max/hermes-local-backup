#!/usr/bin/env bash
# Deploy script for Hermes-Obsidian Integration
# This script restarts the gateway and verifies the API is operational

set -e

HERMES_HOME="C:/Users/apviz/AppData/Local/hermes"
GATEWAY_PID_FILE="$HERMES_HOME/gateway.pid"
GATEWAY_STATE_FILE="$HERMES_HOME/gateway_state.json"

echo "=== Hermes-Obsidian Integration Deploy ==="

# Step 1: Check if gateway is running
if [ -f "$GATEWAY_STATE_FILE" ]; then
    STATE=$(cat "$GATEWAY_STATE_FILE" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('gateway_state','unknown'))" 2>/dev/null || echo "unknown")
    echo "Gateway state: $STATE"
    
    if [ "$STATE" = "running" ]; then
        PID=$(cat "$GATEWAY_STATE_FILE" | python -c "import sys,json; print(json.load(sys.stdin).get('pid',0))")
        echo "Gateway is running with PID $PID"
        
        # Test connection
        STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8642/health 2>/dev/null || echo "000")
        if [ "$STATUS" = "200" ]; then
            echo "Gateway is responding on port 8642"
        else
            echo "Gateway not responding on port 8642 (HTTP $STATUS)"
            echo "Restarting gateway..."
            taskkill //PID $PID //F 2>/dev/null || true
            sleep 2
            cd "$HERMES_HOME"
            python -m hermes_cli.main gateway run &
            sleep 5
        fi
    else
        echo "Gateway is not running. Starting..."
        cd "$HERMES_HOME"
        python -m hermes_cli.main gateway run &
        sleep 5
    fi
else
    echo "No gateway state file found. Starting gateway..."
    cd "$HERMES_HOME"
    python -m hermes_cli.main gateway run &
    sleep 5
fi

# Step 2: Verify API server
echo ""
echo "=== Verifying API Server ==="
API_KEY=$(grep API_SERVER_KEY "$HERMES_HOME/.env" 2>/dev/null | cut -d= -f2)
if [ -z "$API_KEY" ]; then
    echo "ERROR: API_SERVER_KEY not found in .env"
    exit 1
fi

HEALTH=$(curl -s http://127.0.0.1:8642/health 2>/dev/null)
echo "Health: $HEALTH"

CAPS=$(curl -s -H "Authorization: Bearer $API_KEY" http://127.0.0.1:8642/v1/capabilities 2>/dev/null)
RUNS_AVAILABLE=$(echo "$CAPS" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('features',{}).get('run_submission',False))" 2>/dev/null || echo "false")
echo "Runs API available: $RUNS_AVAILABLE"

# Step 3: Verify Obsidian plugin config
echo ""
echo "=== Checking Obsidian Hermes Agent Plugin ==="
OBSIDIAN_PLUGIN="/d/Alex_Knowlege_Vault/.obsidian/plugins/hermes-agent/data.json"
if [ -f "$OBSIDIAN_PLUGIN" ]; then
    TRANSPORT=$(cat "$OBSIDIAN_PLUGIN" | python -c "import sys,json; print(json.load(sys.stdin).get('transport','unknown'))" 2>/dev/null || echo "unknown")
    echo "Plugin transport: $TRANSPORT"
    if [ "$TRANSPORT" = "runs" ]; then
        echo "✓ Transport correctly set to 'runs'"
    else
        echo "✗ Transport is '$TRANSPORT' - expected 'runs'"
    fi
else
    echo "✗ Plugin data.json not found at $OBSIDIAN_PLUGIN"
fi

echo ""
echo "=== Deploy Complete ==="