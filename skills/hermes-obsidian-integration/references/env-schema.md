# Environment Variables Schema

## Required Variables

### API_SERVER_KEY
- **Purpose**: Bearer token for Hermes gateway API server authentication
- **Required**: Yes (gateway will not start API server without it)
- **Generation**: `openssl rand -hex 32`
- **File**: `C:\Users\apviz\AppData\Local\hermes\.env`
- **Format**: `API_SERVER_KEY=<64-char hex string>`
- **Must match**: `apiKey` field in `hermes-agent/data.json`

### API_SERVER_ENABLED
- **Purpose**: Enable the API server explicitly
- **Value**: `true`
- **Optional**: Yes (defaults to true when API_SERVER_KEY is set)

## Optional Variables

### OPENROUTER_API_KEY
- **Purpose**: OpenRouter model access
- **File**: `C:\Users\apviz\AppData\Local\hermes\.env`

### OPENAI_API_KEY
- **Purpose**: OpenAI TTS (for Hermes TTS plugin) and other OpenAI services
- **File**: `C:\Users\apviz\AppData\Local\hermes\.env`

## Reference Files

### Gateway State
- **File**: `C:\Users\apviz\AppData\Local\hermes\gateway_state.json`
- **Purpose**: Real-time gateway status, PID, platform connections

### Gateway PID
- **File**: `C:\Users\apviz\AppData\Local\hermes\gateway.pid`
- **Purpose**: Process ID of running gateway

### Gateway Lock
- **File**: `C:\Users\apviz\AppData\Local\hermes\gateway.lock`
- **Purpose**: Prevents duplicate gateway instances