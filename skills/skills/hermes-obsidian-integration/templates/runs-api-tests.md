# Hermes-Obsidian Integration - Runs API Test Template

## Test 1: Basic Connection
```bash
curl -s http://127.0.0.1:8642/health
```
Expected: `{"status": "ok", "platform": "hermes-agent", "version": "0.18.0"}`

## Test 2: Authenticated Capabilities
```bash
curl -s -H "Authorization: Bearer <API_SERVER_KEY>" \
  http://127.0.0.1:8642/v1/capabilities
```
Expected: `features.run_submission: true`

## Test 3: Submit Simple Run
```bash
curl -s -X POST http://127.0.0.1:8642/v1/runs \
  -H "Authorization: Bearer <API_SERVER_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "Say OK"}], "model": "hermes-agent", "stream": false}'
```
Expected: Returns `run_id` with status `started`

## Test 4: Check Run Status
```bash
curl -s http://127.0.0.1:8642/v1/runs/<run_id> \
  -H "Authorization: Bearer <API_SERVER_KEY>"
```
Expected: status `completed` with output

## Test 5: Obsidian REST API
```bash
curl -s http://127.0.0.1:27124
```
Expected: JSON with version info

## Test 6: Smart Connections Search
```bash
curl -s -X POST http://127.0.0.1:27124/commands/smart-connections:search \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```
Expected: Array of search results

## Test 7: Multi-turn Conversation
```bash
# Create session
curl -s -X POST http://127.0.0.1:8642/api/sessions \
  -H "Authorization: Bearer <API_SERVER_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"name": "test_session"}'
# Use session
curl -s -X POST http://127.0.0.1:8642/api/sessions/<session_id>/chat \
  -H "Authorization: Bearer <API_SERVER_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "Hello"}], "stream": false}'
```
Expected: Conversation continues with context