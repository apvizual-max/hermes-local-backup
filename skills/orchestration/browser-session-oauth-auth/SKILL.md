---
name: browser-session-oauth-auth
description: "OAuth browser auth via real site login, not manual URLs."
version: 1.0.0
author: Sentinel Prime
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [OAuth, Auth, Browser, MCP, Comfy-Cloud, Recovery, Workflow]
---

# Browser-Session OAuth Authentication

## When to Use

A service's MCP server (or API client) authenticates via **browser-stored session/cookies** rather than a manually-exchanged token. Example: `comfy-cloud` MCP server (`url: https://cloud.comfy.org/mcp`) — auth is stored in Chrome's IndexedDB after logging into the website.

The user asks for "an authentication link" or "log into X and authenticate."

## THE TRAP (cost the user 4+ rage iterations)

Do NOT construct manual OAuth `authorize` URLs like:
```
https://service.com/oauth/authorize?response_type=code&client_id=...&redirect_uri=...&scope=...&code_challenge=...&code_challenge_method=S256
```
Many OAuth servers (including `cloud.comfy.org`) **reject every manually-built authorize URL** with `invalid_request / invalid authorization request parameters` (HTTP 400) — even with correct PKCE, registered client_id, and URL-encoded params. The error page often says *"Close this window and try signing in again from the app"* — meaning the app (Hermes) must drive a real browser session, not feed raw URLs.

Confirmed-failed variations (all returned 400): with/without PKCE, raw vs URL-encoded `redirect_uri`, with/without `state`, dynamically-registered vs static `client_id`, minimal vs full param sets.

## Correct Workflow

1. **Research the auth model FIRST** (before generating anything):
   ```bash
   curl -s "https://service.com/.well-known/oauth-authorization-server"   # endpoint + scope info
   curl -s "https://service.com/mcp"                                      # see auth error format
   ```
   If the MCP/API endpoint says *"Authentication required. Provide an X-API-Key header or Authorization: Bearer"* AND the authorize endpoint rejects manual URLs → it's browser-session OAuth.

2. **Open the REAL website** in a browser the user controls:
   ```bash
   start "" "https://cloud.comfy.org"          # Windows
   # or: agent-browser open "https://cloud.comfy.org"
   ```

3. **User logs in** through the actual site UI (email/password, Google, GitHub, etc.).

4. **Session auto-persists** in the browser's IndexedDB — no token copy-paste, no code exchange needed.

5. **Verify** the MCP server connects using the stored session (run `hermes doctor --fix` or call a read-only tool).

## Persistence

Browser IndexedDB is on disk → survives Hermes restarts **and** computer shutdowns (same browser user profile). No refresh-token logic required for session-based auth.

## Recovery: Stuck / Corrupt Session

If login "got stuck on a loading bar after approval" or auth is stale:
```bash
# Windows Chrome — clear the service's IndexedDB
rm -rf "C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\IndexedDB\https_<service>_<tld>_0.indexeddb.leveldb"
```
Then re-open the site and log in fresh.

## Hard Rule (user preference)

When asked for an "auth link" for a browser-based OAuth service: **OPEN THE REAL SITE**, never hand-assemble OAuth URLs. Research the server's actual auth model before producing anything.

## Pitfalls

- `agent-browser open` may hit daemon version-mismatch errors — `start "" "URL"` (Windows) or the browser MCP tool is more reliable for the user-facing step.
- Do NOT run `agent-browser open` in background with `&` inside a foreground terminal command — it gets flagged/silently fails. Use `start` or the browser tool.
- Manual OAuth URL construction = guaranteed 400 on `cloud.comfy.org`. Do not retry it.

## References

- `references/comfy-cloud-oauth.md` — full OAuth server metadata + failure transcripts for Comfy Cloud.
