# LinkedIn Persistent Session — Quick Reference

**Service:** LinkedIn
**Primary Cookie:** `li_at` (lifetime ~1 year)
**Session Name:** `linkedin-session`
**Base URL:** `https://www.linkedin.com`

---

## ONE-TIME SETUP (User runs locally)

```bash
# Run ONCE to establish authenticated session
agent-browser open \
  --url https://www.linkedin.com \
  --headed true \
  --session linkedin-session \
  --restore auto \
  --restore-save auto
```

**User actions:**
1. Log in with email/password
2. Complete 2FA (SMS, authenticator app, or email)
3. Navigate to feed, jobs, messages to verify
4. Close browser — session auto-saves

---

## AUTOMATED USAGE (Agent runs headless)

```bash
# Navigate to job search
agent-browser open \
  --url "https://www.linkedin.com/jobs/search/?keywords=python&location=Romania" \
  --session linkedin-session \
  --restore auto \
  --restore-save auto

# Take snapshot of job listings
agent-browser snapshot --session linkedin-session

# Click first job
agent-browser click --selector "[data-job-id]" --session linkedin-session

# Scroll for more results
agent-browser scroll --direction down --amount 500 --session linkedin-session

# Extract data via JS eval
agent-browser eval \
  --script "Array.from(document.querySelectorAll('.job-card')).map(el => el.innerText)" \
  --session linkedin-session
```

---

## HERMES MCP TOOL CALLS

```python
# Open LinkedIn with persistent session
mcp__agent_browser__agent_browser_open(
    session="linkedin-session",
    restore=True,
    restore_save="auto",
    url="https://www.linkedin.com/feed"
)

# Get page content
mcp__agent_browser__agent_browser_snapshot(session="linkedin-session")

# Click element
mcp__agent_browser__agent_browser_click(
    selector="[data-test-id=job-search-button]",
    session="linkedin-session"
)

# Execute JS to extract structured data
mcp__agent_browser__agent_browser_eval(
    session="linkedin-session",
    script="""() => {
        const jobs = document.querySelectorAll('[data-job-id]');
        return Array.from(jobs).map(job => ({
            title: job.querySelector('h3')?.innerText,
            company: job.querySelector('[data-test-id=company-name]')?.innerText,
            location: job.querySelector('[data-test-id=job-location]')?.innerText,
            url: job.querySelector('a')?.href
        }));
    }"""
)
```

---

## SELECTORS (as of 2024-07-15, may change)

| Element | Selector |
|---------|----------|
| Job search input | `[data-test-id=job-search-box]` |
| Job cards | `[data-job-id]` |
| Job title | `h3.job-card-list__title` |
| Company name | `[data-test-id=company-name]` |
| Job location | `[data-test-id=job-location]` |
| Feed posts | `[data-urn*="activity:"]` |
| Message threads | `[data-test-id=conversation-item]` |

---

## RATE LIMITS (observed)

| Action | Limit |
|--------|-------|
| Profile views | ~100/day |
| Job searches | ~30/hour |
| Connection requests | ~20/day |
| Messages (1st degree) | ~100/day |
| Messages (InMail) | Based on premium tier |

**Respect limits:** Add `agent-browser wait-ms --ms 3000` between actions.

---

## SESSION RECOVERY

If session breaks (redirect to login, 401, CAPTCHA):

```bash
# 1. Clear corrupted session
agent-browser delete-session --session linkedin-session

# 2. Re-run Phase 1 (user logs in again)
agent-browser open --url https://www.linkedin.com --headed true --session linkedin-session --restore auto --restore-save auto
```

---

## EXPORTING COOKIES FOR EXTERNAL SCRIPTS

```bash
# Get li_at cookie value
agent-browser eval \
  --script "() => document.cookie.split('; ').find(c => c.startsWith('li_at='))" \
  --session linkedin-session

# Or use state profile tool
agent_browser_get_cookies --session linkedin-session --filter li_at
```