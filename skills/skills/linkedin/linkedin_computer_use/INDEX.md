# INDEX — linkedin_computer_use Skill

Skill location: `C:\Users\apviz\AppData\Local\hermes\skills\linkedin\linkedin_computer_use\`

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | **MAIN** — Full skill documentation: overview, critical context, prerequisites, 4-phase procedure, pitfalls, verification, related skills. START HERE. |
| `INDEX.md` | This index — map of all files in the skill. |
| `references/launch_sequence.md` | DEEP DIVE — Phase 1 (launch via double-click) + Phase 2 (window management quirks) with exact command outputs observed in-session. |
| `references/multi_page_extraction.md` | DEEP DIVE — Phase 3 (saved jobs navigation) + Phase 4 (Option B: browser_navigate with ?start= offsets) including auth fallback and JS extraction template. |
| `references/in_app_pagination.md` | DEEP DIVE — Phase 3.5: the user-confirmed "Press Next" in-app pagination method (scroll → single-click Next → capture → repeat). PRIMARY navigation when operating the desktop app. |
| `examples/annotated_session.md` | REAL session transcript (2026-07-15) with annotations showing exactly what was typed, what returned, and what was learned at each step. |

## Quick Navigation

- **"How do I just launch LinkedIn?"** → `SKILL.md` PHASE 1, or `references/launch_sequence.md`
- **"Why won't focus_app work?"** → `SKILL.md` PHASE 2, or `references/launch_sequence.md` §Window Quirks
- **"How do I get all saved jobs pages?"** → `SKILL.md` PHASE 4, or `references/multi_page_extraction.md`
- **"Show me the actual session?"** → `examples/annotated_session.md`

## Reproduce In 3 Commands (Launch Only)

```python
computer_use(action="capture", app="screen", mode="som")          # find "LinkedIn   Feed" (index ~5)
computer_use(action="double_click", element=5)                    # LAUNCH (not click!)
computer_use(action="wait", seconds=5)                            # app opens
```

## Reproduce In 3 Commands (Extract All Pages)

```python
browser_navigate("https://www.linkedin.com/my-items/saved-jobs/")        # page 1
browser_navigate("https://www.linkedin.com/my-items/saved-jobs/?start=25")  # page 2
browser_navigate("https://www.linkedin.com/my-items/saved-jobs/?start=50")  # page 3
```
(If browser_navigate hits login, use agent-browser `--session linkedin-session` — see references/multi_page_extraction.md)
