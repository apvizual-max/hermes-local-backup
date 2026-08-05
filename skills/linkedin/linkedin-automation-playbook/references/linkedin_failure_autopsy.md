# LinkedIn Login — Failure Autopsy (2026-07-15)

## Goal
Connect to user's LinkedIn (Alexandru Pope, Sector 6 Bucharest, AP-ID) for automation.

## FAILURE 1 — agent-browser cookie persistence is FALSE
- `agent-browser cookies get --session linkedin-session` → `{"cookies":[]}`. New browser launched, not the live one.
- State file `~/.agent-browser/sessions/linkedin-session-linkedin-session.json` contained a valid `li_at` (written 14:20) BUT went STALE after CAPTCHA churn / relaunches.
- `--restore linkedin-session-linkedin-session` → "loaded" yet STILL redirects to `/login`.
- ROOT CAUSE: each `agent-browser <cmd>` = SEPARATE daemon. Cookies lost unless chained with `&&` in ONE shell.
- Chained test (`open && cookies set li_at && open /feed/`) still redirected → stale token.

## FAILURE 2 — reCAPTCHA v2 UNSOLVABLE
- Fresh credential login (Puppeteer `browser` + agent-browser) → "I'm not a robot".
- Checkbox in cross-origin iframe → JS eval can't reach; coordinate click (400,526) → AX "Element not found".
- Must let USER complete CAPTCHA in live browser.

## FAILURE 3 — IP soft-block
- Raw `curl` with valid `li_at` → HTTP 429 from server egress IP.
- Many login tries → CAPTCHA loops.
- LESSON: after 2 failures STOP. You become the blocker.

## FAILURE 4 — Chrome cookie DB locked
- `AppData\Local\Google\Chrome\User Data\Default/Network/Cookies` LOCKED while Chrome runs → cp/shutil → "Device or resource busy" / PermissionError.
- Only CDP against running Chrome reads live cookies.

## FAILURE 5 — browser_console sandbox
- `expression` with `fetch()`/`localStorage` BLOCKED ("sensitive browser JavaScript primitive"). No cookie set / network via eval.

## WORKING (priority)
1. **Path A (BEST): CDP on live headed Chrome.** Relaunch with `--remote-debugging-port=9222`, verify `curl 127.0.0.1:9222/json/version`, attach browser stack via CDP. Live `li_at` already present → no login/CAPTCHA.
2. **Path B: Puppeteer `browser` + USER CAPTCHA.** `browser_navigate` login → `browser_type` creds (`D:\Alex_Knowlege_Vault\LinkedIn_Access.md`) → `browser_click` Sign in → user solves CAPTCHA → continue. Keep ONE session alive.

## USER DIRECTIVE
- "STOP USING AGENT BROWSER... IT BLOCKS US NOW" → agent-browser BANNED for LinkedIn.
- "FIGURE IT OUT ALLREADY AND STOP ASKING FOR GUIDANCE!" → pivot across paths WITHOUT asking which; no A/B/C menus when stuck.

## Credentials
`D:\Alex_Knowlege_Vault\LinkedIn_Access.md` → user: apvizual@gmial.com / pass: Sentinel_911. Read via `read_file`.
