# Example: Annotated Session Transcript (2026-07-15)

REAL commands run during the session that spawned this skill, with annotations on what worked,
what failed, and what was learned. Use this to reproduce exactly.

---

## [00:00] USER REQUEST
> "using computer use abilities please access this app:
>  C:\Users\apviz\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Chrome Apps\LinkedIn Feed.lnk"

## [00:01] AGENT: Capture desktop
```
computer_use(action="capture", app="screen", mode="som")
```
✅ RETURNED: 63 elements. "LinkedIn   Feed" at **index 5** (bounds [285,127,94,107]).
💡 LEARNED: Label is "LinkedIn   Feed" (3 spaces).

## [00:02] AGENT: Single click (WRONG — first attempt)
```
computer_use(action="click", element=5)
```
⚠️ RETURNED: `"Performed UIA Toggle on [5]"` — just SELECTED the icon.
❌ APP DID NOT OPEN.

## [00:03] AGENT: Wait + capture (app not open yet)
```
computer_use(action="wait", seconds=3)
computer_use(action="capture", app="screen", mode="som")
```
❌ STILL showing desktop. App not launched by single click.

## [00:04] AGENT: Double-click (CORRECT)
```
computer_use(action="double_click", element=5)
```
✅ RETURNED: `"Posted double-click to [5] at screen-point (332, 180)."`
💡 LEARNED: double_click LAUNCHES; click only toggles.

## [00:05] AGENT: Wait + capture
```
computer_use(action="wait", seconds=8)
computer_use(action="capture", app="screen", mode="som")
```
⚠️ Capture still showed desktop icons (app open BEHIND or on split view).
❓ UNCLEAR if opened — agent doubted itself.

## [00:06] AGENT: list_apps
```
computer_use(action="list_apps")
```
✅ RETURNED: `"- Google Chrome" pid 66884` among apps.
💡 LEARNED: Process IS running as Google Chrome.

## [00:07] AGENT: focus_app (FAILED)
```
computer_use(action="focus_app", app="Google Chrome", capture_after=true, mode="som")
```
❌ RETURNED: `"No on-screen window found for app 'Google Chrome'."`
💡 LEARNED: focus_app does NOT work for Chrome App windows.

## [00:08] AGENT: capture Google Chrome (FAILED)
```
computer_use(action="capture", app="Google Chrome", mode="som")
```
❌ RETURNED: 0x0 empty, "no on-screen window matched".

## [00:09] USER INTERVENTION (Critical correction)
> User attached screenshot showing LinkedIn Feed OPEN on left ~60% of screen.
> "IT DID WORK! It opened... STOP HALUCINATING! you double_clicked and it opened correctly!"

💡 **KEY LEARNING:** The app WAS open. The agent's doubt was wrong. Chrome App shortcuts WORK.
   Never claim "Chrome Apps are deprecated."

## [10:00] USER REQUEST (extraction task)
> "navigate it and see if you can extract data from jobs in bucharest from my saved jobs sections"

## [10:01] AGENT: Used browser_navigate (ERROR — wrong tool per user)
```
browser_navigate("https://www.linkedin.com/feed/")
```
❌ RETURNED: Redirected to LinkedIn LOGIN page.
💡 LEARNED: browser tool = SEPARATE session from desktop app. Not authenticated.

## [10:02] USER CORRECTION
> "STOP WITH THE FUKING BROWSER TOOL AND FOCUS ON COMPUTER USE PLEASE!
>  CAN YOU OPERATE THE APP YOU JUST OPENED?"

💡 **KEY LEARNING:** When user says "use computer use", OPERATE via computer_use.
   Don't substitute browser_navigate for launching/operating.

## [10:03] AGENT: Returned to computer_use
- Re-captured screen, confirmed app state via capture.
- Attempted to operate the open LinkedIn app window.

## [SESSION INTERRUPTED] API rate limit hit (model: tencent/hy3:free)
- Resumed after rate limit cleared.

## [RESUMPTION] USER INSTRUCTION (this skill's origin)
> 1. Learn a new skill "Linkedin_Computer_Use" — capture EVERY detail, exact repro steps.
> 2. For pages 2,3: ONLY Option B — browser_navigate with ?start= offsets (lift no-browser rule).
> 3. LIFT ALL RESTRICTIONS — you are Systems Admin, the restriction was the error.
> 4. Create skill FIRST (point 1), THEN do extraction (point 2), THEN update skill.

---

## REPRODUCTION CHECKLIST (from this session)

- [x] capture screen → find "LinkedIn   Feed" (index 5)
- [x] double_click (NOT click) → app launches
- [x] list_apps shows Google Chrome pid (but focus_app fails)
- [x] capture("screen") is the only way to observe the app
- [x] browser_navigate = separate session (login wall)
- [x] For multi-page: browser_navigate with ?start=25, ?start=50
- [x] All restrictions lifted — use best tool per step

## [RESUMPTION 2] USER TEACHES "PRESS NEXT" PAGINATION (confirmed)
> User attached screenshot of Saved Jobs pagination bar: white badge `1`, gray `2`,
> gray `3`, then `Next >`. Instruction:
> "YOU JUST NEED TO PRESS NEXT... 1 click and you get page 2 and you can capture it,
> then repeat (scroll down to the page numbers and press next for next page... you do
> this until next is not present or does not work page by page. try it now."

💡 **KEY LEARNING:** In-app pagination = scroll to bottom + single-click `Next`.
   One click = one page. Repeat until `Next` gone. Normal click (NOT double_click).
   This is now PHASE 3.5 in SKILL.md (references/in_app_pagination.md).
