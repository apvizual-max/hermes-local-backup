# External Service Access Boundaries

## Purpose
Document what external services the Sentinel/Hermes system can and cannot access, to set accurate user expectations and avoid repeated explanations.

## Authentication & Private Account Access

### CANNOT Do
- **Log into personal accounts** on any platform (LinkedIn, Twitter/X, GitHub, GitLab, Gmail, Slack, Discord, Notion, etc.)
- **Handle credentials** — no secure credential storage, no OAuth flows, no session cookie management
- **Bypass authentication** — cannot access content behind login walls
- **Maintain persistent sessions** — each browser session is ephemeral
- **Interact with 2FA/MFA** — cannot complete multi-factor authentication

### CAN Do (Public Content Only)
- **Browse public profiles/pages** — LinkedIn public profiles, company pages, job postings
- **Search public content** — via search engines or platform search (if accessible without login)
- **Extract public data** — from pages that render without authentication
- **Take screenshots** — of public pages for visual reference

## Platform-Specific Notes

### LinkedIn
- Public profiles: accessible (name, headline, public posts, experience if public)
- Private profiles: NOT accessible
- Feed, messages, connections, private posts: NOT accessible
- Job postings: mostly accessible (some require login)
- Company pages: accessible

### GitHub/GitLab
- Public repos: fully accessible (code, issues, PRs, wiki, releases)
- Private repos: NOT accessible
- Gists (public): accessible
- User profiles (public info): accessible

### Twitter/X
- Public tweets/profiles: accessible (rate limited, may require login for full view)
- Private accounts: NOT accessible
- DMs, bookmarks, lists: NOT accessible

### Google Workspace / Microsoft 365 / Notion / Slack / Discord
- All private content: NOT accessible
- Only publicly shared links with "anyone with link" permissions: accessible

## User Workarounds (Guide Users To These)

| Need | Workaround |
|------|------------|
| "Read my LinkedIn messages" | Export data from LinkedIn Settings → Data Privacy → Get a copy of your data |
| "Post to my LinkedIn" | Draft content for user to copy/paste |
| "Analyze my GitHub private repo" | User shares relevant files via copy/paste or file upload |
| "Read my Gmail" | User forwards emails or exports via Google Takeout |
| "Manage my Notion" | User shares specific pages with "public link" or exports as markdown |
| "Post to Twitter" | Draft tweets/threads for user to post |

## Communication Pattern

When user asks for private account access:
1. **Direct answer first**: "I cannot log into your [service] account."
2. **Explain why briefly**: "No credential handling, no session persistence, ToS compliance."
3. **Offer alternatives**: "But I can help you draft/analyze/strategize if you share the content directly."
4. **Reference this doc**: "See `references/external_service_access_boundaries.md` for full list."

## Anti-Patterns to Avoid
- ❌ "Let me try to log in..." — never attempt
- ❌ "Give me your password" — security violation
- ❌ "I'll use a browser session" — sessions don't persist, anti-bot measures block
- ❌ Vague "I can help with LinkedIn" — be specific about public vs. private

## Related Skills
- `optimus-prime-sentinel` (bootstrap protocol includes capability calibration)
- `hermes-data-extraction` (public web extraction patterns)
- `web-search` / `web-extract` / `browser` tools (public content only)