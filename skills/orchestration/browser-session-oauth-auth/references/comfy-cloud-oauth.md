# Comfy Cloud OAuth — Research Findings

## Endpoint Metadata
From `https://cloud.comfy.org/.well-known/oauth-authorization-server`:
- issuer: `https://cloud.comfy.org`
- authorization_endpoint: `https://cloud.comfy.org/oauth/authorize`
- token_endpoint: `https://cloud.comfy.org/oauth/token`
- registration_endpoint: `https://cloud.comfy.org/oauth/register`
- scopes_supported: `comfy-cloud:workflows:read/write`, `comfy-cloud:jobs:read/write`, `comfy-cloud:files:read/write`, `comfy-cloud:assets:read/write`, `comfy-cloud:hub:read/write`, `comfy-cloud:user:read`, `comfy-cloud:settings:read/write`, `comfy-cloud:billing:read`, `comfy-mcp:tools:read`, `comfy-mcp:tools:call`
- code_challenge_methods_supported: `['S256']`
- token_endpoint_auth_methods_supported: `['none']`
- grant_types_supported: `['authorization_code', 'refresh_token']`
- response_types_supported: `['code']`

From `https://cloud.comfy.org/mcp/.well-known/oauth-protected-resource`:
- resource: `https://cloud.comfy.org/mcp`
- authorization_servers: `['https://cloud.comfy.org']`
- scopes_supported: `['comfy-mcp:tools:read', 'comfy-mcp:tools:call']`
- bearer_methods_supported: `['header']`

## MCP Endpoint Behavior
`curl https://cloud.comfy.org/mcp` (no auth):
```
{"jsonrpc":"2.0","error":{"code":-32001,"message":"Authentication required. Provide an X-API-Key header or Authorization: Bearer ***"},"id":null}
```

With `X-API-Key: test`:
```
{"jsonrpc":"2.0","error":{"code":-32001,"message":"Invalid or expired token."},"id":null}
```

WWW-Authenticate header on 401:
```
Bearer realm="comfy-cloud-mcp", resource_metadata="https://cloud.comfy.org/mcp/.well-known/oauth-protected-resource", scope="comfy-mcp:tools:call"
```

## Manual Authorize URL — ALL VARIATIONS FAILED (HTTP 400)
Tested with curl + browser-like headers. Error consistently:
```
{"code":"invalid_request","message":"invalid authorization request parameters"}
```
HTML error page body:
```html
<title>Sign-in error · Comfy</title>
<h1>Something went wrong signing you in</h1>
<p>invalid authorization request parameters.</p>
<p>Close this window and try signing in again from the app.</p>
<p>invalid_request</p>
```

Failed parameter combinations (all 400):
1. Full PKCE + registered client_id + plain redirect_uri
2. Full PKCE + URL-encoded redirect_uri
3. Without PKCE (basic auth code flow)
4. No scope
5. With `state=test123`
6. With browser User-Agent + Accept headers
7. Multiple dynamically-registered client_ids (`comfy-dyn-*` from `/oauth/register`)

## Registration (works, but useless for manual flow)
`POST https://cloud.comfy.org/oauth/register` returns:
```json
{"application_type":"native","client_id":"comfy-dyn-XXXX","client_id_issued_at":...,"client_name":"...","grant_types":["authorization_code","refresh_token"],"redirect_uris":["http://localhost:8675/callback"],"response_types":["code"],"token_endpoint_auth_method":"none"}
```
Registration succeeds but the resulting client_id STILL gets 400 on `/oauth/authorize`.

## Conclusion
The OAuth server requires an authenticated browser session (login cookies) before it will process ANY authorize request. Manual URL construction is fundamentally rejected. The only working path is opening `https://cloud.comfy.org` in a real browser, logging in, and letting the session persist in Chrome IndexedDB.

## Session Storage Location
Chrome IndexedDB:
`C:\Users\apviz\AppData\Local\Google\Chrome\User Data\Default\IndexedDB\https_cloud.comfy.org_0.indexeddb.leveldb`

Clear to force fresh auth:
```bash
rm -rf "C:\Users\apviz\AppData\Local\Google\Chrome\User Data\Default\IndexedDB\https_cloud.comfy.org_0.indexeddb.leveldb"
```
