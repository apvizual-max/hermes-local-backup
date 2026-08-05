"""
WORKING MCP Click Method — cua-driver multi-monitor clicking.

This script demonstrates the proven method for clicking elements
on any monitor (including secondary/upper monitors on different GPUs).

Key insight: cua-driver mcp --no-daemon-relaunch keeps the daemon session
alive across multiple requests, so the element cache survives.

Usage:
    python click_mcp.py <pid> <hwnd> <element_label_substring>
    
Example:
    python click_mcp.py 27416 1507982 "Job tracker"
"""

import subprocess, json, time, re, base64, sys, os


def click_element(pid, hwnd, label_substring, delivery_mode="background"):
    """
    Click an element by label substring using cua-driver MCP persistent session.
    
    Args:
        pid: Process ID of the target window
        hwnd: Window handle (integer)
        label_substring: Part of the element's label to match
        delivery_mode: "background" (default) or "foreground"
    
    Returns:
        dict with keys: success, url_after, element_index, element_label, screenshot_path
    """
    proc = subprocess.Popen(
        ['cua-driver', 'mcp', '--no-daemon-relaunch'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Step 1: Get window state
        req1 = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {
                "name": "get_window_state",
                "arguments": {"pid": pid, "window_id": hwnd, "max_elements": 300}
            }
        }) + "\n"
        proc.stdin.write(req1)
        proc.stdin.flush()
        
        time.sleep(2)
        line = proc.stdout.readline()
        resp1 = json.loads(line)
        
        # Parse text to find element index
        text = resp1['result']['content'][0]['text']
        pattern = rf'\[(\d+)\]\s+\w+\s+"{re.escape(label_substring)}"'
        match = re.search(pattern, text)
        
        if not match:
            return {"success": False, "error": f"Element '{label_substring}' not found"}
        
        element_idx = int(match.group(1))
        
        # Step 2: Click by element_index (same session — cache alive!)
        req2 = json.dumps({
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {
                "name": "click",
                "arguments": {
                    "pid": pid, "window_id": hwnd,
                    "element_index": element_idx,
                    "delivery_mode": delivery_mode
                }
            }
        }) + "\n"
        proc.stdin.write(req2)
        proc.stdin.flush()
        
        time.sleep(1)
        line = proc.stdout.readline()
        resp2 = json.loads(line)
        click_text = resp2.get('result', {}).get('content', [{}])[0].get('text', '')
        
        # Step 3: Verify
        time.sleep(3)
        req3 = json.dumps({
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {
                "name": "get_window_state",
                "arguments": {"pid": pid, "window_id": hwnd, "max_elements": 10}
            }
        }) + "\n"
        proc.stdin.write(req3)
        proc.stdin.flush()
        
        time.sleep(1)
        line = proc.stdout.readline()
        resp3 = json.loads(line)
        text3 = resp3['result']['content'][0]['text']
        
        # Extract URL
        url_match = re.search(r'value="([^"]+)"', text3)
        url_after = url_match.group(1) if url_match else "unknown"
        
        # Save screenshot
        img_data = resp3['result']['content'][1].get('data', '')
        screenshot_path = None
        if img_data:
            screenshot_path = f"click_result_{element_idx}.png"
            with open(screenshot_path, 'wb') as f:
                f.write(base64.b64decode(img_data))
        
        return {
            "success": True,
            "url_after": url_after,
            "element_index": element_idx,
            "click_result": click_text,
            "screenshot_path": screenshot_path
        }
    
    finally:
        proc.terminate()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python click_mcp.py <pid> <hwnd> <label_substring>")
        sys.exit(1)
    
    pid = int(sys.argv[1])
    hwnd = int(sys.argv[2])
    label = sys.argv[3]
    
    result = click_element(pid, hwnd, label)
    print(json.dumps(result, indent=2))